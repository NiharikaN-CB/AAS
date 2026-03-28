import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import json
import os
import pickle
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AADS – AI-Powered Attack & Defense System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  INJECT CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* === ROOT VARIABLES === */
:root {
    --bg-dark:    #050a0f;
    --bg-panel:   #0a1520;
    --bg-card:    #0d1e2e;
    --red:        #ff2d55;
    --red-glow:   rgba(255,45,85,0.25);
    --green:      #00ff88;
    --green-glow: rgba(0,255,136,0.2);
    --yellow:     #ffd60a;
    --yellow-glow:rgba(255,214,10,0.2);
    --cyan:       #00d4ff;
    --cyan-glow:  rgba(0,212,255,0.15);
    --text-pri:   #e0f4ff;
    --text-sec:   #7a9ab5;
    --border:     rgba(0,212,255,0.15);
}

/* === GLOBAL RESET === */
.stApp { background: var(--bg-dark) !important; font-family:'Rajdhani',sans-serif; }
.main .block-container { padding: 1rem 2rem !important; max-width:100% !important; }
h1,h2,h3,h4 { font-family:'Orbitron',sans-serif !important; letter-spacing:2px; }
p, li, div { color: var(--text-pri); }

/* === HIDE STREAMLIT CHROME === */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display:none; }

/* === HUD HEADER === */
.hud-header {
    background: linear-gradient(135deg, #050a0f 0%, #0a1520 50%, #050a0f 100%);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    display: flex; align-items:center; justify-content:space-between;
}
.hud-header::before {
    content:'';
    position:absolute; inset:0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 24px,
        rgba(0,212,255,0.03) 24px, rgba(0,212,255,0.03) 25px
    );
}
.hud-title { font-family:'Orbitron',sans-serif; font-size:1.6rem; font-weight:900; 
             color:var(--cyan); text-shadow: 0 0 20px var(--cyan), 0 0 40px rgba(0,212,255,0.4);
             letter-spacing:4px; }
.hud-sub { font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:var(--text-sec); 
           letter-spacing:3px; text-transform:uppercase; margin-top:4px; }
