# Development build

Use a Linux StartOS packaging workspace, Node.js, Docker and Start CLI.

```sh
npm ci
npm run check
npm run build
python3 -m unittest discover -s tests -v
```

The Dockerfile currently consumes a locally built experimental runtime image via `BASE_IMAGE`; it is not a standalone public-registry build. Source revisions are recorded in BUILD-PROVENANCE.json. CLN additionally needs the pinned source's `contrib/plugins/sideflash` and `contrib/pyln-client` in its Docker build context. Build the image under the matching tag in `startos/manifest/index.ts`, then run `start-cli s9pk pack --arch=x86_64 -o package.s9pk` from this directory. Keep workspace signing keys outside the repository.

Final artifacts and their immutable image IDs/checksums will be recorded after validation. See VALIDATION.md for outstanding checks.
