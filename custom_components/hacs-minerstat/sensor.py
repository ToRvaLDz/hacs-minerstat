from homeassistant.helpers import entity
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from datetime import timedelta
import voluptuous as vol
import urllib.request, json
import homeassistant.helpers.config_validation as cv

__version__ = '1.0.0'

CONF_NAME = 'name'
CONF_ACCESS_KEY = 'access_key'
CONF_RIG_NAME = 'rig_name'
CONF_BASE_CURRENCY = 'base_currency'

DEFAULT_NAME = 'Minerstat'
DEFAULT_CURRENCY = 'USD'
DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)
SCAN_INTERVAL = timedelta(minutes=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_BASE_CURRENCY, default=DEFAULT_CURRENCY): cv.string,
    vol.Required(CONF_ACCESS_KEY): str,
    vol.Required(CONF_RIG_NAME): str,
   
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Minerstat(hass, config)])

class Minerstat(entity.Entity):
    def __init__(self, hass, config):
        self.hass = hass
        self._config = config
        self._state = None
        self._unit = None
        self._exchange = 1
        self.update()

    @property
    def name(self):
        return self._config[CONF_NAME]

    @property
    def icon(self):
        return 'mdi:bitcoin'

    @property
    def state(self):
        return self._state

    def update(self):
        self._unit=self._config[CONF_BASE_CURRENCY]

        req = urllib.request.Request(f'https://api.minerstat.com/v2/stats/{self._config[CONF_ACCESS_KEY]}/{self._config[CONF_RIG_NAME]}', headers={'User-Agent' : "Home-assistant.io"})
        with urllib.request.urlopen(req) as url:
            data = json.loads(url.read().decode())
            self._usd = data[self._config[CONF_RIG_NAME]]['revenue']['usd_month']
            self._cost = data[self._config[CONF_RIG_NAME]]['info']['electricity']
            self._cons = data[self._config[CONF_RIG_NAME]]['info']['consumption']

        self._exchange = 1

        if self._config[CONF_BASE_CURRENCY]!='USD'
            req = urllib.request.Request(f'https://api.exchangeratesapi.io/latest?base={self._config[CONF_BASE_CURRENCY]}&symbols=USD', headers={'User-Agent' : "Home-assistant.io"})
            with urllib.request.urlopen(req) as url:
                data = json.loads(url.read().decode())
                self._exchange = data['rates']['USD']
                
        self._state = (self._usd / self._exchange)  - (self._cons/1000 * self._cost * 24 * 30)
                
    @property
    def device_state_attributes(self):
        return {
            'unit_of_measurement': self._unit
        }
