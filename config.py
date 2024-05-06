import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
QUALYS_API_URL = "https://api.recruiting.app.silk.security/api/qualys/hosts/get/"
CROWDSTRIKE_API_URL = "https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get/"
MONGODB_URI = "mongodb://localhost:27017/"
