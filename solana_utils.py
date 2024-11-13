import time
import base58
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.core import RPCException

# Connect to the Solana cluster
# solana_client = Client("https://api.mainnet-beta.solana.com")
solana_client = Client("https://api.testnet.solana.com")

def is_valid_solana_address(address):
    """Check if the address is of valid length (44 characters) and is in Base58."""
    return isinstance(address, str) and len(address) == 44 and all(c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" for c in address)

def is_valid_private_key(private_key):
    """Check if the provided private key is valid (Base58 encoded and 64 bytes long when decoded)."""
    try:
        decoded = base58.b58decode(private_key)
        return (len(decoded) == 64) and all(c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" for c in private_key)
    except Exception:
        return False

def get_user_wallet_info(db, user_id):
    """Get wallet information for the user."""
    user_data = db.get_user(user_id)

    if not user_data:
        # Create a new wallet if none exists
        wallet_address, private_key, private_key_list = create_new_wallet()  # Get both public and private keys
        
        db.add_user(user_id, {"address": wallet_address, "private_key": private_key, "private_key_list": private_key_list, "sol_balance": 0, "usdt_balance": 0})
        return {"address": wallet_address, "private_key": private_key, "private_key_list": private_key_list, "sol_balance": 0, "usdt_balance": 0}  # Return the new wallet info

    # Fetch balance details
    address = user_data['wallet_info']['address']

    if not is_valid_solana_address(address):
        print(f"Invalid wallet address: {address}")
        return {"address": address, "sol_balance": 0, "usdt_balance": 0}  # Handle invalid address

    for attempt in range(3):
        try:
            response = solana_client.get_balance(Pubkey.from_string(address))
            sol_balance = response.value  # Access the value directly from the response object
            break
        except RPCException as e:
            print(f"Error fetching SOL balance: {e}")
            time.sleep(2)
            sol_balance = 0  # Default to 0 if there's an error

    # Placeholder for USDT balance (real implementation would require a separate API call)
    usdt_balance = 0  # Replace with actual logic to fetch USDT balance

    return {"address": address, "sol_balance": sol_balance, "usdt_balance": usdt_balance}

def create_new_wallet():
    """Create and return a new Solana wallet with its public and private keys."""
    
    while True:
        # Create a new keypair which generates public/private key pair
        new_keypair = Keypair()  # Use generate() to create a new keypair
        
        # Get the public key as a string
        public_key = str(new_keypair.pubkey())
        
        # Get the private key as bytes
        private_key_bytes = new_keypair.secret()
        
        # Convert the private key to a Base58 string directly from bytes
        private_key = base58.b58encode(private_key_bytes.hex()).decode('ascii')
        
        private_key_list = str(list(private_key_bytes + base58.b58decode(public_key))).replace(" ","")
        # Validate the generated keys
        print(public_key, " / ", private_key)
        if is_valid_solana_address(public_key) and is_valid_private_key(private_key):
            return public_key, private_key, private_key_list  # Return both keys only if they are valid

# Example usage of get_user_wallet_info function (assuming db is defined)
# user_info = get_user_wallet_info(db, user_id)
# print(user_info)
