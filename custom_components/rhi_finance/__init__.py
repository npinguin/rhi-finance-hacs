"""Native HA Finance pilot entry; no automatic source or legacy ledger mutation."""
DOMAIN = "rhi_finance"



def _validate_config(config):
    from homeassistant.helpers import config_validation as cv
    return cv.config_entry_only_config_schema(DOMAIN)(config)


CONFIG_SCHEMA = _validate_config


async def async_setup(hass, config):
    from .ha_runtime import register_services
    register_services(hass)
    return True


async def async_setup_entry(hass, entry):
    from .ha_runtime import Runtime
    entry.runtime_data = Runtime(hass, entry)
    await entry.runtime_data.start()
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
