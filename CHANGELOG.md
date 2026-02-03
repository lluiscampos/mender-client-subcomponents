# Mender Client 6.0.0

| Repository | Version |
| --- | --- |
| [mender](https://github.com/mendersoftware/mender) | master |
| [mender-configure-module](https://github.com/mendersoftware/mender-configure-module) | master |
| [mender-connect](https://github.com/mendersoftware/mender-connect) | master |
| [mender-flash](https://github.com/mendersoftware/mender-flash) | master |
| [mender-container-modules](https://github.com/mendersoftware/mender-container-modules) | main |

## mender master (2026-02-02)

### master - 2026-02-02


#### Bug fixes


- Clear the inventory data hash on re-authentication
([MEN-7873](https://northerntech.atlassian.net/browse/MEN-7873)) ([9d1d579](https://github.com/mendersoftware/mender/commit/9d1d579c41137de0328f3a7b2b5de1f406643c1d))  by @jo-lund





- Retry polling on all errors
([MEN-7938](https://northerntech.atlassian.net/browse/MEN-7938)) ([45f88a1](https://github.com/mendersoftware/mender/commit/45f88a13e6eb1b7e8f4b8c65eba6cccb6030f2b7))  by @danielskinstad






  When implementing the backoff for errors when polling for deployment or
  submitting inventory, we added an exception for unauthorized errors.
  After looking at how it was done in Mender Client 3, we discovered
  that such an exception was not present there, and that the backoff
  should be triggered for all types of errors.
- Fix Mender client getting stuck after failure in sync state
([MEN-7900](https://northerntech.atlassian.net/browse/MEN-7900)) ([a97eb04](https://github.com/mendersoftware/mender/commit/a97eb04c87e5baab49bbece6f7646505edbceb23))  by @lluiscampos






  From the code point, the issue was that the re-scheduling of new polls
  for updates or inventory were done from the states _after_ the sync
  state, so unless the state machine reached that point the new polls
  would not be scheduled.
  
  Fix by creating two new states, that just do the re-scheduling, between
  idle and sync. Note that the timer(s) have now been moved to the context
  object so that it can be accessed from multiple states (namely, update
  polling and submit inventory states which would need to manipulate the
  timer for exponential back-off retries.
- Compile with Boost 1.87
([MEN-8051](https://northerntech.atlassian.net/browse/MEN-8051)) ([03f52ba](https://github.com/mendersoftware/mender/commit/03f52ba5f75f6163d56a96ff90a0a48c21667413))  by @jo-lund





- Fix deployment on 32 bit systems when rootfs is larger than 4Gb
([MEN-8062](https://northerntech.atlassian.net/browse/MEN-8062)) ([8ba599b](https://github.com/mendersoftware/mender/commit/8ba599b6ec48b7be9f4e5181593ec8c34d78b271))  by @jo-lund





- Use EscapeString when generating JSON for supplied artifact data
([MEN-7974](https://northerntech.atlassian.net/browse/MEN-7974)) ([d74fba3](https://github.com/mendersoftware/mender/commit/d74fba313f3131121c9cc1a8a8e6462691658b3b))  by @jo-lund





- Inventory-geo appears to hang while wget retries many times
 ([dd881e8](https://github.com/mendersoftware/mender/commit/dd881e8789c1499c76bf6254d9e6488f9e7ff104))  by @deligatedgeek




- Clear response buffer before every HTTP request
([MEN-8554](https://northerntech.atlassian.net/browse/MEN-8554)) ([fc38f8c](https://github.com/mendersoftware/mender/commit/fc38f8ca34f185e89d56f3a15e78d8d32d877635))  by @vpodzime






  Otherwise leftover trailing bytes from a previous response may be
  parsed as a beginning of the new response resulting in HTTP
  parsing errors.
- Make mender-inventory-geo work with busybox.wget
([MEN-8548](https://northerntech.atlassian.net/browse/MEN-8548)) ([033635a](https://github.com/mendersoftware/mender/commit/033635a3eccdd4123dc86b82324ced32bd5f6dd6))  by @michalkopczan




- Use /proc/cmdline for root device detection instead of stat in rootfs update module
 ([f822970](https://github.com/mendersoftware/mender/commit/f82297049b44fc40690f05920c9881aea3625417))  by @adbjo





- Add explicit check and handling for aborted deployments
([ME-527](https://northerntech.atlassian.net/browse/ME-527)) ([2f53d85](https://github.com/mendersoftware/mender/commit/2f53d853692da5e28ce6bde123a89cd9501e075c))  by @danielskinstad




- Add timeout to prevent hanging downloads on connection loss
([MEN-8717](https://northerntech.atlassian.net/browse/MEN-8717)) ([1b51930](https://github.com/mendersoftware/mender/commit/1b519306b97cdb5e0a8228f75f8f16c0164ed280))  by @danielskinstad






  If network connection is lost while downloading an artifact, the client
  can hang when calling `beast::http::async_read_some` in `AsyncReadNextBodyPart`.
  Implement an AsyncWait timer that triggers an error handler after 5 minutes.
- Make Update modules generators POSIX compatible
([MEN-8818](https://northerntech.atlassian.net/browse/MEN-8818)) ([1202183](https://github.com/mendersoftware/mender/commit/1202183572d34b72238f9a0cc5b84f47413e22b0))  by @lluiscampos






- Added warning for invalid NO_PROXY setting containing comma
([ME-586](https://northerntech.atlassian.net/browse/ME-586)) ([9286807](https://github.com/mendersoftware/mender/commit/92868077d1c2437c8203de32158d94f3ece422b2))  by @nickanderson






  While proxy variables are not perfectly standardized, if comma isn't
  correct, it's at least a common option, so a good warning will be helpful to users.
- Use correct variable for error message
 ([0a5acd1](https://github.com/mendersoftware/mender/commit/0a5acd153b9d18958ea33577fc9b1da9e95a2e0c))  by @thall






  Before wrong variable were used when constructing the error message.
- Sanitize Update Module paths - payload_type must not point outside of Update Modules' directory
([MEN-9027](https://northerntech.atlassian.net/browse/MEN-9027)) ([c76f042](https://github.com/mendersoftware/mender/commit/c76f042b381e640b7a8903da459bce9e8d8b8028))  by @michalkopczan




- Fix signature size checking
([MEN-9055](https://northerntech.atlassian.net/browse/MEN-9055)) ([f7a5968](https://github.com/mendersoftware/mender/commit/f7a59687c98e951f632d8744e56c31a62541880a))  by @elkoniu in #1853






  Follwoing the bug report - signature size we are processing
  shall be exact 64 bytes. Other size than that should lead
  to an error.
- Sanitize State Script filenames - paths based on them must not point outside of State Script directory
([MEN-9057](https://northerntech.atlassian.net/browse/MEN-9057)) ([5183bb5](https://github.com/mendersoftware/mender/commit/5183bb54f04df8152911a76f67389871440c9550))  by @michalkopczan




- Sanitize artifact's payload filenames - they must not point outside work directory when extracted
([MEN-9056](https://northerntech.atlassian.net/browse/MEN-9056)) ([f0f3fc8](https://github.com/mendersoftware/mender/commit/f0f3fc8d2ce51d29bb8c928b000b7d38fe3b1175))  by @michalkopczan




- Sanitize header list of payloads and corresponding type-info files
([MEN-9098](https://northerntech.atlassian.net/browse/MEN-9098)) ([8ab0762](https://github.com/mendersoftware/mender/commit/8ab076204cb5421ff09209dc3274b383c3067454))  by @michalkopczan




- Improve handling of arguments in artifact-gen scripts
([MEN-9115](https://northerntech.atlassian.net/browse/MEN-9115)) ([fa7f0af](https://github.com/mendersoftware/mender/commit/fa7f0afcf461e8934fd147713fc86353a08ff356))  by @vpodzime






  Fix how single-file-artifact-gen and directory-artifact-gen parse
  arguments and pass them to mender-artifact. They need to be more
  careful to prevent injected extra arguments going through the
  script to mender-artifact.
- Strip just header compression extension instead of extensions for all files
([MEN-9146](https://northerntech.atlassian.net/browse/MEN-9146)) ([b344dc6](https://github.com/mendersoftware/mender/commit/b344dc60c75e70805dffdd0e0f18b0d598f85987))  by @michalkopczan




- Return error when artifact payload contains files not present in the manifest
([MEN-9109](https://northerntech.atlassian.net/browse/MEN-9109)) ([3367ada](https://github.com/mendersoftware/mender/commit/3367ada2399eb5e027db3191c01a1f4993268c86))  by @michalkopczan




- Use boost beast's tcp_stream object
([MEN-9104](https://northerntech.atlassian.net/browse/MEN-9104)) ([2ea7c40](https://github.com/mendersoftware/mender/commit/2ea7c40216fb42524ef980910bb15da7a2c86276))  by @danielskinstad






  Scheduled async read handlers from boost beast takes a stream
  object which we close and destroy in error handlers. The issue is that on
  cases where we call the error handler with our custom timeout, we
  destroy the stream object which some async read operations still need
  access to. By leveraging boost beast's own tcp_stream object, we can get rid
  of our custom timeout and set the timeout directly in the object which
  will allow the async error handler to do its job.
- Ensure tcp_stream object doesn't hang
 ([d8ddf6d](https://github.com/mendersoftware/mender/commit/d8ddf6da29b9c76eeb68c2711a7508bafacd1701))  by @danielskinstad




- Generate new key in mender-update if needed with embedded auth
([MEN-9132](https://northerntech.atlassian.net/browse/MEN-9132)) ([94f8dd6](https://github.com/mendersoftware/mender/commit/94f8dd6a0951563b5b8c3289aa222e083d04ebac))  by @vpodzime






  When built with `MENDER_EMBED_MENDER_AUTH`, mender-update cannot
  rely on mender-auth generating a new private key if there is no
  pre-existing one.
- Prevent segfault by correctly handling dbus restarts in mender-update and mender-auth
([MEN-9144](https://northerntech.atlassian.net/browse/MEN-9144)) ([43dd888](https://github.com/mendersoftware/mender/commit/43dd88881bb5253b0ff7f3f25ccd991b300b4675))  by @michalkopczan




- Schedule next deployment poll if current one failed early causing no handler to be called
([MEN-9144](https://northerntech.atlassian.net/browse/MEN-9144)) ([6aa4c77](https://github.com/mendersoftware/mender/commit/6aa4c776107ae5b038ced51ecdeee32a8f6b9ee5))  by @michalkopczan




- Add Host header to proxy HTTP CONNECT request
([MEN-9262](https://northerntech.atlassian.net/browse/MEN-9262)) ([23e43e7](https://github.com/mendersoftware/mender/commit/23e43e700dcc687ac354771b3ab6684e41927ac8))  by @LudvigAnderson





- Make JSONL parsing to deployment log more robust
([MEN-9128](https://northerntech.atlassian.net/browse/MEN-9128)) ([39f4a3d](https://github.com/mendersoftware/mender/commit/39f4a3d66457a71541acc75496ee602f14d1846c))  by @vpodzime










#### Features


- Add User-Agent header to HTTP requests
([MEN-1979](https://northerntech.atlassian.net/browse/MEN-1979)) ([64b0a6a](https://github.com/mendersoftware/mender/commit/64b0a6ab091daa720d074edb9b155e2e0e0cbb88))  by @jo-lund





- Add DeviceTier configuration option
([MEN-8650](https://northerntech.atlassian.net/browse/MEN-8650)) ([516541d](https://github.com/mendersoftware/mender/commit/516541d6d66dabc97a44fb7676dce8570f5cced3))  by @danielskinstad





- Enable YAML CPP by default
([MEN-8650](https://northerntech.atlassian.net/browse/MEN-8650)) ([33c2be0](https://github.com/mendersoftware/mender/commit/33c2be010379d1bff12f4c3efe36a29d21ed2768))  by @danielskinstad






  Change MENDER_USE_YAML_CPP default from OFF to ON to enable YAML
  support by default in the build. Also remove the separate build
  requirement for YAML tests since YAML CPP is now enabled by default.
- Implement system_type support for System devices
([MEN-8650](https://northerntech.atlassian.net/browse/MEN-8650)) ([8b4346b](https://github.com/mendersoftware/mender/commit/8b4346bfb9e2eb757d9f37b157c45a61a9c01305))  by @danielskinstad






  System_type is used in two specific cases:
  1) when polling for deployments
  2) when installing manifest artifacts (payload type "mender-orchestrator-manifest")
  
  Regular artifacts (e.g. rootfs updates) continue using device_type even on
  System devices, but note that these are installed through mender-orchestrator
  (through mender standalone mode) since deployment polling uses system_type.
- Send tier in authentication request
([MEN-8636](https://northerntech.atlassian.net/browse/MEN-8636)) ([e41dc3e](https://github.com/mendersoftware/mender/commit/e41dc3e405f324c0938430178db6f27e54dbbe63))  by @danielskinstad




- Error out on comma in NO_PROXY
([ME-586](https://northerntech.atlassian.net/browse/ME-586)) ([c825b8f](https://github.com/mendersoftware/mender/commit/c825b8f433cefd28de3665a48501a80592ae770d))  by @nickanderson






  Instead of warning when the NO_PROXY environment variable contains a
  comma, error out. The warning was easy to miss, and this is an invalid
  configuration that should be reported as an error.
  
  The error message is kept generic to apply to all mender clients that
  use this shared code.
- Delegate `mender_client_version` inventory key to external script
([MEN-9016](https://northerntech.atlassian.net/browse/MEN-9016)) ([9bff508](https://github.com/mendersoftware/mender/commit/9bff508f7a55040f064bda7b64213544f7438be4))  by @lluiscampos







  Mender Client is introducing a new package/recipe
  `mender-client-version-inventory-script` which will provide the Mender
  Client version not only based on `mender-update` version, but in the
  Mender Client as a whole, as documented in our official docs.
  
  Hence `mender-update` now expects the key to exist, and it will fallback
  to the old behaviour if not present.
  
  A new inventory attribute `mender_client_version_provider` is added to
  distinguish the two cases.
- Add configuration option RetryDownloadCount
([ME-589](https://northerntech.atlassian.net/browse/ME-589)) ([b0b4977](https://github.com/mendersoftware/mender/commit/b0b497776f3796e1e9b702e00d104b3be29a3763))  by @michalkopczan




- Handle HTTP 429 Too Many Requests in deployment polling
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([dc34852](https://github.com/mendersoftware/mender/commit/dc348528daf142ba925c8258c3eb3533de4c7e6d))  by @michalkopczan





- Handle HTTP 429 Too Many Requests in inventory polling
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([eaeb970](https://github.com/mendersoftware/mender/commit/eaeb9702e405d0bbcef2f3b4a84c94d5cdaa0e86))  by @michalkopczan





- Handle HTTP 429 Too Many Requests in deployment status and logs pushing
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([bc70b58](https://github.com/mendersoftware/mender/commit/bc70b58d0a3be87316730eb91b5701e6ed72411e))  by @michalkopczan









#### Security


- Bump pytest in /support/modules-artifact-gen/tests
 ([e5c17ff](https://github.com/mendersoftware/mender/commit/e5c17ffa89e1d064e6bac62c40dff8311a40bb40))  by @dependabot[bot]




  Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.3 to 8.3.4.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/8.3.3...8.3.4)
  
  updated-dependencies:
  - dependency-name: pytest
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Bump src/common/vendor/yaml-cpp from `9ce5a25` to `73ef006`
 ([1723ceb](https://github.com/mendersoftware/mender/commit/1723ceb5a095973b361f861cd3aa7a79b1cd6914))  by @dependabot[bot]




  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `9ce5a25` to `73ef006`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/9ce5a25188d83b43dd5cd633f2975be10f5d6608...73ef0060aaa1a9dc742c1d8a36fa336b35e94035)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `1b9a9d1` to `a6255cc`
 ([03fb3b4](https://github.com/mendersoftware/mender/commit/03fb3b41db5f7c14a7ec6fd59414a69f991378c4))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `1b9a9d1` to `a6255cc`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/1b9a9d1f2122e73b69f5d62d0ce3ebda8cd41ff0...a6255cc418c7eb156d71c59cd4d0dc081357f907)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-type: direct:production
  ...
- Remove AreFilesIdentical function
([MEN-7968](https://northerntech.atlassian.net/browse/MEN-7968)) ([db9b255](https://github.com/mendersoftware/mender/commit/db9b2558b3af15e8b130ee0b24cb62a1af199107))  by @victormlg





  AreFilesIdentical is removed because it is not used and contains a security vulnerability.
- Bump src/common/vendor/yaml-cpp from `73ef006` to `39f7374`
 ([fd4f249](https://github.com/mendersoftware/mender/commit/fd4f249f196d72c7cd809083a8012012af5d0cb3))  by @dependabot[bot]




  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `73ef006` to `39f7374`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/73ef0060aaa1a9dc742c1d8a36fa336b35e94035...39f737443b05e4135e697cb91c2b7b18095acd53)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-type: direct:production
  ...
- Bump src/common/vendor/tiny-process-library
 ([1e61696](https://github.com/mendersoftware/mender/commit/1e616961c0a3b225c607c4166bb913ceb085bf50))  by @dependabot[bot]




  Bumps [src/common/vendor/tiny-process-library](https://gitlab.com/eidheim/tiny-process-library) from `6166ba5` to `8bbb5a2`.
  - [Release notes](https://gitlab.com/eidheim/tiny-process-library/tags)
  - [Commits](https://gitlab.com/eidheim/tiny-process-library/compare/6166ba5dce461438cefb57e847832aca25d510d7...8bbb5a211c5c9df8ee69301da9d22fb977b27dc1)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/tiny-process-library
    dependency-type: direct:production
  ...
- Bump src/common/vendor/expected from `3f0ca7b` to `41d3e1f`
 ([15055eb](https://github.com/mendersoftware/mender/commit/15055eb29344e83dc5b20b76e0c25a524ecaef6d))  by @dependabot[bot]




  Bumps [src/common/vendor/expected](https://github.com/TartanLlama/expected) from `3f0ca7b` to `41d3e1f`.
  - [Release notes](https://github.com/TartanLlama/expected/releases)
  - [Commits](https://github.com/TartanLlama/expected/compare/3f0ca7b19253129700a073abfa6d8638d9f7c80c...41d3e1f48d682992a2230b2a715bca38b848b269)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/expected
    dependency-type: direct:production
  ...
- Bump src/common/vendor/optional-lite from `927b5f7` to `67b8c3f`
 ([e7563ff](https://github.com/mendersoftware/mender/commit/e7563ff35fb1e7251e5f80e626dff73a9589a2cb))  by @dependabot[bot]




  Bumps [src/common/vendor/optional-lite](https://github.com/martinmoene/optional-lite) from `927b5f7` to `67b8c3f`.
  - [Release notes](https://github.com/martinmoene/optional-lite/releases)
  - [Commits](https://github.com/martinmoene/optional-lite/compare/927b5f76f6f524552d51a1af185b70e30be5d1fa...67b8c3fe851dbaa3430b540815fa73ee4fa7c5ad)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/optional-lite
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `a6255cc` to `606b634`
 ([b301f01](https://github.com/mendersoftware/mender/commit/b301f01111b5c2d936d46c133cb2722951d633a1))  by @dependabot[bot]






  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `a6255cc` to `606b634`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/a6255cc418c7eb156d71c59cd4d0dc081357f907...606b6347edf0758c531abb6c36743e09a4c48a84)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-type: direct:production
  ...
- Bump ubuntu from 22.04 to 24.04 in /tests
 ([a73e57a](https://github.com/mendersoftware/mender/commit/a73e57a140ab8beab3035864ff00ebf2833c1525))  by @dependabot[bot]





  Bumps ubuntu from 22.04 to 24.04.
  
  updated-dependencies:
  - dependency-name: ubuntu
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `606b634` to `8215dba`
 ([c2f3f01](https://github.com/mendersoftware/mender/commit/c2f3f01ef6e343f50f6394fdd5b67edfc7ec4a18))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `606b634` to `8215dba`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/606b6347edf0758c531abb6c36743e09a4c48a84...8215dbafbdab7c166fad02db86d4ea2a82f851c7)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `8215dba` to `f3dc468`
 ([afe32ad](https://github.com/mendersoftware/mender/commit/afe32adb53f4b22cd74be99fd6e70fceb05ea3f6))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `8215dba` to `f3dc468`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/8215dbafbdab7c166fad02db86d4ea2a82f851c7...f3dc4684b40a124cabc8554967c2cd8db54f15dd)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `f3dc468` to `3a57039`
 ([30e19ce](https://github.com/mendersoftware/mender/commit/30e19ce5c69a5a337ec512873e0089b6b5acb6b9))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `f3dc468` to `3a57039`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/f3dc4684b40a124cabc8554967c2cd8db54f15dd...3a5703931ad70852b668a46cac34354d1b264442)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-type: direct:production
  ...
- Bump src/common/vendor/optional-lite from `67b8c3f` to `44ae889`
 ([be16284](https://github.com/mendersoftware/mender/commit/be162841964674c6ecd931af7001ce0ea73873b7))  by @dependabot[bot]




  Bumps [src/common/vendor/optional-lite](https://github.com/martinmoene/optional-lite) from `67b8c3f` to `44ae889`.
  - [Release notes](https://github.com/martinmoene/optional-lite/releases)
  - [Commits](https://github.com/martinmoene/optional-lite/compare/67b8c3fe851dbaa3430b540815fa73ee4fa7c5ad...44ae889d969117c05d84c96f34e20f9e1b5a1511)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/optional-lite
    dependency-type: direct:production
  ...
- Bump src/common/vendor/yaml-cpp from `39f7374` to `28f93bd`
 ([31b551f](https://github.com/mendersoftware/mender/commit/31b551f6fb8810e4fd20c82defa1bf81abf9ba96))  by @dependabot[bot]




  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `39f7374` to `28f93bd`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/39f737443b05e4135e697cb91c2b7b18095acd53...28f93bdec6387d42332220afa9558060c8016795)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `3a57039` to `dff2b47`
 ([c02244a](https://github.com/mendersoftware/mender/commit/c02244a0110e9745f8be2be96ba003fe5ceeca00))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `3a57039` to `dff2b47`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/3a5703931ad70852b668a46cac34354d1b264442...dff2b4756cedca462721dc9666a2fbc05d47b486)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: dff2b4756cedca462721dc9666a2fbc05d47b486
    dependency-type: direct:production
  ...
- Bump src/common/vendor/yaml-cpp from `28f93bd` to `2f86d13`
 ([855692a](https://github.com/mendersoftware/mender/commit/855692aba72a7253216d2cb0490d4499888f845d))  by @dependabot[bot]






  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `28f93bd` to `2f86d13`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/28f93bdec6387d42332220afa9558060c8016795...2f86d13775d119edbb69af52e5f566fd65c6953b)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-version: 2f86d13775d119edbb69af52e5f566fd65c6953b
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `230bfd1` to `82f4f70`
 ([65afecb](https://github.com/mendersoftware/mender/commit/65afecbdcc17a8f5afe79a71ba6f058a0caa05f6))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `230bfd1` to `82f4f70`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/230bfd15a2bb7f01ebb3fcd3cf898b697ef43c48...82f4f706693f689c6b304313f57666b92024070e)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: 82f4f706693f689c6b304313f57666b92024070e
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `568b708` to `b451735`
 ([2c99e64](https://github.com/mendersoftware/mender/commit/2c99e64d44c54ea5984e2545c1a044484a921aab))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `568b708` to `b451735`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/568b708fd46deeb23a959381393a7564f1586588...b451735fe7bb3283336f934b3f6cd3f484f73649)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: b451735fe7bb3283336f934b3f6cd3f484f73649
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `b451735` to `d33ecd3`
 ([26b7e9b](https://github.com/mendersoftware/mender/commit/26b7e9b95cb0e97922cc24de3cb342a616dcb058))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `b451735` to `d33ecd3`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/b451735fe7bb3283336f934b3f6cd3f484f73649...d33ecd3f3bd11e30aa8bbabb00e0a9cd3f2456d8)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: d33ecd3f3bd11e30aa8bbabb00e0a9cd3f2456d8
    dependency-type: direct:production
  ...
- Bump libboost_log to 1.83.0
 ([ddbfda1](https://github.com/mendersoftware/mender/commit/ddbfda157471dbdeaec8af85ba43acdb79dbe173))  by @danielskinstad




  The following errors are present in mendersoftware/mender-client-docker:mender-master
  
  ```
  mender-auth: error while loading shared libraries: libboost_log.so.1.83.0: cannot open shared object file: No such file or directory
  mender-update: error while loading shared libraries: libboost_log.so.1.83.0: cannot open shared object file: No such file or directory
  ```
- Bump src/common/vendor/json from `d33ecd3` to `c637a8b`
 ([840562a](https://github.com/mendersoftware/mender/commit/840562ab2e51f7918a86f1070a29f54b2c767a72))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `d33ecd3` to `c637a8b`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/d33ecd3f3bd11e30aa8bbabb00e0a9cd3f2456d8...c637a8b453dfc772f7819eb373af1c683c522635)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: c637a8b453dfc772f7819eb373af1c683c522635
    dependency-type: direct:production
  ...
- Bump src/common/vendor/expected from `41d3e1f` to `ea916f3`
 ([30dca11](https://github.com/mendersoftware/mender/commit/30dca11042b4ba1bee92631a8ae25115de6fc24e))  by @danielskinstad





  Bumps [src/common/vendor/expected](https://github.com/TartanLlama/expected) from `41d3e1f` to `ea916f3`.
  - [Release notes](https://github.com/TartanLlama/expected/releases)
  - [Commits](https://github.com/TartanLlama/expected/compare/41d3e1f48d682992a2230b2a715bca38b848b269...ea916f39627f02f192b5ec532210ab184e266e3e)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/expected
    dependency-version: ea916f39627f02f192b5ec532210ab184e266e3e
    dependency-type: direct:production
  ...
  
  After bumping expected we started seeing failures in unit tests that we
  were ignoring returned value types of `ExpectedSize`.
  Check return value of function calls that return ExpectedSize in unit test.
- Bump src/common/vendor/json from `c637a8b` to `4bc4e37`
 ([c58764c](https://github.com/mendersoftware/mender/commit/c58764cc43e7d0d84b5334ee033140ae6ae5eb57))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `c637a8b` to `4bc4e37`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/c637a8b453dfc772f7819eb373af1c683c522635...4bc4e37f4f56f88b3a80abb7a6508b19a244e803)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: 4bc4e37f4f56f88b3a80abb7a6508b19a244e803
    dependency-type: direct:production
  ...
- Bump src/common/vendor/expected from `ea916f3` to `1770e35`
 ([34e3d61](https://github.com/mendersoftware/mender/commit/34e3d61c78b54605c39f93ea6182aecbacb2d885))  by @dependabot[bot]




  Bumps [src/common/vendor/expected](https://github.com/TartanLlama/expected) from `ea916f3` to `1770e35`.
  - [Release notes](https://github.com/TartanLlama/expected/releases)
  - [Commits](https://github.com/TartanLlama/expected/compare/ea916f39627f02f192b5ec532210ab184e266e3e...1770e3559f2f6ea4a5fb4f577ad22aeb30fbd8e4)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/expected
    dependency-version: 1770e3559f2f6ea4a5fb4f577ad22aeb30fbd8e4
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `87a3e4d` to `3ed64e5`
 ([b2169d4](https://github.com/mendersoftware/mender/commit/b2169d407b1e54bef70087bce2c8c0a0cbce6490))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `87a3e4d` to `3ed64e5`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/87a3e4de9903be9acdc66418c29182c6f979d707...3ed64e502a6371311af3c2f309e6525b2f5f6f18)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: 3ed64e502a6371311af3c2f309e6525b2f5f6f18
    dependency-type: direct:production
  ...
- Bump src/common/vendor/optional-lite from `44ae889` to `5411501`
 ([283dc84](https://github.com/mendersoftware/mender/commit/283dc84008ba874f661cf6620c917658b1bee223))  by @dependabot[bot]




  Bumps [src/common/vendor/optional-lite](https://github.com/martinmoene/optional-lite) from `44ae889` to `5411501`.
  - [Release notes](https://github.com/martinmoene/optional-lite/releases)
  - [Commits](https://github.com/martinmoene/optional-lite/compare/44ae889d969117c05d84c96f34e20f9e1b5a1511...54115013989efd1bb5f4a5668af021a1791b5e1f)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/optional-lite
    dependency-version: 54115013989efd1bb5f4a5668af021a1791b5e1f
    dependency-type: direct:production
  ...
- Bump src/common/vendor/yaml-cpp from `2f86d13` to `65c1c27`
 ([6b74266](https://github.com/mendersoftware/mender/commit/6b74266c363ede2a6b303cc42ca87e4062e0a46e))  by @dependabot[bot]




  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `2f86d13` to `65c1c27`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/2f86d13775d119edbb69af52e5f566fd65c6953b...65c1c270dbe7eec37b2df2531d7497c4eea79aee)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-version: 65c1c270dbe7eec37b2df2531d7497c4eea79aee
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `3ed64e5` to `8deac49`
 ([2c1bf75](https://github.com/mendersoftware/mender/commit/2c1bf7567730dd0f06ee4d1a79550b57b6cfe5a8))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `3ed64e5` to `8deac49`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/3ed64e502a6371311af3c2f309e6525b2f5f6f18...8deac49f5039391749606259045acda205fe39ef)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: 8deac49f5039391749606259045acda205fe39ef
    dependency-type: direct:production
  ...
- Bump src/common/vendor/optional-lite from `5411501` to `5f924cb`
 ([97cd21f](https://github.com/mendersoftware/mender/commit/97cd21f4a62b1cb3c5f70ada0e783de6119d556f))  by @dependabot[bot]




  Bumps [src/common/vendor/optional-lite](https://github.com/martinmoene/optional-lite) from `5411501` to `5f924cb`.
  - [Release notes](https://github.com/martinmoene/optional-lite/releases)
  - [Commits](https://github.com/martinmoene/optional-lite/compare/54115013989efd1bb5f4a5668af021a1791b5e1f...5f924cbfc130484d4820bb105d6ad1a42df930e0)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/optional-lite
    dependency-version: 5f924cbfc130484d4820bb105d6ad1a42df930e0
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `8deac49` to `a0e9fb1`
 ([e2e47a2](https://github.com/mendersoftware/mender/commit/e2e47a21b53276136a0854324c62ea0506337851))  by @dependabot[bot]




  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `8deac49` to `a0e9fb1`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/8deac49f5039391749606259045acda205fe39ef...a0e9fb1e638cfbb5b8b556b7c51eaa81977bad48)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: a0e9fb1e638cfbb5b8b556b7c51eaa81977bad48
    dependency-type: direct:production
  ...
- Bump src/common/vendor/json from `02ac0d6` to `14374af`
 ([f7f7a6f](https://github.com/mendersoftware/mender/commit/f7f7a6f6f6739222c99350eafa9ef3c31051a9a2))  by @danielskinstad





  Bumps [src/common/vendor/json](https://github.com/nlohmann/json) from `02ac0d6` to `14374af`.
  - [Release notes](https://github.com/nlohmann/json/releases)
  - [Commits](https://github.com/nlohmann/json/compare/02ac0d6525f2e046f136ca69b5105b4e4f315b2f...14374af9e5727aa824676f2a2f731fdf054c4c97)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/json
    dependency-version: 14374af9e5727aa824676f2a2f731fdf054c4c97
    dependency-type: direct:production
  ...
  
  Modified license checksums
- Bump src/common/vendor/yaml-cpp from `a83cd31` to `c7aa78d`
 ([55f0e30](https://github.com/mendersoftware/mender/commit/55f0e30aacf3aa998af837e6bba2513ac631a52b))  by @dependabot[bot]




  Bumps [src/common/vendor/yaml-cpp](https://github.com/jbeder/yaml-cpp) from `a83cd31` to `c7aa78d`.
  - [Release notes](https://github.com/jbeder/yaml-cpp/releases)
  - [Commits](https://github.com/jbeder/yaml-cpp/compare/a83cd31548b19d50f3f983b069dceb4f4d50756d...c7aa78d294bbe499c1ebc0abfa1e103490c8525f)
  
  updated-dependencies:
  - dependency-name: src/common/vendor/yaml-cpp
    dependency-version: c7aa78d294bbe499c1ebc0abfa1e103490c8525f
    dependency-type: direct:production
  ...




#### Build


- Install `mender-artifact` from final tag on the test container
 ([d9825a9](https://github.com/mendersoftware/mender/commit/d9825a979f9777de9e58e5b15b353c0e9a70d997))  by @lluiscampos




  So that we stop using the experimental APT repos, which we should not
  rely on.




#### Refac


- Added warning when using basic auth
([MEN-7983](https://northerntech.atlassian.net/browse/MEN-7983)) ([bc10461](https://github.com/mendersoftware/mender/commit/bc10461c17cc736975a5f2e7f2d2f4eec6565501))  by @victormlg



- Refactor deployment http handlers to make them testable and prepare for HTTP 429 handling
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([8afd047](https://github.com/mendersoftware/mender/commit/8afd0477da99fd16d79d5529196a8cc3ad441bed))  by @michalkopczan



- Refactor inventory http handlers to make them testable and prepare for HTTP 429 handling
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([51eddb9](https://github.com/mendersoftware/mender/commit/51eddb93939fd2e06ac28c4f116684b5bd6d654d))  by @michalkopczan



- Refactor PushLogs and PushStatus http handlers to make them testable and prepare for HTTP 429 handling
([MEN-8850](https://northerntech.atlassian.net/browse/MEN-8850)) ([87124c6](https://github.com/mendersoftware/mender/commit/87124c60babb94779986187761e454cca332246a))  by @michalkopczan

## mender-configure-module master (2026-02-03)

### master - 2026-02-03


#### Bug fixes


- Make systemd installation systemd_unitdir aware
 ([758d25f](https://github.com/mendersoftware/mender-configure-module/commit/758d25f2b662c0ba2f20dbc6552c0daa6af1cc5f))  by @TheYoctoJester





- Exit with returncode 0 if no jwt token is obtained over dbus
([MEN-8591](https://northerntech.atlassian.net/browse/MEN-8591)) ([7bcd1b7](https://github.com/mendersoftware/mender-configure-module/commit/7bcd1b7f33a4c9dc8cf3970e2da27fe38bf32277))  by @danielskinstad






  `mender-inventory-mender-configure` produces an error when failing to
  fetch the JWT token over DBus. If we exit with 1 mender-update will log:
  ```
  raspberrypi mender-update[1070]: An authentication token could not be obtained over DBus.
  mender-update[1029]: record_id=3 severity=error time="2025-Jun-12 21:53:25.802076" name="Global" msg="'/usr/share/mender/inventory/mender-inventory-mender-configure' failed: Process...
  ```
  Now it will log:
  `raspberrypi mender-update[1070]: mender-inventory-mender-configure: An authentication token could not be obtained over DBus.`
- Fixed outdated LED-path for raspberrypi
([MEN-9002](https://northerntech.atlassian.net/browse/MEN-9002)) ([40a442c](https://github.com/mendersoftware/mender-configure-module/commit/40a442c660070ed9a0393410b4168f942e8c8782))  by @rewanrashid-boop








#### Security


- Bump tests/unit/shunit2 from `47be8b2` to `3334e53`
 ([c3d9c66](https://github.com/mendersoftware/mender-configure-module/commit/c3d9c669875243236d19bcbe025a02e1c11f90bf))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `47be8b2` to `3334e53`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/47be8b23a46a7897e849f1841f0fb704d34d0f6e...3334e53047ad143669870a9c223b70a81156533a)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-type: direct:production
  ...
- Bump tests/integration/mender_test_containers
 ([9f61038](https://github.com/mendersoftware/mender-configure-module/commit/9f6103897189e65d823ce3a9a429524b0e7d9407))  by @dependabot[bot]




  Bumps [tests/integration/mender_test_containers](https://github.com/mendersoftware/mender-test-containers) from `222916a` to `cc27472`.
  - [Commits](https://github.com/mendersoftware/mender-test-containers/compare/222916ae5b0632521139170cc4410d1242c3751d...cc27472c35c41d9fe2614f37d54bc91ccfc2f4f6)
  
  updated-dependencies:
  - dependency-name: tests/integration/mender_test_containers
    dependency-type: direct:production
  ...
- Bump tests/integration/mender_integration
 ([df654b9](https://github.com/mendersoftware/mender-configure-module/commit/df654b971e31b4c42d7f26c734277b564ec9f892))  by @dependabot[bot]




  Bumps [tests/integration/mender_integration](https://github.com/mendersoftware/integration) from `e0ddb9f` to `ca37b76`.
  - [Commits](https://github.com/mendersoftware/integration/compare/e0ddb9f641912775e81953a24002bdc406e8338f...ca37b7694c40baf77ba3837f5a1398ceafe2ee54)
  
  updated-dependencies:
  - dependency-name: tests/integration/mender_integration
    dependency-type: direct:production
  ...
- Bump tests/unit/shunit2 from `3334e53` to `da1e19d`
 ([a81e1b3](https://github.com/mendersoftware/mender-configure-module/commit/a81e1b31e29a0da53da25d4eaee2a329d402db4a))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `3334e53` to `da1e19d`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/3334e53047ad143669870a9c223b70a81156533a...da1e19de845a77628d9684e609cc0f8160782c68)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-type: direct:production
  ...
- Bump tests/unit/shunit2 from `da1e19d` to `100ffe4`
 ([79785c5](https://github.com/mendersoftware/mender-configure-module/commit/79785c5deba85596741e912e7e8c0326d9d7ee56))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `da1e19d` to `100ffe4`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/da1e19de845a77628d9684e609cc0f8160782c68...100ffe4dda539ebbe4ae9867132f08eeee8e80cb)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-type: direct:production
  ...
- Bump tests/unit/shunit2 from `100ffe4` to `0f27c1a`
 ([63f0cdf](https://github.com/mendersoftware/mender-configure-module/commit/63f0cdf0552ececd08a5605b33cfbbc0cbc45cba))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `100ffe4` to `0f27c1a`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/100ffe4dda539ebbe4ae9867132f08eeee8e80cb...0f27c1ac71998835ff41d335d45079d6eb2a4bfe)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-type: direct:production
  ...
- Bump tests/unit/shunit2 from `0f27c1a` to `6d31ca9`
 ([97118cf](https://github.com/mendersoftware/mender-configure-module/commit/97118cf99fecac81e865bbcb0d22d7f024cda730))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `0f27c1a` to `6d31ca9`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/0f27c1ac71998835ff41d335d45079d6eb2a4bfe...6d31ca9b0858cda66843057d08ea499b58c903d6)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-version: 6d31ca9b0858cda66843057d08ea499b58c903d6
    dependency-type: direct:production
  ...
- Bump tests/unit/shunit2 from `6d31ca9` to `e35296d`
 ([67bda00](https://github.com/mendersoftware/mender-configure-module/commit/67bda0056d87dd4ef08c71dcf83cf15f2d57c53e))  by @dependabot[bot]




  Bumps [tests/unit/shunit2](https://github.com/kward/shunit2) from `6d31ca9` to `e35296d`.
  - [Release notes](https://github.com/kward/shunit2/releases)
  - [Commits](https://github.com/kward/shunit2/compare/6d31ca9b0858cda66843057d08ea499b58c903d6...e35296d3be2bcde770f2989d9c09fd1a2af6b567)
  
  updated-dependencies:
  - dependency-name: tests/unit/shunit2
    dependency-version: e35296d3be2bcde770f2989d9c09fd1a2af6b567
    dependency-type: direct:production
  ...

## mender-connect master (2026-01-13)

### master - 2026-01-13


#### Bug fixes


- Preserve group assignments
([ME-530](https://northerntech.atlassian.net/browse/ME-530)) ([f5bea59](https://github.com/mendersoftware/mender-connect/commit/f5bea591ec7a53700122692764689df4a42ca205))  by @danielskinstad




- Make StopShell function re-entrant by protecting stop channel
([MEN-9029](https://northerntech.atlassian.net/browse/MEN-9029)) ([b3fb7ed](https://github.com/mendersoftware/mender-connect/commit/b3fb7edabae4909cbc361bb2ecc34d8d3b86d770))  by @alfrunes









#### Features


- Lower backoff intervals
([ME-546](https://northerntech.atlassian.net/browse/ME-546)) ([8ce8f78](https://github.com/mendersoftware/mender-connect/commit/8ce8f78bbf8747ec0cfdfbc0fdcb851ea9b89f75))  by @danielskinstad






  The previous backoff had a starting interval at 1
  minute and a max backoff at 60 minutes. When it reached 60 minutes it
  would linearly increase to 120 minutes minutes where it would keep
  retrying.
  
  The backoff will now start at 1 second and exponentially increase after
  3 retries until it reaches 30 minutes where it will keep retrying.
  For each interval a jitter between 0 and 5 seconds will be added.
- Enable 10 minute idle timeout by default
([MEN-8260](https://northerntech.atlassian.net/browse/MEN-8260)) ([15df4b2](https://github.com/mendersoftware/mender-connect/commit/15df4b2fa9b4806c76f4356583b4bcb084c0ffd2))  by @danielskinstad






  Introduce a default value of 10 minutes to `ExpireAfterIdle` and set
  `StopExpired` to true by default. This is done in order to prioritize
  auto healing of mender-connect over the ability to have a theoretically
  endless session.




#### Security


- Bump github.com/stretchr/testify from 1.10.0 to 1.11.1
 ([3771554](https://github.com/mendersoftware/mender-connect/commit/37715542c240bf112bc634a287e4c4f7646cadaf))  by @dependabot[bot]




  Bumps [github.com/stretchr/testify](https://github.com/stretchr/testify) from 1.10.0 to 1.11.1.
  - [Release notes](https://github.com/stretchr/testify/releases)
  - [Commits](https://github.com/stretchr/testify/compare/v1.10.0...v1.11.1)
  
  updated-dependencies:
  - dependency-name: github.com/stretchr/testify
    dependency-version: 1.11.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...




#### Refac


- Migrate from gorilla/websocket to coder/websocket
 ([2e8105e](https://github.com/mendersoftware/mender-connect/commit/2e8105e9f3ba8cef3e4161e362d83a38f9997634))  by @alfrunes

## mender-flash master (2026-01-05)

### master - 2026-01-05


#### Bug fixes


- Support flashing more than 4 GiB in 32 bit builds
 ([0031e01](https://github.com/mendersoftware/mender-flash/commit/0031e0184c0ebefc033e8a5bb3a503ea6bf8cae5))  by @vpodzime






  `_FILE_OFFSET_BITS` needs to be set to 64 so that I/O
  functions/syscalls working with files and devices use 64 bits to
  represent sizes. The `off_t` type needs to be used instead of
  `size_t` in places where file/device sizes and total numbers of
  bytes are used. OTOH, `size_t` is the type used by many I/O
  functions/syscalls which has to be respected.
- Fix UBI device detection
([MEN-7156](https://northerntech.atlassian.net/browse/MEN-7156)) ([8100797](https://github.com/mendersoftware/mender-flash/commit/8100797f2caf6221b9cdea0b8596cb544a97bfc2))  by @vpodzime






  Ported commit b69fa5faf6c43c5037853e2564a81d5c950f0287 to use
  a check based on the `/sys/class/ubi` tree rather than major
  device number which is not guaranteed to be stable.
  
  Also, UBI volumes have character device nodes not block device nodes.
- Do `fsync(out_fd)` before `close(out_fd)`
([MEN-7862](https://northerntech.atlassian.net/browse/MEN-7862)) ([5099e88](https://github.com/mendersoftware/mender-flash/commit/5099e88a1c7a80ff1dcd6cd924ddc4bda87ace7c))  by @vpodzime






  `close()` doesn't guarantee a sync:
  
  > A successful close does not guarantee that the data has been
  > successfully saved to disk, as the kernel uses the buffer cache
  > to defer writes.
- Use shoveling for writing to UBI devices
([MEN-8604](https://northerntech.atlassian.net/browse/MEN-8604)) ([8b92ab6](https://github.com/mendersoftware/mender-flash/commit/8b92ab6eff3d5685befa2ce0eb249f021660f14d))  by @vpodzime






  The nicer and fancier syscalls don't support UBI devices.
  
  OTOH, we do support syncing when using them so let's fix the
  comment in two ways with a single change!
- Fix handling of the '-f' short option
 ([280ea2a](https://github.com/mendersoftware/mender-flash/commit/280ea2a994ed2f086b1b8407fc11de6bdbb35c57))  by @vpodzime






  `getopt_long()` is called in two places in the code, so all
  options need to be present in both of the calls. Let's avoid this
  in the future by defining a macro and using it in both places.




#### Features


- A minimal and portable version of mender-flash
 ([bd4acbe](https://github.com/mendersoftware/mender-flash/commit/bd4acbe0b0c21014e5b2435afd50a1de7479f171))  by @vpodzime






  Written in C, much smaller and very straightforward, but doing
  the same thing.
  
  Also much faster to compile/build and with no dependencies.
- Use in-kernel copying on Linux
 ([8aa1e36](https://github.com/mendersoftware/mender-flash/commit/8aa1e36d87a578e275d849529ac2efb91b885274))  by @vpodzime






  Linux provide syscalls to copy data between two file descriptors
  directly in kernel without using user-space buffers. There's no
  reason to not use them to save some CPU cycles and potentially do
  the I/O in a more optimized way.
- Add an option to specify the fsync interval
 ([450fce0](https://github.com/mendersoftware/mender-flash/commit/450fce01d974cca80d5dd89b108349b587299733))  by @vpodzime






  And use BLOCK_SIZE as the default.
- Optimize writes by default and let the user force them
 ([1cf25a5](https://github.com/mendersoftware/mender-flash/commit/1cf25a506a16e32000e8cd795ac4a7486b3a49ed))  by @vpodzime






  Potentially reducing wear of flash memory used as the target
  device and potentially speeding things up if the target device
  has much faster reads than writes.
  
  OTOH, often it's just much faster to write all the data.
- Enable use of sendfile/splice with fsync_interval
 ([65723e1](https://github.com/mendersoftware/mender-flash/commit/65723e1077a78025ee713fbc8522c550b0e7ee86))  by @vpodzime






  We can simply as kernel to handle at most fsync_interval of bytes
  at once. Still fewer syscalls and no unnecessary user-space
  buffers needed.

## mender-container-modules main (2026-01-13)

First release of mender-container-modules

---
## Older releases

Previous to Mender Client 6.0, the release notes & changelog can be found in the pages for the individual components:

* [mender](20.Mender-Client/docs.md)
* [mender-connect](21.mender-connect/docs.md)
* [mender-configure-module](22.mender-configure-module/docs.md)
* [mender-flash](25.mender-flash/docs.md)
* [mender-binary-delta](50.mender-binary-delta/docs.md)
* [monitor-client](51.monitor-client/docs.md)

