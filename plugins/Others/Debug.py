from hydrogram import Client, filters

@Client.on_message(filters.command("debug"))
def debugger(c,m):
  m.reply(f"```json\n{m}\n```")