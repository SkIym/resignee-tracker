from supabase import create_client, Client
import os

url = "https://zhrfmtjpzjkxgtpvwnpk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpocmZtdGpwempreGd0cHZ3bnBrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk1MzMzMDMsImV4cCI6MjA2NTEwOTMwM30.XudJqgXr8iHyRZ8QDRCywE84wJjYGZwaxRVEn9tr0VA"

supabase: Client = create_client(url, key)
