from datetime import datetime, timedelta

from endstone import ColorFormat
from endstone._internal.endstone_python import Command, CommandSender
from endstone._internal.plugin_loader import PermissionDefault
from endstone.plugin import Plugin

class ServerMaintenance(Plugin):
    name = "ServerMaintenance"
    version = "0.1.0"
    api_version = "0.4"
    description = "A simple server maintenance plugin for Endstone servers"
    authors = ["nicholass003"]
    website = "https://github.com/nicholass003/endstone-server-maintenance"
    load = "POSTWORLD"

    MESSAGE = '''Server Maintenance Notice
    Server is currently undergoing maintenance.
    Maintenance Period: {start_date_time} to {end_date_time}
    Thank you for your patience and support.'''

    commands = {
        "maintenance": {
            "description": "Allow users to use all commands provided by this plugin.",
            "usages": [
                "/maintenance ()[enum: EnumType] [text: string]",
                "/maintenance (add|on|off|remove)[enum: EnumType] [text: string]"
                ],
            "aliases": ["mtc"],
            "permissions": ["server_maintenance.command"],
        },
    }

    permissions = {
        "server_maintenance.command": {
            "description": "Allow users to use all commands provided by this plugin.",
            "default": PermissionDefault.OPERATOR,
            "children": {
                "server_maintenance.command.add": True,
                "server_maintenance.command.on": True,
                "server_maintenance.command.off": True,
                "server_maintenance.command.remove": True,
            },
        },
    }

    ACTION_DISABLE = "Disabled"
    ACTION_ENABLE = "Enabled"

    def on_load(self) -> None:
        self._maintenance = {
            "is_maintenance" : False,
            "start_date_time" : 0,
            "end_date_time" : 0,
        }

        self._maintenance_players = {
            "players" : []
        }

    def on_enable(self) -> None:
        from endstone_server_maintenance.event_listener import EventListener
        self._listener = EventListener(self)
        self.register_events(self._listener)
        self.server.scheduler.run_task_timer(self, self.maintenance_task, delay=0, period=10)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not sender.has_permission("server_maintenance.command"):
            sender.send_error_message(f"{ColorFormat.RED}You don't have permission to use this command.")
            return True
        
        match command.name:
            case "maintenance":
                if len(args) > 0:
                    subcommand = args[0].lower()
                    match subcommand:
                        case "add":
                            if len(args) > 1:
                                if self.add_maintenance_player(args[1].lower()) == True:
                                    sender.send_message(f"{ColorFormat.GREEN}Successfully added {args[1]} to maintenance players")
                                else:
                                    sender.send_error_message(f"{ColorFormat.RED}Player with gamertag {args[1]} is exists!")
                            else:
                                sender.send_error_message(f"{ColorFormat.RED}Please input player name.")
                        case "on":
                            if(self.handle_activation(sender=sender, action=self.ACTION_ENABLE, value=True) == True):
                                current_time = int(datetime.now().timestamp())
                                if len(args) > 1:
                                    end_value = self.convert_to_integer(args[1])
                                    if(end_value == None):
                                        sender.send_error_message(f"{ColorFormat.RED}Please input numeric only.")
                                        return True
                                    self._maintenance["end_date_time"] = current_time + int(timedelta(hours=end_value).total_seconds())
                                    sender.send_message(f"{ColorFormat.RED}Setting Maintenance for {end_value} hour ahead.")
                                else:
                                    self._maintenance["end_date_time"] = current_time + int(timedelta(hours=1).total_seconds())
                                    sender.send_message(f"{ColorFormat.RED}Setting default Maintenance for 1 hour ahead.")
                                    
                                self._maintenance["start_date_time"] = current_time
                        case "off":
                            self.handle_activation(sender=sender, action=self.ACTION_DISABLE, value=False)
                        case "remove":
                            if len(args) > 1:
                                if self.remove_maintenance_player(args[1].lower()) == True:
                                    sender.send_message(f"{ColorFormat.GREEN}Successfully removed {args[1]} to maintenance players")
                                else:
                                    sender.send_error_message(f"{ColorFormat.RED}Player with gamertag {args[1]} is not exists!")
                            else:
                                sender.send_error_message(f"{ColorFormat.RED}Please input player name.")
                        case _:
                            sender.send_error_message(f"{ColorFormat.RED}There are no maintenance command with name {args[0]}.")
                else:
                    sender.send_error_message(f"{ColorFormat.RED}Usage: /maintenance [args].")
                    return True
        return True
    
    def handle_activation(self, sender: CommandSender, action: str, value: bool) -> bool:
        current_state = self.is_maintenance

        if current_state == value:
            sender.send_error_message(f"{ColorFormat.RED}Server Maintenance was previously {action}")
            return False
        else:
            self._maintenance["is_maintenance"] = value
            if value == False:
                self._maintenance["start_date_time"] = 0
                self._maintenance["end_date_time"] = 0
            sender.send_message(f"{ColorFormat.GREEN}Server Maintenance has been set to {action}.")
        return True

    def convert_to_integer(self, string_value: str) -> int | None:
        try:
            integer_value = int(string_value)
            return integer_value
        except ValueError as err:
            return None
        
    def maintenance_task(self):
        if int(datetime.now().timestamp()) >= self._maintenance["end_date_time"]:
            if self.is_maintenance == False:
                return
            self._maintenance["is_maintenance"] = False

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