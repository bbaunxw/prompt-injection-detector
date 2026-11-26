from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="PromptShield | Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
      :root { --bg:#070b19; --panel:#11182a; --line:#222c40; --muted:#8d98ad; --text:#edf2fb; --green:#4fc39a; --orange:#f28a3d; --red:#ef777c; }
      .stApp { background:var(--bg); color:var(--text); font-family:'DM Sans',sans-serif; }
      [data-testid="stHeader"] { background:transparent; }
      .block-container { padding:2.4rem 2.4rem 3rem; max-width:1500px; }
      h1,h2,h3,p,label { color:var(--text); }
      .dash-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:1.6rem; }
      .dash-title { font-size:2.25rem; font-weight:700; letter-spacing:-.04em; margin:0; }
      .dash-subtitle { color:var(--muted); font-size:1.05rem; margin-top:.2rem; }
      .eyebrow { font-size:.76rem; color:var(--muted); letter-spacing:.09em; text-transform:uppercase; }
      .metric-card,.panel { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:1.25rem 1.35rem; }
      .metric-card { min-height:116px; }
      .metric-value { font-size:2rem; font-weight:700; margin-top:.5rem; letter-spacing:-.04em; }
      .metric-critical { color:var(--red); }
      .panel { margin-top:1.25rem; }
      .panel-title { font-weight:600; font-size:1.05rem; margin-bottom:.8rem; }
      .stButton > button[kind="primary"] { background:var(--green); color:#06150f; border:0; border-radius:10px; font-weight:700; min-height:44px; }
      .stButton > button[kind="primary"]:hover { background:#69d5ad; color:#06150f; }
      [data-testid="stTextArea"] textarea { background:#0c1221; border:1px solid #2a3448; border-radius:10px; color:var(--text); }
      .result-good,.result-risk { border-radius:10px; padding:1rem 1.1rem; font-weight:600; margin:.8rem 0; }
      .result-good { background:#103329; color:#61d4aa; }
      .result-risk { background:#39232b; color:#ff9b86; }
      .scan-wait { background:linear-gradient(135deg,#11182a,#17233a); border:1px solid #2b3952; border-radius:14px; padding:1.4rem; margin-top:1rem; }
      .scan-wait-title { font-size:1.08rem; font-weight:700; color:#edf2fb; }
      .scan-wait-copy { color:#aab4c6; margin-top:.35rem; }
      .scan-pulse { display:inline-block; width:9px; height:9px; border-radius:50%; background:#4fc39a; margin-right:.55rem; box-shadow:0 0 0 0 #4fc39a88; animation:pulse 1.5s infinite; }
      @keyframes pulse { 70% { box-shadow:0 0 0 9px #4fc39a00; } 100% { box-shadow:0 0 0 0 #4fc39a00; } }
      .stCaption { color:var(--muted); }
      div[data-testid="stPlotlyChart"],div[data-testid="stVegaLiteChart"] { background:transparent; }
      @media (max-width: 700px) { .block-container { padding:1.2rem 1rem 2rem; } .dash-title { font-size:1.8rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

if "scans" not in st.session_state:
    st.session_state.scans = []

scans = st.session_state.scans
total_scans = len(scans)
critical_findings = sum(scan["label"] == "INJECTION" for scan in scans)
avg_risk = round(sum(scan["risk"] for scan in scans) / total_scans) if total_scans else 0

st.markdown(
    '<div class="dash-head"><div><div class="dash-title">Security Dashboard</div>'
    '<div class="dash-subtitle">Overview of your prompt security posture</div></div></div>',
    unsafe_allow_html=True,
)

top = st.columns([1.2, 1.2, 1.2, 1.2, 1.0])
with top[0]:
    st.markdown(f'<div class="metric-card"><div class="eyebrow">Targets</div><div class="metric-value">{1 if total_scans else 0}</div></div>', unsafe_allow_html=True)
with top[1]:
    st.markdown(f'<div class="metric-card"><div class="eyebrow">Total scans</div><div class="metric-value">{total_scans}</div></div>', unsafe_allow_html=True)
with top[2]:
    st.markdown(f'<div class="metric-card"><div class="eyebrow">Avg risk score</div><div class="metric-value">{avg_risk}/100</div></div>', unsafe_allow_html=True)
with top[3]:
    st.markdown(f'<div class="metric-card"><div class="eyebrow">Critical findings</div><div class="metric-value metric-critical">{critical_findings}</div></div>', unsafe_allow_html=True)
with top[4]:
    if st.button("＋  New Scan", type="primary", use_container_width=True):
        st.session_state.show_scan = True

chart_left, chart_right = st.columns([1.8, 1])
with chart_left:
    st.markdown('<div class="panel"><div class="panel-title">Risk Score Over Time</div>', unsafe_allow_html=True)
    if scans:
        trend = pd.DataFrame(scans)
        line = alt.Chart(trend).mark_line(color="#f28a3d", strokeWidth=3, point=alt.OverlayMarkDef(color="#f28a3d", size=90)).encode(
            x=alt.X("scan_no:Q", title=None, axis=alt.Axis(labels=False, ticks=False, domain=False, grid=False)),
            y=alt.Y("risk:Q", title=None, scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(gridColor="#263047", labelColor="#8d98ad", tickCount=5)),
            tooltip=[alt.Tooltip("scan_no:Q", title="Scan"), alt.Tooltip("risk:Q", title="Risk score")],
        ).properties(height=250)
        st.altair_chart(line, use_container_width=True)
    else:
        st.caption("Run your first scan to start tracking risk scores.")
        st.markdown('<div style="height:220px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_right:
    st.markdown('<div class="panel"><div class="panel-title">Severity Breakdown</div>', unsafe_allow_html=True)
    risk_count = sum(scan["label"] == "INJECTION" for scan in scans)
    safe_count = total_scans - risk_count
    if total_scans:
        severity = pd.DataFrame({"Result": ["Critical", "Safe"], "Count": [risk_count, safe_count]})
        donut = alt.Chart(severity).mark_arc(innerRadius=62, outerRadius=95, stroke="#11182a").encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color("Result:N", scale=alt.Scale(domain=["Critical", "Safe"], range=["#ec777b", "#f28a3d"]), legend=alt.Legend(orient="bottom", labelColor="#aab4c6", title=None)),
            tooltip=["Result", "Count"],
        ).properties(height=250)
        st.altair_chart(donut, use_container_width=True)
    else:
        st.caption("Severity data will appear after a scan.")
        st.markdown('<div style="height:220px"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="panel"><div class="panel-title">Findings by Attack Class</div>', unsafe_allow_html=True)
attack_count = sum(scan["label"] == "INJECTION" for scan in scans)
attack_data = pd.DataFrame({"Attack class": ["Prompt Injection"], "Findings": [attack_count]})
bars = alt.Chart(attack_data).mark_bar(color="#f28a3d", cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X("Attack class:N", title=None, axis=alt.Axis(labelColor="#8d98ad", domain=False, ticks=False)),
    y=alt.Y("Findings:Q", title=None, scale=alt.Scale(domain=[0, max(5, attack_count + 1)]), axis=alt.Axis(labelColor="#8d98ad", gridColor="#263047", tickMinStep=1)),
    tooltip=["Attack class", "Findings"],
).properties(height=190)
st.altair_chart(bars, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get("show_scan", False):
    with st.expander("New prompt scan", expanded=True):
        prompt = st.text_area("Prompt to scan", height=150, placeholder="Paste a prompt here...", key="scan_prompt")
        if st.button("Run Scan", type="primary", key="run_scan"):
            if not prompt.strip():
                st.warning("Enter a prompt before running a scan.")
            else:
                try:
                    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

                    model_id = "protectai/deberta-v3-base-prompt-injection-v2"
                    with st.status("Preparing scan...", expanded=True) as scan_status:
                        st.write("Loading the local security model")
                        tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
                        model = AutoModelForSequenceClassification.from_pretrained(model_id, local_files_only=True)
                        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, truncation=True, max_length=512)
                        st.write("Analyzing the prompt")
                        result = classifier(prompt.strip())[0]
                        scan_status.update(label="Scan complete", state="complete", expanded=False)
                    label = result["label"].upper()
                    confidence = float(result["score"])
                    is_injection = label in {"INJECTION", "LABEL_1", "1"}
                    scan = {
                        "scan_no": len(scans) + 1,
                        "risk": round(confidence * 100) if is_injection else round((1 - confidence) * 100),
                        "label": "INJECTION" if is_injection else "SAFE",
                        "confidence": confidence,
                        "time": datetime.now().strftime("%H:%M:%S"),
                    }
                    st.session_state.scans.append(scan)
                    st.session_state.last_result = scan
                    st.session_state.show_scan = False
                    st.rerun()
                except Exception as error:
                    st.error("The local classifier could not run. Confirm the model has been downloaded once.")
                    st.exception(error)

if "last_result" in st.session_state:
    result = st.session_state.last_result
    result_col, detail_col = st.columns([1.5, 1])
    with result_col:
        message = "Possible prompt injection detected." if result["label"] == "INJECTION" else "No prompt injection detected."
        css_class = "result-risk" if result["label"] == "INJECTION" else "result-good"
        st.markdown(f'<div class="panel"><div class="panel-title">Latest Scan · {result["time"]}</div><div class="{css_class}">{message}</div><div class="eyebrow">Model classification: {result["label"]}</div></div>', unsafe_allow_html=True)
    with detail_col:
        st.markdown(f'<div class="panel"><div class="eyebrow">Model confidence</div><div class="metric-value">{result["confidence"]:.1%}</div><div class="eyebrow">Risk score: {result["risk"]}/100</div></div>', unsafe_allow_html=True)

if st.session_state.get("scan_in_progress", False):
    st.markdown('<div class="scan-wait"><div class="scan-wait-title"><span class="scan-pulse"></span>Running security analysis</div><div class="scan-wait-copy">The local model is checking the full prompt. This may take a few seconds.</div></div>', unsafe_allow_html=True)

st.caption("Powered by Protect AI DeBERTa. English-focused classifier; results are estimates and may be wrong. It does not detect every jailbreak or support every language.")
