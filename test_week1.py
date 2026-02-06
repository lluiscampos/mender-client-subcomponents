#!/usr/bin/env python3
"""
Test script for Week 1 implementation:
- Phase 1.2: JSON data layer functions
- Phase 2.1: Replace version_of() function
- Phase 2.2: Update repository path functions
"""

import sys
import os

# Add release-scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'release-scripts'))

# Import the functions we want to test
# We need to do this carefully since release-tagger isn't a .py file
import types

release_tagger_path = os.path.join(os.path.dirname(__file__), 'release-scripts', 'release-tagger')

# Create a module
release_tagger = types.ModuleType('release_tagger')
release_tagger.__file__ = release_tagger_path

# Read and execute the file
with open(release_tagger_path, 'r') as f:
    code = f.read()
    exec(code, release_tagger.__dict__)

sys.modules['release_tagger'] = release_tagger

def test_read_json():
    """Test reading JSON files."""
    print("=" * 60)
    print("TEST 1: Read next.json")
    print("=" * 60)

    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            'subcomponents', 'releases', 'next.json'
        )
        data = release_tagger.read_release_json(json_path)

        print(f"✓ Successfully read {json_path}")
        print(f"  Version: {data['version']}")
        print(f"  Number of components: {len(data['components'])}")
        print(f"  First component: {data['components'][0]['name']}")
        return True
    except Exception as e:
        print(f"✗ Failed to read JSON: {e}")
        return False

def test_get_component_list():
    """Test getting component list from JSON."""
    print("\n" + "=" * 60)
    print("TEST 2: Get component list from JSON")
    print("=" * 60)

    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            'subcomponents', 'releases', 'next.json'
        )
        data = release_tagger.read_release_json(json_path)
        components = release_tagger.get_component_list_from_json(data)

        print(f"✓ Got {len(components)} components:")
        for comp in components:
            print(f"  - {comp['name']}: {comp['version']} (from {comp['source']})")
        return True
    except Exception as e:
        print(f"✗ Failed to get component list: {e}")
        return False

