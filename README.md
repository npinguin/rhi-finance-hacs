# Robotix Home Intelligence · Finance (TEST)

**Protected isolated pilot, not production-ready.** Official Home Assistant OS/Container 2026.11.1, CPython 3.14 musl, 64-bit amd64 and arm64 (Raspberry Pi 4/5, HA Green/Yellow or compatible Intel hosts). Other Python ABIs and platforms are not qualified.

## Installation
1. Back up Home Assistant.
2. In HACS add `https://github.com/npinguin/rhi-finance-hacs` as a custom **Integration**.
3. Enable prereleases and select the immutable TEST version.
4. Restart Home Assistant and add **RHI Finance** from Settings → Devices & services.
5. Check the pilot status sensor. Test with synthetic manual inputs only.

Do not remove existing Basic/Finance configuration, import real historical data or replace an active ledger. Automatic provider registration, tariff ingestion, migration and full UX are not yet available. The pilot is not a second production accounting engine. See [distribution notice](custom_components/rhi_finance/DISTRIBUTION_NOTICE.md).

Use the public issue tracker for installation feedback. No raw Finance business source is distributed.
