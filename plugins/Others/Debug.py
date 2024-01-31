from hydrogram import Client, filters
from hydrogram.enums import ParseMode

@Client.on_message(filters.command("debug"))
def debugger(c,m):
  m.reply(f"<blockquote>{m}</blockquote>", parse_mode=ParseMode.HTML)