from discord import Color

from bot.base import Command, Roles
from bot.config import Config, Embed

class CodeRoles(Roles):
    max = 5
    role_color = Color.from_rgb(137, 204, 240)
    prefix = "code"
    whitelist = [
            "Ada",
            "Assembly",
            "APL",
            "Basic",
            "Brainfuck",
            "C",
            "C++",
            "C#",
            "Dart",
            "F#",
            "Fortran",
            "Go",
            "Groovy",
            "Haskell",
            "HTML/CSS",
            "IDL",
            "Java",
            "Javascript",
            "Julia",
            "Kotlin",
            "Lisp",
            "Lua",
            "Lustre",
            "MATLAB",
            "NXC",
            "Objective-C",
            "OCaml",
            "Pascal",
            "PHP",
            "Python",
            "Perl",
            "QML",
            "R",
            "Ruby",
            "Rust",
            "Scala",
            "Shell",
            "Solidity",
            "Swift",
            "SQL",
            "TeX",
            "Typescript",
            "VBA",
            "XSLT",
            "YaBasic",
            "Zig",
            ] 
            
class cmd(Command):
    """A discord command instance."""

    name = "add"
    usage = "add <language>"
    description = f"Assigns user a role based on selected language, max of {CodeRoles.max} code roles per user."

    async def execute(self, arguments, message) -> None:
        coderoles = CodeRoles()
        embed = Embed(
                title="Code",
                description=await coderoles.addRole(message, arguments[0])
                )
        await message.channel.send(embed=embed) 
