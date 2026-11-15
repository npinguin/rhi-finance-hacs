# RHI Finance

Household financial and inventory ledger, native cumulative meter registration, direct consumption, stock management and period reporting.

## Installation

1. Add `https://github.com/npinguin/rhi-finance-hacs` as a custom Integration repository in HACS. Enable prereleases and select the published TEST version.
2. Back up Home Assistant, install, restart, and add **RHI Finance** in Settings → Devices & services.
3. Enable the optional UX in integration options. Add `/rhi_finance/frontend/finance-card.js` as a JavaScript module dashboard resource and add a card with `type: custom:rhi-finance-card` to an existing view.

Supported TEST: HA OS/Container 2026.11.1, 64-bit amd64 or arm64 (CPython 3.14 musl). No mandatory Foundation. Historical import, supplier contracts, forecasts and full migration are not qualified. Keep existing Finance configuration and a pre-upgrade backup.

## License

See bundled notices for protected TEST permission and third-party licenses.
