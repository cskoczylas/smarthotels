from protocol import TPLinkSmartHomeProtocol
from typing import Optional, Dict


class SmartBulb(object):
    def __init__(self,
                 host: str,
                 protocol: 'TPLinkSmartHomeProtocol' = None) -> None:
        #creating new SmartBulb instance
        self.host = host
        if not protocol:
            protocol = TPLinkSmartHomeProtocol()
        self.protocol = protocol

    def _query_helper(self,
                      target: str,
                      cmd: str,
                      arg: Optional[Dict] = None) -> None:
        if arg is None:
            arg = {}
        try:
            response = self.protocol.query(
                host = self.host,
                request = {target: {cmd: arg}}
            )
        except Exception as ex:
            pass

        #print("\nthis was the response\n")
        #print(response)

    def state(self, bulb_state: str) -> None:
        #Turn the bulb ON or OFF
        if bulb_state == 'ON':
            new_state = 1
        else:
            new_state = 0
        light_state = {"on_off": new_state,}
        
        self._query_helper("smartlife.iot.smartbulb.lightingservice",
                           "transition_light_state", light_state)    

    def brightness(self, brightness: int) -> None:
        #Sets the brightness [0: 100]
        light_state = {"brightness": brightness,}

        self._query_helper("smartlife.iot.smartbulb.lightingservice",
                           "transition_light_state", light_state)
