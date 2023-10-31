import std/[strformat, options, asyncdispatch], chronicles, 
       ../../bridge/bot, dimscord, dimscmd, dimscmd/common,
       mcsrvstatpkg/base

const 
  VirboxMcServer {.strdefine.} = "minecraft.virbos.xyz"
  VirboxMcServerPort {.strdefine.} = "25565"

let server = Server(
  address: VirboxMcServer & ':' & VirboxMcServerPort,
  platform: JAVA
)

proc mcStatus(bot: Bot, m: Message) {.async.} =
  info "[bot/commands/minecraft/status.nim] mcStatus(): getting status!"
  await server.refreshData()
  # let players = server.getPlayers()
  let playerCount = server.playerCount().get()
  let plugins = server.plugins()

  var playerHeader = fmt"{playerCount.online}/{playerCount.max} Online"

  #for player in players:
  #  playerHeader &= '\n' & player.name & " (" & player.uuid & ')'

  var pluginHeader: string
  
  if plugins.isSome:
    for plugin in plugins.get().raw:
      pluginHeader &= '\n' & plugin

  if server.isOnline():
    discard await bot.client.api.sendMessage(
      m.channelId,
      embeds = @[Embed(
        title: some "Minecraft",
        color: some 2,
        description: some server.motd().get().clean[0],
        fields: some @[
          EmbedField(
            name: "**URL:**",
            value: "```" & VirboxMcServer & ':' & VirboxMcServerPort & "```"
          ),
          EmbedField(
            name: "**VERSION:**",
            value: "```" & server.version() & "```"
          ),
          EmbedField(
            name: "**PLAYERS:**",
            value: "```" & playerHeader & "```"
          ),
          EmbedField(
            name: "**PLUGINS:**",
            value: "```" & pluginHeader & "```"
          ),
          EmbedField(
            name: "**PROTOCOL**",
            value: '`' & $server.protocol().get() & '`'
          )
        ]
      )]
    )
  else:
    discard await bot.client.api.sendMessage(
      m.channelId,
      embeds = @[Embed(
        title: some ":x: Cannot connect to server",
        description: some "The Virbox Minecraft server could not be contacted. It is offline."
      )]
    )

proc register*(bot: Bot) =
  info "[bot/commands/minecraft/status.nim] Registering!", address=VirboxMcServer & ':' & VirboxMcServerPort
  bot.handler.addChat("minecraft") do (m: Message, subcmd: string):
    if subcmd == "status":
      await mcStatus(bot, m)
    else:
      error "[bot/commands/minecraft/status.nim] Invalid arguments passed.", subcmd=subcmd
      discard await bot.client.api.sendMessage(
        m.channelId,
        """
:x: Command failed.
```
Usage: v!minecraft <query>

A query can either be "status" or "players"
```
"""
      )
      return
