# Paperclip CLN Sideflash test

This is a separate **experimental, unaudited test app** for StartOS 0.4, x86-64 only. It does not upgrade an existing production app. It creates no channels, transfers no money, and copies no existing wallet data during installation. Runtime tests are not a StartOS device installation test.

Keep the entire app backup. Stop the app before a backup; the package refuses an active-state backup. Restore only with the original instance stopped. Never run both restored and original copies of the same Lightning or Ark identity. Never restore an old Lightning state over a live node.

## Documentation

- [Sideflash integration](https://github.com/connorslab/lightning/blob/feature/sideflash/contrib/plugins/sideflash/README.md)

## What this app provides

Bitcoin Lightning node with the compact Sideflash decoder/payment plugin, XBT hold invoices, and mutually authenticated gRPC.

Peers: 9735; CLN gRPC: 9737; Hold gRPC: 9738. StartOS assigns external ports; copy them from Interfaces. The gRPC endpoints require client certificates. No REST or raw Unix RPC endpoint is exported.

## Setup

1. Open **Interfaces** and note the LAN IP and the assigned CLN gRPC / Hold gRPC ports.
2. Run **Configure test app**. Fill in the labeled fields; existing settings are loaded automatically. Set a private XBT Knots RPC URL, its credentials, and `tls_host` to the LAN IP or stable hostname clients will actually use. Do not put a port in `tls_host`. Mainnet means XBT, not SHA-256 BTC.
3. Start the app. The node generates fresh keys and persistent TLS credentials. Changing the TLS hostname later is intentionally refused; plan a credential migration instead.
4. Run **CLN gRPC** to export the client connection bundle. It includes spending-capable client credentials: keep it private. Replace the two port placeholders with the assigned StartOS ports, then paste the bundle into the Ark app's `cln` configuration field. Never copy the CA signing key or server private key.
5. Obtain the intended ASP's full public key through authenticated context, then set `trusted_server_key` before direct `pay` to Sideflash addresses. Do not infer trust from an arbitrary pasted address.

Sideflash uses the embedded offer with no directory lookup. A named `pay` request needs the full `sfl1...` address, amount in millisats, an explicit `maxfee`, and a stable `label`. Reuse exactly the same label and parameters after a lost response. Lightning settlement alone does not prove the recipient's Ark claim. Ordinary invoice and offer RPCs remain available.

```json
{
  "network": "bitcoin",
  "rpc_url": "http://NODE_LAN_IP:8332",
  "rpc_user": "RPC_USERNAME",
  "rpc_password": "RPC_PASSWORD",
  "alias": "Paperclip Sideflash Test",
  "tls_host": "startos.local",
  "trusted_server_key": ""
}
```

The RPC password is masked. **Check node connection before saving** validates the endpoint without moving funds and explains common DNS/authentication failures. Disable it only to save settings while the node is temporarily offline. The JSON below is a reference, not something you need to edit.

## Backup and access

Stop the app, then use StartOS Backup. Back up all volumes, not only a seed. **Configure test app** can rotate the web access token while stopped. Client TLS credentials are independent of that token. Package signing keys are not wallet keys.

## Validation limits

See VALIDATION.md in the feature branch. These files have not been installed on a StartOS device by the builder. No mainnet funds are included. Start with tiny, disposable test amounts only after verifying connectivity, backup/restore and identity.

## RTL channel management (rc.3)

After CLN starts, open **Interfaces > RTL**. Use **RTL initial password** to reveal the generated password, then sign in. RTL uses a purple dark theme and includes the Sideflash patch. Channels, peers, invoices, offers and on-chain transactions operate on this CLN instance. Sending funds and opening/closing channels require your explicit actions in RTL.

Set the trusted ASP public key in Configure test app before Sideflash payments. Offers are enabled by default. CLN REST is loopback-only and is not exported. RTL requires authentication; keep the interface private.

RTL settings and password changes persist in the additional `rtl` volume and are included in stopped-app backups. A password changed inside RTL replaces the generated initial password. Stop the app and sideload the update over the existing installation; do not uninstall or delete its data.
