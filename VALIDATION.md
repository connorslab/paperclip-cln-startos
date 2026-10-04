# Sideflash rc.1 validation

StartOS 0.4 / x86-64 experimental prerelease.

Passed:
- SDK type checks and JavaScript compilation for all three packages.
- Seven configuration unit tests per package (21 total).
- Rebuilt runtime images; fresh CLN startup, active Sideflash plugin, persistent node identity.
- ASP authentication, configuration validation, fresh server/watchman initialization.
- Wallet creation against the packaged ASP, reusable BOLT12 offer, signed compact Sideflash receive address (823 characters), and wallet persistence after restart.

Runtime tests used isolated Docker containers without published ports. No deposits, channels or payments were created.

Not verified: installation on an actual StartOS device, platform backup/restore, ARM, StartOS 0.3.5, or funded end-to-end transfers using these exact packages. Sideload as separate test apps; this is not a production release.

## rc.2 configuration update

Replaces raw JSON with labeled fields while retaining the stored configuration schema and existing keys. SDK compilation and 12 configuration/connection tests pass. Node checks distinguish DNS, HTTP authentication and connectivity errors without logging secrets. StartOS device installation remains unverified.

## rc.3

All SDK packages compile. 26 configuration/connection tests pass across the packages. Isolated runtime integration verifies CLN identity persistence, authenticated RTL login and node/channel reads, ASP/watchman initialization, wallet creation, signed Sideflash address generation and wallet restart. No funds moved. Labeled forms retain the saved configuration schema and tokens. StartOS device installation and restore remain unverified.
