from supabase import create_client, Client
import os
from dotenv import load_dotenv


# Load env vars
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
