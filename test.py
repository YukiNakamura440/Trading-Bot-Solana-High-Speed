import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if the environment variables are being read correctly
print(f'MONGO_URI: {os.getenv("MONGO_URI")}')
print(f'DB_NAME: {os.getenv("DB_NAME")}')
print(f'SOLANA_RPC_URL: {os.getenv("SOLANA_RPC_URL")}')