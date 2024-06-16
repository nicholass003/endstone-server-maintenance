from datetime import datetime, timedelta

from endstone._internal.endstone_python import CommandSender
from endstone import ColorFormat
from endstone.command import Command
from endstone_server_maintenance.server_maintenance import ServerMaintenance

class MaintenanceCommand(Command):

    ACTION_DISABLE = "Disabled"
    ACTION_ENABLE = "Enabled"

    def __init__(self, plugin: ServerMaintenance) -> None:
        super().__init__("maintenance", "Allow users to use all commands provided by this plugin.", ["/maintenance"], ["mtc"], ["server_maintenance.command.maintenance"])
        self._plugin = plugin
    
    def execute(self, sender: CommandSender, args: list[str]) -> bool:
        if(not self.test_permission(sender)):
            return True
        
        match args[0].lower():
            case "add":
                if len(args) > 0:
                    if self._plugin.add_maintenance_player(args[1].lower()) == True:
                        sender.send_message(f"{ColorFormat.GREEN}Successfully added {args[1]} to maintenance players")
                    else:
                        sender.send_error_message(f"{ColorFormat.RED}Player with gamertag {args[1]} is exists!")
                else:
                    sender.send_error_message(f"{ColorFormat.RED}Please input player name.")
            case "on":
                if(self.handle_activation(sender=sender, action=self.ACTION_ENABLE, value=True) == True):
                    if len(args) > 0:
                        end_value = self.convert_to_integer(args[1])
                        if(end_value == None):
                            sender.send_error_message(f"{ColorFormat.RED}Please input numeric only.")
                            return True
                        self._plugin._maintenance["end_date_time"] = datetime.now() + timedelta(hours=end_value)
                        sender.send_message(f"{ColorFormat.RED}Setting Maintenance for {end_value} hour ahead.")
                    else:
                        self._plugin._maintenance["end_date_time"] = datetime.now() + timedelta(hours=1)
                        sender.send_message(f"{ColorFormat.RED}Setting default Maintenance for 1 hour ahead.")
                    
                    self._plugin._maintenance["start_date_time"] = datetime.now()
            case "off":
                self.handle_activation(sender=sender, action=self.ACTION_DISABLE, value=False)
            case "remove":
                if len(args) > 0:
                    if self._plugin.remove_maintenance_player(args[1].lower()) == True:
                        sender.send_message(f"{ColorFormat.GREEN}Successfully removed {args[1]} to maintenance players")
                    else:
                        sender.send_error_message(f"{ColorFormat.RED}Player with gamertag {args[1]} is not exists!")
                else:
                    sender.send_error_message(f"{ColorFormat.RED}Please input player name.")
            case _:
                sender.send_error_message(f"{ColorFormat.RED}There are no maintenance command with name {args[0]}.")
        return True
    
    def handle_activation(self, sender: CommandSender, action: str, value: bool) -> bool:
        current_state = self._plugin.is_maintenance

        if current_state == value:
            sender.send_error_message(f"{ColorFormat.RED}Server Maintenance was previously {action}")
            return False
        else:
            self._plugin._maintenance["is_maintenance"] = value
            if value == False:
                self._plugin._maintenance["start_date_time"] = 0
                self._plugin._maintenance["end_date_time"] = 0
            sender.send_message(f"{ColorFormat.GREEN}Server Maintenance has been set to {action}.")
        return True

    def convert_to_integer(self, string_value: str) -> int | None:
        try:
            integer_value = int(string_value)
            return integer_value
        except ValueError as err:
            return None
