"""HA-native pilot readiness entity."""
from homeassistant.components.sensor import SensorEntity, SensorStateClass
import hashlib
import json
from homeassistant.core import callback


async def async_setup_entry(hass, entry, async_add_entities):
    runtime=entry.runtime_data
    outputs={}
    @callback
    def publish(configs):
        new=[]
        for config in configs:
            key=runtime.tariff_output_scope(config)
            if key in outputs:
                outputs[key].set_config(config)
            else:
                entity=TariffPrice(entry,config)
                outputs[key]=entity
                new.append(entity)
        if new:
            async_add_entities(new,update_before_add=True)
    runtime.tariff_output_listener=publish
    entry.async_on_unload(lambda:setattr(runtime,"tariff_output_listener",None))
    async_add_entities([PilotStatus(entry)], update_before_add=True)
    publish(entry.options.get("tariff_outputs",[]))


class PilotStatus(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "RHI Finance pilot status"
    _attr_icon = "mdi:wallet"

    def __init__(self, entry):
        self._attr_unique_id = entry.entry_id + "_pilot_status"
        self.runtime = entry.runtime_data

    async def async_added_to_hass(self):
        self.runtime.condition_listener=self.publish_conditions
        self.async_on_remove(lambda:setattr(self.runtime,"condition_listener",None))

    @callback
    def publish_conditions(self,events):
        data=self.runtime.status()
        self._attr_native_value=data["state"]
        self._attr_extra_state_attributes={k:v for k,v in data.items() if k!="state"}
        if events:
            self._attr_extra_state_attributes["rhi_notification_events"]=events
        if self.hass is not None and self.entity_id is not None:
            self.async_write_ha_state()

    async def async_update(self):
        events=await self.runtime.refresh_conditions()
        # Initial update precedes registration. HA writes the resulting state.
        data=self.runtime.status()
        self._attr_native_value=data["state"]
        self._attr_extra_state_attributes={k:v for k,v in data.items() if k!="state"}
        if events:
            self._attr_extra_state_attributes["rhi_notification_events"]=events


class TariffPrice(SensorEntity):
    """Explicit opt-in native price for HA energy/water dashboards."""
    _attr_icon="mdi:currency-eur"
    _attr_state_class=SensorStateClass.MEASUREMENT

    def __init__(self,entry,config):
        self.runtime=entry.runtime_data
        scope=self.runtime.tariff_output_scope(config)
        self._attr_unique_id=entry.entry_id+"_rate_"+hashlib.sha256(json.dumps(scope).encode()).hexdigest()
        self._attr_name="Finance "+config["carrier"]+" "+config["role"]+" price"+(" · "+config["owner"] if config.get("owner") else "")
        self._attr_native_unit_of_measurement=config["currency"]+"/"+config["unit"]
        self.set_config(config)

    @callback
    def set_config(self,config):
        self.config=dict(config)
        self._refresh()
        if self.hass is not None and self.entity_id is not None:
            self.async_write_ha_state()

    def _refresh(self):
        value=self.runtime.current_tariff_output(self.config)
        self._attr_available=value is not None
        self._attr_native_value=value

    async def async_update(self):
        self._refresh()
