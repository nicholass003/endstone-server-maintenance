from datetime import datetime

from endstone.event import event_handler, EventPriority, PlayerLoginEvent

class EventListener:
    def __init__(self, plugin) -> None:
        from endstone_server_maintenance.server_maintenance import ServerMaintenance
        if isinstance(plugin, ServerMaintenance):
             self._plugin = plugin
    

    @event_handler(priority=EventPriority.HIGHEST)
    def on_player_login(self, event: PlayerLoginEvent) -> None:
            is_maintenance = self._plugin.is_maintenance()
            message = self._plugin.MESSAGE
            start_date_time = datetime.fromtimestamp(self._plugin._maintenance["start_date_time"])
            end_date_time = datetime.fromtimestamp(self._plugin._maintenance["end_date_time"])

            is_allowed = self._plugin.is_player_allowed(event.player.name)
            if is_maintenance == True and not is_allowed:
                kick_message = message.format(start_date_time=start_date_time, end_date_time=end_date_time)
                event.kick_message = kick_message
                event.cancelled = True