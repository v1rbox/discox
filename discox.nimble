# Package

version       = "0.1.0"
author        = "xTrayambak"
description   = "Virbox Discord Bot community project ^_^"
license       = "AGPL-3.0-only"

# Dependencies

requires "nim >= 1.6.14"
requires "dimscord"
requires "dimscmd"
requires "mcsrvstat.nim"
requires "chronicles"

task buildBinary, "Build the Nim binary":
  exec "nim c -o:init bot/nimbot.nim"

task buildRelease, "Release mode":
  exec "nim c -d:release -o:init bot/nimbot.nim"
  exec "strip ./init"
