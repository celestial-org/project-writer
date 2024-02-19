from hydrogram import Client, filters
from io import BytesIO
import requests

@Client.on_message(filters.command("image"))
def image_generator(c, m):
    if len(m.command) > 1:
        query = m.text.split(m.command[0])[1]
        response = requests.get("https://diffusion.cloudlapse.workers.dev/", params=dict(q=query))
        if m.from_user:
            name = m.from_user.first_name
        else:
            name = "Channel/Group"
        if response.status_code == 200:
            result = BytesIO(response.content)
            result.name = "image.png"
            m.reply_photo(result, caption=f"By __**{name}**__", quote=True)