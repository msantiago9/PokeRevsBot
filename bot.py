import os
import secrets
import requests
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
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
async def __pokeapi(ctx, *args):
    if len(args) == 0:
        await ctx.send("https://pokeapi.co/")
        return

    channel = ctx.message.channel
    e1 = "https://pokeapi.co/api/v2/pokemon/" + ''.join(str(args[0]))
    e2 = "https://pokeapi.co/api/v2/pokemon-species/" + ''.join(str(args[0]))
    response = requests.get(e1)
    response2 = requests.get(e2)
    data = json.loads(response.text)
    data2 = json.loads(response2.text)
    if data and data2:
        ability_list = []
        types = []
        flavor_texts = []
        hit = False
        for i in range(len(data["abilities"])):
            ability_list.append(data["abilities"][i]["ability"]["name"])
        for i in range(len(data["types"])):
            types.append(data["types"][i]["type"]["name"])
        for i in range(len(data2['flavor_text_entries'])):
            if data2['flavor_text_entries'][i]['language']['name'] == 'en':
                flavor_texts.append(
                    data2['flavor_text_entries'][i]['flavor_text'])
                hit = True

        flavor_text = secrets.choice(flavor_texts) if hit else ""
        img = data["sprites"]["other"]["official-artwork"]["front_default"]
        sprite = data["sprites"]["other"]["front_default"]

        message = discord.Embed(
            title=data["name"],
            description=flavor_text,
            colour=discord.Colour.blue(),
            url="http://pokerevs2.herokuapp.com/pokemon/{data['id']}"
        )

        message.set_footer("Powered by PokeRevs")
        message.set_thumbnail(url=sprite)
        message.set_image(url=img)
        message.add_field(name='Types', value=', '.join(types), inline=False)
        message.add_field(name='Abilities', value=', '.join(
            ability_list), inline=True)
        message.set_author(name="PokeRevs Customer Support", url="https://github.com/msantiago9/PokeRevsBot/",
                           icon_url="https://cdn.discordapp.com/avatars/905312596683522058/f4f3176be9aa627c59d475afa16c2420.png")

        await client.send_message(channel, embed=message)


@client.event
async def on_ready():
    print(f"logged in as {client.user}")


client.run(os.getenv("BOT_TOKEN"))
