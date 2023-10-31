import chronicles, asyncdispatch, bridge/bot, dimscord,
       commands/minecraft/status

proc main {.inline.} =
  let bot = newBot()
  let discord = bot.client

  proc onReady(s: Shard, r: Ready) {.event(discord).} =
    bot.onReady()

  proc messageCreate(s: Shard, msg: Message) {.event(discord).} =
    await bot.onMessage(s, msg)
  
  status.register(bot)
  bot.run()

when isMainModule:
  main()