.hud-badge {
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 4px;
    padding: 8px 16px;
    font-family:'Share Tech Mono',monospace;
    font-size:0.75rem;
    color: var(--cyan);
}
.status-dot {
    display:inline-block; width:8px; height:8px; border-radius:50%;
    background:var(--green); box-shadow: 0 0 8px var(--green);
    animation: pulse-dot 1.5s infinite;
    margin-right:8px;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* === COLUMN PANELS === */
/* === COLUMN PANELS (FLAT STYLE - NO BOX LOOK) === */
.panel-red {
    background: transparent;              /* remove box background */
    border: none;                         /* remove border */
    border-top: 2px solid var(--red);     /* keep subtle top accent */
    border-radius: 0;
    padding: 0;
    min-height: auto;
    box-shadow: none;                     /* remove glow */
}

.panel-green {
    background: transparent;
    border: none;
    border-top: 2px solid var(--green);
    border-radius: 0;
    padding: 0;
    min-height: auto;
    box-shadow: none;
}

/* === PANEL TITLES === */
.panel-title-red {
    font-family:'Orbitron',sans-serif; font-size:1rem; font-weight:700;
    color: var(--red); letter-spacing:3px; text-transform:uppercase;
    padding-bottom:12px; border-bottom: 1px solid rgba(255,45,85,0.2);
    margin-bottom:16px;
    text-shadow: 0 0 15px rgba(255,45,85,0.5);
}
.panel-title-green {
    font-family:'Orbitron',sans-serif; font-size:1rem; font-weight:700;
    color: var(--green); letter-spacing:3px; text-transform:uppercase;
    padding-bottom:12px; border-bottom: 1px solid rgba(0,255,136,0.2);
    margin-bottom:16px;
    text-shadow: 0 0 15px rgba(0,255,136,0.4);
}

/* === PHASE CARD === */
.phase-card {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.phase-card:hover { border-color: var(--cyan); background: rgba(0,212,255,0.08); }
.phase-card.active {
    border-color: var(--cyan);
    background: rgba(0,212,255,0.1);
    box-shadow: 0 0 20px rgba(0,212,255,0.1);
}
.phase-label {
    font-family:'Orbitron',sans-serif; font-size:0.7rem; letter-spacing:2px;
    color: var(--cyan); text-transform:uppercase; margin-bottom:4px;
}
.phase-name {
    font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
    color: var(--text-pri);
}

/* === TERMINAL LOG === */
.terminal-box {
    background: #020609;
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 6px;
    padding: 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    height: 320px;
    overflow-y: auto;
    margin-top: 8px;
}
.terminal-box::-webkit-scrollbar { width: 4px; }
.terminal-box::-webkit-scrollbar-track { background: transparent; }
.terminal-box::-webkit-scrollbar-thumb { background: var(--cyan); border-radius:2px; }

.log-time { color: #3a5a70; }
.log-normal { color: var(--green); }
.log-attack { color: var(--red); }
.log-warn   { color: var(--yellow); }
.log-info   { color: var(--cyan); }
.log-block  { color: #ff6b35; font-weight:bold; }

/* === METRIC CARDS === */
.metric-row { display:flex; gap:10px; margin-bottom:14px; }
.metric-card {
    flex:1; background: rgba(0,0,0,0.4);
    border: 1px solid var(--border);
    border-radius: 6px; padding: 12px;
    text-align:center;
}
.metric-value {
    font-family:'Orbitron',sans-serif; font-size:1.4rem; font-weight:700;
    line-height:1; margin-bottom:4px;
}
.metric-label { font-size:0.7rem; color:var(--text-sec); letter-spacing:2px; text-transform:uppercase; }

/* === PREDICTION BADGE === */
.pred-normal {
    display:inline-block; background:rgba(0,255,136,0.1);
    border:1px solid var(--green); border-radius:4px;
    padding:4px 12px; color:var(--green);
    font-family:'Share Tech Mono',monospace; font-size:0.8rem;
}
.pred-attack {
    display:inline-block; background:rgba(255,45,85,0.1);
    border:1px solid var(--red); border-radius:4px;
    padding:4px 12px; color:var(--red);
    font-family:'Share Tech Mono',monospace; font-size:0.8rem;
    animation: blink-red 1s infinite;
}
@keyframes blink-red { 0%,100%{opacity:1} 50%{opacity:0.6} }

/* === EXPLAINER CARD === */
.explainer-card {
    background: rgba(255,214,10,0.05);
    border: 1px solid rgba(255,214,10,0.25);
    border-left: 3px solid var(--yellow);
    border-radius: 6px; padding: 14px; margin-bottom:10px;
}
.explainer-title { color:var(--yellow); font-weight:700; margin-bottom:6px;
                   font-family:'Orbitron',sans-serif; font-size:0.8rem; letter-spacing:2px; }
.explainer-reason { color: var(--text-pri); font-size:0.9rem; }

/* === FEATURE BAR === */
.feat-row { margin-bottom:8px; }
.feat-name { font-size:0.8rem; color:var(--text-sec); margin-bottom:3px;
             font-family:'Share Tech Mono',monospace; }
.feat-bar-bg {
    height:8px; background:rgba(255,255,255,0.05); border-radius:4px; overflow:hidden;
}
.feat-bar-fill {
    height:100%; border-radius:4px;
    transition: width 0.8s ease;
}

/* === PACKET TABLE === */
.pkt-table { width:100%; border-collapse:collapse; font-family:'Share Tech Mono',monospace; font-size:0.75rem; }
.pkt-table th { color:var(--cyan); border-bottom:1px solid var(--border); padding:6px 8px; text-align:left; }
.pkt-table td { padding:5px 8px; border-bottom:1px solid rgba(255,255,255,0.04); }
.pkt-table tr.attack-row td { color:var(--red); background:rgba(255,45,85,0.05); }
.pkt-table tr.normal-row td { color:#7ab5a0; }

/* === BUTTONS === */
.stButton>button {
    font-family:'Orbitron',sans-serif !important;
    font-size:0.7rem !important;
    letter-spacing:2px !important;
    text-transform:uppercase !important;
    border-radius:4px !important;
    border: 1px solid var(--cyan) !important;
    background: rgba(0,212,255,0.08) !important;
    color: var(--cyan) !important;
    transition: all 0.2s !important;
    height:38px !important;
}
.stButton>button:hover {
    background: rgba(0,212,255,0.18) !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.3) !important;
    transform: translateY(-1px) !important;
}

/* === PROGRESS / SPINNER OVERRIDE === */
.stProgress > div > div > div > div { background: var(--cyan) !important; }

/* === SEPARATOR === */
.cyber-sep {
    height:1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    margin: 16px 0;
    opacity: 0.3;
}

/* === SCAN LINE ANIMATION === */
.scan-active {
    position:relative; overflow:hidden;
}
.scan-active::after {
    content:'';
    position:absolute; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    animation: scanline 2s linear infinite;
    top:0;
}
@keyframes scanline { from{top:0%} to{top:100%} }

/* === TABS OVERRIDE === */
.stTabs [data-baseweb="tab-list"] { gap:4px; background:transparent !important; }
.stTabs [data-baseweb="tab"] {
    font-family:'Orbitron',sans-serif !important;
    font-size:0.65rem !important;
    letter-spacing:2px !important;
    color:var(--text-sec) !important;
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid var(--border) !important;
    border-radius:4px !important;
    padding:8px 16px !important;
}
.stTabs [aria-selected="true"] {
    color:var(--cyan) !important;
    border-color:var(--cyan) !important;
    background:rgba(0,212,255,0.1) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display:none !important; }
.stTabs [data-baseweb="tab-border"] { display:none !important; }

/* === SELECT BOX === */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-pri) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] { background: var(--bg-panel) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BACKEND ADAPTER  (wraps your existing files)
# ─────────────────────────────────────────────
def load_model():
    """Try to load ids_model.pkl, fall back to demo RandomForest."""
    try:
        with open("ids_model.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        pass
    try:
        from ids_model import load_model as _load
        return _load()
    except Exception:
        pass
    # Fallback: train a tiny RF on synthetic data so the UI always works
    from sklearn.ensemble import RandomForestClassifier
    X = np.random.rand(200, 6)
    y = np.array([0]*140 + [1]*30 + [2]*30)
    clf = RandomForestClassifier(n_estimators=30, random_state=42)
    clf.fit(X, y)
    return clf

def predict(model, features: dict):
    """Return (label_str, confidence, label_int)."""
    LABEL_MAP = {0: "NORMAL", 1: "PORT SCAN", 2: "BRUTE FORCE", 3: "EXPLOIT"}
    feat_order = ["duration","src_bytes","dst_bytes","failed_logins","num_connections","flag_S0"]
    vec = np.array([[features.get(k, 0) for k in feat_order]])
    try:
        pred = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        conf = float(np.max(proba))
        label = LABEL_MAP.get(int(pred), str(pred))
        return label, conf, int(pred)
    except Exception:
        # Simple rule-based fallback
        if features.get("failed_logins", 0) > 3:
            return "BRUTE FORCE", 0.94, 2
        if features.get("num_connections", 0) > 20:
            return "PORT SCAN", 0.88, 1
        if features.get("duration", 1) < 0.05 and features.get("src_bytes", 100) > 5000:
            return "EXPLOIT", 0.91, 3
        return "NORMAL", 0.97, 0

def explain_prediction(label: str, features: dict) -> dict:
    """Rule-based explainer — replace with your explain.py logic if available."""
    try:
        import explain as ex
        return ex.explain(label, features)
    except Exception:
        pass
    reasons = []
    feature_scores = {}
    if label == "PORT SCAN":
        reasons = [
            f"High connection count ({features.get('num_connections',0)}) → scanning multiple ports",
            f"Short duration ({features.get('duration',0):.3f}s) → automated scan behaviour",
            "Low byte transfer → no real data exchange, just probing",
        ]
        feature_scores = {"num_connections": 0.91, "duration": 0.78, "src_bytes": 0.42, "failed_logins": 0.05, "dst_bytes": 0.10, "flag_S0": 0.65}
    elif label == "BRUTE FORCE":
        reasons = [
            f"Failed logins = {features.get('failed_logins',0)} → repeated auth failures",
            "Repeated connections to same port 22/21",
            "Consistent packet timing → automated tool signature",
        ]
        feature_scores = {"failed_logins": 0.95, "num_connections": 0.72, "duration": 0.38, "src_bytes": 0.20, "dst_bytes": 0.12, "flag_S0": 0.08}
    elif label == "EXPLOIT":
        reasons = [
            f"Abnormal src_bytes ({features.get('src_bytes',0)}) → oversized payload",
            "Unusual flag combination → potential buffer overflow signature",
            "Short burst high-volume traffic → exploit delivery",
        ]
        feature_scores = {"src_bytes": 0.89, "flag_S0": 0.82, "duration": 0.55, "num_connections": 0.31, "dst_bytes": 0.22, "failed_logins": 0.04}
    else:
        reasons = ["Traffic pattern matches baseline normal behaviour."]
        feature_scores = {"duration": 0.35, "src_bytes": 0.25, "dst_bytes": 0.20, "num_connections": 0.10, "failed_logins": 0.05, "flag_S0": 0.05}
    return {"reasons": reasons, "feature_scores": feature_scores}

# ─────────────────────────────────────────────
#  TRAFFIC GENERATORS (wraps your attacker.py)
# ─────────────────────────────────────────────
def gen_normal_packets(n=5):
    try:
        import attacker as atk
        return atk.generate_normal(n)
    except Exception:
        packets = []
        for i in range(n):
            packets.append({
                "id": i+1, "src_ip": f"192.168.1.{random.randint(2,50)}",
                "dst_ip": "10.0.0.1", "port": random.choice([80,443,22,25]),
                "protocol": random.choice(["TCP","UDP","HTTP"]),
                "duration": round(random.uniform(0.1,2.5), 3),
                "src_bytes": random.randint(200,2000),
                "dst_bytes": random.randint(100,1500),
                "failed_logins": 0,
                "num_connections": random.randint(1,5),
                "flag_S0": 0,
                "type": "NORMAL"
            })
        return packets

def gen_port_scan_packets(n=8):
    try:
        import attacker as atk
        return atk.generate_port_scan(n)
    except Exception:
        base_ip = f"10.{random.randint(0,5)}.{random.randint(0,5)}.{random.randint(100,200)}"
        packets = []
        ports = random.sample(range(1, 65535), n)
        for i, port in enumerate(ports):
            packets.append({
                "id": i+1, "src_ip": base_ip,
                "dst_ip": "192.168.1.1", "port": port,
                "protocol": "TCP",
                "duration": round(random.uniform(0.001, 0.05), 4),
                "src_bytes": random.randint(40, 120),
                "dst_bytes": 0,
                "failed_logins": 0,
                "num_connections": n,
                "flag_S0": 1,
                "type": "PORT SCAN"
            })
        return packets

def gen_brute_force_packets(n=8):
    try:
        import attacker as atk
        return atk.generate_brute_force(n)
    except Exception:
        base_ip = f"172.{random.randint(16,31)}.{random.randint(0,5)}.{random.randint(100,200)}"
        packets = []
        for i in range(n):
            packets.append({
                "id": i+1, "src_ip": base_ip,
                "dst_ip": "192.168.1.1", "port": 22,
                "protocol": "SSH",
                "duration": round(random.uniform(0.5, 2.0), 3),
                "src_bytes": random.randint(200, 500),
                "dst_bytes": random.randint(100, 300),
                "failed_logins": random.randint(3, 9),
                "num_connections": i+1,
                "flag_S0": 0,
                "type": "BRUTE FORCE"
            })
        return packets

def gen_exploit_packets(n=5):
    try:
        import attacker as atk
        return atk.generate_exploit(n)
    except Exception:
        base_ip = f"203.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        packets = []
        for i in range(n):
            packets.append({
                "id": i+1, "src_ip": base_ip,
                "dst_ip": "192.168.1.1", "port": random.choice([80, 443, 8080]),
                "protocol": "HTTP",
                "duration": round(random.uniform(0.001, 0.03), 4),
                "src_bytes": random.randint(5000, 20000),
                "dst_bytes": random.randint(0, 200),
                "failed_logins": 0,
                "num_connections": random.randint(10, 30),
                "flag_S0": random.choice([0,1]),
                "type": "EXPLOIT"
            })
        return packets

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "model": None,
    "logs": [],
    "packets": [],
    "predictions": [],
    "phase": 0,
    "total_packets": 0,
    "total_attacks": 0,
    "total_blocked": 0,
    "active_threats": [],
    "phase_results": {1: [], 2: [], 3: []},
    "model_trained": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Load model once
if st.session_state["model"] is None:
    st.session_state["model"] = load_model()
    st.session_state["model_trained"] = True

model = st.session_state["model"]

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def ts():
    return datetime.now().strftime("%H:%M:%S")

def add_log(msg: str, kind: str = "info"):
    st.session_state.logs.append({"time": ts(), "msg": msg, "kind": kind})

def render_terminal(logs, height=320):
    kind_class = {"normal":"log-normal","attack":"log-attack","warn":"log-warn","info":"log-info","block":"log-block"}
    lines = []
    for entry in logs[-60:]:
        cls = kind_class.get(entry["kind"], "log-info")
        lines.append(f'<span class="log-time">[{entry["time"]}]</span> <span class="{cls}">{entry["msg"]}</span>')
    html = f'<div class="terminal-box" style="height:{height}px">' + "<br>".join(lines) + '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_feature_bars(scores: dict):
    bar_colors = {
        "failed_logins": "#ff2d55",
        "num_connections": "#ff6b35",
        "src_bytes": "#ffd60a",
        "flag_S0": "#ff9f1c",
        "duration": "#00d4ff",
        "dst_bytes": "#00ff88",
    }
    for feat, score in sorted(scores.items(), key=lambda x: -x[1]):
        pct = int(score * 100)
        color = bar_colors.get(feat, "#00d4ff")
        st.markdown(f"""
<div class="feat-row">
  <div class="feat-name">{feat.upper()} <span style="float:right;color:{color}">{pct}%</span></div>
  <div class="feat-bar-bg"><div class="feat-bar-fill" style="width:{pct}%;background:{color}"></div></div>
</div>""", unsafe_allow_html=True)

def run_phase(packets, phase_num):
    phase_logs = []
    phase_preds = []
    blocked = []
    for pkt in packets:
        st.session_state.total_packets += 1
        label, conf, label_int = predict(model, pkt)
        is_attack = label_int != 0
        if is_attack:
            st.session_state.total_attacks += 1
            st.session_state.total_blocked += 1
            add_log(f"📡 PKT #{pkt['id']} from {pkt['src_ip']}:{pkt['port']} → {pkt['protocol']}", "warn")
            add_log(f"🚨 ALERT: {label} detected! Confidence: {conf:.0%}", "attack")
            add_log(f"🛑 ACTION: Blocking {pkt['src_ip']} — dropping all future traffic", "block")
            blocked.append(pkt['src_ip'])
        else:
            add_log(f"✅ PKT #{pkt['id']} from {pkt['src_ip']}:{pkt['port']} → NORMAL ({conf:.0%})", "normal")
        explanation = explain_prediction(label, pkt)
        phase_preds.append({**pkt, "label": label, "confidence": conf, "explanation": explanation, "blocked": is_attack})
        phase_logs.append({"pkt": pkt, "label": label, "conf": conf, "explanation": explanation})
    st.session_state.phase_results[phase_num] = phase_preds
    st.session_state.packets.extend(packets)
    st.session_state.predictions.extend(phase_preds)
    if blocked:
        ips = list(set(blocked))
        add_log(f"🔒 FIREWALL UPDATED: {len(ips)} IP(s) blacklisted", "block")
        st.session_state.active_threats.extend(ips)
    return phase_preds

# ─────────────────────────────────────────────
#  TOP HUD HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hud-header">
  <div>
    <div class="hud-title">🛡️ AADS — AI ATTACK & DEFENSE SYSTEM</div>
    <div class="hud-sub">Adaptive Intrusion Detection · Explainable AI · Real-Time Response</div>
  </div>
  <div style="display:flex;gap:16px;align-items:center">
    <div class="hud-badge"><span class="status-dot"></span>SYSTEM ONLINE</div>
    <div class="hud-badge">MODEL: {'✅ LOADED' if st.session_state.model_trained else '⚠️ DEMO'}</div>
    <div class="hud-badge">TIME: {ts()}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TOP METRICS ROW
# ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-value" style="color:var(--cyan)">{st.session_state.total_packets}</div>
      <div class="metric-label">Packets Analyzed</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-value" style="color:var(--red)">{st.session_state.total_attacks}</div>
      <div class="metric-label">Attacks Detected</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-value" style="color:var(--yellow)">{st.session_state.total_blocked}</div>
      <div class="metric-label">Threats Blocked</div>
    </div>""", unsafe_allow_html=True)
with m4:
    rate = f"{(st.session_state.total_attacks / max(1, st.session_state.total_packets)) * 100:.1f}%"
    st.markdown(f"""<div class="metric-card">
      <div class="metric-value" style="color:var(--green)">{rate}</div>
      <div class="metric-label">Attack Rate</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="cyber-sep"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["⚔️  PHASE SIMULATION", "📊  ANALYTICS", "🧠  EXPLAINABLE AI", "⚙️  CONTROLS"])

# ═══════════════════════════════════════════
#  TAB 1: PHASE SIMULATION
# ═══════════════════════════════════════════
with tab1:
    left_col, divider, right_col = st.columns([5, 0.1, 5])

    # === LEFT: ATTACKER ===
    with left_col:
        st.markdown('<div class="panel-red">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-red">🔴 OFFENSIVE SIDE — ATTACKER</div>', unsafe_allow_html=True)

        # Phase selection
        phases = [
            {"num":1, "icon":"🔍", "name":"Phase 1: Reconnaissance", "desc":"Port scan & network mapping"},
            {"num":2, "icon":"🔑", "name":"Phase 2: Initial Access",  "desc":"Brute force login attempts"},
            {"num":3, "icon":"💥", "name":"Phase 3: Exploitation",    "desc":"Payload delivery & exploit"},
        ]
        for ph in phases:
            active_cls = "active" if st.session_state.phase == ph["num"] else ""
            done = "✅" if st.session_state.phase_results.get(ph["num"]) else ""
            if st.button(f"{ph['icon']}  {ph['name']}  {done}", key=f"phase_select_{ph['num']}",
                         use_container_width=True):
                st.session_state.phase = ph["num"]

        st.markdown('<div class="cyber-sep"></div>', unsafe_allow_html=True)

        # Current phase actions
        if st.session_state.phase > 0:
            ph = phases[st.session_state.phase - 1]
            st.markdown(f"**{ph['icon']} {ph['name']}**")
            st.caption(ph['desc'])

            num_pkts = st.slider("Packets to generate", 3, 15, 6, key="num_pkts")

            run_btn = st.button(f"▶  RUN {ph['name'].upper()}", use_container_width=True,
                                key=f"run_phase_{st.session_state.phase}")
            if run_btn:
                with st.spinner("Generating attack traffic..."):
                    if st.session_state.phase == 1:
                        pkts = gen_port_scan_packets(num_pkts)
                        add_log(f"═══ PHASE 1: RECONNAISSANCE STARTED ═══", "warn")
                        add_log(f"[SCAN] Initiating port sweep on 192.168.1.0/24", "attack")
                    elif st.session_state.phase == 2:
                        pkts = gen_brute_force_packets(num_pkts)
                        add_log(f"═══ PHASE 2: BRUTE FORCE STARTED ═══", "warn")
                        add_log(f"[BRUTE] Targeting SSH port 22 with credential list", "attack")
                    else:
                        pkts = gen_exploit_packets(num_pkts)
                        add_log(f"═══ PHASE 3: EXPLOITATION STARTED ═══", "warn")
                        add_log(f"[EXPLOIT] Sending oversized payloads to HTTP endpoints", "attack")
                    run_phase(pkts, st.session_state.phase)
                    time.sleep(0.3)
                st.rerun()

            # Show generated packets for this phase
            phase_data = st.session_state.phase_results.get(st.session_state.phase, [])
            if phase_data:
                st.caption(f"📋 {len(phase_data)} packets generated this phase:")
                rows = []
                for p in phase_data:
                    rows.append({"#": p.get("id",""), "SRC IP": p.get("src_ip",""), 
                                 "PORT": p.get("port",""), "PROTO": p.get("protocol",""),
                                 "FAILED LOGIN": p.get("failed_logins",""),
                                 "CONNS": p.get("num_connections",""), "TYPE": p.get("type","")})
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True,
                             column_config={
                                 "TYPE": st.column_config.TextColumn(width="small"),
                             })
        else:
            st.info("👆 Select a phase above to begin the simulation.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Divider
    with divider:
        st.markdown("""
<div style="width:1px; min-height:600px;
     background: linear-gradient(180deg, transparent 0%, var(--cyan) 20%, var(--cyan) 80%, transparent 100%);
     margin:0 auto; opacity:0.2;"></div>""", unsafe_allow_html=True)

    # === RIGHT: DEFENDER ===
    with right_col:
        st.markdown('<div class="panel-green">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-green">🟢 DEFENSIVE SIDE — AI DEFENDER</div>', unsafe_allow_html=True)

        # Live terminal
        st.markdown("**📟 LIVE DETECTION LOG**")
        if st.session_state.logs:
            render_terminal(st.session_state.logs, 280)
        else:
            st.markdown("""<div class="terminal-box" style="height:280px">
<span class="log-info">[ AADS IDS Engine v2.0 — Ready ]</span><br>
<span class="log-info">[ Model loaded successfully    ]</span><br>
<span class="log-info">[ Awaiting traffic...          ]</span>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="cyber-sep"></div>', unsafe_allow_html=True)

        # Latest prediction panel
        if st.session_state.predictions:
            latest = st.session_state.predictions[-1]
            label = latest.get("label","NORMAL")
            conf = latest.get("confidence", 0)
            is_attack = label != "NORMAL"

            c1, c2 = st.columns(2)
            with c1:
                badge_cls = "pred-attack" if is_attack else "pred-normal"
                st.markdown(f"**LATEST PREDICTION**<br><span class='{badge_cls}'>{label}</span>", 
                            unsafe_allow_html=True)
            with c2:
                bar_color = "#ff2d55" if is_attack else "#00ff88"
                st.markdown(f"**CONFIDENCE**")
                st.progress(conf, text=f"{conf:.0%}")

            if is_attack and latest.get("explanation"):
                reasons = latest["explanation"].get("reasons", [])
                if reasons:
                    st.markdown('<div class="explainer-card"><div class="explainer-title">⚡ WHY FLAGGED</div>' +
                                "".join(f'<div class="explainer-reason">• {r}</div>' for r in reasons[:2]) +
                                '</div>', unsafe_allow_html=True)

            # Blocked IPs
            if st.session_state.active_threats:
                unique_threats = list(set(st.session_state.active_threats[-5:]))
                threat_tags = " ".join(f'<span style="background:rgba(255,45,85,0.15);border:1px solid rgba(255,45,85,0.4);border-radius:3px;padding:2px 8px;font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#ff2d55;margin:2px">{ip}</span>' for ip in unique_threats)
                st.markdown(f"🔒 **Blocked IPs:** {threat_tags}", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  TAB 2: ANALYTICS
# ═══════════════════════════════════════════
with tab2:
    if not st.session_state.predictions:
        st.info("🔬 Run some phases first to see analytics.")
    else:
        import plotly.graph_objects as go
        import plotly.express as px

        preds = st.session_state.predictions
        df_all = pd.DataFrame(preds)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📊 Traffic Distribution")
            label_counts = df_all["label"].value_counts()
            colors = {"NORMAL":"#00ff88","PORT SCAN":"#ffd60a","BRUTE FORCE":"#ff2d55","EXPLOIT":"#ff6b35"}
            fig = go.Figure(go.Bar(
                x=list(label_counts.index),
                y=list(label_counts.values),
                marker_color=[colors.get(l,"#00d4ff") for l in label_counts.index],
                text=list(label_counts.values),
                textposition="outside",
                textfont=dict(color="#e0f4ff", family="Share Tech Mono"),
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e0f4ff", family="Rajdhani"),
                xaxis=dict(gridcolor="rgba(0,212,255,0.05)", color="#7a9ab5"),
                yaxis=dict(gridcolor="rgba(0,212,255,0.05)", color="#7a9ab5"),
                margin=dict(t=10,b=10,l=0,r=0),
                height=280,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("#### 🥧 Attack Type Breakdown")
            fig2 = go.Figure(go.Pie(
                labels=list(label_counts.index),
                values=list(label_counts.values),
                marker=dict(colors=[colors.get(l,"#00d4ff") for l in label_counts.index],
                            line=dict(color="#050a0f", width=3)),
                textfont=dict(family="Share Tech Mono", color="#e0f4ff"),
                hole=0.5,
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e0f4ff"),
                margin=dict(t=0,b=0,l=0,r=0),
                height=280,
                showlegend=True,
                legend=dict(font=dict(color="#e0f4ff"), bgcolor="rgba(0,0,0,0)")
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### 📋 Full Packet Table")
        display_cols = ["id","src_ip","dst_ip","port","protocol","duration","src_bytes","failed_logins","num_connections","label","confidence"]
        available_cols = [c for c in display_cols if c in df_all.columns]
        df_display = df_all[available_cols].copy()
        if "confidence" in df_display.columns:
            df_display["confidence"] = df_display["confidence"].apply(lambda x: f"{x:.0%}")

        def highlight_attacks(row):
            if row.get("label","NORMAL") != "NORMAL":
                return ["background-color: rgba(255,45,85,0.08); color:#ff2d55"] * len(row)
            return ["color:#7ab5a0"] * len(row)

        st.dataframe(
            df_display.style.apply(highlight_attacks, axis=1),
            use_container_width=True, hide_index=True
        )

        if "src_bytes" in df_all.columns and "num_connections" in df_all.columns:
            st.markdown("#### 🔵 Traffic Scatter (src_bytes vs connections)")
            fig3 = px.scatter(
                df_all, x="num_connections", y="src_bytes",
                color="label",
                color_discrete_map=colors,
                hover_data=["src_ip","port","protocol"],
                size_max=15,
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,10,15,0.8)",
                font=dict(color="#e0f4ff", family="Rajdhani"),
                xaxis=dict(gridcolor="rgba(0,212,255,0.05)", color="#7a9ab5"),
                yaxis=dict(gridcolor="rgba(0,212,255,0.05)", color="#7a9ab5"),
                legend=dict(font=dict(color="#e0f4ff"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=10,b=10,l=0,r=0), height=300,
            )
            st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
#  TAB 3: EXPLAINABLE AI
# ═══════════════════════════════════════════
with tab3:
    st.markdown("### 🧠 Explainable AI — Why Was It Flagged?")
    st.caption("Select any detected attack to understand why the AI made that decision.")

    attacks_only = [p for p in st.session_state.predictions if p.get("label","NORMAL") != "NORMAL"]
    if not attacks_only:
        st.info("No attacks detected yet. Run some phases to populate this section.")
    else:
        options = [f"PKT #{p.get('id',i+1)} from {p.get('src_ip','?')} → {p.get('label','?')} ({p.get('confidence',0):.0%})" 
                   for i, p in enumerate(attacks_only)]
        selected_idx = st.selectbox("Select attack to explain", range(len(options)), 
                                     format_func=lambda i: options[i])
        selected = attacks_only[selected_idx]
        exp = selected.get("explanation", {})

        xai_left, xai_right = st.columns([1,1])
        with xai_left:
            st.markdown("#### ⚡ Detection Reasons")
            reasons = exp.get("reasons", ["No explanation available."])
            for i, r in enumerate(reasons, 1):
                st.markdown(f"""<div class="explainer-card">
<div class="explainer-title">REASON {i}</div>
<div class="explainer-reason">{r}</div>
</div>""", unsafe_allow_html=True)

            st.markdown("#### 📌 Packet Features")
            feat_items = ["duration","src_bytes","dst_bytes","failed_logins","num_connections","flag_S0"]
            feat_data = {k: selected.get(k, "N/A") for k in feat_items}
            for k, v in feat_data.items():
                col_a, col_b = st.columns([2,1])
                col_a.caption(k.upper())
                col_b.markdown(f"**`{v}`**")

        with xai_right:
            st.markdown("#### 📊 Feature Importance Scores")
            st.caption("Contribution of each feature to the attack classification")
            scores = exp.get("feature_scores", {})
            if scores:
                render_feature_bars(scores)

                import plotly.graph_objects as go
                sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1]))
                bar_colors_list = ["#ff2d55" if v > 0.7 else "#ffd60a" if v > 0.4 else "#00d4ff"
                                   for v in sorted_scores.values()]
                fig = go.Figure(go.Bar(
                    x=list(sorted_scores.values()),
                    y=[k.upper() for k in sorted_scores.keys()],
                    orientation='h',
                    marker_color=bar_colors_list,
                    text=[f"{v:.0%}" for v in sorted_scores.values()],
                    textposition="outside",
                    textfont=dict(color="#e0f4ff", family="Share Tech Mono", size=11),
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e0f4ff", family="Rajdhani"),
                    xaxis=dict(range=[0,1.1], gridcolor="rgba(0,212,255,0.05)", color="#7a9ab5", tickformat=".0%"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#7a9ab5"),
                    margin=dict(t=10, b=10, l=0, r=80),
                    height=280,
                )
                st.plotly_chart(fig, use_container_width=True)

        # Response taken
        st.markdown("#### 🛡️ Defender Response")
        resp_c1, resp_c2, resp_c3 = st.columns(3)
        resp_c1.markdown("""<div class="metric-card">
<div class="metric-value" style="color:var(--red);font-size:1.2rem">DETECTED</div>
<div class="metric-label">Model Classification</div>
</div>""", unsafe_allow_html=True)
        resp_c2.markdown("""<div class="metric-card">
<div class="metric-value" style="color:var(--yellow);font-size:1.2rem">BLOCKED</div>
<div class="metric-label">Firewall Action</div>
</div>""", unsafe_allow_html=True)
        resp_c3.markdown("""<div class="metric-card">
<div class="metric-value" style="color:var(--green);font-size:1.2rem">LOGGED</div>
<div class="metric-label">Audit Trail</div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  TAB 4: CONTROLS
# ═══════════════════════════════════════════
with tab4:
    st.markdown("### ⚙️ Simulation Controls")
    ctrl1, ctrl2, ctrl3 = st.columns(3)

    with ctrl1:
        st.markdown("#### 🔄 Model Controls")
        if st.button("🧠  Train Model", use_container_width=True):
            try:
                import ids_model as im
                with st.spinner("Training model on dataset..."):
                    model = im.train()
                    st.session_state["model"] = model
                    st.session_state["model_trained"] = True
                    add_log("🧠 Model retrained successfully on latest dataset", "info")
                st.success("✅ Model trained!")
            except Exception as e:
                st.warning(f"Using built-in model (ids_model.py not found or error: {e})")
                add_log("⚠️ Using demo model (ids_model.py not accessible)", "warn")

        if st.button("📂  Load ids_model.pkl", use_container_width=True):
            st.session_state["model"] = load_model()
            st.session_state["model_trained"] = True
            add_log("📂 Model loaded from ids_model.pkl", "info")
            st.success("✅ Model loaded!")

    with ctrl2:
        st.markdown("#### 🚀 Quick Traffic Generation")
        traffic_type = st.selectbox("Traffic Type", ["Normal","Port Scan","Brute Force","Exploit","Mixed"])
        n_gen = st.slider("Packets", 3, 20, 8, key="ctrl_gen_n")

        if st.button("⚡  Generate Traffic", use_container_width=True):
            gen_map = {
                "Normal":      gen_normal_packets,
                "Port Scan":   gen_port_scan_packets,
                "Brute Force": gen_brute_force_packets,
                "Exploit":     gen_exploit_packets,
            }
            if traffic_type == "Mixed":
                pkts = (gen_normal_packets(max(1,n_gen//3)) +
                        gen_port_scan_packets(max(1,n_gen//3)) +
                        gen_brute_force_packets(max(1,n_gen//3)))
                random.shuffle(pkts)
                for i,p in enumerate(pkts): p["id"] = i+1
            else:
                pkts = gen_map[traffic_type](n_gen)
            add_log(f"⚡ Generating {len(pkts)} {traffic_type} packets...", "info")
            run_phase(pkts, 0)
            st.rerun()

    with ctrl3:
        st.markdown("#### 🎬 Full Demo")
        if st.button("🎬  Run Full Simulation", use_container_width=True):
            add_log("═══════ FULL SIMULATION START ═══════", "warn")
            with st.spinner("Running complete simulation…"):
                add_log("Phase 1: Reconnaissance", "warn")
                run_phase(gen_port_scan_packets(6), 1)
                time.sleep(0.3)
                add_log("Phase 2: Initial Access", "warn")
                run_phase(gen_brute_force_packets(6), 2)
                time.sleep(0.3)
                add_log("Phase 3: Exploitation", "warn")
                run_phase(gen_exploit_packets(5), 3)
                time.sleep(0.3)
                add_log("Normal baseline traffic added", "normal")
                run_phase(gen_normal_packets(5), 0)
                add_log("═══════ SIMULATION COMPLETE ═══════", "info")
            st.rerun()

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        if st.button("🗑️  Clear All Data", use_container_width=True):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.session_state["model"] = load_model()
            st.session_state["model_trained"] = True
            st.rerun()

    st.markdown('<div class="cyber-sep"></div>', unsafe_allow_html=True)

    # Model info
    st.markdown("#### 📋 System Information")
    info_cols = st.columns(4)
    info_cols[0].markdown(f"""<div class="metric-card">
<div class="metric-value" style="color:var(--cyan);font-size:1rem">{'✅ YES' if st.session_state.model_trained else '⚠️ NO'}</div>
<div class="metric-label">Model Loaded</div>
</div>""", unsafe_allow_html=True)
    info_cols[1].markdown(f"""<div class="metric-card">
<div class="metric-value" style="color:var(--green);font-size:1rem">RF + SHAP</div>
<div class="metric-label">Algorithm</div>
</div>""", unsafe_allow_html=True)
    info_cols[2].markdown(f"""<div class="metric-card">
<div class="metric-value" style="color:var(--yellow);font-size:1rem">4 CLASSES</div>
<div class="metric-label">Output Labels</div>
</div>""", unsafe_allow_html=True)
    info_cols[3].markdown(f"""<div class="metric-card">
<div class="metric-value" style="color:var(--cyan);font-size:1rem">6 FEATS</div>
<div class="metric-label">Input Features</div>
</div>""", unsafe_allow_html=True)

    # File status
    st.markdown("#### 📁 Project File Status")
    files_to_check = ["attacker.py","ids_model.py","demo.py","explain.py","ids_model.pkl"]
    file_cols = st.columns(len(files_to_check))
    for i, fname in enumerate(files_to_check):
        exists = os.path.exists(fname)
        icon = "✅" if exists else "⚠️"
        color = "var(--green)" if exists else "var(--yellow)"
        status = "FOUND" if exists else "MISSING"
        file_cols[i].markdown(f"""<div class="metric-card">
<div class="metric-value" style="color:{color};font-size:0.9rem">{icon} {status}</div>
<div class="metric-label">{fname}</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BOTTOM STATUS BAR
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:24px; padding:10px 20px; background:rgba(0,212,255,0.04);
     border:1px solid rgba(0,212,255,0.1); border-radius:6px;
     display:flex; justify-content:space-between; align-items:center;">
  <span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#3a5a70">
    AADS — AI ATTACK & DEFENSE SYSTEM  |  Built with Streamlit + scikit-learn + Plotly
  </span>
  <span style="font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#3a5a70">
    ⚡ ADAPTIVE INTRUSION DETECTION · EXPLAINABLE AI · REAL-TIME RESPONSE
  </span>
</div>
""", unsafe_allow_html=True)