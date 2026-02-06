# Implementation Plan: JSON-based Release Tool

## Overview
Transform release-tagger from YAML/integration-based to JSON/subcomponents-based system.

---

## Critical Architectural Concept: Components vs Repositories

### The Distinction
The JSON files contain **components** (public names), but git operations must work on **repositories** (actual git repos).

**Example:**
- `mender-auth` and `mender-update` are separate **components** (appear as separate entries in JSON)
- Both share the same **source**: `github.com/mendersoftware/mender`
- This means they are in the same git **repository**: `mender`

### Implications for Implementation

**Git Operations (fetch, tag, log, etc.):**
- Must deduplicate by source repository
- Only operate once per unique source
- Example: Tag `mender` repo once, not twice for mender-auth and mender-update

**State Management:**
- State tracks decisions per **repository name** (state["mender"]["version"])
- NOT per component (NOT state["mender-auth"]["version"])
- Components sharing a repo will have identical versions

**Version Determination:**
- Interactive prompts happen per **repository**
- User decides once for `mender`, applies to both mender-auth and mender-update
- Git log shows combined changes from the repository

**JSON Structure:**
```json
{
  "version": "next",
  "components": [
    {"name": "mender-auth", "version": "master", "source": "github.com/mendersoftware/mender"},
    {"name": "mender-update", "version": "master", "source": "github.com/mendersoftware/mender"}
  ]
}
```
Both components will always have the same version since they share the same source.

### Helper Functions Added
```python
extract_repo_name_from_source(source)
# 'github.com/mendersoftware/mender' -> 'mender'

get_unique_sources_from_json(json_data)
# Returns 7 unique sources from 8 components (mender appears once)

get_repos_from_json(json_data)
# Returns list of repo dicts with component mappings:
# {'repo': 'mender', 'source': '...', 'components': ['mender-auth', 'mender-update'], 'version': '...'}

get_repos_from_current_json(state)
# Preferred function for git operations - returns unique repositories
```

---

## Phase 1: Foundation - Remove Old, Add New Data Layer

### 1.1 Remove Component Class System
**Files to change:** `release-tagger`

**Remove:**
- `Component` class (lines 68-220)
- `get_docker_compose_data_from_json_list()` (line 445)
- `docker_compose_files_list()` (line 437)
- `filter_docker_compose_files_list()` (line 406)
- `get_docker_compose_data()` (line 549)
- `get_docker_compose_data_for_rev()` (line 560)
- `version_specific_docker_compose_data_patching()` (if exists)

**Impact:** ~400+ lines removed

### 1.2 Add JSON Data Layer ✅ COMPLETED
**New functions created:**

**Basic JSON operations:**
```python
def read_release_json(json_path):
    """Read and parse a release JSON file."""

def write_release_json(json_path, data):
    """Write release data to JSON file with proper formatting."""

def get_current_release_json_path(state=None, version=None):
    """Determine which JSON file to read based on current context."""
```

**Component-level operations (for JSON structure):**
```python
def get_component_list_from_json(json_data):
    """Extract component list from JSON."""

def find_component_in_json(json_data, component_name):
    """Find specific component in JSON data."""

def get_source_for_component(json_data, component_name):
    """Get the source URL for a component."""

def get_components_for_source(json_data, source):
    """Get all component names that share a source."""
```

**Repository-level operations (for git operations):**
```python
def extract_repo_name_from_source(source):
    """Extract repository name from source URL.
    'github.com/mendersoftware/mender' -> 'mender'
    """

def get_unique_sources_from_json(json_data):
    """Get list of unique source repositories (deduplicated)."""

def get_repos_from_json(json_data):
    """Get list of unique repositories with their component mappings.
    Returns: list of dicts with 'repo', 'source', 'components', 'version'
    """

def get_repos_from_current_json(state):
    """Get repository list from current JSON (unique, for git operations).
    PREFERRED function for iterating over repositories.
    """
```

**Location:** Lines 406-648 in release-tagger
**Status:** ✅ Implemented and tested (10/10 tests passing)

---

## Phase 2: Update Core Version & Repository Functions

### 2.1 Replace version_of() Function ✅ COMPLETED
**Old implementation:** Lines 715-827 (113 lines) - reads from YAML via get_docker_compose_data()

**New implementation:** Lines 807-866 (51 lines, 55% reduction!)

```python
def version_of(repo_dir, repo_name, in_release_version=None):
    """Get version of a repository from JSON files.

    IMPORTANT: Works with REPOSITORY NAMES, not component names.
    Multiple components can share the same repository.

    Args:
        repo_dir: Base directory (now mender-client-subcomponents)
        repo_name: Name of repository (e.g., 'mender', NOT 'mender-auth')
        in_release_version: Which release to query (e.g., '5.0.0', '6.0.x', 'next')

    Returns: version string (branch name, tag, or version)
    """
    # Uses get_repos_from_json() to find repo by name
    # Handles version ranges (e.g., '5.0.0..6.0.0')
    # Returns version field from first component in repo
```

