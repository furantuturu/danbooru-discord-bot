import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
KEY = os.getenv("API_KEY")

import discord
from discord.ext import commands 
import urllib.parse
import requests

api_posts = "https://danbooru.donmai.us/posts.json?"
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix=">")

i = 0 # paging purpose

@client.event
async def on_ready():
    print(f"{client.user} is now online, ID:{client.user.id}")

@client.command()
async def tags(ctx, tag_args):
    tags = tag_args
    url = api_posts + urllib.parse.urlencode({"tags": tags, "key": KEY})
    json_data = requests.get(url).json()
    print(url)
    print(json_data[0]["id"])
    
    embed = discord.Embed(
        colour=discord.Color.from_rgb(r=175, g=138, b=101),
        title="Search results:"
    )
    embed.set_thumbnail(url="https://i.ibb.co/ckNDxTD/danbooru-logo-128x128-ea111b6658173e847734.png")
    embed.set_image(url=json_data[i]["file_url"])
    embed.set_author(name=f"ID: {json_data[i]['id']}", url=f"https://danbooru.donmai.us/posts/{json_data[i]['id']}")
    embed.add_field(name="General Tags:", value=json_data[i]["tag_string_general"], inline=False)
    embed.add_field(name="Character Tags:", value=json_data[i]["tag_string_character"])
    embed.add_field(name="Game/Anime/Franchise:", value=json_data[i]["tag_string_copyright"])
    embed.add_field(name="Artist:", value=f"{json_data[i]['tag_string_artist']} - https://danbooru.donmai.us/posts?tags={json_data[i]['tag_string_artist']}", inline=False)
    
    await ctx.send(embed=embed)
    
def run_discord():
    client.run(DISCORD_TOKEN)