from flask import Flask, jsonify, request, render_template_string
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

CONTRACT_ADDRESS = "0xWM970000FUSDollarURCHAIN"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Hashcash AutoMiner + Order Book</title>
  <style>
    body {
      background-color: white;
      color: black;
      font-family: monospace;
      text-align: center;
      padding-top: 40px;
    }
    h1 { color: orange; }
    button {
      background-color: orange;
      color: white;
      border: none;
      padding: 12px 24px;
      margin: 8px;
      font-size: 16px;
      cursor: pointer;
    }
    input {
      font-size: 16px;
      padding: 6px;
      width: 200px;
    }
    .panel { display: none; margin-top: 20px; border: 1px solid #ccc; padding: 15px; border-radius: 8px; background-color: #f9f9f9; }
    .log { margin-top: 15px; white-space: pre-wrap; text-align: left; padding: 0 20px; max-height: 200px; overflow-y: scroll; border: 1px solid #eee; background-color: #fff; }
    table {
      width: 80%;
      margin: auto;
      border-collapse: collapse;
    }
    th, td {
      padding: 8px;
      border: 1px solid #ccc;
      text-align: center;
    }
    th { background-color: orange; color: white; }
    .info-line { margin-bottom: 5px; }
  </style>
</head>
<body>
  <h1>🟧 Hashcash AutoMiner + Order Book</h1>
  <p>Access Code:</p>
  <input type="text" id="accessCode" placeholder="1776-XX" />
  <button onclick="validate()">Enter</button>

  <div id="miner" class="panel">
    <h2>⛏️ Miner Panel</h2>
    <div class="info-line">Network: <span id="networkType">Detecting...</span></div>
    <div class="info-line">Hashrate: <span id="hashrate">0</span> MH/s</div>
    <div class="info-line">Auto-Mining Reward: <span id="reward">$0</span></div>
    <div class="info-line">Total Hashpower Contributed: <span id="totalHashpower">0</span> MH/s</div>
    <div class="info-line">Blocks Mined: <span id="blocksMined">0</span></div>
    <div class="info-line">Mining Difficulty: <span id="miningDifficulty">1</span></div>
    <div class="log" id="mineLog"></div>
  </div>

  <div id="wallet" class="panel">
    <h2>💼 Wallet</h2>
    <div class="info-line">Balance: <span id="walletBal">$0</span></div>
    <div class="info-line">Network Liquidity: <span id="networkLiquidity">$0</span></div>
    <div class="info-line">Your Liquidity Provided: <span id="liquidityProvided">$0</span></div>
    <div class="info-line">Liquidity Reward Rate: <span id="liquidityRewardRate">0%</span></div>
    <div class="info-line">Liquidity Earnings: <span id="liquidityEarnings">$0</span></div>
    <div class="log" id="txLog"></div>
  </div>

  <div id="orderBook" class="panel">
    <h2>📈 Live Order Book</h2>
    <table>
      <thead>
        <tr><th>Price (USD)</th><th>Amount (HCASH)</th><th>Type</th></tr>
      </thead>
      <tbody id="orderRows">
        <tr><td>100</td><td>50</td><td>Buy</td></tr>
        <tr><td>110</td><td>30</td><td>Sell</td></tr>
      </tbody>
    </table>
  </div>

  <div id="admin" class="panel">
    <h2>🛠 Admin Panel</h2>
    <input type="text" id="newUser" placeholder="1776-XX" />
    <button onclick="addUser()">Create User</button>
    <div class="log" id="adminLog"></div>
  </div>

  <script>
    let accessList = ["1776-17"];
    let balance = 0;
    let totalHashpower = 0;
    let blocksMined = 0;
    let miningDifficulty = 1;
    let networkLiquidity = 1000000; // Starting network liquidity
    let liquidityProvided = 0;
    const liquidityRewardRate = 0.005; // 0.5% of provided liquidity per cycle
    let liquidityEarnings = 0;

    function validate() {
      const code = document.getElementById("accessCode").value;
      if (!code.startsWith("1776-")) return alert("Invalid code");
      if (code === "1776-1776") {
        showAll();
        document.getElementById("admin").style.display = "block";
      } else if (accessList.includes(code)) {
        showAll();
      } else {
        alert("Access denied");
      }
    }

    function showAll() {
      document.getElementById("miner").style.display = "block";
      document.getElementById("wallet").style.display = "block";
      document.getElementById("orderBook").style.display = "block";
      updateUI(); // Initial UI update
      autoMine();
    }

    function addUser() {
      const user = document.getElementById("newUser").value;
      if (user.startsWith("1776-") && !accessList.includes(user)) {
        accessList.push(user);
        document.getElementById("adminLog").innerText += "✅ Added user: " + user + "\\n";
      } else {
        document.getElementById("adminLog").innerText += "❌ Invalid or duplicate user\\n";
      }
    }

    function updateUI() {
        document.getElementById("walletBal").innerText = `$${balance.toFixed(2)}`;
        document.getElementById("totalHashpower").innerText = totalHashpower.toLocaleString();
        document.getElementById("blocksMined").innerText = blocksMined;
        document.getElementById("miningDifficulty").innerText = miningDifficulty.toFixed(2);
        document.getElementById("networkLiquidity").innerText = `$${networkLiquidity.toFixed(2)}`;
        document.getElementById("liquidityProvided").innerText = `$${liquidityProvided.toFixed(2)}`;
        document.getElementById("liquidityRewardRate").innerText = `${(liquidityRewardRate * 100).toFixed(2)}%`;
        document.getElementById("liquidityEarnings").innerText = `$${liquidityEarnings.toFixed(2)}`;
    }

    function autoMine() {
      let network = navigator.connection || navigator.webkitConnection || navigator.mozConnection;
      let netType = "Unknown";
      let rate = 100000;

      if (network) {
        if (network.type === "wifi") {
          netType = "Wi-Fi";
          rate = 900000;
        } else if (network.type === "cellular") {
          netType = "Mobile";
          rate = 400000;
        } else {
          netType = network.type;
          rate = 250000;
        }
      }

      // Adjust reward based on difficulty (simplified)
      const basePayout = (rate / 2000) * 30000000000;
      const payout = basePayout / miningDifficulty;

      document.getElementById("networkType").innerText = netType;
      document.getElementById("hashrate").innerText = rate.toLocaleString();
      document.getElementById("reward").innerText = `$${payout.toFixed(2)}`;

      totalHashpower += rate;
      blocksMined++;
      miningDifficulty += 0.05; // Difficulty slowly increases

      // Simulate network liquidity growth
      networkLiquidity += Math.random() * 5000;

      // Simulate user providing liquidity (e.g., 50% of current balance, capped)
      const potentialLiquidity = balance * 0.5;
      liquidityProvided = Math.min(potentialLiquidity, balance); // Cannot provide more than owned

      // Calculate liquidity earnings
      const currentLiquidityReward = liquidityProvided * liquidityRewardRate;
      liquidityEarnings += currentLiquidityReward;
      balance += currentLiquidityReward; // Add liquidity earnings to balance

      // Add mining reward
      balance += payout;


      let mineLogEntry = `🟢 Block ${blocksMined} mined at ${rate} MH/s (Difficulty: ${miningDifficulty.toFixed(2)}) → Mining Reward: +$${payout.toFixed(2)}`;
      if (currentLiquidityReward > 0) {
          mineLogEntry += `, Liquidity Reward: +$${currentLiquidityReward.toFixed(2)}`;
      }
      mineLogEntry += `\\n`;
      document.getElementById("mineLog").innerText += mineLogEntry;
      document.getElementById("mineLog").scrollTop = document.getElementById("mineLog").scrollHeight; // Scroll to bottom

      updateUI(); // Update all displayed values

      setTimeout(autoMine, 5000); // Shorter interval for faster updates
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/contract_address', methods=['GET'])
def get_contract_address():
    return jsonify({'contract_address': CONTRACT_ADDRESS}), 200

# Keep your blockchain API routes here (mine, transactions, etc.)
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender='0', recipient='miner_address', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations, you mined a block!',
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()
    transaction_keys = ['sender', 'recipient', 'amount']
    if not json_data or not all(key in json_data for key in transaction_keys):
        return 'Some elements are missing', 400
    index = blockchain.add_transaction(json_data['sender'], json_data['recipient'], json_data['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        return jsonify({'message': 'The Blockchain is valid.'}), 200
    else:
        return jsonify({'message': 'The Blockchain is invalid.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
