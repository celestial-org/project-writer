from hydrogram import Client, filters
import platform
import requests


async def server_info():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        provider = data.get("org", "N/A")

        server_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nProvider: {provider}"

    except Exception as e:
        server_info = f"Error: {e}"

    return server_info


@Client.on_message(filters.command("server"))
async def bot_server_info(c, m):
    ver = platform.version()
    name = platform.uname()
    system = platform.system()
    server = await server_info()
    msg_text = (f"```{system}\n"
                f"INFO:\n{name}\n\n"
                f"VERSION:\n{ver}\n\n"
                f"{server}\n"
                "```")

    await m.reply(msg_text, quote=True)
