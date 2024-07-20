import os
import requests
from pymongo import MongoClient

mongo_url = os.getenv("MONGO_URL")


class DatabaseNotFoundError(Exception):
    pass


class UrlNotFoundError(Exception):
    pass


class UrlExistsError(Exception):
    pass


class NotesDB:

    def __init__(self):
        self.client = MongoClient(mongo_url)
        self.db = self.client.mo9973_notes
        self.collection = self.db.notes

    def add(self, note_name: str, url: str):
        existing_entry = self.collection.find_one({"_id": note_name})
        if existing_entry:
            if url not in existing_entry["urls"]:
                self.collection.update_one({"_id": note_name}, {"$push": {"urls": url}})
            else:
                raise UrlExistsError("Url đã tồn tại")
        else:
            self.collection.insert_one({"_id": note_name, "urls": [url]})

    def remove(self, note_name: str, url: str):
        existing_entry = self.collection.find_one({"_id": note_name})
        if existing_entry:
            if url in existing_entry["urls"]:
                updated_urls = [u for u in existing_entry["urls"] if u != url]
                self.collection.update_one(
                    {"_id": note_name}, {"$set": {"urls": updated_urls}}
                )
            else:
                raise UrlNotFoundError("URL không tồn tại trong kho lưu trữ")
        else:
            raise DatabaseNotFoundError("Không tìm thấy dữ liệu")

    def all(self, note_name: str):
        existing_entry = self.collection.find_one({"_id": note_name})
        if existing_entry:
            return existing_entry["urls"]
        else:
            raise DatabaseNotFoundError("Không tìm thấy dữ liệu")

    def check(self, note_name: str):
        existing_entry = self.collection.find_one({"_id": note_name})
        if existing_entry:
            removed_urls = []
            for url in existing_entry["urls"]:
                try:
                    response = requests.get(
                        url,
                        headers={"User-Agent": "v2rayNG"},
                        proxies={
                            "http": "http://127.0.0.1:6868",
                            "https": "http://127.0.0.1:6868",
                        },
                        timeout=60,
                    )
                except Exception as e:
                    print(e)
                    removed_urls.append(url)
                    continue
                if (
                    response.status_code != 200
                    or response.text is None
                    or "{" in response.text
                ):
                    removed_urls.append(url)
            updated_urls = [u for u in existing_entry["urls"] if u not in removed_urls]
            self.collection.update_one(
                {"_id": note_name}, {"$set": {"urls": updated_urls}}
            )
            return removed_urls
        else:
            raise DatabaseNotFoundError("Không tìm thấy dữ liệu")
