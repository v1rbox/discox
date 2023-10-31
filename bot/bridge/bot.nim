import std/[os, osproc, asyncdispatch], 
       dimscord, dimscmd, dimscmd/common, chronicles, taskpools

var tp = Taskpool.new(num_threads=4)

const NimblePkgVersion {.strdefine.} = "???"

type
  Bot* = ref object of RootObj
    client*: DiscordClient
    handler*: CommandHandler

proc onReady*(bot: Bot) =
  info "[bot/bridge/bot.nim] Discox ready! Using v" & NimblePkgVersion 

  discard tp.spawn execCmd("python3 bot")

  info "[bot/bridge/bot.nim] Started Python-side of bot!"

proc onMessage*(bot: Bot, shard: Shard, msg: Message) {.async.} =
  echo '[' & $msg.author & "]: " & msg.content
  discard await bot.handler.handleMessage("v!", shard, msg)

proc run*(bot: Bot) =
  waitFor bot.client.startSession()

proc newBot*: Bot =
  var bot = Bot()
  
  assert existsEnv("DISCOX_TOKEN"), "No token exists! (export DISCOX_TOKEN!)"
  bot.client = newDiscordClient(getEnv("DISCOX_TOKEN"))
  bot.handler = bot.client.newHandler()

  bot
