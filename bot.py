import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

import discord
from discord import app_commands
from discord.ext import commands

import urllib.parse
import requests

import embeds

api_posts = "https://danbooru.donmai.us/posts.json?"
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix=">")

# color(s)
embed_color = discord.Color.from_rgb(r=175, g=138, b=101)

# error msg
key_err_msg = "⚠️ I don't own a premium account. You cannot search for more than 2 tags at a time."
ind_err_msg = "⚠️ Either it contains explicit content or it doesn't exist."

# paging purpose
i = 0 

@client.event
async def on_ready():
    print(f"{client.user} is now online, ID:{client.user.id}")

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception:
        print(Exception)

@client.command()
async def fetchbooru(ctx, *, tags: str):
    try:
        tag_args = tags + " rating:general"
        url = api_posts + urllib.parse.urlencode({"tags": tag_args})
        json_data = requests.get(url).json()
        print(url)
        print(json_data[i]["id"])
        
        embed = embeds.main_response_embed(json_data=json_data, page=i, embed_color=embed_color)
        
        await ctx.send(embed=embed)
        
    except KeyError:
        err_embed = discord.Embed(
            colour=embed_color,
            description=key_err_msg
        )
        
        await ctx.send(embed=err_embed)

    except IndexError:
        err_embed = discord.Embed(
            colour=embed_color,
            description=ind_err_msg
        )
        
        await ctx.send(embed=err_embed)
        
@client.tree.command(name="fetchbooru", description="Fetch an art/image with the 2 tags of your choice")
@app_commands.describe(tags="Enter a danbooru valid format tags, separated by space")        
async def fetchbooru(interaction: discord.Interaction, tags: str):
    try:
        tag_args = tags + " rating:general"
        url = api_posts + urllib.parse.urlencode({"tags": tag_args})
        json_data = requests.get(url).json()
        print(url)
        print(json_data[i]["id"])
        
        embed = embeds.main_response_embed(json_data=json_data, page=i, embed_color=embed_color)
        
        await interaction.response.send_message(embed=embed)
        
    except KeyError:
        err_embed = discord.Embed(
            colour=embed_color,
            description=key_err_msg
        )
        
        await interaction.response.send_message(embed=err_embed)

    except IndexError:
        err_embed = discord.Embed(
            colour=embed_color,
            description=ind_err_msg
        )
        
        await interaction.response.send_message(embed=err_embed)

def run_discord():
    client.run(DISCORD_TOKEN)