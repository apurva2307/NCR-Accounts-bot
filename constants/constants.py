from decouple import config

markup_commands = ["test", "staff", "officer"]
API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"