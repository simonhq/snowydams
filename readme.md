# Snowy Dams
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Creates sensors for Home Assistant with the Snowy Hydro Reservoir level information_


## Lovelace Examples

![Example of the entities in Lovelace](https://github.com/simonhq/snowydams/blob/master/snowy_dams_entities.PNG)

![An Entity has capacity and current volume](https://github.com/simonhq/snowydams/blob/master/snowy_dams_entity.PNG)

## Installation

This app is best installed using [HACS](https://github.com/custom-components/hacs), so that you can easily track and download updates.

Alternatively, you can download the `snowydams` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `snowydams` module.

## How it works

The [Snowy Hydro](https://www.snowyhydro.com.au/our-energy/water/storages/lake-levels-calculator/) site provides this information, this just scrapes the page and makes the information available as sensors in HA.

As this is non time critical sensor, it only gets the information once per day at 5.17am.

I have also set it for you to provide an input_boolean that you specify for when to update the sensor beyond the daily schedule. You can obviously automate when you want that input_boolean to turn on.

### To Run

You will need to create an input_boolean entity to watch for when to update the sensor. When this `input_boolean` is turned on, whether manually or by another automation you
create, the scraping process will be run to create/update the sensor.

## AppDaemon Libraries

Please add the following packages to your appdaemon 4 configuration on the supervisor page of the add-on.

``` yaml
system_packages: []
python_packages:
  - bs4
init_commands: []
```

## App configuration

In the apps.yaml file in the appdaemon/apps directory - 

```yaml
snowy_dams:
  module: snowydams
  class: Get_Snowy_Dams
  DAM_FLAG: "input_boolean.check_snowy_dams"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `snowydams`
`class` | False | string | | `Get_Snowy_Dams`
`DAM_FLAG` | False | string || The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_snowy_dams 

## Sensors Created

This version will create 4 sensors

* sensor.snowy_dam_last_updated
* sensor.snowy_dam_eucumbene
* sensor.snowy_dam_jindabyne
* sensor.snowy_dam_tantangara

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.