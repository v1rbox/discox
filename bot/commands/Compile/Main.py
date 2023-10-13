from bot.base import Command

import discord
import subprocess

async def compile_command(ctx, *args, **kwargs):
  """Compiles the given code and returns the output.

  Args:
    *args: A list of positional arguments.
    **kwargs: A dictionary of keyword arguments.
  """

  # Get the code to compile.
  code = " ".join(args)

  # Get the compiler flags.
  compiler_flags = kwargs["compiler_flags"]

  # Compile the code.
  output = subprocess.check_output(["python", "-c", code] + compiler_flags)

  # Send the output to the user.
  await ctx.send(output.decode())

# Register the compile command.
discord.Client.command()(compile_command)
