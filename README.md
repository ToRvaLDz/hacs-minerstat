# hacs-minerstat

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
![Validate](https://github.com/ToRvaLDz/hacs-minerstat/workflows/Validate/badge.svg)

A integration with [Minerstart](https://minerstat.com/) to create a sensor from your rig's hashrate.

## Usage
`configuration.yaml`:
```yaml
sensor:
  - platform: hacs-minerstat
    name: "My Awesome Rig"
    access_key: "00000000"
    rig_name: "RIG1"
    base_currency: "EUR"
```

## Options
|Name|Type|Necessity|Default|Description|
|----|:--:|:-------:|:-----:|-----------|
|`platform`|string|**Required**|`hacs-minerstat`|The platform name|
|`access_key`|string|**Required**||Your personal access key from https://my.minerstat.com/|
|`rig_name`|string|**Required**||The name that you defined for your rig at Minerstat|
|`base_currency`|string|Optional*||The base currency for showing profit|
|`name`|string|Optional|`Minerstat`|Custom name for the sensor|


