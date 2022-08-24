import random
import string

def generate_wallet_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(8)) + "-" + ''.join(random.choice(characters) for i in range(4)) + "-" + \
        ''.join(random.choice(characters) for i in range(4)) + "-" + ''.join(random.choice(characters) for i in range(12))

def generate_response(data: dict, success: bool):
    return dict(
        data=data,
        status="Success" if success else "Failed"
    )
