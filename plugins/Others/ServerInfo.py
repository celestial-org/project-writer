from hydrogram import Client, filters
import platform, requests


def server_info():
    try:
        # Sử dụng ipinfo.io để lấy thông tin về địa chỉ IP
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Trích xuất thông tin từ dữ liệu JSON
        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        provider = data.get("org", "N/A")

        server_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nProvider: {provider}"

    except Exception as e:
        server_info = f"Error: {e}"

    return server_info


@Client.on_message(filters.command("info"))
def bot_server_info(c, m):
    ver = platform.version()
    name = platform.uname()
    system = platform.system()
    server = server_info()
    msg_text = (
        f"```{system}\n" f"INFO:\n{name}\n\n" f"VERSION:\n{ver}\n\n" f"{server}\n" "```"
    )

    m.reply(msg_text)
