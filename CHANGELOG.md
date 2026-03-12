
---

# Older releases (pre Mender Client 6.0)

The release notes & changelogs can be found in the pages for the individual components:

* [mender](20.Mender-Client/docs.md)
* [mender-connect](21.mender-connect/docs.md)
* [mender-configure-module](22.mender-configure-module/docs.md)
* [mender-flash](25.mender-flash/docs.md)
* [mender-binary-delta](50.mender-binary-delta/docs.md)
* [monitor-client](51.monitor-client/docs.md)

The following release notes & changelogs are for the `mender` repository alone.

## mender 5.0.3

_Released 11.03.2025_

### Changelogs

#### mender (5.0.3)

New changes in mender since 5.0.2:

##### Bug Fixes

* Fix an issue where a user-aborted deployment would reboot and rollback
  during e.g. download. This is fixed by adding a new state event, `DeploymentAborted`,
  which is posted when sending status updates to the server. Each state that sends
  deployment status now explicitly checks if the deployment is aborted and handles
  it accordingly.
  ([ME-527](https://northerntech.atlassian.net/browse/ME-527))
* Fix an issue where mender-update hangs when network connection is
  lost during artifact download. Implement a 5-minute timeout in `AsyncReadNextBodyPart`
  to allow the HTTP resumer to resume the download.
  ([MEN-8717](https://northerntech.atlassian.net/browse/MEN-8717))
* Add warning and instruction to use space for separating multiple `NO_PROXY` values
  ([ME-586](https://northerntech.atlassian.net/browse/ME-586))

##### Other

* Use the new package repositories
  ([QA-1090](https://northerntech.atlassian.net/browse/QA-1090))


## mender 5.0.2

_Released 07.24.2025_

### Changelogs

#### mender (5.0.2)

New changes in mender since 5.0.1:

##### Bug Fixes

* Fix issue where trailing bytes in an HTTP response
  break parsing of the future HTTP responses, resulting in `bad
  version` errors and failed HTTP requests
  ([MEN-8554](https://northerntech.atlassian.net/browse/MEN-8554))
* Make mender-inventory-geo work with both wget provided by busybox and full version of wget
  ([MEN-8548](https://northerntech.atlassian.net/browse/MEN-8548))


#### mender (5.0.1)

New changes in mender since 5.0.0:

##### Bug fixes

* Clear the inventory data hash on re-authentication
  ([MEN-7873](https://northerntech.atlassian.net/browse/MEN-7873))
* All errors on attempts to communicate with the server
  are retried with an exponential backoff. This aligns the behavior
  of the state machine with Mender Client 3.
  ([MEN-7938](https://northerntech.atlassian.net/browse/MEN-7938))
* Fix issue where any error in Sync state (triggered for
  example with an error in Sync_Enter state scripts) leaves the client
  stuck in idle state forever and no new polls for update nor submit of
  inventory would be attempted again.
  ([MEN-7900](https://northerntech.atlassian.net/browse/MEN-7900))
* Compile with Boost 1.87
  ([MEN-8051](https://northerntech.atlassian.net/browse/MEN-8051))
* Fix deployment on 32 bit systems when rootfs is larger than 4Gb
  ([MEN-8062](https://northerntech.atlassian.net/browse/MEN-8062))
* Use EscapeString when generating JSON for supplied artifact data
  ([MEN-7974](https://northerntech.atlassian.net/browse/MEN-7974))
* Set a maximum of two tries for `mender-inventory-geo` when
  gathering geo info to avoid hanging for many tries when gathering the
  inventory.


## mender 5.0.0

_Released 12.18.2024_

### Changelogs

#### mender (5.0.0)

New changes in mender since 4.0.5:

##### Bug fixes

* Fix a bug where a failure in checking the working directory
  will not exit cleanly from `Cleanup` state.
* changed bash to sh and updated code to be compatible with sh
  and the new parsing of passthrough args.
* Improve error messages when executable can't be found.
* Fall back on bootloader when boot env modification tool is broken.
* Don't hide out-of-space messages when streaming in update modules.
* Fix download failure to always do a proper
  cancellation and cleanup of internal HTTP stuctures to avoid
  breaking future HTTP requests. Fixes `bad_version` error.
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))
* Fix download resuming to reset the HTTP state and
  avoid repeatedly hitting the same error in case of a bad state
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))
* Fix inventory reporting of device_type to correctly select
  the file based on Mender configuration and Mender environment variables
* On failures attempting to communicate with the server when
  submitting inventory or polling for deployment, a backoff mechanism
  will cancel and take over for the `InventoryPollIntervalSeconds` and
  `UpdatePollIntervalSeconds` intervals. The maxmimum backoff interval
  is configured with `RetryPollIntervalSeconds`, and it will retry
  `RetryPollCount` times. This allows mender-update to recover quicker
  in case of potential race conditions, such as if mender-update starts
  polling before mender-auth has generated the key on first boot.
  ([MEN-7790](https://northerntech.atlassian.net/browse/MEN-7790))
* Resend the inventory when the device has reauthenticated
  ([MEN-7820](https://northerntech.atlassian.net/browse/MEN-7820))

##### Features

* Replace `--data` flag with `--datastore` flag. This aligns
  better with the environment variables with the same names. The old
  `--data` flag is still accepted for backwards compatibility, but note
  that it does not have the same meaning as the `MENDER_DATA_DIR`
  environment variable (hence the rename).
* Add mender-inventory-inventory script to default install.

  To list configured polling intervals in device inventory.
* Change the generated key from RSA to ED25519. This is
  generated if there is no key provided in the configuration file, and if
  and if there is no previously generated key. Existing keys won't be affected,
  so this will only affect installation in new devices.
  The motivation for this change is more efficient computation.
  ([MEN-7534](https://northerntech.atlassian.net/browse/MEN-7534))
* Add `--stop-before` flag which can be used with the
  `install`, `commit`, and `rollback` standalone commands to stop before
  certain states. Use `resume` to continue, which also supports the same
  flag. These are the allowed states:
  * `ArtifactInstall_Enter`
  * `ArtifactCommit_Enter`
  * `ArtifactCommit_Leave`
  * `ArtifactRollback_Enter`
  * `ArtifactFailure_Enter`
  * `Cleanup`
  The flag can be specified multiple times.
  ([MEN-7115](https://northerntech.atlassian.net/browse/MEN-7115))

##### Other

* Returns an error when passing type, or when passing
  metadata to docker-artifact gen, and overrides output path
  and name when passed as passthrough argument.
  ([MEN-7110](https://northerntech.atlassian.net/browse/MEN-7110))
* Move `deb`, `docker`, `rpm` and `script` Update Modules out
  from `mender` repository to `mender-update-modules` repository. From
  this version on, `mender` will ship by default only with `rootfs`,
  `file` and `directory` Update Modules (both in `meta-mender` recipes and
  Debian binary packages).
  ([MEN-7672](https://northerntech.atlassian.net/browse/MEN-7672))
* Add systemd mender-data-dir.service optionally installed
  with MENDER_DATA_DIR_SYSTEMD_UNIT CMake variable. This
  service historically has been in meta-mender repository and
  used elsewhere from there. By moving it to the source
  repository we'll have it better aligned with authd and
  updated services
* Fix an issue with tar archive parsing where the client
  erroneously interpreted zero-filled records at the end of the archive as
  invalid, throwing `Superfluous data at the end of the archive` error.
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))


## mender 4.0.7

_Released 03.27.2025_

### Changelogs

#### mender (4.0.7)

New changes in mender since 4.0.6:

##### Bug fixes

* Clear the inventory data hash on re-authentication
  ([MEN-7873](https://northerntech.atlassian.net/browse/MEN-7873))
* Compile with Boost 1.87
  ([MEN-8051](https://northerntech.atlassian.net/browse/MEN-8051))
* Fix deployment on 32 bit systems when rootfs is larger than 4Gb
  ([MEN-8062](https://northerntech.atlassian.net/browse/MEN-8062))
* Use EscapeString when generating JSON for supplied artifact data
  ([MEN-7974](https://northerntech.atlassian.net/browse/MEN-7974))
* Set a maximum of two tries for `mender-inventory-geo` when
  gathering geo info to avoid hanging for many tries when gathering the
  inventory.


## mender 4.0.6

_Released 12.20.2024_

### Changelogs

#### mender (4.0.6)

New changes in mender since 4.0.5:

##### Bug fixes

* Fix download failure to always do a proper
  cancellation and cleanup of internal HTTP stuctures to avoid
  breaking future HTTP requests. Fixes `bad_version` error.
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))
* Fix download resuming to reset the HTTP state and
  avoid repeatedly hitting the same error in case of a bad state
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))
* Fix inventory reporting of device_type to correctly select
  the file based on Mender configuration and Mender environment variables
* Resend the inventory when the device has reauthenticated
  ([MEN-7820](https://northerntech.atlassian.net/browse/MEN-7820))

##### Other

* Fix an issue with tar archive parsing where the client
  erroneously interpreted zero-filled records at the end of the archive as
  invalid, throwing `Superfluous data at the end of the archive` error.
  ([MEN-7810](https://northerntech.atlassian.net/browse/MEN-7810))


## mender 4.0.5

_Released 12.02.2024_

### Security fixes

* Fixed CVE-2024-55959 - Insecure permissions on private key file
  generated by the Mender Client. See the official announcement
  for more information:
  [mender.io/blog/cve-2024-55959](https://mender.io/blog/cve-2024-55959)

### Changelogs

#### mender (4.0.5)

New changes in mender since 4.0.4:

##### Bug fixes

* Fix crash when `Sync_Leave` returns error during a
  deployment. The error message would be:
  ```
  State machine event DeploymentStarted was not handled by any transition
  ```
  and would happen on the next deployment following the `Sync_Leave`
  error. With a long polling interval, this could cause the bug to be
  latent for quite a while.
  ([MEN-7379](https://northerntech.atlassian.net/browse/MEN-7379))
* Fix systemd race condition when restarting mender from
  `ArtifactReboot` script. The symptom would be an error message like:
  ```
  Process returned non-zero exit status: ArtifactReboot: Process exited with status 15
  ```
  And the `ArtifactReboot_Error` state scripts would be executed, even
  though they should not.
* Progress reader updates the output only when progressing
  ([MEN-7159](https://northerntech.atlassian.net/browse/MEN-7159))
* rootfs-image: Add missing filesystem sync when not using mender-flash.
* rootfs-image: Make it safe to roll back after `ArtifactCommit`.
* Fix error while loading OpenSSL config file, by explicitly
  initializing the SSL context prior to loading. Without the explicit
  initialisation of SSL, the config might not be properly loaded if e.g.
  it has sections specifying ssl settings. This was the case with the
  example configuration for OpenSSL 1.1.1w from Debian Bullseye.
  ([MEN-7549](https://northerntech.atlassian.net/browse/MEN-7549))
* Invalidate cached inventory data on unauthentication event
  to prevent an issue with which the client would not send inventory
  data to the server after being unauthorized and authorized again.
  ([MEN-7617](https://northerntech.atlassian.net/browse/MEN-7617))
* Fix possible integer overflow when dealing with large files
  on 32-bit platforms.
  ([MEN-7613](https://northerntech.atlassian.net/browse/MEN-7613))
* During Artifact header parsing, correctly report generic
  errors instead of returning "Multiple header entries found" error for
  any kind of error.
  ([MEN-7721](https://northerntech.atlassian.net/browse/MEN-7721))
* Verify the integrity of the `version` file content during
  Artifact parsing.
  ([MEN-7721](https://northerntech.atlassian.net/browse/MEN-7721))
* Fix potential integer underflow in Artifact's manifest parsing
  ([MEN-7722](https://northerntech.atlassian.net/browse/MEN-7722))
* Limit file name length for the Artifact manifest
  ([MEN-7722](https://northerntech.atlassian.net/browse/MEN-7722))
* Ensured strict permissions of private key files created by mender-auth
  ([MEN-7752](https://northerntech.atlassian.net/browse/MEN-7752))

##### Other

* Clarify in the update module protocol documentation that
  going into `ArtifactRollback` is still possible after an
  `ArtifactCommit`, and it must still roll back successfully. While this
  may seem like it introduces new requirements into a stable protocol,
  it's important to remember that this was always possible, if the
  device lost power after having run the steps inside `ArtifactCommit`,
  but before the device could record having done so. In this case
  `ArtifactRollback` would be the next step, so this is just formalizing
  this possibility and subsequent requirement.
* Add info level messages for inventory sent/skipped


## mender 4.0.4

_Released 08.01.2024_

### Changelogs

#### mender (4.0.4)

New changes in mender since 4.0.3:

##### Bug fixes

* Make crypto load and use the openssl.cnf file
  ([MEN-7353](https://northerntech.atlassian.net/browse/MEN-7353))
* Basic authentication (https://user:password@host/) is now supported for proxy URLs and connections
  ([MEN-7402](https://northerntech.atlassian.net/browse/MEN-7402))


## mender 4.0.3

_Released 06.12.2024_

### Changelogs

#### mender (4.0.3)

New changes in mender since 4.0.2:

##### Bug fixes

* Amend default paths printed in CLI help pages. Previously
  they could be modified by user environment variables.
  ([MEN-7133](https://northerntech.atlassian.net/browse/MEN-7133))
* Fix committing mender-update artifacts when using mender-partuuid
* Invalid Range request when content_length is 0 (unknown)
* Fix error which could sometimes happen with restrictive
  firewalls, resulting in this output:
  ```
  Programming error, should not happen: Assert `deployment_id != ""`
  ```
  ([MEN-7327](https://northerntech.atlassian.net/browse/MEN-7327))

##### Features

* Add `SYSTEMD_UNIT_DIR` CMake variable.

  Use it to customize the location of the systemd unit files. Usually it
  is set to `/lib/systemd/system`.


## mender 4.0.2

_Released 03.21.2024_

### Changelogs

#### mender (4.0.2)

New changes in mender since 4.0.1:

##### Bug fixes

* Submit inventory as soon as the device is accepted.
* Fix line processing of data when reading a single byte

  When reading a single byte it was not being saved in the trailing line
  and, eventually, lost.


## mender 4.0.1

_Released 02.12.2024_

### Statistics

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 2 (66.7%) |
| Sebastian Opsahl | 1 (33.3%) |

| Developers with the most changed lines | |
|---|---|
| Sebastian Opsahl | 54 (94.7%) |
| Kristian Amlie | 3 (5.3%) |

| Developers with the most lines removed | |
|---|---|
| Sebastian Opsahl | 7 (12.3%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 3 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 57 (100.0%) |

| Employers with the most hackers (total 2) | |
|---|---|
| Northern.tech | 2 (100.0%) |

### Changelogs

#### mender (4.0.1)

New changes in mender since 4.0.0:

##### Bug fixes

* Unify meta-data element support in mender-artifact and C++ parser, and relax to accept all valid JSON
  ([MEN-6199](https://northerntech.atlassian.net/browse/MEN-6199))
* Artifact name is now properly marked as "INCONSISTENT" if
  there is an error in the `ArtifactFailure_Leave` script during an
  installation.
* Update incorrect default value for `--data` flag in help screen.


## mender 4.0.0

_Released 01.15.2024_

### Statistics

A total of 70335 lines added, 61546 removed (delta 8789)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 478 (47.5%) |
| Ole Petter Orhagen | 246 (24.4%) |
| Vratislav Podzimek | 155 (15.4%) |
| Lluis Campos | 104 (10.3%) |
| Peter Grzybowski | 4 (0.4%) |
| Lars Erik Wik | 4 (0.4%) |
| Lukasz Finster | 3 (0.3%) |
| Adam Duskett | 2 (0.2%) |
| Alan | 2 (0.2%) |
| Alf-Rune Siqveland | 2 (0.2%) |

| Developers with the most changed lines | |
|---|---|
| Kristian Amlie | 78431 (66.4%) |
| Ole Petter Orhagen | 15419 (13.1%) |
| Vratislav Podzimek | 14779 (12.5%) |
| Lluis Campos | 7198 (6.1%) |
| Peter Grzybowski | 1055 (0.9%) |
| Adam Duskett | 535 (0.5%) |
| Lars Erik Wik | 330 (0.3%) |
| Lukasz Finster | 138 (0.1%) |
| Josef Holzmayr | 114 (0.1%) |
| Alf-Rune Siqveland | 42 (0.0%) |

| Developers with the most lines removed | |
|---|---|
| Kristian Amlie | 19656 (31.9%) |
| Adam Duskett | 132 (0.2%) |
| Josef Holzmayr | 81 (0.1%) |
| Fabio Tranchitella | 1 (0.0%) |

| Developers with the most signoffs (total 6) | |
|---|---|
| Vratislav Podzimek | 3 (50.0%) |
| Ole Petter Orhagen | 2 (33.3%) |
| Kristian Amlie | 1 (16.7%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 1001 (99.4%) |
| Tronel | 3 (0.3%) |
| aduskett@gmail.com | 2 (0.2%) |
| BlackBerry Limited | 1 (0.1%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 117379 (99.4%) |
| aduskett@gmail.com | 535 (0.5%) |
| Tronel | 138 (0.1%) |
| BlackBerry Limited | 32 (0.0%) |

| Employers with the most signoffs (total 6) | |
|---|---|
| Northern.tech | 6 (100.0%) |

| Employers with the most hackers (total 16) | |
|---|---|
| Northern.tech | 13 (81.2%) |
| aduskett@gmail.com | 1 (6.2%) |
| Tronel | 1 (6.2%) |
| BlackBerry Limited | 1 (6.2%) |

### Changelogs

#### mender (4.0.0)

Mender client version 4.0.0 has been completely rewritten from scratch in C++. To ensure a
successful migration, there are a number of changes which are important to pay attention to. The
complete list of changes is below, but for a more user friendly migration guide, please see the
[Upgrading guide](https://docs.mender.io/3.7/client-installation/install-with-debian-package/upgrading)
in the Mender documentation.

New changes in mender since 3.5.2:

##### Bug fixes

* disabled implicit conversion form Error to bool
  ([MEN-6409](https://northerntech.atlassian.net/browse/MEN-6409))
* README: add build instructions for C++-client
* latest openssl reports "no such file" if the cert doesn't exist
* Rootfs scripts in the C++ client are checked in the same way as
  `Artifact` scripts, and hence, we are now moving it to support only `version 3`.
  While in the old `Golang` client both version `2` and `3` were supported.
  ([MEN-6671](https://northerntech.atlassian.net/browse/MEN-6671))
* The client no longer erronously commits a rootfs-image
  artifact after being restarted using `systemctl restart` in the
  `ArtifactReboot` state.
  ([MEN-6633](https://northerntech.atlassian.net/browse/MEN-6633))

##### Features

* The client's HSM crypto-module support is changed so that the
  `PrivateKey` used for `authentication` is always taken from the configurations:
  `security.AuthPrivateKey`, and the `HttpsClient.private_key` is only used as the
  key for the associated certificate `HttpsClient.client_certificate`. The two can
  still use the same key, but this means now that you add the same key `url` in
  both places.
  ([MEN-6668](https://northerntech.atlassian.net/browse/MEN-6668))

##### Other

* The rootfs-image updater is no longer built in, but is an
  Update Module, available under the name `rootfs-image`.
* Remove `DbusEnabled` config option.

  Mender now always depends on DBus.
  ([MEN-6662](https://northerntech.atlassian.net/browse/MEN-6662))
* Remove `BootUtilitiesGetNextActivePart` and
  `BootUtilitiesSetActivePart` config options. These are not necessary
  anymore since the choice of tool, including its calling arguments, can
  be programmed directly into each update module instead.
  ([MEN-6662](https://northerntech.atlassian.net/browse/MEN-6662))
* Update Control support has been removed from the client.
  ([MEN-6647](https://northerntech.atlassian.net/browse/MEN-6647))
* `--forcebootstrap` is not a global cli option anymore,
  but an option specific to `mender-auth daemon` and `mender-auth
  bootstrap` commands.
  ([MEN-6679](https://northerntech.atlassian.net/browse/MEN-6679))
* Mender daemon does not anymore integrate with `syslog`,
  handling the logs is responsibility of `systemd` or the caller.
  ([MEN-6679](https://northerntech.atlassian.net/browse/MEN-6679))
* Global flag `--no-syslog` is removed.
  ([MEN-6679](https://northerntech.atlassian.net/browse/MEN-6679))
* Remove `--passphrase-file` option from command scopes where
  it has no use. Move it to `mender-auth daemon` and `mender-auth
  bootstrap` commands.
  ([MEN-6679](https://northerntech.atlassian.net/browse/MEN-6679))
* mention the deprecation of control maps
  ([MEN-6648](https://northerntech.atlassian.net/browse/MEN-6648))
* Mender client does not use HTTP Keep-Alive anymore. The
  related configuration option `Connectivity` is deprecated. The TCP
  connection will be terminated as soon as the HTTP request/response is
  finished, and every subsequent HTTP request will open a new TCP
  connection.
  ([MEN-6862](https://northerntech.atlassian.net/browse/MEN-6862))
* systemd service `mender-client` does not exist anymore.
  Dependencies shall depend either `mender-authd` or `mender-updated`.
  ([MEN-6858](https://northerntech.atlassian.net/browse/MEN-6858))


## mender 3.5.3

_Released 06.12.2024_

### Changelogs

#### mender (3.5.3)

New changes in mender since 3.5.1:

##### Bug fixes

* Fix a rare bug which could corrupt the very end of a
  rootfs-image update on a sudden powerloss. The circumstances where it
  could happen are quite specific: The filesystem size in the update
  need to *not* be a multiple of the native sector size, which is very
  uncommon. The sector size is typically 512 bytes almost everywhere,
  and hence filesystem also follow this block size, if not bigger. The
  exception is raw Flash/UBI devices, where the sector size can be much
  larger, and not a power of two, and hence these platforms may be more
  susceptible.
* doing so return 1 in Download_Enter state scripts aborts instead of retrying in an endless loop
  ([MEN-6319](https://northerntech.atlassian.net/browse/MEN-6319))
* Fix so the Download_error state script gets executed for failures due to signature
  ([MEN-6402](https://northerntech.atlassian.net/browse/MEN-6402))
* recover from a corrupted database renaming it as `broken` and starting with a new empty one
  ([MEN-6848](https://northerntech.atlassian.net/browse/MEN-6848))


## mender 3.5.2

_Released 12.28.2023_

### Statistics

| Developers with the most changesets | |
|---|---|
| Lluis Campos | 1 (33.3%) |
| Peter Grzybowski | 1 (33.3%) |
| Kristian Amlie | 1 (33.3%) |

| Developers with the most changed lines | |
|---|---|
| Peter Grzybowski | 39 (78.0%) |
| Kristian Amlie | 10 (20.0%) |
| Lluis Campos | 1 (2.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 3 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 50 (100.0%) |

| Employers with the most hackers (total 3) | | | |
|---|---|
| Northern.tech | 3 (100.0%) |

### Changelogs

#### mender (3.5.2)

New changes in mender since 3.5.1:

##### Bug fixes

* Fix a rare bug which could corrupt the very end of a
  rootfs-image update on a sudden powerloss. The circumstances where it
  could happen are quite specific: The filesystem size in the update
  need to *not* be a multiple of the native sector size, which is very
  uncommon. The sector size is typically 512 bytes almost everywhere,
  and hence filesystem also follow this block size, if not bigger. The
  exception is raw Flash/UBI devices, where the sector size can be much
  larger, and not a power of two, and hence these platforms may be more
  susceptible.

##### Features

* recover from a corrupted database renaming it as `broken` and starting with a new empty one
  ([MEN-6848](https://northerntech.atlassian.net/browse/MEN-6848))


## mender 3.5.1

_Released 07.28.2023_

### Statistics

A total of 1119 lines added, 1075 removed (delta 44)

| Developers with the most changesets | |
|---|---|
| Peter Grzybowski | 5 (38.5%) |
| Lluis Campos | 3 (23.1%) |
| Kristian Amlie | 2 (15.4%) |
| Alf-Rune Siqveland | 1 (7.7%) |
| Marcin Pasinski | 1 (7.7%) |
| Ole Petter Orhagen | 1 (7.7%) |

| Developers with the most changed lines | |
|---|---|
| Peter Grzybowski | 1024 (88.5%) |
| Alf-Rune Siqveland | 41 (3.5%) |
| Lluis Campos | 36 (3.1%) |
| Ole Petter Orhagen | 24 (2.1%) |
| Marcin Pasinski | 22 (1.9%) |
| Kristian Amlie | 10 (0.9%) |

| Developers with the most lines removed | |
|---|---|
| Ole Petter Orhagen | 23 (2.1%) |
| Lluis Campos | 2 (0.2%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 13 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 1157 (100.0%) |

| Employers with the most hackers (total 6) | |
|---|---|
| Northern.tech | 6 (100.0%) |

### Changelogs

#### mender (3.5.1)

New changes in mender since 3.5.0:

##### Bug fixes

* Authmanager can blocks forever on unbuffered chan
  ([MEN-6621](https://northerntech.atlassian.net/browse/MEN-6621))
* do a full commonInit only when needed.
  ([MEN-6618](https://northerntech.atlassian.net/browse/MEN-6618))

##### Features

* inventory script: parse and support location data.
  ([MEN-5915](https://northerntech.atlassian.net/browse/MEN-5915))

##### Other

* mender-artifact set to 3.10.x in go.mod


## mender 3.5.0

_Released 02.20.2023_

### Statistics

A total of 2751 lines added, 849 removed (delta 1902)

| Developers with the most changesets | |
|---|---|
| Lluis Campos | 16 (34.0%) |
| Kristian Amlie | 8 (17.0%) |
| Ole Petter Orhagen | 7 (14.9%) |
| Mikael Torp-Holte | 4 (8.5%) |
| Fabio Tranchitella | 3 (6.4%) |
| Josef Holzmayr | 2 (4.3%) |
| Alan | 2 (4.3%) |
| Marcin Pasinski | 1 (2.1%) |
| Alf-Rune Siqveland | 1 (2.1%) |
| Uri Ishon | 1 (2.1%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 1543 (53.4%) |
| Mikael Torp-Holte | 522 (18.0%) |
| Kristian Amlie | 381 (13.2%) |
| Michael Ho | 154 (5.3%) |
| Fabio Tranchitella | 97 (3.4%) |
| Marcin Pasinski | 72 (2.5%) |
| Ole Petter Orhagen | 58 (2.0%) |
| Josef Holzmayr | 26 (0.9%) |
| Uri Ishon | 20 (0.7%) |
| Alan | 12 (0.4%) |

| Developers with the most lines removed | |
|---|---|
| Fabio Tranchitella | 43 (5.1%) |

| Developers with the most signoffs (total 3) | |
|---|---|
| Lluis Campos | 2 (66.7%) |
| Esteban Aguero Perez | 1 (33.3%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 45 (95.7%) |
| uishon@gmail.com | 1 (2.1%) |
| callmemikeh@gmail.com | 1 (2.1%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 2718 (94.0%) |
| callmemikeh@gmail.com | 154 (5.3%) |
| uishon@gmail.com | 20 (0.7%) |

| Employers with the most signoffs (total 3) | |
|---|---|
| Northern.tech | 3 (100.0%) |

| Employers with the most hackers (total 12) | |
|---|---|
| Northern.tech | 10 (83.3%) |
| callmemikeh@gmail.com | 1 (8.3%) |
| uishon@gmail.com | 1 (8.3%) |

### Changelogs

#### mender (3.5.0)

New changes in mender since 3.4.0:

##### Bug fixes

* The daemon no longer exits in the edge case where it cannot bring
  down the proxy server due to timeouts.
  ([ME-3](https://northerntech.atlassian.net/browse/ME-3))
* The websockets are no longer left trying to open a connection to the
  server, when the proxy server is shut down.
  ([ME-3](https://northerntech.atlassian.net/browse/ME-3))
* Expand the check for new openssl version
* systemd: Always try restarting the client if it exits.
  ([ME-33](https://northerntech.atlassian.net/browse/ME-33))
* websocket connectivity through http-proxy if configured

  Enables websocket connections to be established through an
  http-proxy configurable by setting the `HTTPS_PROXY` environment
  variable. This renders services that relies on websocket
  connections, such as `mender-connect`, compatible with
  http-proxying. ([ME-5](https://northerntech.atlassian.net/browse/ME-5))
* client not to skip custom TLS if an http-proxy is configured

  Previously, Mender client supported http-proxying but ignored
  custom TLS client configuration if present. This change renders
  any custom TLS configurations, such as Mutual TLS, compatible with
  http-proxying.
  ([MEN-6009](https://northerntech.atlassian.net/browse/MEN-6009))
* do not ignore software versioning opts in the module artifact gens
  ([MEN-6026](https://northerntech.atlassian.net/browse/MEN-6026))
* Add `--no-syslog` to the service file to ensure no
  duplicate log messages in the journal.
  ([MEN-6070](https://northerntech.atlassian.net/browse/MEN-6070))
* change mender-inventory-hostinfo to use the output of hostname

##### Features

* Install bootstrap Artifact on first start-up.

  On start-up, Mender checks for the existence of an special bootstrap
  Artifact in path `/var/lib/mender/bootstrap.mender` and installs it in
  order to initialize the device database.

  This applies both for `daemon` start and cli commands `bootstrap` and
  `install`.

  The Artifact is not installed if the device already has a database. When
  the Artifact is not found (and the database is empty) the database is
  initialized with `artifact-name=unknown`.

  In addition, Mender can also understand other kinds of "empty" Artifacts
  and install them either in managed or standalone modes.
  ([MEN-2583](https://northerntech.atlassian.net/browse/MEN-2583))
* Remove support for `artifact_info` file. The initial artifact
  name will be populated in the database using a bootstrap Artifact.
  ([MEN-2583](https://northerntech.atlassian.net/browse/MEN-2583))
* do not check if the artifact is already installed
  ([MEN-6129](https://northerntech.atlassian.net/browse/MEN-6129))
* Support multiple verifications keys

  https://hub.mender.io/t/multiple-artifactverifykeys/4309/6

  Creates a new client config parameter called ArtifactVerifyKeys that is
  a list of paths to keys. Any matching key can be used to verify an
  artifact - e.g. if 5 verification keys are provided, only 1 needs to
  match to verify the artifact.
* Add a thread: <proxy> field to the proxy logger

  Now the proxy logger stands out in the logs more, and can thus be filtered
  easier with tools parsing structured logs. This means that a log line from the
  `proxy` thread goes from looking like:

  ```
  Oct 05 08:50:06 qemux86-64 mender[259]: time="2022-10-05T08:50:06Z" level=error msg="error forwarding from client to backend: websocket: close 1006 (abnormal closure): unexpected EOF"
  ```

  To:

  ```
  Oct 05 08:50:06 qemux86-64 mender[259]: time="2022-10-05T08:50:06Z" level=error thread="proxy" msg="error forwarding from client to backend: websocket: close 1006 (abnormal closure): unexpected EOF"
  ```
* The default folders (`/etc/mender`, `/usr/share/mender` and
  `/var/lib/mender`) can now be overridden through the environment
  variables: `MENDER_CONF_DIR`, `MENDER_DATA_DIR`, `MENDER_DATASTORE_DIR`.
* Add zstd compression support

##### Other

* Replace obsolescent `egrep` with `grep -E` in inventory script


## mender 3.4.0

_Released 09.25.2022_

### Statistics

A total of 1308 lines added, 668 removed (delta 640)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 7 (22.6%) |
| Mikael Torp-Holte | 4 (12.9%) |
| Alf-Rune Siqveland | 3 (9.7%) |
| Lluis Campos | 2 (6.5%) |
| Ole Petter Orhagen | 2 (6.5%) |
| Fabio Tranchitella | 2 (6.5%) |
| Maciej Tomczuk | 2 (6.5%) |
| Domenic Rodriguez | 2 (6.5%) |
| Peter Grzybowski | 2 (6.5%) |
| Drew Moseley | 2 (6.5%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 721 (51.8%) |
| Kristian Amlie | 362 (26.0%) |
| Alf-Rune Siqveland | 128 (9.2%) |
| Ole Petter Orhagen | 57 (4.1%) |
| Maciej Tomczuk | 43 (3.1%) |
| Mikael Torp-Holte | 24 (1.7%) |
| Domenic Rodriguez | 20 (1.4%) |
| Peter Grzybowski | 11 (0.8%) |
| Drew Moseley | 8 (0.6%) |
| Michael Ho | 8 (0.6%) |

| Developers with the most lines removed | |
|---|---|
| Ole Petter Orhagen | 24 (3.6%) |
| Jonas Vautherin | 3 (0.4%) |
| Kristian Amlie | 2 (0.3%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 25 (80.6%) |
| Gecko Robotics | 2 (6.5%) |
| drew@moseleynet.net | 2 (6.5%) |
| callmemikeh@gmail.com | 1 (3.2%) |
| jonas.vautherin@protonmail.ch | 1 (3.2%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 1350 (97.1%) |
| Gecko Robotics | 20 (1.4%) |
| drew@moseleynet.net | 8 (0.6%) |
| callmemikeh@gmail.com | 8 (0.6%) |
| jonas.vautherin@protonmail.ch | 5 (0.4%) |

| Employers with the most hackers (total 13) | |
|---|---|
| Northern.tech | 9 (69.2%) |
| Gecko Robotics | 1 (7.7%) |
| drew@moseleynet.net | 1 (7.7%) |
| callmemikeh@gmail.com | 1 (7.7%) |
| jonas.vautherin@protonmail.ch | 1 (7.7%) |

### Changelogs

#### mender (3.4.0)

New changes in mender since 3.3.0:

##### Bug fixes

* setenv: Fix script input syntax.
* rootfs-image-v2: Make sure to set mender_boot_part_hex
* By default we bind to 127.0.0.1:0 instead of localhost.
* Over D-Bus we return the ProxyHost equal to 127.0.0.1
* Upgrade openssl dependency to fix cast error in recent Go.
* If paused before ArtifactReboot, and then manually
  rebooting the device outside of Mender, the client will properly
  resume the update now, instead of failing and rolling back.
  ([MEN-5709](https://northerntech.atlassian.net/browse/MEN-5709))
* Append log entries to syslog at the correct level
* The client update and inventory checks are now unaffected by the use
  of the `check-update` and `send-inventory` commands. While previously, this
  would both move the intervals at which checks we're done, and also extend them
  beyond the expected polling intervals configured.
  ([MEN-5547](https://northerntech.atlassian.net/browse/MEN-5547))
* Resolve symlinks for /dev/disk/by-partlabel

##### Features

* Add DaemonLogLevel parameter in configuration file
  ([MEN-5583](https://northerntech.atlassian.net/browse/MEN-5583))

##### Other

* Upgrade mender-artifact library to v0.0.0-20220913084855-9ed8ad0d53d0


## mender 3.3.2

_Released 03.10.2023_

### Statistics

A total of 599 lines added, 142 removed (delta 457)

| Developers with the most changesets | |
|---|---|
| Mikael Torp-Holte | 3 (23.1%) |
| Kristian Amlie | 2 (15.4%) |
| Lluis Campos | 2 (15.4%) |
| Ole Petter Orhagen | 2 (15.4%) |
| Alf-Rune Siqveland | 1 (7.7%) |
| Fabio Tranchitella | 1 (7.7%) |
| Josef Holzmayr | 1 (7.7%) |
| Alan | 1 (7.7%) |

| Developers with the most changed lines | |
|---|---|
| Mikael Torp-Holte | 521 (86.5%) |
| Lluis Campos | 55 (9.1%) |
| Ole Petter Orhagen | 8 (1.3%) |
| Josef Holzmayr | 8 (1.3%) |
| Kristian Amlie | 3 (0.5%) |
| Alf-Rune Siqveland | 3 (0.5%) |
| Fabio Tranchitella | 3 (0.5%) |
| Alan | 1 (0.2%) |

| Developers with the most signoffs (total 3) | |
|---|---|
| Lluis Campos | 3 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 13 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 602 (100.0%) |

| Employers with the most signoffs (total 3) | |
|---|---|
| Northern.tech | 3 (100.0%) |

| Employers with the most hackers (total 8) | |
|---|---|
| Northern.tech | 8 (100.0%) |

### Changelogs

#### mender (3.3.2)

New changes in mender since 3.3.1:

##### Bug fixes

* Expand the check for new openssl version
* systemd: Always try restarting the client if it exits.
  ([ME-33](https://northerntech.atlassian.net/browse/ME-33))
* websocket connectivity through http-proxy if configured

  Enables websocket connections to be established through an
  http-proxy configurable by setting the `HTTPS_PROXY` environment
  variable. This renders services that relies on websocket
  connections, such as `mender-connect`, compatible with
  http-proxying.
  ([ME-5](https://northerntech.atlassian.net/browse/ME-5))
* client not to skip custom TLS if an http-proxy is configured

  Previously, Mender client supported http-proxying but ignored
  custom TLS client configuration if present. This change renders
  any custom TLS configurations, such as Mutual TLS, compatible with
  http-proxying.
  ([MEN-6009](https://northerntech.atlassian.net/browse/MEN-6009))
* do not ignore software versioning opts in the module artifact gens
  ([MEN-6026](https://northerntech.atlassian.net/browse/MEN-6026))

##### Other

* Replace obsolescent `egrep` with `grep -E` in inventory script


## mender 3.3.1

_Released 10.19.2022_

### Statistics

A total of 628 lines added, 238 removed (delta 390)

| Developers with the most changesets | |
|---|---|
| Ole Petter Orhagen | 5 (31.2%) |
| Kristian Amlie | 5 (31.2%) |
| Peter Grzybowski | 2 (12.5%) |
| Michael Ho | 1 (6.2%) |
| Mikael Torp-Holte | 1 (6.2%) |
| Lluis Campos | 1 (6.2%) |
| Maciej Tomczuk | 1 (6.2%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 418 (64.0%) |
| Ole Petter Orhagen | 92 (14.1%) |
| Kristian Amlie | 82 (12.6%) |
| Maciej Tomczuk | 40 (6.1%) |
| Peter Grzybowski | 11 (1.7%) |
| Michael Ho | 8 (1.2%) |
| Mikael Torp-Holte | 2 (0.3%) |

| Developers with the most lines removed | |
|---|---|
| Ole Petter Orhagen | 2 (0.8%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 15 (93.8%) |
| callmemikeh@gmail.com | 1 (6.2%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 645 (98.8%) |
| callmemikeh@gmail.com | 8 (1.2%) |

| Employers with the most hackers (total 7) | |
|---|---|
| Northern.tech | 6 (85.7%) |
| callmemikeh@gmail.com | 1 (14.3%) |

### Changelogs

#### mender (3.3.1)

New changes in mender since 3.3.0:

##### Bug fixes

* Upgrade openssl dependency to fix cast error in recent Go.
* If paused before ArtifactReboot, and then manually
  rebooting the device outside of Mender, the client will properly
  resume the update now, instead of failing and rolling back.
  ([MEN-5709](https://northerntech.atlassian.net/browse/MEN-5709))
* The client update and inventory checks are now unaffected by the use
  of the `check-update` and `send-inventory` commands. While previously, this
  would both move the intervals at which checks we're done, and also extend them
  beyond the expected polling intervals configured.
  ([MEN-5547](https://northerntech.atlassian.net/browse/MEN-5547))
* Append log entries to syslog at the correct level
* By default we bind to 127.0.0.1:0 instead of localhost.
* Over D-Bus we return the ProxyHost equal to 127.0.0.1
* Resolve symlinks for /dev/disk/by-partlabel
* The daemon no longer exits in the edge case where it cannot bring
  down the proxy server due to timeouts.
* The websockets are no longer left trying to open a connection to the
  server, when the proxy server is shut down.


## mender 3.3.0

_Released 06.14.2022_

### Statistics

A total of 928 lines added, 608 removed (delta 320)

| Developers with the most changesets | |
|---|---|
| Ole Petter Orhagen | 13 (43.3%) |
| Peter Grzybowski | 6 (20.0%) |
| Kristian Amlie | 4 (13.3%) |
| Domenic Rodriguez | 2 (6.7%) |
| Fabio Tranchitella | 1 (3.3%) |
| Mikael Torp-Holte | 1 (3.3%) |
| Sven Schermer | 1 (3.3%) |
| Lluis Campos | 1 (3.3%) |
| Adam Duskett | 1 (3.3%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter Orhagen | 507 (46.6%) |
| Kristian Amlie | 284 (26.1%) |
| Peter Grzybowski | 249 (22.9%) |
| Domenic Rodriguez | 20 (1.8%) |
| Sven Schermer | 16 (1.5%) |
| Lluis Campos | 9 (0.8%) |
| Fabio Tranchitella | 2 (0.2%) |
| Mikael Torp-Holte | 1 (0.1%) |
| Adam Duskett | 1 (0.1%) |

| Developers with the most lines removed | |
|---|---|
| Kristian Amlie | 54 (8.9%) |
| Lluis Campos | 2 (0.3%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 26 (86.7%) |
| Gecko Robotics | 2 (6.7%) |
| Disruptive Technologies | 1 (3.3%) |
| aduskett@gmail.com | 1 (3.3%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 1052 (96.6%) |
| Gecko Robotics | 20 (1.8%) |
| Disruptive Technologies | 16 (1.5%) |
| aduskett@gmail.com | 1 (0.1%) |

| Employers with the most hackers (total 9) | |
|---|---|
| Northern.tech | 6 (66.7%) |
| Gecko Robotics | 1 (11.1%) |
| Disruptive Technologies | 1 (11.1%) |
| aduskett@gmail.com | 1 (11.1%) |

### Changelogs

#### mender (3.3.0)

New changes in mender since 3.2.1:

##### Bug fixes

* Only fall back to older endpoints on HTTP 404's



  Make the client only fall back to older endpoints on HTTP 404 error codes when
  polling the `deployments/next` endpoint.

  Previous functionality fell back to older endpoints on all error codes. This in
  turn meant that when the client got rate-limited by the server on 429's, the
  client fell back to the older endpoints.

  The problem with this is that only the POSTv2 endpoint supports control maps, so
  when an update with control maps was in progress, the other endpoints would
  return 204, and the client would think the deployment was aborted from the server.
  ([MEN-5421](https://northerntech.atlassian.net/browse/MEN-5421))
* Fixed an issue in which long-running systems, with a long time
  between reboots, and multiple updates encountered the `Tried maximum amount of
  times` error, due to an error in the retry logic.
* Log the fallback to the `artifact_info` file at log level Warn, when
  the Artifact name can not be retrieved from the database.
* add an After systemd dependency on mender-client-data-dir
* The `mender-client.service` file now has an explicit `After`
  dependency on the `data.mount` target, to make sure it is mounted, before the
  client commences operation.
* Fix Git error when installing after the fix for the
  [CVE-2022-24765 Git
  vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2022-24765)
  ([Github's description of the
  issue](https://github.blog/2022-04-12-git-security-vulnerability-announced/)).
  This also fixes a subtle "pseudo abort" issue which can occur in the
  Yocto build environment.
* the HTTP proxy must bind on localhost, not on all the interfaces
  ([MEN-5642](https://northerntech.atlassian.net/browse/MEN-5642))
* Don't accumulate zombies when command output parsing fails.
  ([MEN-5587](https://northerntech.atlassian.net/browse/MEN-5587))
* Only capture module stdout when requested
  ([MEN-5098](https://northerntech.atlassian.net/browse/MEN-5098))
* Fix printing of update module stdout in real-time

##### Features

* Allow to disable HTTP Keep-Alive from config, set idle timeout.
* Inventory push retries and backoff.

  We use RetryPollIntervalSeconds in inventory with the exponential
  backoff via GetExponentialBackoffTime together with a new setting:
  * RetryPollCount -- the max number of tries
  * inventory by default tries 3 times with one minute intervals
    (GetExponentialBackoffTime defaults)
* RetryPollCount applies to all places where backoff is present

##### Other

* Add alternate EFI path to mender-inventory-bootloader-integration
* Add alternate EFI path to mender-inventory-bootloader-inte…
* Add support for the `GET /v2/deployments/device/deployments/{id}/update_control_map` endpoint.
  ([MEN-5542](https://northerntech.atlassian.net/browse/MEN-5542))

##### Dependabot bumps

* Aggregated Dependabot Changelogs:
  * Bumps [github.com/stretchr/testify](https://github.com/stretchr/testify) from 1.7.0 to 1.7.1.
      - [Release notes](https://github.com/stretchr/testify/releases)
      - [Commits](https://github.com/stretchr/testify/compare/v1.7.0...v1.7.1)

      ```
      updated-dependencies:
      - dependency-name: github.com/stretchr/testify
        dependency-type: direct:production
        update-type: version-update:semver-patch
      ```


## mender 3.2.1

_Released 02.02.2022_

### Statistics

A total of 113 lines added, 22 removed (delta 91)

| Developers with the most changesets | |
|---|---|
| Ole Petter Orhagen | 2 (100.0%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter Orhagen | 115 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 2 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 115 (100.0%) |

| Employers with the most hackers (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

### Changelogs

#### mender (3.2.1)

New changes in mender since 3.2.0:

* fix(client_update): Only fall back to older endpoints on HTTP 404's

  Make the client only fall back to older endpoints on HTTP 404 error codes when
  polling the `deployments/next` endpoint.

  Previous functionality fell back to older endpoints on all error codes. This in
  turn meant that when the client got rate-limited by the server on 429's, the
  client fell back to the older endpoints.

  The problem with this is that only the POSTv2 endpoint supports control maps, so
  when an update with control maps was in progress, the other endpoints would
  return 204, and the client would think the deployment was aborted from the server.
  ([MEN-5421](https://northerntech.atlassian.net/browse/MEN-5421))


## mender 3.2.0

_Released 01.24.2022_

### Statistics

A total of 4572 lines added, 1819 removed (delta 2753)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 23 (39.0%) |
| Lluis Campos | 16 (27.1%) |
| Ole Petter Orhagen | 12 (20.3%) |
| Fabio Tranchitella | 4 (6.8%) |
| Zachary T Welch | 1 (1.7%) |
| Jesus | 1 (1.7%) |
| Maciej Tomczuk | 1 (1.7%) |
| Alf-Rune Siqveland | 1 (1.7%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 2786 (53.9%) |
| Kristian Amlie | 1295 (25.1%) |
| Ole Petter Orhagen | 1035 (20.0%) |
| Fabio Tranchitella | 32 (0.6%) |
| Alf-Rune Siqveland | 9 (0.2%) |
| Jesus | 6 (0.1%) |
| Zachary T Welch | 2 (0.0%) |
| Maciej Tomczuk | 1 (0.0%) |

| Developers with the most lines removed | |
|---|---|
| Kristian Amlie | 272 (15.0%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Lluis Campos | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 57 (96.6%) |
| Timesys Corporation | 1 (1.7%) |
| wjaxxx@gmail.com | 1 (1.7%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 5158 (99.8%) |
| wjaxxx@gmail.com | 6 (0.1%) |
| Timesys Corporation | 2 (0.0%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 8) | |
|---|---|
| Northern.tech | 6 (75.0%) |
| wjaxxx@gmail.com | 1 (12.5%) |
| Timesys Corporation | 1 (12.5%) |

### Changelogs

#### mender (3.2.0)

New changes in mender since 3.1.0:

* [FIX] Fetch geo location data once per power cycle
* The client now shows output from scripts executed in the log as regular
  log messages, prefixed by the filedescriptor they are written to, and the script
  executed, like this: 'Output (stdout|stderr) from command \"/usr/bin/foo\": bar.'
  ([MEN-5098](https://northerntech.atlassian.net/browse/MEN-5098))
* Bump github.com/mendersoftware/mender-artifact to 3.6.1
* Fix error not finding active partition for systems where /dev/root is a symlink
* installer/bootenv: support systemd-boot tools
* Upgrade golang.org/x/crypto to the latest version
* Title if the update module has not already requested a reboot. This
  is done, in the case that ArtifactInstall never finished, and hence the reboot
  information from the update module is never collected.
  ([MEN-4882](https://northerntech.atlassian.net/browse/MEN-4882))
* Upgrade from deprecated `golang.org/x/crypto/ssh/terminal` to
  `golang.org/x/term`
  ([QA-235](https://northerntech.atlassian.net/browse/QA-235))
* Mender starts a local HTTP server that will proxy incoming
  requests to `/api/devices` to the currently authenticated Mender server.
  The existing D-Bus API endpoints GetJwtToken and JwtTokenStateChange
  will now return the local address together with the JWT token. Supports
  also websocket upgrade when calling
  `/api/devices/v1/deviceconnect/connect` endpoint
  ([MEN-5216](https://northerntech.atlassian.net/browse/MEN-5216))
* mender setup: Deprecate `--demo` flag and split its
  functionality across new flags `--demo-server` to configure the device
  for a Mender demo server and `--demo-polling` to use demo polling
  intervals. ([MEN-5138](https://northerntech.atlassian.net/browse/MEN-5138))
* Client will no longer cache the Authorization token from
  the server across restarts, meaning that it is no longer possible to
  end up in the situation where a rootfs update with invalid
  authorization data succeeds, only to fail authorization later on when
  the token expires.
  ([MEN-5217](https://northerntech.atlassian.net/browse/MEN-5217))
* It is no longer possible to change the identity of a device
  with a rootfs update. This was not supported before either, but worked
  in a hacky way by abusing the authorization token to get a rootfs
  update with new identity data to succeed. Afterwards the device would
  show up as a new device when the token expired.
  ([MEN-5217](https://northerntech.atlassian.net/browse/MEN-5217))
* ubi: Get rid of useless warning: `Could not resolve path link: ubi..`
* Refresh update control maps before failing an update

  Fix the issue where if a state takes longer than the expiration time
  for the enabled update control map, then by the time the client checks its
  control maps, the map is expired, and the update fails.

  Now the client refreshes the update maps from the server before each pause, and
  hence, this issue will be avoided.
  ([MEN-5096](https://northerntech.atlassian.net/browse/MEN-5096))
* Handle the possibility of losing network connectivity when refreshing
  the update control maps.
* Fix a race condition which can happen during a reboot if
  systemd kills the `reboot` command before it kills the Mender client.
  ([MEN-5340](https://northerntech.atlassian.net/browse/MEN-5340))
* When an update is paused, the client now queries the server
  for updates using the `UpdatePollIntervalSeconds` interval if it is
  shorter than `UpdateControlMapExpirationTimeSeconds`, enabling quicker
  response when continuing an update.
* Fix a (possible) file descriptor leak.
* vendor: Bump mender-artifact to latest master version


## mender 3.1.1

_Released 02.09.2022_

### Statistics

A total of 430 lines added, 58 removed (delta 372)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 7 (41.2%) |
| Ole Petter | 6 (35.3%) |
| Lluis Campos | 3 (17.6%) |
| Jesus | 1 (5.9%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter | 259 (60.1%) |
| Kristian Amlie | 151 (35.0%) |
| Lluis Campos | 15 (3.5%) |
| Jesus | 6 (1.4%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Ole Petter | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 16 (94.1%) |
| wjaxxx@gmail.com | 1 (5.9%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 425 (98.6%) |
| wjaxxx@gmail.com | 6 (1.4%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 3 (75.0%) |
| wjaxxx@gmail.com | 1 (25.0%) |

### Changelogs

#### mender (3.1.1)

New changes in mender since 3.1.0:

* Fix error not finding active partition for systems where /dev/root is a symlink
* Title if the update module has not already requested a reboot. This
  is done, in the case that ArtifactInstall never finished, and hence the reboot
  information from the update module is never collected.
  ([MEN-4882](https://northerntech.atlassian.net/browse/MEN-4882))
* Refresh update control maps before failing an update
  Fix the issue where if a state takes longer than the expiration time
  for the enabled update control map, then by the time the client checks its
  control maps, the map is expired, and the update fails.
  Now the client refreshes the update maps from the server before each pause, and
  hence, this issue will be avoided.
  ([MEN-5096](https://northerntech.atlassian.net/browse/MEN-5096))
* Handle the possibility of losing network connectivity when refreshing
  the update control maps.
* Fix a race condition which can happen during a reboot if
  systemd kills the `reboot` command before it kills the Mender client.
  ([MEN-5340](https://northerntech.atlassian.net/browse/MEN-5340))
* Fix a (possible) file descriptor leak.
* Bump github.com/mendersoftware/mender-artifact to 3.6.x


## mender 3.1.0

_Released 09.28.2021_

### Statistics

A total of 588 lines added, 396 removed (delta 192)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 11 (36.7%) |
| Lluis Campos | 5 (16.7%) |
| Alf-Rune Siqveland | 3 (10.0%) |
| Ole Petter Orhagen | 3 (10.0%) |
| Fabio Tranchitella | 2 (6.7%) |
| Uri Ishon | 2 (6.7%) |
| Prashanth Joseph Babu | 2 (6.7%) |
| Alan Martinovic | 1 (3.3%) |
| Manuel Zedel | 1 (3.3%) |

| Developers with the most changed lines | |
|---|---|
| Kristian Amlie | 414 (58.5%) |
| Ole Petter Orhagen | 117 (16.5%) |
| Lluis Campos | 58 (8.2%) |
| Prashanth Joseph Babu | 46 (6.5%) |
| Uri Ishon | 31 (4.4%) |
| Alf-Rune Siqveland | 24 (3.4%) |
| Alan Martinovic | 13 (1.8%) |
| Fabio Tranchitella | 4 (0.6%) |
| Manuel Zedel | 1 (0.1%) |

| Developers with the most lines removed | |
|---|---|
| Lluis Campos | 32 (8.1%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Kristian Amlie | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 26 (86.7%) |
| Complete Solution Robotics, LLC | 2 (6.7%) |
| prashanthjbabu@gmail.com | 2 (6.7%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 631 (89.1%) |
| prashanthjbabu@gmail.com | 46 (6.5%) |
| Complete Solution Robotics, LLC | 31 (4.4%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 9) | |
|---|---|
| Northern.tech | 7 (77.8%) |
| prashanthjbabu@gmail.com | 1 (11.1%) |
| Complete Solution Robotics, LLC | 1 (11.1%) |

### Changelogs

#### mender (3.1.0)

New changes in mender since 3.0.0:

* Fix a bug which could sometimes lead the client to do a
  rollback after it had already committed. This could happen if the
  client happened to spontaneously reboot or fail during the status
  update to the server. Doing this is not correct according to the state
  flow, and can have unexpected consequences depending on the
  combination of Update Modules and State Scripts.
  ([MEN-4830](https://northerntech.atlassian.net/browse/MEN-4830))
* mender-inventory-network: Fix incompatibility with busybox,
  by using short command line options in grep command.
  ([MEN-4851](https://northerntech.atlassian.net/browse/MEN-4851))
* Do not put useless and sometimes even incorrect zero values
  in the configuration file when running `mender setup`.
  ([MEN-4857](https://northerntech.atlassian.net/browse/MEN-4857))
* Extend logs for docker module
* Add artifact_name to device provides if not found in store
* Support passing docker run CLI arguments when deploying
  an artifact using the `docker` _update module_.
* Implement support for non-U-Boot tool names.
  The tools still have to be command line compatible with the U-Boot
  tools (either u-boot-fw-utils or libubootenv), but the names can be
  different. This allows having U-Boot tools installed alongside
  grub-mender-grubenv tools, whose new names are
  `grub-mender-grubenv-set` and `grub-mender-grubenv-print`, instead of
  `fw_setenv` and `fw_printenv`.
  The two new configuration settings `BootUtilitiesSetActivePart` and
  `BootUtilitiesGetNextActivePart` have been introduced to configure the
  names. If no names are set, then the default is to try the
  grub-mender-grubenv tools first, followed by the "fw_" tools if the
  former are not found.
  ([MEN-3978](https://northerntech.atlassian.net/browse/MEN-3978))
* Add missing filesystem sync which could produce an empty or
  corrupted Update Module file tree in
  `/var/lib/mender/modules/v3/payloads/0000/tree/files/` after an
  unexpected reboot.
* If the mender.conf file has a new server URL or tenant token, the
  client will now remove the cached authorization token upon the next restart of
  the dameon, and hence respect the new configuration, as opposed to letting it
  expire, which was the old functionality.
  ([MEN-3420](https://northerntech.atlassian.net/browse/MEN-3420))
* [FIX] Fetch geo location data once per power cycle


## mender 3.0.2

_Released 02.09.2022_

### Statistics

A total of 430 lines added, 58 removed (delta 372)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 7 (41.2%) |
| Ole Petter | 6 (35.3%) |
| Lluis Campos | 3 (17.6%) |
| Jesus | 1 (5.9%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter | 259 (60.1%) |
| Kristian Amlie | 151 (35.0%) |
| Lluis Campos | 15 (3.5%) |
| Jesus | 6 (1.4%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Ole Petter | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 16 (94.1%) |
| wjaxxx@gmail.com | 1 (5.9%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 425 (98.6%) |
| wjaxxx@gmail.com | 6 (1.4%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 3 (75.0%) |
| wjaxxx@gmail.com | 1 (25.0%) |

#### mender (3.0.2)

### Changelogs

New changes in mender since 3.0.1:

* Fix error not finding active partition for systems where /dev/root is a symlink
* Title if the update module has not already requested a reboot. This
  is done, in the case that ArtifactInstall never finished, and hence the reboot
  information from the update module is never collected.
  ([MEN-4882](https://northerntech.atlassian.net/browse/MEN-4882))
* Refresh update control maps before failing an update
  Fix the issue where if a state takes longer than the expiration time
  for the enabled update control map, then by the time the client checks its
  control maps, the map is expired, and the update fails.
  Now the client refreshes the update maps from the server before each pause, and
  hence, this issue will be avoided.
  ([MEN-5096](https://northerntech.atlassian.net/browse/MEN-5096))
* Handle the possibility of losing network connectivity when refreshing
  the update control maps.
* Fix a race condition which can happen during a reboot if
  systemd kills the `reboot` command before it kills the Mender client.
  ([MEN-5340](https://northerntech.atlassian.net/browse/MEN-5340))
* Fix a (possible) file descriptor leak.
* Bump github.com/mendersoftware/mender-artifact to 3.6.x


## mender 3.0.1

_Released 09.29.2021_

### Statistics

A total of 94 lines added, 48 removed (delta 46)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 4 (50.0%) |
| Prashanth Joseph Babu | 2 (25.0%) |
| Alf-Rune Siqveland | 1 (12.5%) |
| Lluis Campos | 1 (12.5%) |

| Developers with the most changed lines | |
|---|---|
| Prashanth Joseph Babu | 46 (48.9%) |
| Kristian Amlie | 31 (33.0%) |
| Alf-Rune Siqveland | 9 (9.6%) |
| Lluis Campos | 8 (8.5%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Kristian Amlie | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 6 (75.0%) |
| prashanthjbabu@gmail.com | 2 (25.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 48 (51.1%) |
| prashanthjbabu@gmail.com | 46 (48.9%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 3 (75.0%) |
| prashanthjbabu@gmail.com | 1 (25.0%) |


### Changelogs

#### mender (3.0.1)

New changes in mender since 3.0.0:

* Add artifact_name to device provides if not found in store
* Add missing filesystem sync which could produce an empty or
  corrupted Update Module file tree in
  `/var/lib/mender/modules/v3/payloads/0000/tree/files/` after an
  unexpected reboot.
* [FIX] Fetch geo location data once per power cycle


## mender 3.0.0

_Released 07.14.2021_

### Statistics

A total of 7715 lines added, 3584 removed (delta 4131)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 51 (48.6%) |
| Ole Petter Orhagen | 22 (21.0%) |
| Lluis Campos | 19 (18.1%) |
| Alf-Rune Siqveland | 3 (2.9%) |
| Fabio Tranchitella | 3 (2.9%) |
| Manuel Zedel | 2 (1.9%) |
| Nils Olav Kvelvane Johansen | 2 (1.9%) |
| Prashanth Joseph Babu | 2 (1.9%) |
| Grant Sloman | 1 (1.0%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter Orhagen | 4160 (51.9%) |
| Kristian Amlie | 2479 (30.9%) |
| Lluis Campos | 1175 (14.7%) |
| Alf-Rune Siqveland | 80 (1.0%) |
| Nils Olav Kvelvane Johansen | 43 (0.5%) |
| Manuel Zedel | 35 (0.4%) |
| Prashanth Joseph Babu | 25 (0.3%) |
| Fabio Tranchitella | 22 (0.3%) |
| Grant Sloman | 1 (0.0%) |

| Developers with the most signoffs (total 4) | |
|---|---|
| Ole Petter Orhagen | 3 (75.0%) |
| Lluis Campos | 1 (25.0%) |

| Developers with the most report credits (total 1) | |
|---|---|
| Alex Stout | 1 (100.0%) |

| Developers who gave the most report credits (total 1) | |
|---|---|
| Kristian Amlie | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 102 (97.1%) |
| prashanthjbabu@gmail.com | 2 (1.9%) |
| Violet Ultra Ltd | 1 (1.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 7994 (99.7%) |
| prashanthjbabu@gmail.com | 25 (0.3%) |
| Violet Ultra Ltd | 1 (0.0%) |

| Employers with the most signoffs (total 4) | |
|---|---|
| Northern.tech | 4 (100.0%) |

| Employers with the most hackers (total 9) | |
|---|---|
| Northern.tech | 7 (77.8%) |
| prashanthjbabu@gmail.com | 1 (11.1%) |
| Violet Ultra Ltd | 1 (11.1%) |

### Changelogs

#### mender (3.0.0)

New changes in mender since 2.6.0:

* mender setup: when configuring for demo using self-signed
  certificate, install the certificate in the local trust store so that
  all components in the system (namely, Mender addons) can trust the
  Mender server without extra configuration.
  ([MEN-4580](https://northerntech.atlassian.net/browse/MEN-4580))
* Warn in the log when the system certificates contain the demo cert.
* Dont Verify SSL if skip verify is set
  If skip verify is set , then we shouldnt call VerifyResult
* Fix infinite carriage return output when running in ADB shell
* Add a DBus endpoint for the UpdateControlMap, which allows
  a user to set the `ID` and `Priority` of a given update process.
  ([MEN-4535](https://northerntech.atlassian.net/browse/MEN-4535))
* The daemon will no longer crash if mender check-update or send-inventory is used before the daemon has finished its set up.
  ([MEN-4074](https://northerntech.atlassian.net/browse/MEN-4074))
* Update Modules Artifact generators: correct --software-version flag
* single-file-artifact-gen: Support concurrent executions
* single-file Update Module: fix rollback functionality
* Add UpdateControlMapBootExpirationTimeSeconds to mender.conf.
* The location of the device type file is now determined by the mender.conf file. If the device type file is not used in mender.conf, the device type file is determined by the --data flag and if the flag is not used, the device type file is set to default. In addition, the scripts and modules directories location is consistent with the --data flag now.
  ([MEN-4669](https://northerntech.atlassian.net/browse/MEN-4669))
* Implement the continue/pause/fail state machine logic
  This adds support for the explit control of the Mender state machine through the
  update control maps functionality.
  The state machine can be controlled through the verbs, puase/continue/fail in
  the states:
  * ArtifactInstall_Enter
  * ArtifactCommit_Enter
  * ArtifactReboot_Enter
  ([MEN-4549](https://northerntech.atlassian.net/browse/MEN-4549))
* Fix D-Bus timeout on errors by finishing handling
  ([MEN-4703](https://northerntech.atlassian.net/browse/MEN-4703))
* Report to deployments/status when pausing in any state
  ([MEN-4624](https://northerntech.atlassian.net/browse/MEN-4624))
* Fix race condition in menderAuthManagerService due to
  concurrent map access. This could manifest either as a crash, or as a
  failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix race condition in `dbus.RegisterMethodCallCallback` due
  to concurrent map access. This could manifest either as a crash, or as
  a failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix: Correctly log the error response message from server errors
* Fix occasional crash when exiting using SIGTERM.
* Fix: `mender-client.service` and the old `mender.service`
  services can no longer run at the same time. If anyone has both, then
  `mender.service` should be removed from the system.
* Previously the Mender client would hide output from the
  child processes it ran, leading to errors from tools such as
  `fw_printenv`, not showing up in the logs.
  Now default to showing all output from the child processes called in
  the client logs.
* The client now supports the HTTP Device API v2.
  ([MEN-4785](https://northerntech.atlassian.net/browse/MEN-4785))
* Mark deployment as failed on bad signature instead of retrying.
* CLI commands prefixed with hyphen are now deprecated, use
  instead directly the command name. For example `mender daemon`, `mender
  commit`, `mender show-artifact`, etc.
  ([MEN-4808](https://northerntech.atlassian.net/browse/MEN-4808))
* Remove deprecated flag --log-modules
  ([MEN-4808](https://northerntech.atlassian.net/browse/MEN-4808))
* Fix a bug which could sometimes lead the client to do a
  rollback after it had already committed. This could happen if the
  client happened to spontaneously reboot or fail during the status
  update to the server. Doing this is not correct according to the state
  flow, and can have unexpected consequences depending on the
  combination of Update Modules and State Scripts.
  ([MEN-4830](https://northerntech.atlassian.net/browse/MEN-4830))
* mender-inventory-network: Fix incompatibility with busybox,
  by using short command line options in grep command.
  ([MEN-4851](https://northerntech.atlassian.net/browse/MEN-4851))
* Do not put useless and sometimes even incorrect zero values
  in the configuration file when running `mender setup`.
  ([MEN-4857](https://northerntech.atlassian.net/browse/MEN-4857))

## mender 2.6.1

_Released 07.14.2021_

### Statistics

A total of 506 lines added, 215 removed (delta 291)

| Developers with the most changesets | |
|---|---|
| Lluis Campos | 6 (37.5%) |
| Kristian Amlie | 5 (31.2%) |
| Ole Petter Orhagen | 2 (12.5%) |
| Nils Olav Kvelvane Johansen | 2 (12.5%) |
| Prashanth Joseph Babu | 1 (6.2%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 290 (49.9%) |
| Kristian Amlie | 186 (32.0%) |
| Ole Petter Orhagen | 58 (10.0%) |
| Nils Olav Kvelvane Johansen | 44 (7.6%) |
| Prashanth Joseph Babu | 3 (0.5%) |

| Developers with the most lines removed | |
|---|---|
| Kristian Amlie | 47 (21.9%) |

| Developers with the most signoffs (total 2) | |
|---|---|
| Ole Petter Orhagen | 2 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 15 (93.8%) |
| prashanthjbabu@gmail.com | 1 (6.2%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 578 (99.5%) |
| prashanthjbabu@gmail.com | 3 (0.5%) |

| Employers with the most signoffs (total 2) | |
|---|---|
| Northern.tech | 2 (100.0%) |

| Employers with the most hackers (total 5) | |
|---|---|
| Northern.tech | 4 (80.0%) |
| prashanthjbabu@gmail.com | 1 (20.0%) |

### Changelogs

#### mender (2.6.1)

New changes in mender since 2.6.0:

* Dont Verify SSL if skip verify is set
  If skip verify is set , then we shouldnt call VerifyResult
* Update Modules Artifact generators: correct --software-version flag
* single-file-artifact-gen: Support concurrent executions
* single-file Update Module: fix rollback functionality
* The daemon will no longer crash if mender check-update or send-inventory is used before the daemon has finished its set up.
  ([MEN-4074](https://northerntech.atlassian.net/browse/MEN-4074))
* Fix D-Bus timeout on errors by finishing handling
  ([MEN-4703](https://northerntech.atlassian.net/browse/MEN-4703))
* The location of the device type file is now determined by the mender.conf file. If the device type file is not used in mender.conf, the device type file is determined by the --data flag and if the flag is not used, the device type file is set to default. In addition, the scripts and modules directories location is consistent with the --data flag now.
  ([MEN-4669](https://northerntech.atlassian.net/browse/MEN-4669))
* Fix race condition in menderAuthManagerService due to
  concurrent map access. This could manifest either as a crash, or as a
  failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix race condition in `dbus.RegisterMethodCallCallback` due
  to concurrent map access. This could manifest either as a crash, or as
  a failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix occasional crash when exiting using SIGTERM.
* Fix: Correctly log the error response message from server errors
* Fix a bug which could sometimes lead the client to do a
  rollback after it had already committed. This could happen if the
  client happened to spontaneously reboot or fail during the status
  update to the server. Doing this is not correct according to the state
  flow, and can have unexpected consequences depending on the
  combination of Update Modules and State Scripts.
  ([MEN-4830](https://northerntech.atlassian.net/browse/MEN-4830))
* mender-inventory-network: Fix incompatibility with busybox,
  by using short command line options in grep command.
  ([MEN-4851](https://northerntech.atlassian.net/browse/MEN-4851))

## mender 2.6.0

_Released 04.16.2021_

### Changelogs

#### mender (2.6.0)

New changes in mender since 2.5.0:

* fix, support white spaces in single-file artifacts' names
([MEN-4179](https://northerntech.atlassian.net/browse/MEN-4179))
* Change provider in inventory-geo script to ipinfo.io
* Cache geo-location inventory data in volatile memory
* Log which scripts are run at the info level
* Filter out docker network interfaces in inventory
This adds functionality for filtering out interfaces matching
* br-.*
* veth.*
* docker.*
by default, so that docker network interfaces do not flood the inventory on
hosts running a lot of docker containers.
If re-adding this functionality is required, set the environment variable:
* INCLUDE_DOCKER_INTERFACES=true
([MEN-4487](https://northerntech.atlassian.net/browse/MEN-4487))
* single-file: Use atomic file operations.
* single-file: Use stderr for all error messages.
* Remove deprecated field HttpsClient from config file (gets
the rid of bogus SSL warnings on `mender show-artifact` and any other
cli operation).
([MEN-4398](https://northerntech.atlassian.net/browse/MEN-4398))
* Send the inventory after a successful deployment, even though the
device has not rebooted.
([MEN-4518](https://northerntech.atlassian.net/browse/MEN-4518))
* mender setup: when configuring for demo using self-signed
certificate, install the certificate in the local trust store so that
all components in the system (namely, Mender addons) can trust the
Mender server without extra configuration.
([MEN-4580](https://northerntech.atlassian.net/browse/MEN-4580))
* Warn in the log when the system certificates contain the demo cert.
* Aggregated Dependabot Changelogs:
* Bumps [github.com/stretchr/testify](https://github.com/stretchr/testify) from 1.6.1 to 1.7.0.
- [Release notes](https://github.com/stretchr/testify/releases)
- [Commits](https://github.com/stretchr/testify/compare/v1.6.1...v1.7.0)


## mender 2.5.4

_Released 02.09.2022_

### Statistics

A total of 297 lines added, 52 removed (delta 245)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 7 (53.8%) |
| Lluis Campos | 3 (23.1%) |
| Ole Petter | 2 (15.4%) |
| Jesus | 1 (7.7%) |

| Developers with the most changed lines | |
|---|---|
| Kristian Amlie | 152 (49.8%) |
| Ole Petter | 125 (41.0%) |
| Lluis Campos | 22 (7.2%) |
| Jesus | 6 (2.0%) |

| Developers with the most signoffs (total 2) | |
|---|---|
| Lluis Campos | 1 (50.0%) |
| Ole Petter | 1 (50.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 12 (92.3%) |
| wjaxxx@gmail.com | 1 (7.7%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 299 (98.0%) |
| wjaxxx@gmail.com | 6 (2.0%) |

| Employers with the most signoffs (total 2) | |
|---|---|
| Northern.tech | 2 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 3 (75.0%) |
| wjaxxx@gmail.com | 1 (25.0%) |

### Changelogs

#### mender (2.5.4)

New changes in mender since 2.5.3:

* Fix error not finding active partition for systems where /dev/root is a symlink
* Title if the update module has not already requested a reboot. This
  is done, in the case that ArtifactInstall never finished, and hence the reboot
  information from the update module is never collected.
  ([MEN-4882](https://northerntech.atlassian.net/browse/MEN-4882))
* Fix a race condition which can happen during a reboot if
  systemd kills the `reboot` command before it kills the Mender client.
  ([MEN-5340](https://northerntech.atlassian.net/browse/MEN-5340))
* Fix a (possible) file descriptor leak.
* Bump github.com/mendersoftware/mender-artifact to 3.5.x


## mender 2.5.3

_Release date 09.29.2021_

### Statistics

A total of 97 lines added, 51 removed (delta 46)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 5 (55.6%) |
| Prashanth Joseph Babu | 2 (22.2%) |
| Alf-Rune Siqveland | 1 (11.1%) |
| Lluis Campos | 1 (11.1%) |

| Developers with the most changed lines | |
|---|---|
| Prashanth Joseph Babu | 46 (47.4%) |
| Kristian Amlie | 34 (35.1%) |
| Alf-Rune Siqveland | 9 (9.3%) |
| Lluis Campos | 8 (8.2%) |

| Developers with the most signoffs (total 1) | |
|---|---|
| Kristian Amlie | 1 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 7 (77.8%) |
| prashanthjbabu@gmail.com | 2 (22.2%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 51 (52.6%) |
| prashanthjbabu@gmail.com | 46 (47.4%) |

| Employers with the most signoffs (total 1) | |
|---|---|
| Northern.tech | 1 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 3 (75.0%) |
| prashanthjbabu@gmail.com | 1 (25.0%) |

### Changelogs

#### mender (2.5.3)

New changes in mender since 2.5.2:

* Add artifact_name to device provides if not found in store
* Add missing filesystem sync which could produce an empty or
  corrupted Update Module file tree in
  `/var/lib/mender/modules/v3/payloads/0000/tree/files/` after an
  unexpected reboot.
* [FIX] Fetch geo location data once per power cycle


## mender 2.5.2

_Released 07.14.2021_

### Statistics

A total of 506 lines added, 215 removed (delta 291)

| Developers with the most changesets | |
|---|---|
| Kristian Amlie | 5 (33.3%) |
| Lluis Campos | 5 (33.3%) |
| Ole Petter Orhagen | 2 (13.3%) |
| Nils Olav Kvelvane Johansen | 2 (13.3%) |
| Prashanth Joseph Babu | 1 (6.7%) |

| Developers with the most changed lines | |
|---|---|
| Lluis Campos | 289 (49.7%) |
| Kristian Amlie | 186 (32.0%) |
| Ole Petter Orhagen | 58 (10.0%) |
| Nils Olav Kvelvane Johansen | 45 (7.7%) |
| Prashanth Joseph Babu | 3 (0.5%) |

| Developers with the most lines removed | |
|---|---|
| Kristian Amlie | 47 (21.9%) |

| Developers with the most signoffs (total 2) | |
|---|---|
| Ole Petter Orhagen | 2 (100.0%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 14 (93.3%) |
| prashanthjbabu@gmail.com | 1 (6.7%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 578 (99.5%) |
| prashanthjbabu@gmail.com | 3 (0.5%) |

| Employers with the most signoffs (total 2) | |
|---|---|
| Northern.tech | 2 (100.0%) |

| Employers with the most hackers (total 5) | |
|---|---|
| Northern.tech | 4 (80.0%) |
| prashanthjbabu@gmail.com | 1 (20.0%) |

### Changelogs

#### mender (2.5.2)

New changes in mender since 2.5.1:

* Dont Verify SSL if skip verify is set
  If skip verify is set , then we shouldnt call VerifyResult
* Update Modules Artifact generators: correct --software-version flag
* single-file-artifact-gen: Support concurrent executions
* single-file Update Module: fix rollback functionality
* The daemon will no longer crash if mender check-update or send-inventory is used before the daemon has finished its set up.
  ([MEN-4074](https://northerntech.atlassian.net/browse/MEN-4074))
* Fix D-Bus timeout on errors by finishing handling
  ([MEN-4703](https://northerntech.atlassian.net/browse/MEN-4703))
* The location of the device type file is now determined by the mender.conf file. If the device type file is not used in mender.conf, the device type file is determined by the --data flag and if the flag is not used, the device type file is set to default. In addition, the scripts and modules directories location is consistent with the --data flag now.
  ([MEN-4669](https://northerntech.atlassian.net/browse/MEN-4669))
* Fix race condition in menderAuthManagerService due to
  concurrent map access. This could manifest either as a crash, or as a
  failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix race condition in `dbus.RegisterMethodCallCallback` due
  to concurrent map access. This could manifest either as a crash, or as
  a failure to deliver the JwtToken to dependent processes, such as
  mender-connect.
* Fix occasional crash when exiting using SIGTERM.
* Fix: Correctly log the error response message from server errors
* Fix a bug which could sometimes lead the client to do a
  rollback after it had already committed. This could happen if the
  client happened to spontaneously reboot or fail during the status
  update to the server. Doing this is not correct according to the state
  flow, and can have unexpected consequences depending on the
  combination of Update Modules and State Scripts.
  ([MEN-4830](https://northerntech.atlassian.net/browse/MEN-4830))

## mender 2.5.1

_Released 16.04.2021_

### Changelogs

#### mender (2.5.1)

New changes in mender since 2.5.0:

* Change provider in inventory-geo script to ipinfo.io
* Cache geo-location inventory data in volatile memory
* Remove deprecated field HttpsClient from config file (gets
the rid of bogus SSL warnings on `mender show-artifact` and any other
cli operation).
([MEN-4398](https://northerntech.atlassian.net/browse/MEN-4398))
* single-file: Use atomic file operations.
* single-file: Use stderr for all error messages.
* Send the inventory after a successful deployment, even though the
device has not rebooted.
([MEN-4518](https://northerntech.atlassian.net/browse/MEN-4518))

## mender 2.5.0

_Released 01.20.2021_

### Changelogs

#### mender (2.5.0)

New changes in mender since 2.4.0:

* Fix rootfs-image-v2 commit in standalone mode when upgrade fails
* Add --reboot-exit-code parameter to "install" command.
* Fixed wrong error produced by rootfs-image commit
* Gracefully shutdown on SIGTERM
* implement "show-provides" command on client
([MEN-3074](https://northerntech.atlassian.net/browse/MEN-3074))
* add inventory script to list the artifact provides data
([MEN-3073](https://northerntech.atlassian.net/browse/MEN-3073))
* add support for software version flags in artifact generators
([MEN-3481](https://northerntech.atlassian.net/browse/MEN-3481))
* Support for `clears_artifact_provides` field in Artifacts.
([MEN-3075](https://northerntech.atlassian.net/browse/MEN-3075))
* switch to the new PUT endpoint to update inventory attributes
([MEN-4001](https://northerntech.atlassian.net/browse/MEN-4001))
* Add Glib's GIO dependency for D-Bus interface. It can be
opt-out using `nodbus` at compile time.
([MEN-4032](https://northerntech.atlassian.net/browse/MEN-4032))
* Add support for probing the U-Boot environment separator
([MEN-3970](https://northerntech.atlassian.net/browse/MEN-3970))
* Allow to load private key from the Security configuration section
([MEN-3924](https://northerntech.atlassian.net/browse/MEN-3924))
* artifact-gen: Improve error message when mender-artifact is not found.
([MEN-4044](https://northerntech.atlassian.net/browse/MEN-4044))
* Fix: Do not switch boot partitions on installation errors on the
active partition.
([MEN-3980](https://northerntech.atlassian.net/browse/MEN-3980))
* Correctly log the error message from the server on failed update
download attempts.
* mender-inventory-geo: Set connection timeout to 10s.
* Decrease the verbosity of 'Authorization requests failed' errors in
the log output.
* service API to register object interfaces over System DBus
([MEN-4009](https://northerntech.atlassian.net/browse/MEN-4009))
* Add DBus support to AuthManager implementing WithDBus
* implement DBus signal ValidJwtTokenAvailable
([MEN-4017](https://northerntech.atlassian.net/browse/MEN-4017))
* Add an inventory script for reporting the update-modules currently
installed on a device.
* Add busconfig file for DBus API to install steps.
([MEN-4030](https://northerntech.atlassian.net/browse/MEN-4030))
* Replace the current progressbar with a minimalistic and less verbose implementation.
* The 'inventory-geo-script' now has a separate install target:
'install-inventory-network-scripts'. Note however that it is still installed by
the default 'install-inventory-scripts' target.
* When available, enable D-Bus interface by default
* Exit with code 0 on a received SIGTERM signal.
([MEN-4170](https://northerntech.atlassian.net/browse/MEN-4170))
* Add passphrase-file global option.
* Fix error parsing response for getting tenant token on setup
([MEN-4245](https://northerntech.atlassian.net/browse/MEN-4245))
* Extend the D-Bus API to return the server URL
([MEN-4360](https://northerntech.atlassian.net/browse/MEN-4360))
* Aggregated Dependabot Changelogs:
* Bumps [github.com/mendersoftware/openssl](https://github.com/mendersoftware/openssl) from 1.0.9 to 1.0.10.
- [Release notes](https://github.com/mendersoftware/openssl/releases)
- [Commits](https://github.com/mendersoftware/openssl/compare/v1.0.9...v1.0.10)
* Bump github.com/mendersoftware/openssl from 1.0.9 to 1.0.10
* Bumps [github.com/mendersoftware/openssl](https://github.com/mendersoftware/openssl) from 1.0.10 to 1.1.0.
- [Release notes](https://github.com/mendersoftware/openssl/releases)
- [Commits](https://github.com/mendersoftware/openssl/compare/v1.0.10...v1.1.0)
* Bump github.com/mendersoftware/openssl from 1.0.10 to 1.1.0

## mender 2.4.2

_Released 01.21.2021_

### Changelogs

#### mender (2.4.2)

New changes in mender since 2.4.0:

* Add support for probing the U-Boot environment separator
([MEN-3970](https://northerntech.atlassian.net/browse/MEN-3970))
* Fix: Do not switch boot partitions on installation errors on the
active partition.
([MEN-3980](https://northerntech.atlassian.net/browse/MEN-3980))
* Allow to load private key from the Security configuration section
([MEN-3924](https://northerntech.atlassian.net/browse/MEN-3924))
* mender-inventory-geo: Set connection timeout to 10s.
* Fix error parsing response for getting tenant token on setup
([MEN-4245](https://northerntech.atlassian.net/browse/MEN-4245))

## mender 2.4.1

_Released 11.03.2020_

### Statistics

A total of 397 lines added, 161 removed (delta 236)

| Developers with the most changesets | |
|---|---|
| Ole Petter Orhagen | 4 (36.4%) |
| Peter Grzybowski | 3 (27.3%) |
| Lluis Campos | 3 (27.3%) |
| Fabio Tranchitella | 1 (9.1%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter Orhagen | 314 (77.0%) |
| Peter Grzybowski | 51 (12.5%) |
| Lluis Campos | 42 (10.3%) |
| Fabio Tranchitella | 1 (0.2%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 11 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 408 (100.0%) |

| Employers with the most hackers (total 4) | |
|---|---|
| Northern.tech | 4 (100.0%) |

### Changelogs

#### mender (2.4.1)

New changes in mender since 2.4.0:

* Add support for probing the U-Boot environment separator
([MEN-3970](https://northerntech.atlassian.net/browse/MEN-3970))
* Fix: Do not switch boot partitions on installation errors on the
active partition.
([MEN-3980](https://northerntech.atlassian.net/browse/MEN-3980))
* Allow to load private key from the Security configuration section
([MEN-3924](https://northerntech.atlassian.net/browse/MEN-3924))

## mender 2.4.0

_Released 09.11.2020_

### Changelogs

#### mender (2.4.0)

New changes in mender since 2.3.0:

* keystore: use openssl bindings
Switch the code that signs the server's authentication request
to use openssl. This allows to use ssl_engines, which permit to
use PKCS#11 or TPMs as keystore.
* vendor: switch openssl bindings to github.com/Linutronix/golang-openssl
spacemonkeygo/openssl depends on spacelog, which increases binary
size by about 2MB due to using reflect.
Switch to a fork which has the logger removed.
This patch can hopefully be reverted someday, when the logger
removal has been mainlined.
* Log state-script stderr as info, not error
([MEN-3316](https://northerntech.atlassian.net/browse/MEN-3316))
* mender-inventory-geo script to return geo localization data
* Add support for libubootenv as boot loader user space tools
provider. ([MEN-3684](https://northerntech.atlassian.net/browse/MEN-3684))
* Remove Server config warn on mender setup command
([MEN-3652](https://northerntech.atlassian.net/browse/MEN-3652))
* Fix broken logging to syslogger.
([MEN-3676](https://northerntech.atlassian.net/browse/MEN-3676))
* chmod 600 on config file
([MEN-3762](https://northerntech.atlassian.net/browse/MEN-3762))
* mender-device-identity: skip dummyX interfaces
* mender.service: update to run after network-online.target
* Switch to OpenSSL for all server communication.
([MEN-3730](https://northerntech.atlassian.net/browse/MEN-3730))
* keystore: support ed25519 keys
* Add the ability to configure the client with a client certificate and
private key in order to enable mTLS in the client communication setup.
([MEN-3115](https://northerntech.atlassian.net/browse/MEN-3115))

## mender 2.3.3

_Released 16.04.2021_

### Changelogs

#### mender (2.3.3)

New changes in mender since 2.3.2:

* single-file: Use atomic file operations.
* single-file: Use stderr for all error messages.
* Send the inventory after a successful deployment, even though the
device has not rebooted.
([MEN-4518](https://northerntech.atlassian.net/browse/MEN-4518))
* fix, support white spaces in single-file artifacts' names
([MEN-4179](https://northerntech.atlassian.net/browse/MEN-4179))

## mender 2.3.2

_Released 01.21.2021_

### Changelogs

#### mender (2.3.2)

New changes in mender since 2.3.0:

* Add support for probing the U-Boot environment separator
([MEN-3970](https://northerntech.atlassian.net/browse/MEN-3970))
* Fix: Do not switch boot partitions on installation errors on the
active partition.
([MEN-3980](https://northerntech.atlassian.net/browse/MEN-3980))
* Fix error parsing response for getting tenant token on setup
([MEN-4245](https://northerntech.atlassian.net/browse/MEN-4245))

## mender 2.3.1

_Released 11.03.2020_

### Statistics

A total of 211 lines added, 26 removed (delta 185)

| Developers with the most changesets | |
|---|---|
| Ole Petter Orhagen | 5 (55.6%) |
| Lluis Campos | 3 (33.3%) |
| Fabio Tranchitella | 1 (11.1%) |

| Developers with the most changed lines | |
|---|---|
| Ole Petter Orhagen | 179 (80.6%) |
| Lluis Campos | 42 (18.9%) |
| Fabio Tranchitella | 1 (0.5%) |

| Top changeset contributors by employer | |
|---|---|
| Northern.tech | 9 (100.0%) |

| Top lines changed by employer | |
|---|---|
| Northern.tech | 222 (100.0%) |

| Employers with the most hackers (total 3) | |
|---|---|
| Northern.tech | 3 (100.0%) |

### Changelogs

#### mender (2.3.1)

New changes in mender since 2.3.0:

* Add support for probing the U-Boot environment separator
([MEN-3970](https://northerntech.atlassian.net/browse/MEN-3970))
* Fix: Do not switch boot partitions on installation errors on the
active partition.
([MEN-3980](https://northerntech.atlassian.net/browse/MEN-3980))

## mender 2.3.0

_Released 07.15.2020_

### Changelogs

#### mender (2.3.0)

New changes in mender since 2.2.0:

* Fix "State transition loop detected" when retrying status update.
* Remove text/template dependency from the cli library reducing
mender client binary size by approximately 20%
* Renamed systemd mender.service -> mender-client.service
([MEN-2948](https://northerntech.atlassian.net/browse/MEN-2948))
* Fixes various logging nitpicks
* Deprecated the log-modules cli commandline flag
([MEN-3251](https://northerntech.atlassian.net/browse/MEN-3251))
* Make the system logger respect the global log level
([MEN-3135](https://northerntech.atlassian.net/browse/MEN-3135))
* Make the system logger write to the LOG_USER facility by default
* Fix Stat_t.Dev/Rdev type assumption
* Send Provides in the deployments API call
([MEN-2587](https://northerntech.atlassian.net/browse/MEN-2587))
* Report function caller on all logs when loglevel=Debug

## mender 2.2.1

_Released 07.15.2020_

### Changelogs

#### mender (2.2.1)

New changes in mender since 2.2.0:

* Fix check-update and send-inventory options on deb install
([MEN-3277](https://northerntech.atlassian.net/browse/MEN-3277))
* Fix Stat_t.Dev/Rdev type assumption
* Log state-script stderr as info, not error
([MEN-3316](https://northerntech.atlassian.net/browse/MEN-3316))
* Fix broken logging to syslogger.
([MEN-3676](https://northerntech.atlassian.net/browse/MEN-3676))
* Add support for libubootenv as boot loader user space tools
provider. ([MEN-3684](https://northerntech.atlassian.net/browse/MEN-3684))
* Make interactive setup device type default to configured device type
([MEN-3777](https://northerntech.atlassian.net/browse/MEN-3777))

## mender 2.2.0

_Released 03.05.2020_

### Changelogs

#### mender (2.2.0)

New changes in mender since 2.2.0b1:

* Remove text/template dependency from the cli library reducing
mender client binary size by approximately 20%
* Fix "State transition loop detected" when retrying status update.

New changes in mender since 2.1.2:

* mender setup cli command and new CLI package
([MEN-2418](https://northerntech.atlassian.net/browse/MEN-2418), [MEN-2806](https://northerntech.atlassian.net/browse/MEN-2806))
* Fix UBI device size calculation
* store: Save artifact provides for dependency verifications
* app: Verify artifact (version >= 3) dependencies with current artifact
* store/app{standalone}: Artifact dependency checking for artifact v3
* app/store{standalone}: Unit tests Artifact v3 depends and provides
* Enable the usage of the full Mender-Artifact version 3 format
([MEN-2642](https://northerntech.atlassian.net/browse/MEN-2642))
* support: modules-artifact-gen: Fix typo in default name of output file
* Rename --mender-professional flag to --hosted-mender
* Add --quiet flag and remove --run-daemon option and confirm device
* Now the client stores Artifact provides parameters across reboots in
standalone mode. Previously this data was ignored, and hence upgrading with an
Artifact with provides parameters these were lost.
([MEN-2969](https://northerntech.atlassian.net/browse/MEN-2969))
* Set default device type to hostname for interactive setup
* New command: `snapshot dump` to dump current rootfs
* Skip special device "rootfs" when determining rootfs type
* Report 'Unknown' rootfs type if we can't detect it
* Optimize rootfs-update image writes
([MEN-2939](https://northerntech.atlassian.net/browse/MEN-2939))
* Make `single-file-artifact-gen` script POSIX compliant.
([MEN-3049](https://northerntech.atlassian.net/browse/MEN-3049))
* Fix segfault when running `mender setup` on a read-only
filesystem.
* Fix crash when specified certificate can't be opened.
Both the `ServerCertificate` setting and the system certificates are
now optional, in the sense that the client will run without them.
However, the client will not be able to connect without the right
certificates, so the main usecase of this change is to have a workable
client that will roll back if connections can't be made, instead of
exiting. ([MEN-3047](https://northerntech.atlassian.net/browse/MEN-3047))
* Add warning message when server certificate can't be parsed.
* snapshot: Added watchdog timer to keep system from freezing
* snapshot: Add compression options to speed up transfer
* Improved error message when an update-module is missing
([MEN-3007](https://northerntech.atlassian.net/browse/MEN-3007))
* snapshot: New flag `--source` specifying the source
filesystem to snapshot

## mender 2.1.3

_Released 03.05.2020_

### Changelogs

#### mender (2.1.3)

New changes in mender since 2.1.2:

* Fix crash when specified certificate can't be opened.
Both the `ServerCertificate` setting and the system certificates are
now optional, in the sense that the client will run without them.
However, the client will not be able to connect without the right
certificates, so the main usecase of this change is to have a workable
client that will roll back if connections can't be made, instead of
exiting. ([MEN-3047](https://northerntech.atlassian.net/browse/MEN-3047))
* Add warning message when server certificate can't be parsed.


## mender 2.1.2

_Released 12.05.2019_

### Changelogs

#### mender (2.1.2)

New changes in mender since 2.1.1:

* Fix UBI device size calculation

## mender 2.1.1

_Released 10.23.2019_

### Changelogs

#### mender (2.1.1)

New changes in mender since 2.1.0:

* module/single-file: fix rollback state by correctly defining filename
* Check for -f option in stat command
* Set hard limit(10) for client update status report retries
This fixes an issue where the maxSendingAttemps in
updateReportRetry state could be set real high, since it is calculated
as UpdatePollIntervalSeconds / RetryPollIntervalSeconds. This adds a
hard upper limit of 10 retries for the client in any case.
([MEN-2676](https://northerntech.atlassian.net/browse/MEN-2676))

## mender 2.1.2

_Released 12.05.2019_

### Changelogs

#### mender (2.1.2)

New changes in mender since 2.1.0:

* module/single-file: fix rollback state by correctly defining filename
* Check for -f option in stat command
* Set hard limit(10) for client update status report retries
This fixes an issue where the maxSendingAttemps in
updateReportRetry state could be set real high, since it is calculated
as UpdatePollIntervalSeconds / RetryPollIntervalSeconds. This adds a
hard upper limit of 10 retries for the client in any case.
([MEN-2676](https://northerntech.atlassian.net/browse/MEN-2676))
* Fix UBI device size calculation

## mender 2.1.0

_Released 09.16.2019_

### Changelogs

#### mender (2.1.0)

New changes in mender since 2.0.1:

* rootfs-image-v2: Make sure to follow the spec regarding `stream-next`.
We should to read the final empty entry to make sure the client does
not block.
* Restore error code 2 behavior when there is nothing to commit.
* Fix read error masking in installer.chunkedCopy(...) func
* Update vendored dependencies for client.
* When set, HTTP proxy settings in http_proxy/https_proxy environment variables are respected now.
* module-artifact-gen: Fix inability to specify more than one device_type.
* Make all errors checked or explicitly ignored
All possible errors must be checked across all code base.
If an error is intentionally ignored it should be done explicitly.
* add state-scripts example scripts to wait for network connectivity
before trying to connect to the Mender server.
([MEN-2457](https://northerntech.atlassian.net/browse/MEN-2457))
* Artifact gen: Support argument passthrough to `mender-artifact`.
Use `--` to signal that remaining arguments should be passed directly
to `mender-artifact`.
* Make the device type file location configurable
* Make channel receiving user signals buffered
The commit fixes improper usage of signal.Notify(...) func from Go stdlib.
A channel must be buffered to properly receive signals:
https://golang.org/pkg/os/signal/#Notify
Also there is no need to reallocate channel and defer signal.Stop(...)
each time user signal is received. Thus less resources are used.
* standalone: Fix artifact committing not working after upgrading from 1.x.
([MEN-2465](https://northerntech.atlassian.net/browse/MEN-2465))
* Print warning on an invalid server certificate.
([MEN-2378](https://northerntech.atlassian.net/browse/MEN-2378))
* add state-script example to preserve ssh keys accross updates
([MEN-2457](https://northerntech.atlassian.net/browse/MEN-2457))
* Fix `/bin/lsb_release` not being picked up by inventory script.
* Fix misspells in comments and error messages
* Make sure ARM64 is included in bootloader integration inventory.
* Added example to retain systemd network configuration.
* single-file module: Make sure permissions are preserved.
Also make sure that backup preserves permissions.
* add state-script example to utilize dbus to broadcast
Mender states ([MEN-2457](https://northerntech.atlassian.net/browse/MEN-2457))
* Provide command line interface to force inventory update.
([MEN-2131](https://northerntech.atlassian.net/browse/MEN-2131))

## mender 2.0.1

_Released 06.24.2019_

### Changelogs

#### mender (2.0.1)

New changes in mender since 2.0.0:

* module-artifact-gen: Fix inability to specify more than one device_type.
* single-file module: Make sure permissions are preserved.
Also make sure that backup preserves permissions.
* Artifact gen: Support argument passthrough to `mender-artifact`.
Use `--` to signal that remaining arguments should be passed directly
to `mender-artifact`.
* Restore error code 2 behavior when there is nothing to commit.

## mender 2.0.0

_Released 05.07.2019_

### Changelogs

#### mender (2.0.0)

New changes in mender since 2.0.0b1:

* Version files are now allowed to contain a newline character. Also
some minor changes, as readVersion now accepts an io.Reader, and files are
opened outside of the function. This means that the error message is now
consistent for all the uses of readVersion.
([MEN-2318](https://northerntech.atlassian.net/browse/MEN-2318))
* file-install modules: Don't destroy original before we know we have a backup.
* Fix File Install UM to not wipe out dest_dir on single file installs
* standalone: Fix artifact committing not working after upgrading from 1.x.
([MEN-2465](https://northerntech.atlassian.net/browse/MEN-2465))
* Deprecate old file-install Update Module and create instead
two new ones: single-file-install and file-tree-install. These have a
simpler logic and clearer scope. See for details.
([MEN-2442](https://northerntech.atlassian.net/browse/MEN-2442))
* Don't push network interfaces without a mac address to inventory
* Disallow installing file trees on root destination dir for
File Install Update Module
* Make sure ARM64 is included in bootloader integration inventory.
* Mender no longer misidentifies LVM volumes.
([MEN-2302](https://northerntech.atlassian.net/browse/MEN-2302))
* Update modules: Implement `NeedsArtifactReboot` -> `Automatic`.
([MEN-2011](https://northerntech.atlassian.net/browse/MEN-2011))

New changes in mender since 1.7.0:

* Bugfix: State-script error code in Sync-Enter causes infinite loop
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Allow rootfsPartA and rootfsPartB to be symlinks
* Rewrite AuthorizeWaitState to fix an infinite loop bug
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Modify design for exec.Cmd stdout/stderr logging
* Place UM generator scripts in a dedicated folder
([MEN-2371](https://northerntech.atlassian.net/browse/MEN-2371))
* Write Update Module to do file(s) install
([MEN-2371](https://northerntech.atlassian.net/browse/MEN-2371))
* Set StateScriptTimeout default to 1h
([MEN-2409](https://northerntech.atlassian.net/browse/MEN-2409))
* Add source-installation instructions to README.md.
* Add `rootfs-image-v2` as a demonstration of how to
reimplement Mender's `rootfs-image` update type as an update module.
It's also useful as inspiration if users want to make their own
slightly tweaked rootfs-image type.
([MEN-2392](https://northerntech.atlassian.net/browse/MEN-2392))
* Swapped definition of StateScriptRetryTimeout and
StateScriptRetryInterval for the names to represent what they are
actually doing. This change breaks compatibility with current usage of
these configurable parameters. See documentation for correct usage.
([MEN-2409](https://northerntech.atlassian.net/browse/MEN-2409))
* Updated the copyright year to 2019 in LICENSE.
* Write update module for doing container setup
([MEN-2232](https://northerntech.atlassian.net/browse/MEN-2232))
* Add example update modules for shell commands and pkg installs.
* Remove misleading warning message when ServerCert is missing.
* Remove jq dependency for file-install Update Module
* Implement initial version of update modules.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* Add support for Mender Artifact format version 3.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* Artifact name is now stored in the local database, and
`/etc/mender/artifact_info` acts only as a fallback if no name has
been stored yet. This is typically the case for devices provisioned
directly from a disk image. Scripts should use the client
`-show-artifact` argument instead of parsing the file.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* `-rootfs` argument has been removed and replaced with the
`-install` argument, which works the same way.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* Mender now runs a stripped down set of state scripts when
installing artifacts in standalone mode, and the `-f` flag is no
longer required to install such artifacts, nor is it valid. The
scripts that run are:
* `Download` scripts
* `ArtifactInstall` scripts
* `ArtifactCommit` scripts
* `ArtifactRollback` scripts
* `ArtifactFailure` scripts
Reboot scripts do not run, so these must be handled manually in
standalone mode.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* Behavior change: `ArtifactCommit_Error` scripts now run
after an `ArtifactCommit_Leave` script has returned an error.
([MEN-2000](https://northerntech.atlassian.net/browse/MEN-2000))
* Bugfix in killing mechanism for State Scripts
timing out ([MEN-2409](https://northerntech.atlassian.net/browse/MEN-2409))
* Update vendored dependency net/http2 to latest version
* Support installing most files using Makefile `install` target.
The device_type file is not supported, since it is highly hardware
specific. Also the configuration will be very bare bones, and will
require changes unless Hosted Mender is being used.
([MEN-2383](https://northerntech.atlassian.net/browse/MEN-2383))
* Make output from `-show-artifact` easier to consume by limiting logging.
* Fix state logic for the case of actual wait
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Properly fail the update when writes to the underlying storage fail.
([MEN-2285](https://northerntech.atlassian.net/browse/MEN-2285))
* Work around occasional OOM bug in mmc driver.
([MEN-2285](https://northerntech.atlassian.net/browse/MEN-2285))
* Make sure state directory is created if it doesn't exist.

## mender 1.7.1

_Released 05.07.2019_

### Changelogs

#### mender (1.7.1)

New changes in mender since 1.7.0:

* Remove misleading warning message when ServerCert is missing.
* Bugfix: State-script error code in Sync-Enter causes infinite loop
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Update vendored dependency net/http2 to latest version
* Rewrite AuthorizeWaitState to fix an infinite loop bug
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Fix state logic for the case of actual wait
([MEN-2195](https://northerntech.atlassian.net/browse/MEN-2195))
* Make sure ARM64 is included in bootloader integration inventory.
* Mender no longer misidentifies LVM volumes.
([MEN-2302](https://northerntech.atlassian.net/browse/MEN-2302))
* Updated the copyright year to 2019 in LICENSE.

## mender 1.7.0

_Released 12.13.2018_

### Changelogs

#### mender (1.7.0)

New changes in mender since 1.7.0b1:

* Allow rootfsPartA and rootfsPartB to be symlinks

New changes in mender since 1.6.0:

* FIX: Enabling compiling ppc64le
* Fix active partition detection when using non-native
filesystems.
* Add inventory scripts for rootfs type and bootloader integration.
([MEN-2059](https://northerntech.atlassian.net/browse/MEN-2059))
* New feature: Fail-over Mender server(s)
([MEN-1972](https://northerntech.atlassian.net/browse/MEN-1972))
* New inventory script for "os" attribute, installed by default.
([MEN-2060](https://northerntech.atlassian.net/browse/MEN-2060))
* Mender client now loads configuration settings from
both /etc/mender/mender.conf and (if it exists)
/var/lib/mender/mender.conf. The second file is located
on the data partition, so it allows any subset of configuration
changes to survive upgrades.
([MEN-2073](https://northerntech.atlassian.net/browse/MEN-2073))
* Print a message to the mender log when the
mender client has confirmed the authenticity of an
artifact's digital signature.
([MEN-2152](https://northerntech.atlassian.net/browse/MEN-2152))
* Fix update check not working under BusyBox.
([MEN-2159](https://northerntech.atlassian.net/browse/MEN-2159))
* Add Community Code of Conduct
* Detect if inactive part is mounted and unmount
([MEN-2084](https://northerntech.atlassian.net/browse/MEN-2084))
* Improve error message when running mender as non-root user
([MEN-2083](https://northerntech.atlassian.net/browse/MEN-2083))

## mender 1.6.1

_Released 12.13.2018_

### Changelogs

#### mender (1.6.1)

New changes in mender since 1.6.0:

* Fix update check not working under BusyBox.
([MEN-2159](https://northerntech.atlassian.net/browse/MEN-2159))
* Print a message to the mender log when the
mender client has confirmed the authenticity of an
artifact's digital signature.
([MEN-2152](https://northerntech.atlassian.net/browse/MEN-2152))

## mender 1.6.0

_Released 09.18.2018_

### Changelogs

#### mender (1.6.0)

New changes in mender since 1.6.0b1:

* Fix active partition detection when using non-native
filesystems.
* New inventory script for "os" attribute, installed by default.
([MEN-2060](https://northerntech.atlassian.net/browse/MEN-2060))
* FIX: Enabling compiling ppc64le
* Add inventory scripts for rootfs type and bootloader integration.
([MEN-2059](https://northerntech.atlassian.net/browse/MEN-2059))

New changes in mender since 1.5.0:

* FIXED: HTTP error 401 is not handled by all states
([MEN-1854](https://northerntech.atlassian.net/browse/MEN-1854))
* ArtifactReboot_Enter scripts are no longer rerun
if interrupted by an unexpected reboot. It will be treated
as if Mender itself rebooted.
* Enable user to force an update-check locally
The user can now force an update check by either running mender with the
-check-update option, or send a signal [SIGUSR1] to the running mender process.
([MEN-1905](https://northerntech.atlassian.net/browse/MEN-1905))
* Add automatic check for canary value in U-Boot environment
to try to detect if there is a problem in the environment setup of
U-Boot and/or the u-boot-fw-utils tools.
* Mender client key generator script
* log active partition before and after reboot.
([MEN-1880](https://northerntech.atlassian.net/browse/MEN-1880))

## mender 1.5.1

_Released 09.18.2018_

### Changelogs

#### mender (1.5.1)

New changes in mender since 1.5.0:

* FIX: Enabling compiling ppc64le
* Fix active partition detection when using non-native
filesystems.


## mender 1.5.0b1

_Released 05.15.2018_

### Changelogs

#### mender (1.5.0b1)
* Regenerate keys on all key errors, not just when keys are missing.
([MEN-1823](https://northerntech.atlassian.net/browse/MEN-1823))
* cli: New client option to show installed artifact name
([MEN-1806](https://northerntech.atlassian.net/browse/MEN-1806))
* Spontaneous-reboot hardening of the client
([MEN-1187](https://northerntech.atlassian.net/browse/MEN-1187))
* FIXED: Log writes not flushed from memory
([MEN-1726](https://northerntech.atlassian.net/browse/MEN-1726))
* Allow multiple digit partition numbers.
* log request-id in case of bad API requests
([MEN-1738](https://northerntech.atlassian.net/browse/MEN-1738))
* Abort upgrade if artifact name is not retrievable from artifact_info
([MEN-1824](https://northerntech.atlassian.net/browse/MEN-1824))

## mender 1.5.0

_Released 06.07.2018_

### Changelogs

#### mender (1.5.0)
* FIXED: HTTP error 401 is not handled by all states
([MEN-1854](https://northerntech.atlassian.net/browse/MEN-1854))
* Mender client key generator script


## mender 1.4.1

_Released 06.04.2018_

### Changelogs

#### mender (1.4.1)
* FIXED: Log writes not flushed from memory
([MEN-1726](https://northerntech.atlassian.net/browse/MEN-1726))
* Regenerate keys on all key errors, not just when keys are missing.
([MEN-1823](https://northerntech.atlassian.net/browse/MEN-1823))
* Mender client key generator script


## mender 1.4.0b1

_Released 02.09.2018_

### Changelogs

#### mender (1.4.0b1)
* Report update status for scripts and states
([MEN-1015](https://northerntech.atlassian.net/browse/MEN-1015))
* Print detailed logs about authorization errors.
([MEN-1660](https://northerntech.atlassian.net/browse/MEN-1660), [MEN-1661](https://northerntech.atlassian.net/browse/MEN-1661))
* mender-device-identity: Check if file exists before reading
Mender on orangepi fails to run because identity script exit with error like:
/usr/share/mender/identity/mender-device-identity
cat: can't open '/sys/class/net/bonding_masters/type': Not a directory
Add check before reading type to avoid problems.
* Remove trailing slash from server URL configuration.
([MEN-1620](https://northerntech.atlassian.net/browse/MEN-1620))

## mender 1.4.0

_Released 03.20.2018_

### Changelogs

#### mender (1.4.0)
* Allow multiple digit partition numbers.


## mender 1.3.1

_Released 02.09.2018_

### Changelogs

#### mender (1.3.1)
* Print detailed logs about authorization errors.
([MEN-1660](https://northerntech.atlassian.net/browse/MEN-1660), [MEN-1661](https://northerntech.atlassian.net/browse/MEN-1661))

## mender 1.3.0b1

_Released 11.14.2017_

### Changelogs

#### mender (1.3.0b1)
* Mender now logs whatever a state-script outputs to stderr
([MEN-1349](https://northerntech.atlassian.net/browse/MEN-1349))
* mender-device-identity: only collect MAC from ARPHRD_ETHER types
* Fix 'unexpected EOF' error when downloading large updates.
([MEN-1511](https://northerntech.atlassian.net/browse/MEN-1511))
* Implement ability for client to resume a download from
where it left off if the connection is broken.
([MEN-1511](https://northerntech.atlassian.net/browse/MEN-1511))
* Improve error messages for state scripts errors.
Rely on the full error description instead of just the error code.
* Fix compile for ARM64.
* set return code = 2, when there is nothing to commit
* Added retry-later functionality on top of the state-script functionality
* Correctly fail state script execution if stderr can not be opened.
It would not be impossible to continue execution in this case, but it
is bad to lose log output, and not being able to open stderr is a
pretty uncommon case that might indicate a more serious issue like
resource starvation.

## mender 1.3.0

_Released 12.21.2017_

### Changelogs

#### mender (1.3.0)
* Remove trailing slash from server URL configuration.
([MEN-1620](https://northerntech.atlassian.net/browse/MEN-1620))


## mender 1.2.1

_Released 10.02.2017_

### Changelogs

#### mender (1.2.1)
* Improve error messages for state scripts errors.
Rely on the full error description instead of just the error code.
* Fix checksum not being verified for headers, only
payload. ([MEN-1412](https://northerntech.atlassian.net/browse/MEN-1412))

## mender 1.2.0

_Released 09.05.2017_

### Changelogs

#### mender (1.2.0)
* Refactored all store implementations into /store
* Improve error message when manifest field/file cannot be read.
* Fixed format check to conform to the expected artifact-file-format
([MEN-1289](https://northerntech.atlassian.net/browse/MEN-1289))
* installer: improve incompatible image error message
* Client will not run state scripts from cmd-line except when forced.
([MEN-1235](https://northerntech.atlassian.net/browse/MEN-1235))
* Fixed behaviour when no sys-cert is available on the system.
([MEN-1151](https://northerntech.atlassian.net/browse/MEN-1151))
* Mender now logs whatever a state-script outputs to stderr
([MEN-1349](https://northerntech.atlassian.net/browse/MEN-1349))
* Fix misleading version being displayed for non-tagged builds.
([MEN-1178](https://northerntech.atlassian.net/browse/MEN-1178))
* Changed the errormessage to more closely reflect the issue.
([MEN-1215](https://northerntech.atlassian.net/browse/MEN-1215))
* Removed the DeviceKey option in menderConfig.
* Fix - Now throws an error when committing nothing.
([MEN-505](https://northerntech.atlassian.net/browse/MEN-505))
* Introduction of state script feature. State scripts can be
used to execute scripts at various stages of Mender's execution. See
documentation for more information.
* Introduce experimental support for writing to UBI volumes
* Logs an error when device_type file not found.
([MEN-505](https://northerntech.atlassian.net/browse/MEN-505))
* remove no longer referenced client certificate code

## mender 1.1.2

_(Never released publicly)_

### Changelogs

#### mender (1.1.2)
* Fix checksum not being verified for headers, only
payload. ([MEN-1412](https://northerntech.atlassian.net/browse/MEN-1412))

