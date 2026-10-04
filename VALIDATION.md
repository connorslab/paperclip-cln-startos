# Validation status

Experimental StartOS 0.4 / x86-64 packaging branch. SDK type checks and JavaScript compilation passed for all three packages.

Zero-funded Docker checks exercised fresh CLN identity persistence, Sideflash plugin loading, ASP setup/authentication and watchman startup, wallet creation and reusable-offer/Sideflash API access. Final Sideflash receive creation after an ASP restart remains under test.

Final image rebuild, signed s9pk packing/verification, StartOS installation, backup/restore, and funded end-to-end testing of the exact final artifacts are not yet complete. No production readiness is claimed. The user will sideload the resulting packages.

Configuration unit tests: 7 passed per package (21 total). Publication checks found no embedded private keys or known deployment credentials.
