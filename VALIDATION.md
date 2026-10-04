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
