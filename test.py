import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey

def create_solana_wallet():
    """Create and return a new Solana wallet with its public and private keys."""
    
    # Generate a new keypair
    keypair = Keypair()
    
    # Get the public key (wallet address)
    public_key = str(keypair.pubkey())
    
    # Get the private key as bytes (this includes both public and private key)
    private_key_bytes = keypair.secret()  # This returns a 64-byte array

    print(public_key)
    print(list(base58.b58decode(public_key)))
    print(private_key_bytes.hex())
    
    # Convert the private key bytes to a list of integers
    private_key_list = list(private_key_bytes)
    print(private_key_list)  # Print the private key in the desired format

    print(str(list(base58.b58decode(public_key) + private_key_bytes)).replace(" ",""))

    # Convert the private key to a Base58 string
    private_key = base58.b58encode(private_key_bytes.hex()).decode('ascii')
    
    print(private_key)

    return public_key, private_key

def is_valid_solana_address(address):
    """Check if the provided address is a valid Solana address."""
    try:
        Pubkey.from_string(address)
        return True
    except ValueError:
        return False

def is_valid_private_key(private_key):
    """Check if the provided private key is valid (Base58 encoded and 64 bytes long when decoded)."""
    try:
        decoded = base58.b58decode(private_key)
        return len(decoded) == 64
    except Exception as e:
        print(f"Error in validating private key: {e}")
        return False

# Generate and validate a new wallet
public_key, private_key = create_solana_wallet()

print(f"Public Key (Wallet Address): {public_key}")
print(f"Private Key: {private_key}")
print(f"Public Key is valid: {is_valid_solana_address(public_key)}")
print(f"Private Key is valid: {is_valid_private_key(private_key)}")