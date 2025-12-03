SHELL := /bin/bash

ALL_RELEASES := $(sort $(patsubst subcomponents/releases/%.json,%,$(wildcard subcomponents/releases/*.json)))
LATEST_RELEASE := $(shell echo "$(ALL_RELEASES)" | tr ' ' '\n' | sort -V | tail -n1)
RELEASE ?= $(LATEST_RELEASE)

DESTDIR ?= /
prefix ?= $(DESTDIR)
inventorydir ?= /usr/share/mender/inventory

CONFLICTS_SEP ?=

help:
	@echo 'Main commands:'
	@echo '  build                      - Run all build-* targets'
	@echo '  build-inventory-script     - Build the inventory script'
	@echo '  install                    - Run all install-* targets'
	@echo '  install-inventory-script   - Install the inventory script'
	@echo '  generate-conflicts         - Output conflicts string for package/recipe of this release'
	@echo ''
	@echo 'Using Mender Client release: $(RELEASE)'
	@echo 'Available versions: $(ALL_RELEASES)'
	@echo 'Use "RELEASE=... make" to specify a release'
	@echo ''
	@echo 'Other commands:'
	@echo '  check-deps                 - Check dependencies'


inventory-script/mender-inventory-client-version: build-inventory-script

build: build-inventory-script

build-inventory-script:
	$(eval MENDER_CLIENT_VERSION := $(shell jq -r '.version' subcomponents/releases/$(RELEASE).json))
	MENDER_CLIENT_VERSION=$(MENDER_CLIENT_VERSION) envsubst '$$MENDER_CLIENT_VERSION' < inventory-script/mender-inventory-client-version.in > inventory-script/mender-inventory-client-version

install: install-inventory-script

install-inventory-script: inventory-script/mender-inventory-client-version
	install -d -m 755 $(prefix)$(inventorydir)
	install -m 755 inventory-script/mender-inventory-client-version $(prefix)$(inventorydir)/

generate-conflicts:
	@jq -r '.components[] | "\(.name) (< \(.version))$(CONFLICTS_SEP) \(.name) (> \(.version))$(CONFLICTS_SEP)"' subcomponents/releases/$(RELEASE).json | tr '\n' ' ' | sed 's/$(CONFLICTS_SEP) $$//'

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


.PHONY: help
.PHONY: build
.PHONY: build-inventory-script
.PHONY: generate-conflicts
.PHONY: check-dependencies
