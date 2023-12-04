import requests, os
from deta import Deta

deta = Deta(os.getenv("DETA_KEY"))
db = deta.Base("v2ray-notes")


class DatabaseNotFoundError(Exception):
  pass


class UrlNotFoundError(Exception):
  pass


class UrlExistsError(Exception):
  pass


def save_url(filename, url):
  existing_entry = db.get(filename)
  if existing_entry:
    if url not in existing_entry['urls']:
      db.update({'urls': existing_entry['urls'] + [url]}, filename)
    else:
      raise UrlExistsError("Url đã tồn tại")
  else:
    db.put({'key': filename, 'urls': [url]})


def remove_url(filename, url):
  existing_entry = db.get(filename)
  if existing_entry:
    if url in existing_entry['urls']:
      updated_urls = [u for u in existing_entry['urls'] if u != url]
      db.update({'urls': updated_urls}, filename)
    else:
      raise UrlNotFoundError("URL không tồn tại trong kho lưu trữ")
  else:
    raise DatabaseNotFoundError("Không tìm thấy dữ liệu")


def get_all(filename):
  existing_entry = db.get(filename)
  if existing_entry:
    urls = existing_entry['urls']
    return urls
  else:
    raise DatabaseNotFoundError("Không tìm thấy dữ liệu")


def check_all(filename):
  existing_entry = db.get(filename)
  if existing_entry:
    removed_urls = []
    for url in existing_entry['urls']:
      response = requests.get(f"https://convert.v2ray-subscribe.workers.dev/?url={url}")
      if response.status_code != 200:
          removed_urls.append(url)
    updated_urls = [u for u in existing_entry['urls'] if u not in removed_urls]
    db.update({'urls': updated_urls}, filename)
    return removed_urls
  else:
    raise DatabaseNotFoundError("Không tìm thấy dữ liệu")
