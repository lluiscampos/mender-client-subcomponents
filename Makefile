SHELL := /bin/bash

ALL_RELEASES := $(sort $(patsubst subcomponents/releases/%.json,%,$(wildcard subcomponents/releases/*.json)))
# By default define RELEASE from Git tag. Remove the release candidate suffix
GIT_VERSION = $(shell git describe --tags --exact-match 2>/dev/null | sed 's/-build[0-9]\+$$//')
RELEASE ?= $(GIT_VERSION)

DESTDIR ?= /
prefix ?= $(DESTDIR)
inventorydir ?= /usr/share/mender/inventory

CONFLICTS_SEP ?=
CONFLICTS_FILE ?= build/conflicts

help:
	@echo 'Main commands:'
	@echo '  build                      - Run all build-* targets'
	@echo '  build-inventory-script     - Build the inventory script'
	@echo '  install                    - Run all install-* targets'
	@echo '  install-inventory-script   - Install the inventory script'
	@echo '  generate-conflicts         - Output conflicts string for package/recipe of this release'
	@echo '  clean                      - Remove auto generated files'
	@echo ''
	@echo 'Using Mender Client release: $(RELEASE)'
	@echo 'Available versions: $(ALL_RELEASES)'
	@echo ''
	@echo 'Use "RELEASE=... make" to specify a release. When not specified,
	@echo 'it defaults to the checked out Git tag. And if not in a Git tag,
	@echo 'it uses "unsupported" for the versions and generates no conflicts'
	@echo ''
	@echo 'Other commands:'
	@echo '  check-deps                 - Check dependencies'


inventory-script/mender-inventory-client-version: build-inventory-script

build: build-inventory-script

build-inventory-script:
	@if [ -z "$(RELEASE)" ]; then \
		echo "Warning: No RELEASE specified, using 'unsupported'"; \
		MENDER_CLIENT_VERSION=unsupported envsubst '$$MENDER_CLIENT_VERSION' < inventory-script/mender-inventory-client-version.in > inventory-script/mender-inventory-client-version; \
	else \
		test -f subcomponents/releases/$(RELEASE).json || { \
			echo "Error: Release file subcomponents/releases/$(RELEASE).json not found"; \
			exit 1; \
		}; \
		MENDER_CLIENT_VERSION=$$(jq -r '.version' subcomponents/releases/$(RELEASE).json); \
		test "$$MENDER_CLIENT_VERSION" != "null" || { \
			echo "Error: Could not extract version from subcomponents/releases/$(RELEASE).json"; \
			exit 1; \
		}; \
		MENDER_CLIENT_VERSION=$$MENDER_CLIENT_VERSION envsubst '$$MENDER_CLIENT_VERSION' < inventory-script/mender-inventory-client-version.in > inventory-script/mender-inventory-client-version; \
	fi

install: install-inventory-script

install-inventory-script: inventory-script/mender-inventory-client-version
	install -d -m 755 $(prefix)$(inventorydir)
	install -m 755 inventory-script/mender-inventory-client-version $(prefix)$(inventorydir)/

$(CONFLICTS_FILE): generate-conflicts

generate-conflicts:
	@mkdir --parents $(shell dirname $(CONFLICTS_FILE))
	@if [ -z "$(RELEASE)" ]; then \
		echo "Warning: No RELEASE specified, generating empty conflicts file"; \
		echo "" > $(CONFLICTS_FILE); \
	else \
		test -f subcomponents/releases/$(RELEASE).json || { \
			echo "Error: Release file subcomponents/releases/$(RELEASE).json not found"; \
			exit 1; \
		}; \
		jq -r '.components[] | "\(.name) (< \(.version))$(CONFLICTS_SEP) \(.name) (> \(.version))$(CONFLICTS_SEP)"' \
			subcomponents/releases/$(RELEASE).json | \
			tr '\n' ' ' | \
			sed 's/$(CONFLICTS_SEP) $$//' | tee $(CONFLICTS_FILE); \
	fi

check-dependencies:
	@missing=""; \
	for cmd in jq envsubst; do \
		which $$cmd >/dev/null 2>&1 || missing="$$missing $$cmd"; \
	done; \
	if [ -n "$$missing" ]; then \
		echo "Error: The following required dependencies are missing:$$missing"; \
		exit 1; \
	fi
	@echo "All dependencies are installed"

clean:
	rm -rfv $(CONFLICTS_FILE)
	rm -rfv inventory-script/mender-inventory-client-version


.PHONY: help
.PHONY: build
.PHONY: build-inventory-script
.PHONY: generate-conflicts
.PHONY: check-dependencies
.PHONY: clean
