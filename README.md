<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Multi-Agent AI Support System — Royson</title>
  <style>
    :root{
      --bg:#0f1724; --card:#0b1220; --muted:#94a3b8;
      --accent:#2563eb; --accent2:#06b6d4; --glass: rgba(255,255,255,0.03);
      --success:#10b981; --danger:#ef4444; --panel:#071027;
      color-scheme: dark;
    }
    html,body{height:100%;margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial;}
    body{background:linear-gradient(180deg,#071226 0%, #00121a 100%); color:#e6eef8; line-height:1.5;}
    .wrap{max-width:1100px;margin:28px auto;padding:24px;}
    header{display:flex;gap:16px;align-items:center}
    .title{font-size:22px;font-weight:700;letter-spacing:-0.2px}
    .subtitle{color:var(--muted);font-size:13px;margin-top:4px}
    .badges{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
    .badge{background:var(--glass);padding:6px 10px;border-radius:8px;font-size:12px;color:var(--muted);display:inline-flex;align-items:center;gap:8px}
    main{margin-top:18px;display:grid;grid-template-columns: 1fr 360px; gap:18px;}
    section.card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border-radius:12px;padding:18px; box-shadow: 0 6px 20px rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.03)}
    h2{margin:0 0 8px 0;font-size:18px}
    p.lead{color:var(--muted);margin-top:4px}
    ul.inline{display:flex;flex-wrap:wrap;gap:10px;padding-left:0;list-style:none;margin:12px 0}
    ul.inline li{background:rgba(255,255,255,0.02);padding:6px 8px;border-radius:8px;font-size:13px;color:var(--muted)}
    table{width:100%;border-collapse:collapse;margin-top:12px}
    th,td{padding:8px;border-bottom:1px dashed rgba(255,255,255,0.03);text-align:left;font-size:13px;color:#dbeafe}
    th{color:var(--accent2);font-weight:600}
    .small{font-size:13px;color:var(--muted)}
    pre.code{background:#021021;padding:12px;border-radius:8px;overflow:auto;font-size:13px;color:#cde8ff}
    .flow-wrap{background:linear-gradient(180deg, rgba(2,6,23,0.6), rgba(0,8,15,0.6));padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,0.03)}
    .right-col .card + .card{margin-top:12px}
    .pill{display:inline-flex;align-items:center;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.02);color:var(--muted);font-size:13px}
    footer{margin-top:18px;color:var(--muted);font-size:13px;text-align:center}
    /* SVG styles */
    .arch-title{font-size:14px;color:var(--muted);margin-bottom:8px}
    /* Responsive */
    @media (max-width:980px){
      main{grid-template-columns: 1fr; }
      .badges{order:3;width:100%;justify-content:flex-start}
    }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <div class="title">Multi-Agent AI Support System</div>
        <div class="subtitle">Intelligent Customer Support — Google ADK & Gemini (Hackathon project)</div>
      </div>
      <div class="badges">
        <span class="badge">⚡ Gemini 2.0</span>
        <span class="badge">🧭 Google ADK</span>
        <span class="badge">🧪 Flask</span>
        <span class="badge">✨ React (Vite)</span>
      </div>
    </header>

    <main>
      <section class="card">
        <h2>🎯 The Problem</h2>
        <p class="lead">Modern customer support is broken — long waits, repetitive queries, low accuracy from simple chatbots, and agent burnout. This project demonstrates a multi-agent approach to fix that.</p>

        <ul class="inline">
          <li>Slow response times</li>
          <li>Repeating answers</li>
          <li>No 24/7 support</li>
          <li>Inconsistent communication</li>
        </ul>

        <h2 style="margin-top:18px">💡 Solution: Multi-Agent Architecture</h2>
        <p class="small">Instead of one all-purpose model, the system runs a set of specialized agents that collaborate via an Orchestrator (ADK Runner + Flask API).</p>

        <table>
          <thead><tr><th>Agent</th><th>Role</th><th>Why it matters</th></tr></thead>
          <tbody>
            <tr><td>🧠 Intent Detector</td><td>Parse user intent</td><td>Prevents miscommunication</td></tr>
            <tr><td>📋 Classifier</td><td>Category routing</td><td>Routes to correct solution</td></tr>
            <tr><td>💭 Sentiment Analyzer</td><td>Emotion detection</td><td>Adjust tone / escalate</td></tr>
            <tr><td>🔍 Knowledge Searcher</td><td>Find KB results</td><td>Accurate answers</td></tr>
            <tr><td>🔧 Troubleshooter</td><td>Step-by-step fixes</td><td>Solves problems</td></tr>
            <tr><td>⚠ Escalation Checker</td><td>Flag complex issues</td><td>Reduce churn</td></tr>
            <tr><td>👤 Human Connector</td><td>Hand over to human</td><td>Seamless escalation</td></tr>
          </tbody>
        </table>

        <h2 style="margin-top:18px">Why this works</h2>
        <p class="small">Specialization + parallel processing + context sharing = higher accuracy and better escalations.</p>

        <h2 style="margin-top:18px">Request Flow Example</h2>
        <ol class="small">
          <li>User → Frontend posts message to Flask</li>
          <li>Flask validates & calls ADK runner</li>
          <li>Runner orchestrates agents and tools</li>
          <li>Agents call tools (KB search / escalate)</li>
          <li>Runner returns composed response → Frontend</li>
        </ol>

        <div style="margin-top:12px">
          <strong>Sample response</strong>
          <pre class="code">I understand this is frustrating. Try:
1) Unplug router 30s
2) Check cables
3) Restart device
Would you like me to connect you to a specialist?</pre>
        </div>
      </section>

      <aside class="right-col">
        <section class="card">
          <div class="arch-title">🏗 Architecture (interactive SVG)</div>
          <div class="flow-wrap">
            <!-- Scalable architecture SVG -->
            <svg viewBox="0 0 1000 520" width="100%" height="260" preserveAspectRatio="xMidYMid meet">
              <!-- Presentation layer -->
              <defs>
                <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                  <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.5"/>
                </filter>
                <style>
                  .box{fill:#071226;stroke:#08324a;stroke-width:1.5;rx:8;filter:url(#shadow)}
                  .lbl{fill:#9ecfff;font-weight:700;font-size:13px}
                  .sub{fill:#bcdffb;font-size:12px}
                  .muted{fill:#7ea6c9;font-size:11px}
                  .arrow{stroke:#0ea5a8;stroke-width:2;marker-end:url(#arr)}
                </style>
                <marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L10,5 L0,10 z" fill="#0ea5a8" />
                </marker>
              </defs>

              <!-- Presentation -->
              <rect class="box" x="40" y="20" width="920" height="70" rx="10" />
              <text x="64" y="45" class="lbl">Presentation Layer — React (Vite)</text>
              <text x="64" y="62" class="muted">Chat UI • Agent activity • Connection status</text>

              <!-- Application -->
              <rect class="box" x="60" y="110" width="880" height="90" rx="10" />
              <text x="84" y="138" class="lbl">Application Layer — Flask REST API</text>
              <text x="84" y="156" class="muted">POST /api/chat/message • Session management • Health</text>

              <!-- Orchestration -->
              <rect class="box" x="120" y="220" width="760" height="90" rx="10" />
              <text x="150" y="248" class="lbl">Orchestration Layer — Google ADK Runner</text>
              <text x="150" y="266" class="muted">Agent lifecycle • Tool execution • Session persistence</text>

              <!-- Agents layer (boxes) -->
              <g transform="translate(60,340)">
                <rect class="box" x="0" y="0" width="880" height="140" rx="10" />
                <text x="18" y="22" class="lbl">Agent Layer — Gemini + Virtual Sub-Agents</text>
                <text x="18" y="38" class="muted">Tools: search_knowledge_base, escalate_to_human</text>

                <!-- smaller agent boxes -->
                <g transform="translate(14,50)">
                  <rect x="0" y="0" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="12" y="24" class="sub">Intent Detector</text>

                  <rect x="200" y="0" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="212" y="24" class="sub">Classifier</text>

                  <rect x="400" y="0" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="412" y="24" class="sub">Sentiment Analyzer</text>

                  <rect x="600" y="0" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="612" y="24" class="sub">Knowledge Search</text>

                  <rect x="14" y="54" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="26" y="78" class="sub">Troubleshooter</text>

                  <rect x="214" y="54" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="226" y="78" class="sub">Escalation Checker</text>

                  <rect x="414" y="54" width="180" height="38" rx="8" fill="#052233" stroke="#0a4d66" />
                  <text x="426" y="78" class="sub">Human Connector</text>

                  <!-- arrow from orchestration to agents -->
                  <path class="arrow" d="M500 310 L500 330" />
                </g>
              </g>

              <!-- arrows: presentation -> application -> orchestration -->
              <path class="arrow" d="M500 90 L500 110" />
              <path class="arrow" d="M500 200 L500 220" />
            </svg>
          </div>

          <p class="small" style="margin-top:10px">Save this page as README.html — SVG is responsive and will look crisp in presentations.</p>
        </section>

        <section class="card" style="margin-top:12px">
          <h2>⚙ Setup & Installation</h2>
          <div class="small">
            <strong>Backend</strong>
            <pre class="code">cd ai_customer_support_agent/multi-agent-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env &amp;&amp; edit .env (add GOOGLE_API_KEY)
python app.py</pre>

            <strong>Frontend</strong>
            <pre class="code">cd ai_customer_support_agent/multi-agent-vite
npm install
npm run dev</pre>
            <p class="small">Open <code>http://localhost:3000</code>. API runs on <code>http://localhost:5000</code>.</p>
          </div>
        </section>

        <section class="card" style="margin-top:12px">
          <h2>🔒 Security & Production Checklist</h2>
          <ul class="small" style="margin:8px 0 0 16px">
            <li>Add OAuth 2.0 / API auth</li>
            <li>Rate limiting &amp; request signing</li>
            <li>Session storage in Redis (not in-memory)</li>
            <li>HTTPS, logging, monitoring, secrets rotation</li>
          </ul>
        </section>

      </aside>
    </main>

    <section class="wrap" style="max-width:1100px;padding:0 24px">
      <section class="card" style="margin-top:18px">
        <h2>🧪 Tests & Examples</h2>
        <div class="small">
          <p><strong>Health check</strong></p>
          <pre class="code">curl http://localhost:5000/health</pre>

          <p><strong>Start session</strong></p>
          <pre class="code">curl -X POST http://localhost:5000/api/chat/start -H "Content-Type: application/json" -d "{}"</pre>

          <p><strong>Send message</strong></p>
          <pre class="code">curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id":"YOUR_SESSION_ID",
    "user_id":"YOUR_USER_ID",
    "message":"My internet is down"
  }'</pre>
        </div>
      </section>

      <section class="card" style="margin-top:12px">
        <h2>📄 API</h2>
        <div class="small">
          <p><strong>POST /api/chat/start</strong> → returns session_id, user_id</p>
          <p><strong>POST /api/chat/message</strong> → body: session_id, user_id, message → returns agent_response + metadata</p>
          <p><strong>GET /api/chat/history/{session_id}</strong> → returns conversation history</p>
          <p><strong>POST /api/chat/end/{session_id}</strong> → returns summary</p>
        </div>
      </section>

      <section class="card" style="margin-top:12px">
        <h2>🎯 Usage Examples</h2>
        <p class="small"><strong>Internet troubleshooting</strong> — "My Wi-Fi stopped working" → Troubleshooting steps + option to escalate.</p>
        <p class="small"><strong>Billing</strong> — "Why was I charged twice?" → KB search + steps to dispute + escalate option.</p>
        <p class="small"><strong>Angry user</strong> — "THIS IS THE THIRD TIME!" → Sentiment detection triggers escalate prompt.</p>
      </section>

      <section class="card" style="margin-top:12px">
        <h2>📞 Contact & License</h2>
        <p class="small">Developer: Royson Salis — <a style="color:var(--accent2)" href="mailto:roysonsalis2005@gmail.com">roysonsalis2005@gmail.com</a></p>
        <p class="small">GitHub: <a style="color:var(--accent2)" href="https://github.com/Royson-salis-18">Royson-salis-18</a></p>
        <p class="small">License: MIT</p>
      </section>
    </section>

    <footer>
      Built with ❤ for the Google ADK Hackathon — Multi-Agent AI Support System
    </footer>
  </div>
</body>
</html>
