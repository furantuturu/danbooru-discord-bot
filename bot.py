import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

import discord
from discord import app_commands
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

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception:
        print(Exception)

@client.command()
async def fetchbooru(ctx, *, tag_args: str):
    try:
        tags = tag_args + " rating:general"
        url = api_posts + urllib.parse.urlencode({"tags": tags})
        json_data = requests.get(url).json()
        print(url)
        print(json_data[i]["id"])
        
        embed = discord.Embed(
            colour=discord.Color.from_rgb(r=175, g=138, b=101),
            title="Search results:"
        )
        embed.set_thumbnail(url="https://i.ibb.co/ckNDxTD/danbooru-logo-128x128-ea111b6658173e847734.png")
        embed.set_image(url=json_data[i]["file_url"])
        embed.set_author(name=f"ID: {json_data[i]['id']}", url=f"https://danbooru.donmai.us/posts/{json_data[i]['id']}")
        embed.add_field(
            name="General Tags:", 
            value=json_data[i]["tag_string_general"], 
            inline=False
            )
        embed.add_field(
            name="Character Tags:", 
            value=json_data[i]["tag_string_character"].replace("_", "\_"), 
            inline=False)
        embed.add_field(
            name="Origin:", 
            value=json_data[i]["tag_string_copyright"].replace("_", "\_"), 
            inline=False)
        embed.add_field(
            name="Artist:", 
            value=f'{json_data[i]["tag_string_artist"].replace("_", chr(92) + "_")} - https://danbooru.donmai.us/posts?tags={json_data[i]["tag_string_artist"]}', # chr(92) is "\"", bc f-strings doesnt allow "\"
            inline=False)
        
        await ctx.send(embed=embed)
        
    except KeyError:
        err_embed = discord.Embed(
            colour=discord.Color.from_rgb(r=175, g=138, b=101),
            description="⚠️ You cannot search for more than 2 tags at a time."
        )
        
        await ctx.send(embed=err_embed)

@client.tree.command(name="fetchbooru", description="Fetch an art/image with the 2 tags of your choice")
@app_commands.describe(tag1="Enter a danbooru valid tag")        
@app_commands.describe(tag2="Enter a danbooru valid tag")        
async def fetchbooru(interaction: discord.Interaction, tag1: str, tag2: str):
    await interaction.response.send_message(f"Your tags: {tag1}, {tag2} ")

def run_discord():
    client.run(DISCORD_TOKEN)