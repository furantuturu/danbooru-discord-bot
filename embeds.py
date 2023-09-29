import discord

def main_response_embed(*, json_data, page: int, embed_color: discord.Color) -> discord.Embed:
    embed = discord.Embed(
            colour=embed_color,
            title="Search results:"
        )
    embed.set_thumbnail(url="https://i.ibb.co/ckNDxTD/danbooru-logo-128x128-ea111b6658173e847734.png")
    embed.set_image(url=json_data[page]["file_url"])
    embed.set_author(name=f"ID: {json_data[page]['id']}", url=f"https://danbooru.donmai.us/posts/{json_data[page]['id']}")
    embed.add_field(
        name="General Tags:", 
        value=json_data[page]["tag_string_general"], 
        inline=False
        )
    embed.add_field(
        name="Character Tags:", 
        value=json_data[page]["tag_string_character"].replace("_", "\_"), 
        inline=False)
    embed.add_field(
        name="Origin:", 
        value=json_data[page]["tag_string_copyright"].replace("_", "\_"), 
        inline=False)
    embed.add_field(
        name="Artist:", 
        value=f'{json_data[page]["tag_string_artist"].replace("_", chr(92) + "_")} - https://danbooru.donmai.us/posts?tags={json_data[page]["tag_string_artist"]}', # chr(92) is "\"", bc f-strings doesnt allow "\"
        inline=False)
    
    return embed