# Updating

Use feature/sideflash only. Keep each test app ID stable. Pin all three upstream source commits and record base/output image IDs in BUILD-PROVENANCE.json. Build native x86-64 images, run runtime checks, compile the SDK, then pack with the private workspace signing key. Never include that key, configuration, credentials, live volumes, or recovery phrases in git or the s9pk. No automated publication is enabled.
