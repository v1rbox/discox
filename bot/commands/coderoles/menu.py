from discord import Color

from bot.base import Command, RoleView
from bot.config import Config, Embed


class CodeRoles(RoleView):
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
        "Clojure",
        "Crystal",
        "COBOL",
        "CoffeeScript",
        "D",
        "Dart",
        "Elixir",
        "Elvish",
        "Erlang",
        "F#",
        "Fortran",
        "GDScript",
        "Go",
        "Groovy",
        "Haskell",
        "Haxe",
        "Holy C",
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
        "Nim",
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
        "Scheme",
        "Shell",
        "Solidity",
        "Swift",
        "SQL",
        "TCL",
        "TeX",
        "Typescript",
        "Vala",
        "VBA",
        "XSLT",
        "YaBasic",
        "Zig",
    ]


class cmd(Command):
    """A discord command instance."""

    name = "menu"
    usage = "menu"
    description = f"Code Roles Menu"

    async def execute(self, arguments, message) -> None:
        code = CodeRoles(message)
        await message.channel.send(embed=code.default_embed, view=code)
