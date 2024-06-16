from endstone.event import event_handler, EventPriority, PlayerLoginEvent
from endstone_server_maintenance.server_maintenance import ServerMaintenance

class EventListener:
    def __init__(self, plugin: ServerMaintenance) -> None:
        self._plugin = plugin

    @event_handler(priority=EventPriority.HIGHEST)
    def on_player_login(self, event: PlayerLoginEvent) -> None:
            is_maintenance = self._plugin.is_maintenance
            message = self._plugin.config["message"]
            start_date_time = self._plugin._maintenance["start_date_time"]
            end_date_time = self._plugin._maintenance["end_date_time"]

            is_allowed = self._plugin.is_player_allowed(event.player.name)
            if is_maintenance == True & is_allowed == False:
                event.kick_message = message.format(start_date_time=start_date_time, end_date_time=end_date_time)
                event.cancelled = True