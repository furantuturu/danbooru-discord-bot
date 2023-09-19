import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

import discord
from discord.ext import commands 
import api

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix=">")

i = 1

@client.event
async def on_ready():
    print(f"{client.user} is now online, ID:{client.user.id}")

@client.command()
async def tags(ctx):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(r=175, g=138, b=101),
        title="Search results:"
    )
    embed.set_thumbnail(url="https://danbooru.donmai.us/packs/static/images/danbooru-logo-128x128-ea111b6658173e847734.png")
    embed.set_image(url=api.json_data[i]["large_file_url"])
    embed.set_author(name=f"ID: {api.json_data[i]['id']}", url=f"https://danbooru.donmai.us/posts/{api.json_data[i]['id']}")
    embed.add_field(name="Tags:", value=api.json_data[i]["tag_string"], inline=False)
    embed.add_field(name="Artist:", value=f"{api.json_data[i]['tag_string_artist']} - https://danbooru.donmai.us/posts?tags={api.json_data[i]['tag_string_artist']}")
    
    await ctx.send(embed=embed)
    
def run_discord():
    client.run(DISCORD_TOKEN)