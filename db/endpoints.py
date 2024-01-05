from db.base import endpoints as db

def add(sponsor, prefix, endpoint):
  db.put(data={"sponsor": sponsor, "endpoint": endpoint}, key=prefix)
 
def get(prefix):
  item = get(prefix)
  sponsor = item["sponsor"]
  endpoint = item["endpoint"]
  return sponsor, endpoint
  
def get_list():
  items = db.fetch().items
  results = []
  for item in items:
    prefix = item["prefix"]
    sponsor = item["sponsor"]
    result = f"`{prefix}` - **{sponsor}**"
    results.append(result)
  return results