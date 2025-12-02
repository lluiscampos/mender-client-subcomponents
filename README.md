[![Build Status](https://gitlab.com/Northern.tech/Mender/mender-artifact/badges/master/pipeline.svg)](https://gitlab.com/Northern.tech/Mender/mender-artifact/pipelines)

# Mender Client subcomponents

Mender is an open source over-the-air (OTA) software updater for embedded Linux
devices. Mender comprises a client running at the embedded device, as well as
a server that manages deployments across many devices.

This repository serves two main purposes:

1. **Inventory Script**: Provides `mender-inventory-client-version`, an
   inventory script that reports the `mender_client_version` key. See the
   [Default inventory from Mender Docs](https://docs.mender.io/client-installation/inventory#default-inventory).
   The script is available as both Yocto recipe and Debian package which ensures
   a supported combination of Mender subcomponents running on the device.

2. **Subcomponents Relationship**: Maintains JSON files defining the
   relationship between Mender Client subcomponents for each release (e.g.,
   `{"mender-update": "1.2.3", "mender-connect": "4.5.6", ...}`). See the
   [Mender Client subcomponents from Mender Docs](https://docs.mender.io/release-information/supported-releases#mender-client-subcomponents).
   New files are added with each release. .

Additionally, this repository builds and publishes the Virtual Device for application
updates, used for Mender on-boarding. The Docker configuration was migrated from the
[integration repository](https://github.com/mendersoftware/integration/tree/e896c9e62263b6ad9d41e330f0c52d23d159ded9/extra/mender-client-docker-addons).

## Contributing

We welcome and ask for your contribution. If you would like to contribute to Mender, please read our guide on how to best get started [contributing code or
documentation](https://github.com/mendersoftware/mender/blob/master/CONTRIBUTING.md).

## License

Mender is licensed under the Apache License, Version 2.0. See
[LICENSE](https://github.com/mendersoftware/artifacts/blob/master/LICENSE) for the
full license text.

## Security disclosure

We take security very seriously. If you come across any issue regarding
security, please disclose the information by sending an email to
[security@mender.io](security@mender.io). Please do not create a new public
issue. We thank you in advance for your cooperation.

## Connect with us

* Join the [Mender Hub discussion forum](https://hub.mender.io)
* Follow us on [Twitter](https://twitter.com/mender_io). Please
  feel free to tweet us questions.
* Fork us on [Github](https://github.com/mendersoftware)
* Create an issue in the [bugtracker](https://northerntech.atlassian.net/projects/MEN)
* Email us at [contact@mender.io](mailto:contact@mender.io)
* Connect to the [#mender IRC channel on Libera](https://web.libera.chat/?#mender)