def test_find_component():
    """Test finding a specific component."""
    print("\n" + "=" * 60)
    print("TEST 3: Find specific component in JSON")
    print("=" * 60)

    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            'subcomponents', 'releases', 'next.json'
        )
        data = release_tagger.read_release_json(json_path)

        # Test finding existing component
        component = release_tagger.find_component_in_json(data, 'mender-auth')
        if component:
            print(f"✓ Found 'mender-auth': version={component['version']}")
        else:
            print("✗ Failed to find 'mender-auth'")
            return False

        # Test finding non-existing component
        component = release_tagger.find_component_in_json(data, 'non-existing')
        if component is None:
            print("✓ Correctly returned None for non-existing component")
        else:
            print("✗ Should have returned None for non-existing component")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_subcomponents_dir():
    """Test subcomponents_dir() function."""
    print("\n" + "=" * 60)
    print("TEST 4: Get subcomponents directory")
    print("=" * 60)

    try:
        path = release_tagger.subcomponents_dir()
        print(f"✓ subcomponents_dir() = {path}")

        # Verify it exists
        if os.path.isdir(path):
            print(f"✓ Directory exists")
        else:
            print(f"✗ Directory does not exist")
            return False

        # Verify it has expected structure
        releases_dir = os.path.join(path, 'subcomponents', 'releases')
        if os.path.isdir(releases_dir):
            print(f"✓ Found subcomponents/releases directory")
        else:
            print(f"✗ subcomponents/releases directory not found")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_integration_dir():
    """Test that integration_dir() now points to subcomponents."""
    print("\n" + "=" * 60)
    print("TEST 5: integration_dir() compatibility")
    print("=" * 60)

    try:
        int_path = release_tagger.integration_dir()
        sub_path = release_tagger.subcomponents_dir()

        if int_path == sub_path:
            print(f"✓ integration_dir() correctly points to subcomponents_dir()")
            print(f"  Path: {int_path}")
        else:
            print(f"✗ Paths don't match:")
            print(f"  integration_dir(): {int_path}")
            print(f"  subcomponents_dir(): {sub_path}")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_get_current_release_json_path():
    """Test getting JSON path for different versions."""
    print("\n" + "=" * 60)
    print("TEST 6: Get current release JSON path")
    print("=" * 60)

    try:
        # Test default (should return next.json)
        path = release_tagger.get_current_release_json_path()
        if path.endswith('next.json'):
            print(f"✓ Default returns next.json: {path}")
        else:
            print(f"✗ Default should return next.json, got: {path}")
            return False

        # Test with specific version
        path = release_tagger.get_current_release_json_path(version='5.0.0')
        if path.endswith('5.0.0.json'):
            print(f"✓ Version '5.0.0' returns 5.0.0.json: {path}")
        else:
            print(f"✗ Version '5.0.0' should return 5.0.0.json, got: {path}")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_extract_repo_name():
    """Test extracting repository name from source URL."""
    print("\n" + "=" * 60)
    print("TEST 7: Extract repository name from source")
    print("=" * 60)

    try:
        # Test with standard GitHub URL
        repo = release_tagger.extract_repo_name_from_source('github.com/mendersoftware/mender')
        if repo == 'mender':
            print(f"✓ Extracted 'mender' from GitHub URL")
        else:
            print(f"✗ Expected 'mender', got '{repo}'")
            return False

        # Test with trailing slash
        repo = release_tagger.extract_repo_name_from_source('github.com/mendersoftware/mender-connect/')
        if repo == 'mender-connect':
            print(f"✓ Extracted 'mender-connect' with trailing slash")
        else:
            print(f"✗ Expected 'mender-connect', got '{repo}'")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_unique_sources():
    """Test getting unique sources from JSON (deduplication)."""
    print("\n" + "=" * 60)
    print("TEST 8: Get unique sources from JSON")
    print("=" * 60)

    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            'subcomponents', 'releases', 'next.json'
        )
        data = release_tagger.read_release_json(json_path)
        sources = release_tagger.get_unique_sources_from_json(data)

        print(f"✓ Got {len(sources)} unique sources:")
        for source in sources:
            repo_name = release_tagger.extract_repo_name_from_source(source)
            print(f"  - {repo_name} ({source})")

        # Verify we have fewer sources than components (due to mender having 2 components)
        num_components = len(data['components'])
        if len(sources) < num_components:
            print(f"✓ Sources deduplicated: {len(sources)} sources from {num_components} components")
        else:
            print(f"✗ Expected deduplication: {len(sources)} sources from {num_components} components")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_repos_from_json():
    """Test getting repository list with component mappings."""
    print("\n" + "=" * 60)
    print("TEST 9: Get repos from JSON with component mappings")
    print("=" * 60)

    try:
        json_path = os.path.join(
            os.path.dirname(__file__),
            'subcomponents', 'releases', 'next.json'
        )
        data = release_tagger.read_release_json(json_path)
        repos = release_tagger.get_repos_from_json(data)

        print(f"✓ Got {len(repos)} unique repositories:")
        for repo_info in repos:
            print(f"  - {repo_info['repo']}: {len(repo_info['components'])} component(s)")
            for comp_name in repo_info['components']:
                print(f"    * {comp_name}")

        # Find mender repo and verify it has multiple components
        mender_repo = next((r for r in repos if r['repo'] == 'mender'), None)
        if mender_repo:
            if len(mender_repo['components']) > 1:
                print(f"✓ mender repo has {len(mender_repo['components'])} components: {mender_repo['components']}")
            else:
                print(f"✗ Expected mender repo to have multiple components")
                return False
        else:
            print(f"✗ Could not find mender repo")
            return False

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_version_of():
    """Test the new version_of() function with REPO NAMES."""
    print("\n" + "=" * 60)
    print("TEST 10: version_of() function (using repo names)")
    print("=" * 60)

    try:
        # Test with REPO NAME (mender, not mender-auth)
        version = release_tagger.version_of(None, 'mender', in_release_version='next')
        print(f"✓ mender repo in next.json: {version}")

        # Test getting version from 5.0.0.json
        version = release_tagger.version_of(None, 'mender', in_release_version='5.0.0')
        print(f"✓ mender repo in 5.0.0.json: {version}")

        # Test getting version from 5.0.3.json with different repo
        version = release_tagger.version_of(None, 'mender-connect', in_release_version='5.0.3')
        print(f"✓ mender-connect repo in 5.0.3.json: {version}")

        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n")
    print("*" * 60)
    print("* Week 1 Implementation Tests (Source-based)")
    print("*" * 60)
    print()

    tests = [
        test_read_json,
        test_get_component_list,
        test_find_component,
        test_subcomponents_dir,
        test_integration_dir,
        test_get_current_release_json_path,
        test_extract_repo_name,
        test_unique_sources,
        test_repos_from_json,
        test_version_of,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
