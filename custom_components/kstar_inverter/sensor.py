"""Sensor platform for Kstar Inverter (RS485 / TCP Modbus)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    REVOLUTIONS_PER_MINUTE,
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfReactivePower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import KstarDataUpdateCoordinator
from .entity import KstarEntity


@dataclass(frozen=True)
class KstarSensorEntityDescription(SensorEntityDescription):
    """Describes Kstar sensor entity."""


SENSORS: tuple[KstarSensorEntityDescription, ...] = (
    # Status & Diagnostics
    KstarSensorEntityDescription(
        key="operating_mode",
        name="Operating Status",
        icon="mdi:solar-power-variant",
    ),
    KstarSensorEntityDescription(
        key="dsp_alarm",
        name="DSP Alarm",
        icon="mdi:alert-outline",
    ),
    KstarSensorEntityDescription(
        key="dsp_error",
        name="DSP Error",
        icon="mdi:alert-circle-outline",
    ),
    KstarSensorEntityDescription(
        key="iv_scan_status",
        name="I/V Scan Status",
        icon="mdi:chart-bell-curve",
    ),
    # PV Inputs
    KstarSensorEntityDescription(
        key="pv1_voltage",
        name="PV1 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv1_current",
        name="PV1 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv1_power",
        name="PV1 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv2_voltage",
        name="PV2 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv2_current",
        name="PV2 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv2_power",
        name="PV2 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pv3_voltage",
        name="PV3 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="pv3_current",
        name="PV3 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="pv3_power",
        name="PV3 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    # Grid & AC Output
    KstarSensorEntityDescription(
        key="grid_power",
        name="Grid-Tied Active Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="apparent_power",
        name="Apparent Power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="reactive_power",
        name="Reactive Power",
        native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="power_factor",
        name="Power Factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="grid_voltage_r",
        name="Grid Voltage R-Phase",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="grid_voltage_s",
        name="Grid Voltage S-Phase",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="grid_voltage_t",
        name="Grid Voltage T-Phase",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="grid_frequency_r",
        name="Grid Frequency R-Phase",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="grid_current_r",
        name="Grid Current R-Phase",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="grid_current_s",
        name="Grid Current S-Phase",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="grid_current_t",
        name="Grid Current T-Phase",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    # Energy Yield
    KstarSensorEntityDescription(
        key="daily_energy",
        name="Daily Energy Yield",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    KstarSensorEntityDescription(
        key="annual_energy",
        name="Annual Energy Yield",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    KstarSensorEntityDescription(
        key="total_energy",
        name="Total Energy Yield",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Temperatures & Hardware Health
    KstarSensorEntityDescription(
        key="radiator_temperature",
        name="Radiator Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="module_temperature",
        name="Module Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    KstarSensorEntityDescription(
        key="pbus_voltage",
        name="Positive Bus Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="nbus_voltage",
        name="Negative Bus Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    KstarSensorEntityDescription(
        key="dc_insulation_resistance",
        name="DC Insulation Resistance",
        native_unit_of_measurement="kΩ",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:omega",
    ),
    KstarSensorEntityDescription(
        key="fan_a_speed",
        name="Fan A Speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kstar sensors based on a config entry."""
    coordinator: KstarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KstarSensor(coordinator, description) for description in SENSORS
    )


class KstarSensor(KstarEntity, SensorEntity):
    """Representation of a Kstar Inverter sensor."""

    entity_description: KstarSensorEntityDescription

    def __init__(
        self,
        coordinator: KstarDataUpdateCoordinator,
        description: KstarSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.key)
