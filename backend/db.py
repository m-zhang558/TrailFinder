import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('API_KEY')


url: str = os.environ.get(supabase_url)
key: str = os.environ.get(supabase_key)
supabase: Client = create_client(url, key)

