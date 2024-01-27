# from db.base import endpoints as db
# 
# def add(sponsor, sponsor_id, prefix, endpoint):
#   db.put(data={"sponsor": sponsor, "sponsor_id": str(sponsor_id),  "endpoint": endpoint}, key=prefix)
#  
# def get(prefix):
#   item = db.get(prefix)
#   sponsor = item["sponsor"]
#   sponsor_id = item["sponsor_id"]
#   endpoint = item["endpoint"]
#   return sponsor, int(sponsor_id), endpoint
#   
# def rm(prefix):
#   db.delete(prefix)
#   
# def get_list():
#   items = db.fetch().items
#   results = []
#   for item in items:
#     prefix = item["key"]
#     sponsor = item["sponsor"]
#     result = f"/test{prefix} - **{sponsor}**"
#     results.append(result)
#   return results
#   
# def get_all():
#     items = db.fetch().items
#     return items
#         