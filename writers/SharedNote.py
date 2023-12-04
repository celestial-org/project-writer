import os, re, time
from pyrogram import Client, filters, idle, enums
from database import save_url, remove_url, get_all, check_all

v2tool = os.getenv('V2TOOL')


@Client.on_message(filters.command("share"))
def add_url(c, m):
  text = m.text
  if m.reply_to_message:
    text = m.reply_to_message.text
  urls = re.findall(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
      text)
  if not urls:
    err = m.reply_text("Vui lòng cung cấp URL")
    time.sleep(10)
    c.delete_messages(m.chat.id, err.id)
    m.delete()
    return
  for url in urls:
    try:
      save_url("share", url)
    except Exception as e:
      err = m.reply_text(f'Error: {e}')
      time.sleep(5)
      c.delete_messages(m.chat.id, err.id)
      m.delete()
  done = m.reply_text(f'Đã thêm {len(urls)} URL')
  time.sleep(10)
  c.delete_messages(m.chat.id, done.id)
  m.delete()


@Client.on_message(filters.command("unshare"))
def delete_url(c, m):
  text = m.text
  if m.reply_to_message:
    text = m.reply_to_message.text
  urls = re.findall(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
      text)
  if not urls:
    err = m.reply_text("Vui lòng cung cấp URL")
    time.sleep(10)
    c.delete_messages(m.chat.id, err.id)
    m.delete()
    return
  for url in urls:
    worked = False
    try:
      remove_url("share", url)
      worked = True
    except Exception as e:
      err = m.reply_text(f'Error: {e}')
      time.sleep(10)
      c.delete_messages(m.chat.id, err.id)
  if worked == True:
    done = m.reply_text(f'Đã xoá {len(urls)} URL')
    time.sleep(10)
    c.delete_messages(m.chat.id, done.id)
  m.delete()


@Client.on_message(filters.command("checkshare"))
def check_all_urls(c, m):
  if m.from_user.id != 5665225938:
    m.reply('`Forbidden`', quote=True)
    return
  try:
    removed_urls = check_all("share")
    if removed_urls:
      removed_urls_str = '\n'.join(removed_urls)
      m.reply_text(f' Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}')
    else:
      err = m.reply_text('No URLs were removed')
      time.sleep(10)
      c.delete_messages(m.chat.id, err.id)
  except Exception as e:
    err = m.reply_text(f'Error: {e}')
    time.sleep(10)
    c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("sharelist"))
def get_all_urls(c, m):
  if m.from_user.id != 5665225938:
    m.reply("`Forbidden`", quote=True)
    return
  try:
    urls = get_all("share")
    if urls:
      urls_str = '\n'.join(urls)
      m.reply_text(f'Tìm thấy {len(urls)} URL:\n{urls_str}')
    else:
      err = m.reply_text('No URLs found')
      time.sleep(10)
      c.delete_messages(m.chat.id, err.id)
  except Exception as e:
    err = m.reply_text(f'Error: {e}')
    time.sleep(10)
    c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("shared"))
def get_urls(c, m):
  config_url = f"{v2tool}/config/share"
  m.reply_text(f"Liên kết chứa cấu hình được chia sẻ là:\n\n{v2tool}/config/share")