**Key Changes:**
- ✅ Parameter renamed: `component_name` → `repo_name`
- ✅ Uses `get_repos_from_json()` for repository deduplication
- ✅ Removed git_version parameter (always git now)
- ✅ Simplified logic (no docker/git type distinction)
- ✅ No Component class dependency
- ✅ Direct JSON reading from subcomponents/releases/*.json

**Status:** ✅ Implemented and tested

### 2.2 Update Repository Path Functions ✅ COMPLETED

**New function added:**
```python
def subcomponents_dir():
    """Return the location of the mender-client-subcomponents repository."""
    # Same implementation as old integration_dir()
```

**Updated function for backward compatibility:**
```python
def integration_dir():
    """Return the location of the mender-client-subcomponents repository.

    Note: This function is kept for backward compatibility but now points to
    mender-client-subcomponents instead of the deprecated integration repo.
    New code should use subcomponents_dir() instead.
    """
    return subcomponents_dir()
```

**Location:** Lines 384-403 in release-tagger
**Status:** ✅ Implemented and tested

### 2.3 Update Base Repository References
**Replace all instances of:**
- `state["integration"]` → `state["subcomponents"]` or remove entirely
- `"integration"` string literals → `"mender-client-subcomponents"`
- Repo type checks that look for "integration"

---

## Phase 3: Version Determination Phase

### 3.1 Add Changelog PR Link Display
**Modify:** `determine_version_to_include_in_release()` at line 2199

**Add at start:**
```python
# Show changelog link once (use a flag to show only first time)
if not hasattr(state, '_changelog_shown'):
    print("Changelog PRs: https://github.com/mendersoftware/mender-client-subcomponents/pulls?q=is%3Apr+is%3Aopen+label%3A%22autorelease%3A+pending%22")
    state['_changelog_shown'] = True
```

### 3.2 Change Git Log to One-Liner
**Current:** Line 2258 uses `["log", "%s..%s" % (prev_of_repo, follow_branch)]`

**Change to:**
```python
git_cmd = ["log", "--oneline", "%s..%s" % (prev_of_repo, follow_branch)]
```

### 3.3 Update Version Lookup Logic
**Modify:** Lines 2208-2253 in `determine_version_to_include_in_release()`

**Replace:**
- `version_of(integration_dir(), repo, in_integration_version=...)`
- With: `version_of(subcomponents_dir(), repo.name, in_release_version=...)`

---

## Phase 4: State Management Simplification

### 4.1 Remove "following" Branch Tracking
**Changes in:**
- `assign_default_following_branch()` - Remove or simplify
- `find_default_following_branch()` - Remove or simplify
- State updates that set `state[repo]["following"]` - Remove

**Replace with:**
- Read branch from current JSON file when needed
- Add helper: `get_component_branch_from_json(component_name)`

### 4.2 Update State Structure
**Remove from state:**
```python
state[repo]["following"]  # Read from JSON instead
state["integration"]      # No longer needed
```

**Keep in state:**
```python
state["repo_dir"]         # Base directory for component repos
state["version"]          # Release version (e.g., "6.0.0")
state[component_name]["version"]  # Decided version for component
```

---

## Phase 5: Tag Generation & JSON Commits

### 5.1 Modify generate_new_tags()
**Current:** Line 1247

**Changes:**
- Remove docker-compose file modifications
- Remove version bumps in YAML
- Instead: Create/update JSON file in temp checkout

**New flow:**
```python
# 1. Read current JSON (6.0.x.json)
# 2. For each component, update version to build tag or final tag
# 3. Write new JSON (6.0.0-build1.json or 6.0.0.json)
# 4. If build tag: leaf commit, tag only, don't push branch
# 5. If final tag: commit, tag, push branch
```

### 5.2 Modify tag_and_push()
**Current:** Line 1341 - creates temp checkout of integration, modifies YAMLs

**Replace with:**
```python
def tag_and_push(state, tag_avail, next_tag_avail, final):
    # Create temp checkout of mender-client-subcomponents
    tmpdir = setup_temp_git_checkout(
        state, "mender-client-subcomponents", current_branch
    )

    # Read current JSON
    current_json = read_release_json(get_current_json_path(state))

    # Create new JSON with updated versions
    new_json = create_updated_json(current_json, next_tag_avail)

    # Write new JSON file
    json_filename = f"{next_tag_avail['version']}.json"
    write_release_json(os.path.join(tmpdir, "subcomponents/releases", json_filename), new_json)

    # Commit
    commit_json_file(tmpdir, json_filename, next_tag_avail)

    # Fetch to real repo
    execute_git(state, "mender-client-subcomponents", ["fetch", tmpdir, "HEAD"])

    # Tag all component repos
    tag_component_repos(state, next_tag_avail)

    # Push behavior depends on final vs build
    if final:
        # Push branch and tags
        push_final_release(state, next_tag_avail)
    else:
        # Only push tags (leaf commit)
        push_build_tags_only(state, next_tag_avail)

    cleanup_temp_git_checkout(tmpdir)
```

### 5.3 Update check_tag_availability()
**Current:** Line 1013

**Minor changes:**
- Remove references to `Component.get_components_of_type("git")`
- Replace with: reading component list from current JSON
- Keep tag scanning logic in component repos (unchanged)

---

## Phase 6: Menu Operations

### 6.1 Remove Menu Options
**In do_release()** at line 2317:

**Remove from menu:**
```python
# Line ~2407: Remove "B) Trigger build"
# Line ~2410: Remove "D) Update Docker tags"
```

**Remove handlers:**
```python
# elif reply.lower() == "b": trigger_build(...)  - Remove
# elif reply.lower() == "d": push_latest_docker_tags(...) - Remove
```

**Keep helper functions:** `trigger_build()`, `push_latest_docker_tags()` for manual use

### 6.2 Modify "I" Option
**Current:** Line 2422 - "Put currently followed branch names into integration's git-versions"

**Replace with:**
```python
print("  I) Commit current JSON to mender-client-subcomponents")
```

**Handler:**
```python
elif reply.lower() == "i":
    do_commit_json_file(state)
```

**New function:**
```python
def do_commit_json_file(state):
    """Commit current JSON file to mender-client-subcomponents branch."""
    # Similar to do_git_version_branches_from_follows but for JSON
    # Create temp checkout
    # Write/update JSON with current state versions
    # Commit and push
```

---

## Phase 7: Branch Creation & Management

### 7.1 Update create_release_branches()
**Current:** Line 1976 - creates X.Y.x branches in component repos

**Changes:**
- Keep branch creation logic (mostly unchanged)
- After creating branches, create X.Y.x.json file
- Commit and push X.Y.x.json to mender-client-subcomponents

**Add:**
```python
# After branches created:
create_and_commit_release_json(state, tag_avail)
```

### 7.2 Keep Most Git Operations As-Is
**No changes needed:**
- `refresh_repos()` - git fetch operations
- `purge_build_tags()` - cleanup build tags
- `merge_release_tag()` - merge operations
- `find_upstream_remote()` - remote detection
- `execute_git()` - git command wrapper

---

## Phase 8: Initialization Flow

### 8.1 Update do_release() Initialization
**Current:** Line 2317

**Changes:**
```python
# 1. Load or create state (keep as-is)

# 2. Determine repo_dir (keep as-is)
if state_value(state, ["repo_dir"]) is None:
    reply = ask("Which directory contains all the Git repositories? ")
    update_state(state, ["repo_dir"], reply)

# 3. Determine release version (keep as-is)
if state_value(state, ["version"]) is None:
    update_state(state, ["version"], ask("Which release will this be? "))

# 4. NEW: Verify we're in subcomponents repo
verify_in_subcomponents_repo()

# 5. NEW: Read next.json to get component list
json_data = read_release_json("subcomponents/releases/next.json")
components = get_component_list_from_json(json_data)

# 6. Fetch repos (optional, keep as-is)
if ask("Fetch latest tags/branches? "):
    refresh_repos(state)

# 7. Version determination loop - REPLACE Component.get_components_of_type
# OLD: repos = sorted(Component.get_components_of_type("git"), key=repo_sort_key)
# NEW: repos = sorted(components, key=lambda c: c['name'])
while len(repos) > 0:
    repo = repos.pop(0)
    if not determine_version_to_include_in_release(state, repo):
        repos.append(repo)
```

---

## Phase 9: Helper & Utility Updates

### 9.1 Update Repo Iteration Patterns
**CRITICAL: Use repository-based iteration for git operations!**

**Find and replace pattern for git operations:**
```python
# OLD:
for repo in Component.get_components_of_type("git"):
    repo_name = repo.git()
    # ... git operations ...

# NEW (CORRECT - deduplicates by source):
for repo_info in get_repos_from_current_json(state):
    repo_name = repo_info['repo']
    components = repo_info['components']  # List of component names
    # ... git operations on repo_name ...
    # Example: execute_git(state, repo_name, ["fetch"])
```

**WRONG pattern (DO NOT USE for git operations):**
```python
# This would perform git operations multiple times on same repo!
for component in get_component_list_from_json(json_data):
    repo_name = component['name']  # WRONG! This is component name
    # ... git operations ...  # Would duplicate for mender-auth and mender-update
```

**When to use component iteration:**
- Only for JSON structure manipulation
- Only when NOT performing git operations
- Example: Building a new JSON file structure

**When to use repository iteration:**
- All git operations (fetch, tag, log, etc.)
- Version determination (interactive prompts)
- State management (state uses repo names as keys)

### 9.2 Add JSON Context Helpers ✅ COMPLETED

**Already implemented:**
```python
def get_repos_from_current_json(state):
    """Get repository list from current JSON (unique, for git operations).
    Returns: list of repo dicts with 'repo', 'source', 'components', 'version'
    """
    json_path = get_current_release_json_path(state)
    json_data = read_release_json(json_path)
    return get_repos_from_json(json_data)
```

**Status:** ✅ Already implemented (lines 640-648)

**Future enhancement (if needed):**
```python
def determine_current_json_path(state):
    """Determine which JSON to read based on current release state."""
    # If final tag exists: X.Y.Z.json
    # Elif release branch exists: X.Y.x.json
    # Else: next.json
```
Note: `get_current_release_json_path(state)` already handles this

### 9.3 Update report_release_state()
**Current:** Line 1105

**Changes:**
- Remove Component class usage
- Use component list from JSON
- Keep display logic mostly same

---

## Phase 10: Testing & Cleanup

### 10.1 Remove Dead Code
**After all changes, remove:**
- Unused YAML parsing functions
- Docker compose related functions
- Component class and all methods
- `version_specific_docker_compose_data_patching()`
- `set_component_version_to()` (if it was for YAML)

### 10.2 Update Imports
**Remove if unused:**
```python
# yaml import might stay for state file
# Remove any docker-compose specific imports
```

### 10.3 Add New Constants
```python
SUBCOMPONENTS_REPO_NAME = "mender-client-subcomponents"
RELEASES_JSON_DIR = "subcomponents/releases"
CHANGELOG_PR_URL = "https://github.com/mendersoftware/mender-client-subcomponents/pulls?q=is%3Apr+is%3Aopen+label%3A%22autorelease%3A+pending%22"
```

---

## Implementation Order

### Week 1: Foundation ✅ COMPLETED
1. ✅ Phase 1.2: Add JSON data layer functions
   - Basic JSON operations: read, write, get path
   - Component-level operations: list, find, get source, get components for source
   - **Repository-level operations: extract repo name, unique sources, repos from JSON**
2. ✅ Phase 2.1: Replace version_of() function
   - **Updated to use repository names instead of component names**
   - Simplified from 113 lines to 51 lines
   - Uses get_repos_from_json() for deduplication
3. ✅ Phase 2.2: Update repository path functions
   - Added subcomponents_dir()
   - Updated integration_dir() for backward compatibility
4. ✅ Test: Can read JSON and get component versions
   - **10/10 tests passing including source deduplication tests**
   - Verified mender repo has 2 components (mender-auth, mender-update)
   - Verified 7 unique sources from 8 components

**Key Achievement:** Established source-based architecture for repository deduplication

### Week 2: Core Flow
5. Phase 4: Simplify state management
6. Phase 3: Update version determination phase
7. Phase 8: Update initialization flow
8. Test: Can start release and determine versions

### Week 3: Tag Operations
9. Phase 5.3: Update check_tag_availability()
10. Phase 5.1-5.2: Modify tag generation and push
11. Phase 7: Update branch creation
12. Test: Can create build tags and final tags

### Week 4: Menu & Cleanup
13. Phase 6: Update menu operations
14. Phase 9: Update helpers and utilities
15. Phase 10: Remove dead code
16. Phase 1.1: Remove Component class (last!)
17. Final testing: Complete release cycle

---

## Risk Mitigation

### High Risk Areas
1. **Tag generation flow** - Most complex change
   - Mitigation: Test with dry-run mode extensively

2. **State management** - Structure will change, old state files incompatible
   - Mitigation: Users start fresh releases (no migration needed)

3. **Temp checkout pattern** - Must work correctly for leaf commits
   - Mitigation: Test build tag flow thoroughly

### Testing Strategy
1. Create test release branch in subcomponents repo
2. Use test component repos (or local clones)
3. Test each phase incrementally
4. Keep old tool available for comparison
5. Document differences in behavior

---

## Success Criteria

- [ ] Can read next.json and start a release
- [ ] Can determine versions for all components interactively
- [ ] Can create X.Y.x.json with branch names
- [ ] Can create build tags (leaf commits)
- [ ] Can create final tags (pushed commits)
- [ ] Can purge build tags from component repos
- [ ] JSON files are correctly formatted and committed
- [ ] State file can be saved and resumed
- [ ] All menu options work as expected
- [ ] No references to integration repo remain
- [ ] No references to Component class remain
- [ ] No references to YAML parsing remain (except state file)
