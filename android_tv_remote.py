import asyncio

from .. import fhem, generic
from androidtvremote2 import (
    AndroidTVRemote,
    CannotConnect,
    ConnectionClosed,
    InvalidAuth,
)

class android_tv_remote(generic.FhemModule):
    def __init__(self, logger):
        super().__init__(logger)

    # FHEM FUNCTION
    async def Define(self, hash, args, argsh):
        self.logger.error(f"{len(args)}")
        if len(args) < 4:
            await fhem.readingsSingleUpdate(hash, "state", "Usage: define remote fhempy android_tv_remote (ip or dns name) -> Please delete and redefine", 1)
            return "Usage: define remote fhempy android_tv_remote (ip or dns name)"
        await super().Define(hash, args, argsh)
        self.logger.error(f"Defined android TV Remote")
        
        
        
        attr_config = {
            "tv": {
                "format": "string",
                "help": "set Android TV IP or dns Name",
            }
        }
        await self.set_attr_config(attr_config)

        set_config = {
            "register": {
                "args": ["code"],
                "params": { "code": { "default": "" , "optional": True }},
            }
        }
        await self.set_set_config(set_config)
        
        self.hostname =  args[3]
        await fhem.readingsBeginUpdate(hash)
        await fhem.readingsBulkUpdateIfChanged(hash, "state", f"connecting to {self.hostname}...")
        await fhem.readingsEndUpdate(hash, 1)

    # Attribute function format: set_attr_NAMEOFATTRIBUTE(self, hash)
    # self._attr_NAMEOFATTRIBUTE contains the new state
    async def set_attr_interval(self, hash):
        # attribute was set to self._attr_interval
        # you can use self._attr_interval already with the new variable
        pass

    # Set functions in format: set_NAMEOFSETFUNCTION(self, hash, params)
    async def set_register(self, hash, params):
        # user can specify mode as mode=eco or just eco as argument
        # params['mode'] contains the mode provided by user
        mode = params["mode"]
        await fhem.readingsSingleUpdate(hash, "mode", mode, 1)

    async def set_desiredTemp(self, hash, params):
        temp = params["temperature"]
        await fhem.readingsSingleUpdate(hash, "mode", temp, 1)

    async def set_holidayMode(self, hash, params):
        start = params["start"]
        end = params["end"]
        temp = params["temperature"]
        await fhem.readingsSingleUpdate(hash, "start", start, 1)
        await fhem.readingsSingleUpdate(hash, "end", end, 1)
        await fhem.readingsSingleUpdate(hash, "temp", temp, 1)
