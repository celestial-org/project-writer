import os

admin = os.getenv("ADMIN_ID", "5665225938")
if admin.isdigit():
    if not admin.startswith("0"):
        admin = int(admin)
