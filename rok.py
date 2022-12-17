import os

import discord
from pyngrok import ngrok


def start_ngrok():
    ngrok.set_auth_token(os.environ["NGROK_AUTH_TOKEN"])
    public_url = ngrok.connect(os.environ["GTNH_PORT"] or 25565, "tcp").public_url
    return public_url.replace("tcp://", "")


if __name__ == "__main__":
    client = discord.Client(intents=discord.Intents.default())


    @client.event
    async def on_ready():
        guild = client.get_guild(int(os.environ["DISCORD_GUILD_ID"]))
        channel = guild.get_channel(int(os.environ["DISCORD_CHANNEL_ID"]))
        address = start_ngrok()
        await channel.send(embed=discord.Embed(
            title="Server is up!",
            description=address,
        ))


    client.run(os.getenv('ROK_DISCORD_BOT_TOKEN'))
