from endstone.plugin import Plugin
from endstone_server_maintenance.event_listener import EventListener

class ServerMaintenance(Plugin):
    name = "ServerMaintenance"
    version = "0.1.0"
    api_version = "0.4"
    description = "A simple server maintenance plugin for Endstone servers"
    authors = ["nicholass003"]
    website = "https://github.com/nicholass003/endstone-server-maintenance"
    load = "POSTWORLD"

    def on_load(self) -> None:
        self.save_default_config()

        self._maintenance = {
            "is_maintenance" : False,
            "start_date_time" : 0,
            "end_date_time" : 0,
        }

        self._maintenance_players = {
            "players" : []
        }

    def on_enable(self) -> None:
        self._listener = EventListener(self)
        self.register_events(self._listener)

    def is_maintenance(self) -> bool:
        return self._maintenance["is_maintenance"]
    
    def get_maintenance(self) -> object:
        return self._maintenance
    
    def set_maintenance(self, object: object) -> None:
        self._maintenance = object

    def get_maintenance_players(self) -> object:
        return self._maintenance_players
    
    def is_player_allowed(self, name: str) -> bool:
        while name in self._maintenance_players:
            return True
        return False

    def add_maintenance_player(self, name: str) -> bool:
        while name not in self._maintenance_players:
            self._maintenance_players.append(name)
            return True
        return False
    
    def remove_maintenance_player(self, name: str) -> bool:
        while name in self._maintenance_players:
            self._maintenance_players.remove(name)
            return True
        return False