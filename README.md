<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Forge.host – Home</title>

<style>
:root {
  --bg: #121212;
  --panel: #1a1a1a;
  --panel-border: #2a2a2a;
  --text: #f0f0f0;
  --muted: #a3a3a3;
  --accent: #c86b6b;
  --accent-soft: #b55a5a;
  --accent-hover: #d97b7b;
}

* { box-sizing: border-box; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, sans-serif; }
body { margin: 0; background: linear-gradient(180deg, #181818, #101010); color: var(--text); }

.navbar { height: 64px; background: #151515; display: flex; align-items: center; padding: 0 24px; border-bottom: 1px solid #262626; }
.brand { font-weight: 700; font-size: 18px; color: var(--accent); }
.nav-links { margin-left: 32px; display: flex; gap: 24px; color: var(--muted); font-size: 14px; }
.nav-right { margin-left: auto; display: flex; align-items: center; gap: 16px; }
.create-btn { background: linear-gradient(135deg, var(--accent), var(--accent-soft)); color: #fff; padding: 8px 14px; border-radius: 8px; font-weight: 600; font-size: 14px; cursor: pointer; }
.login-btn { border: 1px solid #2a2a2a; padding: 8px 14px; border-radius: 8px; font-size: 14px; color: var(--muted); cursor: pointer; }

.main { min-height: calc(100vh - 160px); display: flex; justify-content: center; padding-top: 20px; }
.card { height: 500px; width: 380px; background: linear-gradient(180deg, #1d1d1d, #161616); border: 1px solid var(--panel-border); border-radius: 16px; padding: 28px; box-shadow: 0 25px 70px rgba(0,0,0,.55); }
.card h1 { text-align: center; margin: 10px 0 4px; font-size: 26px; }
.subtitle { text-align: center; color: var(--muted); font-size: 14px; margin-bottom: 20px; }
.label { font-size: 13px; margin-bottom: 6px; }
input { width: 100%; padding: 12px; border-radius: 10px; background: #141414; border: 1px solid #2b2b2b; color: var(--text); margin-bottom: 18px; }
input:focus { outline: none; border-color: var(--accent); }
.signin-btn { width: 100%; padding: 13px; border-radius: 12px; border: none; background: linear-gradient(135deg, var(--accent), var(--accent-soft)); color: #fff; font-weight: 700; font-size: 15px; cursor: pointer; }
.signup { text-align: center; margin-top: 18px; font-size: 13px; color: var(--muted); }
.signup a { color: var(--accent); cursor: pointer; text-decoration: none; }
.error { color: #ff6b6b; text-align: center; margin-bottom: 12px; font-size: 13px; height: 16px; }

.footer { position: fixed; bottom: 0; width: 100%; background: #151515; border-top: 1px solid #262626; padding: 14px 24px; display: flex; justify-content: space-between; }
.free-btn { background: linear-gradient(135deg, var(--accent), var(--accent-soft)); padding: 10px 18px; border-radius: 999px; font-weight: 600; color: #fff; text-decoration: none; }
</style>
</head>

<body>

<div class="navbar">
  <div class="brand">Forge.host</div>
  <div class="nav-links">
    <div>Servers</div>
    <div>Blogs</div>
    <div>Tools</div>
  </div>
  <div class="nav-right">
    <div class="create-btn" onclick="showSignUp()">+ Create Server</div>
    <div class="login-btn" onclick="showSignIn()">Login</div>
  </div>
</div>

<div class="main">
  <div class="card" id="card"></div>
</div>

<div class="footer">
  <div>Start a free server — instant setup on Forge.host</div>
  <a href="#" class="free-btn">Get a Free Server →</a>
</div>

<script>
const card = document.getElementById("card");

function showError(msg) {
  const errDiv = document.getElementById("error");
  if(errDiv) errDiv.innerText = msg;
}

function showSignIn() {
  card.innerHTML = `
    <h1>Sign In</h1>
    <div class="subtitle">Welcome back to Forge.host</div>
    <div id="error" class="error"></div>

    <div class="label">Username</div>
    <input id="login_user" placeholder="Enter username">

    <div class="label">Password</div>
    <input type="password" id="login_pass" placeholder="Enter password">

    <button class="signin-btn" id="loginBtn">Sign In</button>

    <div class="signup">
      Don't have an account? <a id="toSignup">Sign up</a>
    </div>
  `;

  document.getElementById("loginBtn").onclick = () => {
    const u = document.getElementById("login_user").value.trim();
    const p = document.getElementById("login_pass").value;
    
    // Check if user exists and password matches
    if (localStorage.getItem(u) && localStorage.getItem(u + "_pw") === p) {
      localStorage.setItem("currentUser", u);
      window.location.href = "panel.html";
    } else {
      showError("Invalid username or password");
    }
  };

  document.getElementById("toSignup").onclick = showSignUp;
}

function showSignUp() {
  card.innerHTML = `
    <h1>Sign Up</h1>
    <div class="subtitle">Create your Forge.host account</div>
    <div id="error" class="error"></div>

    <div class="label">Username</div>
    <input id="reg_user" placeholder="Choose username">

    <div class="label">Email</div>
    <input id="reg_email" placeholder="Enter your email">

    <div class="label">Password</div>
    <input type="password" id="reg_pass" placeholder="Create password">

    <button class="signin-btn" id="registerBtn">Create Account</button>

    <div class="signup">
      Already have an account? <a id="toSignin">Sign in</a>
    </div>
  `;

  document.getElementById("registerBtn").onclick = () => {
    const u = document.getElementById("reg_user").value.trim();
    const e = document.getElementById("reg_email").value.trim();
    const p = document.getElementById("reg_pass").value;

    if (!u || !p || !e) return showError("Fill all fields");
    if (localStorage.getItem(u)) return showError("Username exists");

    // Create the unique User Object for the Dashboard
    const userData = {
      username: u,
      email: e,
      // Generates an 8-character hex ID like 'eaae2a59'
      id: Math.floor(Math.random() * 0xFFFFFFFF).toString(16).padEnd(8, '0'),
      // Sets the current date
      joined: new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
    };

    // Save data
    localStorage.setItem(u, JSON.stringify(userData));
    localStorage.setItem(u + "_pw", p);
    
    // Set active session and redirect
    localStorage.setItem("currentUser", u);
    window.location.href = "panel.html";
  };

  document.getElementById("toSignin").onclick = showSignIn;
}

// Default view
showSignIn();
</script>

</body>
</html>
