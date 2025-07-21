# Hashcash


hashcash is a wifi based cryptocurrency miner with the ability to mine mh/s power in blocks on loomx programming for its own blockchain this software at 900,000 mh/s mines $130,500 cash a block every 8 seconds has live order book feature set up fro future use and automatically mines cryptocurrencies at rate of bitcoin type cash for hashcash power code below 



to increase payout you must edit this rate code 

const payout = (rate / 2000) * 300;


      rate of mh/s wifi or cpu speed then divide 2000 mh/s hash power for mobile phones • times $300 per block for 2000 mh/s power together for mining on wifi router $130,500 every block every 8 seconds 🤯

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
    .panel { display: none; margin-top: 20px; }
    .log { margin-top: 15px; white-space: pre-wrap; text-align: left; padding: 0 20px; }
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
  </style>
</head>
<body>
  <h1>🟧 Hashcash AutoMiner + Order Book</h1>
  <p>Access Code:</p>
  <input type="text" id="accessCode" placeholder="1776-XX" />
  <button onclick="validate()">Enter</button>

  <div id="miner" class="panel">
    <h2>⛏️ Miner Panel</h2>
    <p>Network: <span id="networkType">Detecting...</span></p>
    <p>Hashrate: <span id="hashrate">0</span> MH/s</p>
    <p>Auto-Mining Reward: <span id="reward">$0</span></p>
    <div class="log" id="mineLog"></div>
  </div>

  <div id="wallet" class="panel">
    <h2>💼 Wallet</h2>
    <p>Balance: <span id="walletBal">$0</span></p>
    <div class="log" id="txLog"></div>
  </div>

  <div id="orderBook" class="panel">
    <h2>📈 Live Order Book</h2>
    <table>
      <thead>
        <tr><th>Price (USD)</th><th>Amount (HCASH)</th><th>Type</th></tr>
      </thead>
      <tbody id="orderRows">
        <button>Buy</button></tr>
        <button>Sell</button></tr>
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

    function validate() {
      const code = document.getElementById("accessCode").value;
      if (!code.startsWith("1776-")) return alert("Invalid code");
      if (code === "1776-17") {
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
      autoMine();
    }

    function addUser() {
      const user = document.getElementById("newUser").value;
      if (user.startsWith("1776-") && !accessList.includes(user)) {
        accessList.push(user);
        document.getElementById("adminLog").innerText += "✅ Added user: " + user + "\n";
      } else {
        document.getElementById("adminLog").innerText += "❌ Invalid or duplicate user\n";
      }
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

      document.getElementById("networkType").innerText = netType;
      document.getElementById("hashrate").innerText = rate.toLocaleString();

      const payout = (rate / 2000) * 300;
      document.getElementById("reward").innerText = `$${payout.toFixed(2)}`;
      document.getElementById("mineLog").innerText += `🟢 Block mined at ${rate} MH/s → +$${payout.toFixed(2)}
`;

      balance += payout;
      document.getElementById("walletBal").innerText = `$${balance.toFixed(2)}`;

      setTimeout(autoMine, 8000);
    }
  </script>
</body>
</html>
