import os
import sys

import discord
from pyngrok import ngrok, conf, installer


def install_ngrok(path):
    import ssl
    # https://github.com/alexdlaird/pyngrok/issues/93#issuecomment-945019968
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    installer.install_ngrok(path, context=ctx)


def start_ngrok(port, protocol):
    ngrok_path = conf.get_default().ngrok_path
    if not os.path.exists(ngrok_path):
        install_ngrok(ngrok_path)
    ngrok.set_auth_token(os.environ["NGROK_AUTH_TOKEN"])
    public_url = ngrok.connect(port, protocol).public_url
    return public_url.replace(f"{protocol}://", "")


if __name__ == "__main__":
    ngrok_port = int(
        (sys.argv[1] if len(sys.argv) > 1 else None)
        or os.getenv("ROK_PORT")
        or 25565
    )
    ngrok_protocol = sys.argv[2] if len(sys.argv) > 2 else "tcp"
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        guild = client.get_guild(int(os.environ["ROK_DISCORD_GUILD_ID"]))
        channel = guild.get_channel(int(os.environ["ROK_DISCORD_CHANNEL_ID"]))
        address = start_ngrok(ngrok_port, ngrok_protocol)
        await channel.send(embed=discord.Embed(
            title="Server is up!",
            description=address,
        ))

    client.run(os.getenv("ROK_DISCORD_BOT_TOKEN"))
