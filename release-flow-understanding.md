# Release Tagger Flow - Current Implementation

## Current `--release` Flow Summary

### 1. **Initialization & State Management**
- Uses a YAML state file (`release-state.yml`) to track release progress
- State can be resumed or started fresh
- State stores: repo directory, release version, and per-component versions/following branches

### 2. **Data Sources (Current YAML-based)**
- **`component-maps.yml`**: Defines components, their types (git/docker/container), relationships, and which are "release_component"
- **`git-versions*.yml`**: Docker compose files with git-based versions (format: `mendersoftware/image:version`)
- **`docker-compose*.yml`**: Docker compose files with Docker tag versions
- **`other-components*.yml`**: Additional component definitions
- All read from the integration repository (either checked-out or from a specific git revision via `git show`)

### 3. **Version Determination Phase**
- Iterates through all git components
- For each component:
  - Looks up previous version from integration repo's YAML files
  - Shows `git log` of changes since last version
  - Interactively asks user: "Is there a reason for a new release?"
  - Proposes version number (based on semver bump logic)
  - Stores decision in state: `state[repo_name]["version"]`

### 4. **Tag Discovery**
- `check_tag_availability()` scans all repos for:
  - Final tags (e.g., `5.0.0`)
  - Build tags (e.g., `5.0.0-build1`, `5.0.0-build2`)
  - Returns `tag_avail` structure with highest tags, SHAs, release status

### 5. **Interactive Menu Loop**
Operations like:
- **T**: Create build tags pointing to followed branches
- **F**: Create final tags from build tags
- **B**: Trigger CI build
- **D**: Update Docker registry tags (`:latest`, `:5.0`)
- **I**: Write git-versions files back to integration repo
- etc.

### 6. **Key Functions**
- `version_of()`: Extracts a component's version from integration's YAML files
- `get_docker_compose_data()`: Parses YAML files into simplified dict structure
- `Component` class: Maps component names/types and reads from `component-maps.yml`

## New JSON-Based Flow

### Data Source Migration
Replace the YAML files in the integration repository with JSON files in the mender-client-subcomponents repository.

### JSON File Evolution During Release

The release flow creates different JSON files as the release progresses:

```
main branch: next.json
  - version: "next"
  - components have branches: "master" or "main"
        ↓
  Create branch 6.0.x from main
        ↓
6.0.x branch: 6.0.x.json
  - version: "6.0.x"
  - components have version-specific branches: "6.0.x", "5.0.x", etc.
  - These branches are created by the tool in each component repo
        ↓
  Work on release candidates
        ↓
6.0.x branch: 6.0.0-build1.json (leaf commit for testing)
  - version: "6.0.0-build1"
  - components have build tags: "5.0.1-build1", "6.0.0-build1", etc.
        ↓
  Test, iterate with more build candidates if needed
        ↓
6.0.x branch: 6.0.0.json (final)
  - version: "6.0.0"
  - components have final tags: "5.0.1", "6.0.0", etc.
```

### JSON Structure

All JSON files follow the same structure:
```json
{
  "version": "next|X.Y.x|X.Y.Z-buildN|X.Y.Z",
  "components": [
    {
      "name": "component-name",
      "version": "branch-name|X.Y.Z-buildN|X.Y.Z",
      "source": "github.com/mendersoftware/repo"
    }
  ]
}
```

### Example: Releasing 6.0.0 where mender-auth only needs 5.0.1

- `next.json`: `mender-auth` version = `"master"`
- `6.0.x.json`: `mender-auth` version = `"5.0.x"` (branch created by tool)
- `6.0.0-build1.json`: `mender-auth` version = `"5.0.1-build1"` (build tag)
- `6.0.0.json`: `mender-auth` version = `"5.0.1"` (final tag)

### Key Points
- `next.json` in main branch is never modified during a release
- Only two files persist in release branch: `X.Y.x.json` and `X.Y.Z.json`
- Build candidate JSONs (`X.Y.Z-buildN.json`) are leaf commits for testing (NOT pushed to branch)
- Base repo: mender-client-subcomponents (replaces deprecated integration repo)

### Build Tag Behavior

**mender-client-subcomponents repo:**
- Build JSON files (6.0.0-build1.json) are in leaf commits
- These commits are NOT pushed to the 6.0.x branch
- Only the git tag is pushed (pointing to the leaf commit)
- Branch only contains X.Y.x.json and final X.Y.Z.json

**Source component repos (mender, mender-connect, etc.):**
- Build tags (5.0.1-build1) point to latest commit in their release branch
- These build tags ARE created and pushed
- Build tags are cleaned up at the end of the release process
- Only final tags (5.0.1) remain after cleanup

### Version Determination Phase Changes

**Changelog PR Link:**
- Show once at the beginning of version determination phase
- Link format: `https://github.com/mendersoftware/mender-client-subcomponents/pulls?q=is%3Apr+is%3Aopen+label%3A%22autorelease%3A+pending%22`
- Contains aggregated changelogs for all components
- Human finds relevant changelog for each component

**Git Log Display:**
- Keep same range logic: `prev_version..branch`
- Change to one-liner format: `git log --oneline prev_version..branch`
- Show for each component individually during interactive prompts

**Interactive Flow:**
```
[Show changelog PR link once]

For each component:
  [Show git log --oneline output]
  Based on this, is there a reason for a new release of {component}? (Yes/No/Skip)
```

### Component System Simplification

**Eliminate Component Class & component-maps.yml:**
- Remove the entire `Component` class
- Remove `component-maps.yml` dependency
- Derive everything from JSON files

**Only Git Repositories:**
- No `docker_image` or `docker_container` types
- Only deal with git repositories
- Each component in JSON = one git repository

**Release Component Definition:**
- If it's in the JSON, it's a release component
- No need for "release_component" flag
- No optional/non-release components
- Everything is explicit in the JSON

### State Management & Branch Following

**Simplify State File:**
- Remove `state[repo]["following"]` tracking
- Read branch/version info directly from current JSON file (e.g., `6.0.x.json`)
- When creating build tags, point to branches from JSON

**State File Contents (Simplified):**
- `repo_dir`: Directory containing all git repositories
- `version`: Release version (e.g., "6.0.0")
- `[repo]["version"]`: Decided version for each component

### Interactive Menu Changes

**Remove Menu Options:**
- **B) Trigger build** - Remove from menu, keep helper function
- **D) Update Docker tags** - Remove from menu, keep helper function
- **I) Update git-versions files** - Replace with "Commit JSON to mender-client-subcomponents" (to be confirmed)

**Keep Menu Options:**
- **R) Refresh repositories**
- **T) Generate and push build tags**
- **F) Generate and push final tags**
- **P) Push current build tags**
- **U) Purge build tags**
- **M) Merge release tag into release branch**
- **C) Create new series branches**
- **O) Move from beta to final**
- **Q) Quit**

### JSON File Management Approach

**Use temporary checkout pattern (Option A):**
- Create temp checkout: `{repo_dir}/tmp_checkout/mender-client-subcomponents/`
- Make JSON changes in temp checkout
- Commit in temp directory
- Fetch commit to real repo: `git fetch {tmpdir} HEAD`
- Push from real repo
- Cleanup temp directory

**Benefits:**
- Doesn't interfere with user's working directory
- User can have uncommitted changes
- Consistent with current tool behavior
- No requirement for clean working directory

**Assumptions:**
- Tool runs from within mender-client-subcomponents repo
- All component repos are cloned under `repo_dir`
- User manages their own local checkout state
