import os
import requests
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents, help_command=None)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]['q'] + " -" + data[0]['a']
    return quote


@client.command(aliases=['quote', 'q'])
async def __remember(ctx):
    await ctx.send(get_quote())


@client.command(aliases=[''])
async def __nil(ctx):
    await ctx.send("...")


@client.command(aliases=['git', 'g', 'github', 'project', 'repo', 'repository'])
async def __repo(ctx):
    repo = os.getenv('REPO')
    await ctx.send(repo)


@client.command(aliases=['heroku', 'app', 'h', 'deploy'])
async def __heroku(ctx):
    url = os.getenv('APP')
    await ctx.send(url)


@client.command(aliases=['emails', 'e', 'email', 'e-mail', 'gmail', 'gmails', 'mail', 'mails', 'contact', 'contacts'])
async def __emails(ctx):
    emails = os.getenv('EMAILS')
    await ctx.send(emails)


@client.command(aliases=['help', 'commands', 'c', 'command', '?'])
async def __help(ctx):
    commands = os.getenv('COMMANDS')
    await ctx.send(commands)


@client.event
async def on_ready():
    print(f"logged in as {client.user}")

client.run(os.getenv('BOT_TOKEN'))
