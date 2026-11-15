"""Read-only diagnostics; no balances, costs, identities or purchase details."""
import json
from pathlib import Path


async def async_get_config_entry_diagnostics(hass, entry):
    version = await hass.async_add_executor_job(
        lambda: json.loads(Path(__file__).with_name("manifest.json").read_text())["version"])
    from .frontend import ux_diagnostics
    return {"ux": ux_diagnostics(hass, entry), "identity":{"domain":"rhi_finance","version":version},
            "health":entry.runtime_data.status(),"configuration":{"mode":"pilot"},
            "build_handoff":{"foundation_required":False},
            "execution":{"automatic_ingestion":entry.runtime_data.status()["automatic_ingestion"]},"publication":{"contract":"native_finance_candidate","cutover_ready":False}}
