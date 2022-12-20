import os
import sys

import discord
from pyngrok import ngrok, conf, installer
from mcstatus import JavaServer
import base64
import tempfile

from config import Config


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
    ngrok.set_auth_token(Config.ngrok_auth_token)
    public_url = ngrok.connect(port, protocol).public_url
    return public_url.replace(f"{protocol}://", "")


if __name__ == "__main__":
    ngrok_port = int(
        (sys.argv[1] if len(sys.argv) > 1 else None)
        or Config.ngrok_port
    )
    ngrok_protocol = sys.argv[2] if len(sys.argv) > 2 else "tcp"

    client = discord.Client(intents=discord.Intents.default())


    @client.event
    async def on_ready():
        address = start_ngrok(ngrok_port, ngrok_protocol)
        address = Config.address_handler(address)

        guild = client.get_guild(Config.discord_guild_id)
        channel = guild.get_channel(Config.discord_channel_id)

        status = JavaServer.lookup(f"127.0.0.1:{ngrok_port}").status()
        embed = discord.Embed(
            title="Minecraft server is up!",
            description=f"{status.description} on {status.version.name}\nAddress: **{address}**",
        )

        file = None
        if status.favicon:
            # decode b64 and write to a tmp file
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file.write(base64.b64decode(status.favicon.split(",")[1].replace("\n", "")))
            tmp_file.flush()
            embed = embed.set_thumbnail(url="attachment://favicon.jpeg")
            # create a discord file from the tmp file
            file = discord.File(filename="favicon.jpeg", fp=tmp_file.name)

        await channel.send(embed=embed, file=file)


    client.run(Config.discord_bot_token)
