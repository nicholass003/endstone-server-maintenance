## ServerMaintenance

Simple server maintenance manager for survival Endstone servers.

### Warning
This was developed using 0.4.6 endstone dev build.
Consider using this on [development wheel of endstone](https://github.com/EndstoneMC/endstone/actions/workflows/wheel.yml)

## Commands
`/maintenance [args]`

Aliases: `/mtc`

Enable or Disable server maintenance.

## SubCommands
`/maintenance add [text: string]`

Add player name to allow joining server during maintenance.


`/maintenance on [text: string]`

Enable server maintenance, default 1 hours. The text must be numbers.

`/maintenance off`

Disable server maintenance.

`/maintenance remove [text: string]`

Remove player name to disallow joining server during maintenance.

## Requirements
- [Endstone 0.4.6 dev build or higher](https://github.com/EndstoneMC/endstone)