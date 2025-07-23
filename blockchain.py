import hashlib, time, json, os

class Blockchain:
    def __init__(self, data_file='chain.json'):
        self.data_file = data_file
        self.tokens_mined = 0
        self.current_tx = []
        self.chain = self.load_chain() or []
        if not self.chain:
            self.new_block(prev_hash='1', proof=100)

    def save_chain(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.chain, f)

    def load_chain(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return None

    def new_block(self, proof, prev_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_tx,
            'proof': proof,
            'previous_hash': prev_hash or self.hash(self.chain[-1])
        }
        self.current_tx = []
        self.chain.append(block)
        self.save_chain()
        return block

    def new_tx(self, sender, recipient, amount):
        self.current_tx.append({'sender': sender, 'recipient': recipient, 'amount': amount})
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.hash({'last_proof': last_proof, 'proof': proof})[:4] != "0000":
            proof += 1
        return proof

    def mine_token(self, recipient, reward=1):
        self.tokens_mined += reward
        self.new_tx('0', recipient, reward)
        self.new_block(self.proof_of_work(self.last_block['proof']))
        return True

class UserManager:
    def __init__(self, user_file='users.json'):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f)

    def register_user(self, username, password, role="miner"):
        if username in self.users:
            return False
        # Store password hash for security (simple sha256 hash)
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {
            "password_hash": pw_hash,
            "role": role,
            "wallet": f"wallet_{username}",
            "balance": 0
        }
        self.save_users()
        return True

    def verify_user(self, username, password):
        user = self.users.get(username)
        if not user:
            return False
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        return pw_hash == user['password_hash']

    def get_user(self, username):
        return self.users.get(username)

    def add_balance(self, username, amount):
        if username in self.users:
            self.users[username]['balance'] = self.users[username].get('balance', 0) + amount
            self.save_users()
            return True
        return False

    def subtract_balance(self, username, amount):
        if username in self.users and self.users[username].get('balance', 0) >= amount:
            self.users[username]['balance'] -= amount
            self.save_users()
            return True
        return False

    def list_users(self):
        return self.users