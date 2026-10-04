<p align="center"><img src="icon.svg" alt="Paperclip logo" width="96"></p>

# Paperclip CLN on StartOS — Sideflash test

Bitcoin Lightning node with the compact Sideflash decoder/payment plugin, XBT hold invoices, and mutually authenticated gRPC.

This is a separate **experimental, unaudited test app** for StartOS 0.4, x86-64 only. It does not upgrade an existing production app. It creates no channels, transfers no money, and copies no existing wallet data during installation. Runtime tests are not a StartOS device installation test.

Keep the entire app backup. Stop the app before a backup; the package refuses an active-state backup. Restore only with the original instance stopped. Never run both restored and original copies of the same Lightning or Ark identity. Never restore an old Lightning state over a live node.

## Table of Contents

- [Image and Container Runtime](#image-and-container-runtime)
- [Volume and Data Layout](#volume-and-data-layout)
- [File Models](#file-models)
- [Dependencies](#dependencies)
- [Network Access and Interfaces](#network-access-and-interfaces)
- [Installation and First-Run Flow](#installation-and-first-run-flow)
- [Actions](#actions)
- [Tasks](#tasks)
- [Health Checks](#health-checks)
- [Backups and Restore](#backups-and-restore)
- [Limitations and Differences](#limitations-and-differences)
- [Quick Reference for AI Consumers](#quick-reference-for-ai-consumers)

## Image and Container Runtime

Bitcoin Lightning node with the compact Sideflash decoder/payment plugin, XBT hold invoices, and mutually authenticated gRPC. Images are embedded in the signed s9pk; the installer does not need the local build tags. Runtime base/output IDs and source revisions are recorded in BUILD-PROVENANCE.json. Wrappers run under the service container root, with umask 077 and persistent files mode 0600. No host Docker socket or privileged mode is mounted.

## Volume and Data Layout

`main`: settings, Lightning keys, databases, Sideflash idempotency records, hold state, TLS keys. `startos`: configuration state and generated tokens.

## File Models

`startos/store.json`: configuration, access token and database secret. Configuration is validated by the packaged runtime before saving. Main rewrites `/data/settings.json` from that state. Secrets are never part of the image.

## Dependencies

An operator-supplied, reachable XBT node RPC endpoint is required. StartOS package dependencies are not hardcoded so compatible node implementations can be used.

## Network Access and Interfaces

Peers: 9735; CLN gRPC: 9737; Hold gRPC: 9738. StartOS assigns external ports; copy them from Interfaces. The gRPC endpoints require client certificates. No REST or raw Unix RPC endpoint is exported. Interfaces do not automatically enable internet or Tor access. Use the LAN for this first test.

## Installation and First-Run Flow

A critical setup task blocks first startup. Follow instructions.md. All identities are fresh and app IDs are separate from production.

## Actions

`configure`: stopped-only labeled configuration fields, masked RPC password, existing-settings prefill, and an optional read-only node connection check. `connection-info`: private mTLS client bundle.

## Tasks

A critical configuration task is registered until setup state exists.

## Health Checks

Readiness checks the primary listening port, and PostgreSQL for Ark. A listening port is not proof of chain synchronization, sufficient liquidity or payment delivery.

## Backups and Restore

All declared volumes are backed up together. The pre-backup guard rejects a started app. Ark uses stopped PostgreSQL physical storage, not a live directory copy. Restore with the original instance stopped. Device-level backup/restore remains a tester gate.

## Limitations and Differences

StartOS 0.4 x86-64 only; no 0.3.5 or ARM package is claimed. Experimental Sideflash recipient allowlist, server pin and 24-hour validity remain enforced. No production rollout or on-chain/Lightning spending is performed by package setup. Docker runtime checks do not verify StartOS host networking or platform restore behavior.

## Quick Reference for AI Consumers

```yaml
package_id: paperclip-cln-sideflash
branch: feature/sideflash
architectures: [x86_64]
startos: "0.4"
version: "0.1.0:0"
production_ready: false
```
