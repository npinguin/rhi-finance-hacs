"""Native, event-driven stock condition projection; Finance ledger owns the facts."""
import hashlib
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import callback


async def async_setup_entry(hass,entry,async_add_entities):
    runtime=entry.runtime_data
    entities={}

    @callback
    def publish(rows):
        new=[]
        for row in rows:
            key=row["asset_id"]
            if key in entities:
                entities[key].update_fact(row)
            else:
                entity=StockCondition(entry.entry_id,row)
                entities[key]=entity
                new.append(entity)
        if new:
            async_add_entities(new)

    runtime.alert_listener=publish
    entry.async_on_unload(lambda: setattr(runtime,"alert_listener",None))
    publish(await runtime.invoke("stock_alerts"))


class StockCondition(BinarySensorEntity):
    _attr_should_poll=False
    _attr_device_class=BinarySensorDeviceClass.PROBLEM
    _attr_icon="mdi:package-variant-closed"

    def __init__(self,entry_id,row):
        self._attr_unique_id=entry_id+"_stock_"+hashlib.sha256(row["asset_id"].encode()).hexdigest()
        self.update_fact(row)

    @callback
    def update_fact(self,row):
        self._attr_name=row["origin"]["title"]
        self._attr_available=row["available"]
        self._attr_is_on=row["active"] if row["available"] else None
        self._attr_extra_state_attributes={"rhi_notification_origin":row["origin"],
                                          "rhi_notification_observation":row["observation"]}
        if self.hass is not None:
            self.async_write_ha_state()
