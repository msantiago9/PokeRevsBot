import os
import requests
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from random import randint
from secrets import choice

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents, help_command=None)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]["q"] + " -" + data[0]["a"]
    return quote


def get_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    data = json.loads(response.text)
    if data["type"] == "twopart":
        joke = data["setup"] + " " + data["delivery"]
        return joke
    return data["joke"]


@client.command(aliases=["quote", "q"])
async def __remember(ctx):
    await ctx.send(get_quote())


@client.command(aliases=["joke", "j"])
async def __joke(ctx):
    await ctx.send(get_joke())


@client.command(aliases=[""])
async def __nil(ctx):
    await ctx.send("...")


@client.command(aliases=["git", "g", "github", "project", "repo", "repository"])
async def __repo(ctx):
    repo = os.getenv("REPO")
    await ctx.send(repo)


@client.command(aliases=["heroku", "app", "h", "deploy"])
async def __heroku(ctx):
    url = os.getenv("APP")
    await ctx.send(url)


@client.command(aliases=["party"])
async def __party(ctx):
    party_gifs = [
        "https://cdn.discordapp.com/attachments/595772150078767106/910374273288376330/pikachu-dancing.gif",
        "https://cdn.discordapp.com/attachments/595772150078767106/910374273334525962/IncompatibleTautAcaciarat-max-1mb.gif",
        "https://cdn.discordapp.com/attachments/595772150078767106/910374270545309746/dancing-pikachu-gif-11.gif",
    ]
    await ctx.send(choice(party_gifs))


@client.command(aliases=["hello"])
async def __hello(ctx):
    await ctx.send("hi")


@client.command(
    aliases=[
        "goodbye",
        "bye",
        "adios",
        "seeya",
    ]
)
async def __goodbye(ctx):
    await ctx.send(
        "https://cdn.discordapp.com/attachments/595772150078767106/916008659195162704/sad-pikachu.gif"
    )
    await ctx.send("Bye bye...")


@client.command(
    aliases=[
        "emails",
        "e",
        "email",
        "e-mail",
        "gmail",
        "gmails",
        "mail",
        "mails",
        "contact",
        "contacts",
    ]
)
async def __emails(ctx):
    emails = os.getenv("EMAILS")
    await ctx.send(emails)


@client.command(aliases=["help", "commands", "c", "command", "?"])
async def __help(ctx):
    commands = os.getenv("COMMANDS")
    await ctx.send(commands)


@client.command(aliases=["api"])
async def __pokeapi(ctx, *args: list[str]):
    if len(args) == 0:
        await ctx.send("https://pokeapi.co/")
        return
    endpoint = "https://pokeapi.co/api/v2/pokemon/" + args[0]
    response = requests.get(endpoint)
    data = json.loads(response.text)
    if data:
        ability_list = []
        moves = []
        types = []
        for i in range(len(data["abilities"])):
            ability_list.append(data["abilities"][i]["ability"]["name"])
        for i in range(len(data["moves"])):
            moves.append(data["moves"][i]["move"]["name"])
        for i in range(len(data["types"])):
            types.append(data["types"][i]["type"]["name"])

        message = """
        **{}**
        Abilities: {}
        Moves: {}
        Types: {}
        PokeRevs: {}
        """.format(
            data["name"],
            ", ".join(ability_list),
            ", ".join(moves),
            ", ".join(types),
            f"http://pokerevs2.herokuapp.com/pokemon/{data[id]}",
        )

        await ctx.send(data["sprites"]["other"]["official-artwork"]["front_default"])
        await ctx.send(message)
        return
    await ctx.send("No such pokemon: " + args[0])


@client.event
async def on_ready():
    print(f"logged in as {client.user}")


client.run(os.getenv("BOT_TOKEN"))
