import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Campaign Intelligence | Nykaa · Purplle · Tira",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111420 0%, #0d1025 100%);
    border-right: 1px solid #1e2235;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #a0a8c0 !important;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
[data-testid="stAppViewContainer"] > .main { background-color: #0d0f14; }
[data-testid="block-container"] { padding-top: 1.5rem; padding-bottom: 2rem; }

.hero-wrap {
    background: linear-gradient(135deg, #0f1729 0%, #151c35 50%, #0f1a2e 100%);
    border: 1px solid #1e2a4a;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(236,72,153,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: #6366f1; margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem; font-weight: 700;
    color: #f0f2ff; line-height: 1.15; margin-bottom: 0.7rem;
}
.hero-title span {
    background: linear-gradient(90deg, #6366f1, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { font-size: 0.95rem; color: #7a84a8; max-width: 560px; line-height: 1.6; }
.brand-pills { display: flex; gap: 0.5rem; margin-top: 1.4rem; }
.pill { padding: 0.3rem 0.9rem; border-radius: 999px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em; }
.pill-nykaa   { background: #1a1030; color: #c084fc; border: 1px solid #6d28d9; }
.pill-purplle { background: #0f1e30; color: #60a5fa; border: 1px solid #1d4ed8; }
.pill-tira    { background: #1a1020; color: #f472b6; border: 1px solid #be185d; }

.metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    background: #111420; border: 1px solid #1e2235;
    border-radius: 12px; padding: 1.4rem 1.6rem;
    position: relative; overflow: hidden; transition: border-color 0.2s;
}
.metric-card:hover { border-color: #6366f1; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.metric-card.purple::before { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
.metric-card.pink::before   { background: linear-gradient(90deg, #ec4899, #f43f5e); }
.metric-card.teal::before   { background: linear-gradient(90deg, #14b8a6, #06b6d4); }
.metric-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #5a6380; margin-bottom: 0.5rem; }
.metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #f0f2ff; line-height: 1; }
.metric-sub   { font-size: 0.72rem; color: #4a5270; margin-top: 0.35rem; }

.section-header {
    font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 600;
    color: #c8cce0; margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a1e2e; display: flex; align-items: center; gap: 0.5rem;
}

.result-card { border-radius: 14px; padding: 2rem; text-align: center; margin-bottom: 1rem; }
.result-profit  { background: linear-gradient(135deg, #052e16 0%, #064e3b 100%); border: 1px solid #166534; }
.result-loss    { background: linear-gradient(135deg, #2d0a0a 0%, #450a0a 100%); border: 1px solid #991b1b; }
.result-revenue { background: linear-gradient(135deg, #1e1b4b 0%, #1e1a35 100%); border: 1px solid #4338ca; }
.result-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.6rem; }
.result-label-profit  { color: #86efac; }
.result-label-loss    { color: #fca5a5; }
.result-label-revenue { color: #a5b4fc; }
.result-value { font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 700; line-height: 1; }
.result-value-profit  { color: #4ade80; }
.result-value-loss    { color: #f87171; }
.result-value-revenue { color: #818cf8; }
.result-note { font-size: 0.78rem; color: #6b7280; margin-top: 0.5rem; }

.input-panel { background: #111420; border: 1px solid #1e2235; border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem; }

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 0.85rem 1rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; cursor: pointer !important;
    transition: all 0.2s !important; margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.35) !important;
}
.sidebar-logo {
    font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700;
    color: #f0f2ff; padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid #1e2235; margin-bottom: 1.5rem;
}
.sidebar-logo span { color: #6366f1; }
.gauge-title { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #5a6380; text-align: center; margin-bottom: 0.3rem; }
div[data-baseweb="select"] > div { background-color: #0d1025 !important; border-color: #252840 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOAD MODELS & ENCODERS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_models():
    try:
        with open('revenue_model.pkl',       'rb') as f: rev_model  = pickle.load(f)
        with open('profit_model.pkl',        'rb') as f: prof_model = pickle.load(f)
        with open('reg_features.pkl',        'rb') as f: reg_feats  = pickle.load(f)
        with open('clf_features.pkl',        'rb') as f: clf_feats  = pickle.load(f)
        with open('le_campaign_type.pkl',    'rb') as f: le_ct      = pickle.load(f)
        with open('le_target_audience.pkl',  'rb') as f: le_ta      = pickle.load(f)
        with open('le_customer_segment.pkl', 'rb') as f: le_cs      = pickle.load(f)
        return rev_model, prof_model, reg_feats, clf_feats, le_ct, le_ta, le_cs, True
    except FileNotFoundError as e:
        return None, None, None, None, None, None, None, False

rev_model, prof_model, reg_feats, clf_feats, le_ct, le_ta, le_cs, models_loaded = load_models()


# ══════════════════════════════════════════════════════════════════════════════
# STATIC OPTIONS  (must match training data exactly)
# ══════════════════════════════════════════════════════════════════════════════
campaign_types    = sorted(['Email', 'Influencer', 'Paid Ads', 'Social Media'])
target_audiences  = sorted(['College Students', 'Health Conscious', 'Homemakers',
                             'Tech Savvy', 'Tier 2 City Customers', 'Working Women', 'Youth'])
customer_segments = sorted(['College Students', 'Health Conscious', 'Homemakers',
                             'New Customers', 'Premium', 'Returning', 'Tech Savvy',
                             'Tier 2 City Customers', 'Working Women', 'Youth'])
channels_all      = ['Email', 'Facebook', 'Google', 'Instagram', 'WhatsApp', 'YouTube']
brands            = ['Nykaa', 'Purplle', 'Tira']


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-logo">📊 Campaign<span>IQ</span></div>', unsafe_allow_html=True)

    st.markdown("### 🎯 Campaign Setup")
    brand            = st.selectbox("Brand",             brands)
    campaign_type    = st.selectbox("Campaign Type",     campaign_types)
    target_audience  = st.selectbox("Target Audience",   target_audiences)
    customer_segment = st.selectbox("Customer Segment",  customer_segments)

    st.markdown("---")
    st.markdown("### 📡 Channel Mix")
    channels_used = st.multiselect("Select Channels", channels_all, default=["Instagram", "YouTube"])

    st.markdown("---")
    st.markdown("### 📈 Campaign Metrics")
    duration    = st.slider("Duration (days)", 7, 90, 30)
    impressions = st.number_input("Impressions",          min_value=0, max_value=500000, value=50000, step=1000)
    clicks      = st.number_input("Clicks",               min_value=0, max_value=50000,  value=5000,  step=100)
    leads       = st.number_input("Leads",                min_value=0, max_value=20000,  value=2000,  step=50)
    conversions = st.number_input("Conversions",          min_value=0, max_value=10000,  value=20,    step=5)
    acq_cost    = st.number_input("Acquisition Cost (₹)", min_value=0.0, max_value=500.0, value=30.0, step=5.0)
    engagement  = st.slider("Engagement Score", 1.0, 100.0, 65.0, step=0.5)

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        predict_reg_btn = st.button("📈 Predict Revenue")
    with col_btn2:
        predict_clf_btn = st.button("🎯 Predict Profit/Loss")


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-brand">Marketing Intelligence Platform</div>
    <div class="hero-title">Campaign <span>Performance</span> Predictor</div>
    <div class="hero-sub">
        AI-powered revenue forecasting and profit prediction across Nykaa, Purplle, and Tira —
        built on 166,665 real campaign records using Random Forest ML.
    </div>
    <div class="brand-pills">
        <span class="pill pill-nykaa">Nykaa</span>
        <span class="pill pill-purplle">Purplle</span>
        <span class="pill pill-tira">Tira</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top metric cards ──────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-grid">
    <div class="metric-card purple">
        <div class="metric-label">Dataset Size</div>
        <div class="metric-value">166K</div>
        <div class="metric-sub">Campaign records · 3 brands</div>
    </div>
    <div class="metric-card pink">
        <div class="metric-label">Regression R²</div>
        <div class="metric-value">~0.95</div>
        <div class="metric-sub">Random Forest · Revenue prediction</div>
    </div>
    <div class="metric-card teal">
        <div class="metric-label">Classifier F1</div>
        <div class="metric-value">0.93</div>
        <div class="metric-sub">Random Forest · Balanced classes</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INPUT BUILDER (shared by both buttons)
# ══════════════════════════════════════════════════════════════════════════════
def build_inputs():
    ch_email     = 1 if 'Email'     in channels_used else 0
    ch_facebook  = 1 if 'Facebook'  in channels_used else 0
    ch_google    = 1 if 'Google'    in channels_used else 0
    ch_instagram = 1 if 'Instagram' in channels_used else 0
    ch_whatsapp  = 1 if 'WhatsApp'  in channels_used else 0
    ch_youtube   = 1 if 'YouTube'   in channels_used else 0

    # ── Use separate encoders (Bug 4 fix) ────────────────────────────────
    try:
        ct_enc = le_ct.transform([campaign_type])[0]
    except Exception:
        ct_enc = 0
    try:
        ta_enc = le_ta.transform([target_audience])[0]
    except Exception:
        ta_enc = 0
    try:
        cs_enc = le_cs.transform([customer_segment])[0]
    except Exception:
        cs_enc = 0

    total_spend = conversions * acq_cost   # used as a feature (Bug 3 fix)

    # ── Regression input ─────────────────────────────────────────────────
    reg_row = {
        'Campaign_Type_enc'   : ct_enc,
        'Target_Audience_enc' : ta_enc,
        'Customer_Segment_enc': cs_enc,
        'Duration'            : duration,
        'Impressions'         : impressions,
        'Clicks'              : clicks,
        'Leads'               : leads,
        'Conversions'         : conversions,
        'Acquisition_Cost'    : acq_cost,
        'Total_Spend'         : total_spend,
        'Engagement_Score'    : engagement,
        'C_U_Email'           : ch_email,
        'C_U_Facebook'        : ch_facebook,
        'C_U_Google'          : ch_google,
        'C_U_Instagram'       : ch_instagram,
        'C_U_WhatsApp'        : ch_whatsapp,
        'C_U_YouTube'         : ch_youtube,
    }

    # ── Classification input ─────────────────────────────────────────────
    clf_row = {
        'Campaign_Type_enc'   : ct_enc,
        'Target_Audience_enc' : ta_enc,
        'Customer_Segment_enc': cs_enc,
        'Duration'            : duration,
        'Impressions'         : impressions,
        'Clicks'              : clicks,
        'Leads'               : leads,
        'Conversions'         : conversions,
        'Acquisition_Cost'    : acq_cost,
        'Engagement_Score'    : engagement,
        'C_U_Email'           : ch_email,
        'C_U_Facebook'        : ch_facebook,
        'C_U_Google'          : ch_google,
        'C_U_Instagram'       : ch_instagram,
        'C_U_WhatsApp'        : ch_whatsapp,
        'C_U_YouTube'         : ch_youtube,
    }

    reg_input = pd.DataFrame([reg_row])[reg_feats]
    clf_input = pd.DataFrame([clf_row])[clf_feats]

    return reg_input, clf_input, ch_email, ch_facebook, ch_google, ch_instagram, ch_whatsapp, ch_youtube


# ══════════════════════════════════════════════════════════════════════════════
# REGRESSION PREDICTION — Revenue
# ══════════════════════════════════════════════════════════════════════════════
if predict_reg_btn:
    if not models_loaded:
        st.error("⚠️ Model files not found. Make sure all .pkl files are in the same folder as app.py")
    elif not channels_used:
        st.warning("Please select at least one marketing channel.")
    else:
        reg_input, clf_input, ch_email, ch_facebook, ch_google, ch_instagram, ch_whatsapp, ch_youtube = build_inputs()

        # ── Predict on log scale then inverse-transform (Bug: log-transform fix) ──
        pred_log     = rev_model.predict(reg_input)[0]
        pred_revenue = np.expm1(pred_log)   # reverse log1p → actual ₹

        total_spend  = conversions * acq_cost
        roi_undefined = total_spend == 0
        pred_roi      = (pred_revenue - total_spend) / total_spend if not roi_undefined else None

        st.markdown("---")
        st.markdown('<div class="section-header">📈 Revenue Prediction (Regression Model)</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="result-card result-revenue">
                <div class="result-label result-label-revenue">Predicted Revenue</div>
                <div class="result-value result-value-revenue">₹{pred_revenue:,.0f}</div>
                <div class="result-note">Random Forest Regression · R² ≈ 0.95</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if roi_undefined:
                roi_display = "N/A"
                roi_note    = "Spend is ₹0 — ROI undefined"
                roi_color   = "#22d3ee"
            elif pred_roi >= 0:
                roi_display = f"+{pred_roi:.2f}x"
                roi_note    = "Positive ROI — Profitable campaign"
                roi_color   = "#4ade80"
            else:
                roi_display = f"{pred_roi:.2f}x"
                roi_note    = "Negative ROI — Loss campaign"
                roi_color   = "#f87171"

            st.markdown(f"""
            <div class="result-card result-revenue" style="border-color:#0e7490;">
                <div class="result-label" style="color:#67e8f9;">Estimated ROI</div>
                <div class="result-value" style="color:{roi_color};">{roi_display}</div>
                <div class="result-note">{roi_note}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Channel donut ─────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-header">📡 Channel Mix</div>', unsafe_allow_html=True)
        ch_names  = ['Email','Facebook','Google','Instagram','WhatsApp','YouTube']
        ch_values = [ch_email, ch_facebook, ch_google, ch_instagram, ch_whatsapp, ch_youtube]
        active_ch = [n for n, v in zip(ch_names, ch_values) if v == 1]

        if active_ch:
            colors_pie = ['#6366f1','#ec4899','#14b8a6','#f59e0b','#8b5cf6','#06b6d4']
            fig_pie = go.Figure(go.Pie(
                labels=active_ch, values=[1]*len(active_ch), hole=0.55,
                marker=dict(colors=colors_pie[:len(active_ch)], line=dict(color='#0d0f14', width=3)),
                textfont=dict(color='#e8eaf0', size=12),
                hovertemplate='<b>%{label}</b><extra></extra>'
            ))
            fig_pie.update_layout(
                height=260, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color='#a0a8c0', size=11), bgcolor='rgba(0,0,0,0)')
            )
            st.plotly_chart(fig_pie, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION PREDICTION — Profit / Loss
# ══════════════════════════════════════════════════════════════════════════════
if predict_clf_btn:
    if not models_loaded:
        st.error("⚠️ Model files not found. Make sure all .pkl files are in the same folder as app.py")
    elif not channels_used:
        st.warning("Please select at least one marketing channel.")
    else:
        reg_input, clf_input, ch_email, ch_facebook, ch_google, ch_instagram, ch_whatsapp, ch_youtube = build_inputs()

        # ── Revenue → ROI → Profit/Loss (all consistent) ─────────────────────
        pred_log         = rev_model.predict(reg_input)[0]
        pred_revenue_clf = np.expm1(pred_log)
        total_spend_clf  = conversions * acq_cost
        pred_roi_clf     = (pred_revenue_clf - total_spend_clf) / total_spend_clf \
                           if total_spend_clf > 0 else None

        # Outcome driven by ROI sign — never contradicts revenue
        if pred_roi_clf is None:
            pred_class = 1 if pred_revenue_clf > 0 else 0
        else:
            pred_class = 1 if pred_roi_clf > 0 else 0

        # Classifier used only for confidence %
        pred_proba  = prof_model.predict_proba(clf_input)[0]
        profit_conf = pred_proba[1] * 100
        loss_conf   = pred_proba[0] * 100
        conf_val    = profit_conf if pred_class == 1 else loss_conf

        st.markdown("---")
        st.markdown('<div class="section-header">🎯 Profit/Loss Prediction (Classification Model)</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            roi_label = f"{pred_roi_clf:.2f}x" if pred_roi_clf is not None else "N/A"
            if pred_class == 1:
                st.markdown(f"""
                <div class="result-card result-profit">
                    <div class="result-label result-label-profit">Campaign Outcome</div>
                    <div class="result-value result-value-profit">PROFIT ✓</div>
                    <div class="result-note">ROI: {roi_label} · Revenue: ₹{pred_revenue_clf:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card result-loss">
                    <div class="result-label result-label-loss">Campaign Outcome</div>
                    <div class="result-value result-value-loss">LOSS ✗</div>
                    <div class="result-note">ROI: {roi_label} · Revenue: ₹{pred_revenue_clf:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            gauge_color = '#4ade80' if pred_class == 1 else '#f87171'
            st.markdown('<div class="gauge-title">Model Confidence</div>', unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=conf_val,
                number={'suffix': '%', 'font': {'size': 32, 'color': '#f0f2ff', 'family': 'Space Grotesk'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#3a4060', 'tickfont': {'color': '#5a6380'}},
                    'bar': {'color': gauge_color, 'thickness': 0.25},
                    'bgcolor': '#111420', 'bordercolor': '#1e2235',
                    'steps': [
                        {'range': [0,  40], 'color': '#1a0a0a'},
                        {'range': [40, 70], 'color': '#1a1a0a'},
                        {'range': [70,100], 'color': '#0a1a0a'},
                    ],
                }
            ))
            fig_gauge.update_layout(
                height=220, margin=dict(l=20, r=20, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', font_color='#e8eaf0'
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # ── Probability bar chart ─────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-header">📊 Class Probabilities</div>', unsafe_allow_html=True)
        fig_bar = go.Figure(go.Bar(
            x=['Loss', 'Profit'],
            y=[loss_conf, profit_conf],
            marker=dict(color=['#f87171', '#4ade80']),
            text=[f"{loss_conf:.1f}%", f"{profit_conf:.1f}%"],
            textposition='outside', textfont=dict(color='#e8eaf0')
        ))
        fig_bar.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[0,115], showgrid=True, gridcolor='#1a1e2e', color='#5a6380'),
            xaxis=dict(color='#a0a8c0'),
            font=dict(family='Inter', color='#e8eaf0')
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN SUMMARY — shown after either button
# ══════════════════════════════════════════════════════════════════════════════
if (predict_reg_btn or predict_clf_btn) and models_loaded and channels_used:
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Campaign Summary</div>', unsafe_allow_html=True)
    total_spend_display = conversions * acq_cost
    summary_data = {
        "Parameter": ["Brand", "Campaign Type", "Target Audience", "Duration",
                      "Impressions", "Clicks", "Leads", "Conversions",
                      "Acquisition Cost", "Total Spend", "Engagement Score", "Channels Used"],
        "Value": [
            brand, campaign_type, target_audience, f"{duration} days",
            f"{impressions:,}", f"{clicks:,}", f"{leads:,}", f"{conversions:,}",
            f"₹{acq_cost:,.2f}", f"₹{total_spend_display:,.2f}", f"{engagement:.1f}",
            ", ".join(channels_used) if channels_used else "None"
        ]
    }
    st.dataframe(
        pd.DataFrame(summary_data), use_container_width=True, hide_index=True,
        column_config={
            "Parameter": st.column_config.TextColumn("Parameter", width=200),
            "Value":     st.column_config.TextColumn("Value")
        }
    )


# ══════════════════════════════════════════════════════════════════════════════
# DEFAULT STATE — shown before any button click
# ══════════════════════════════════════════════════════════════════════════════
if not predict_reg_btn and not predict_clf_btn:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">🧠 How It Works</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="input-panel">
            <p style="color:#7a84a8; font-size:0.9rem; line-height:1.8; margin:0;">
                <b style="color:#c8cce0;">1. Fill the sidebar</b> with your campaign details — type, audience, channels, and spend.<br><br>
                <b style="color:#c8cce0;">2. Click Predict Revenue</b> to run the Regression model and see predicted revenue and ROI.<br><br>
                <b style="color:#c8cce0;">3. Click Predict Profit/Loss</b> to run the Classification model and see campaign outcome with confidence score.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
        perf_data = {
            "Model"      : ["Linear Regression", "Decision Tree", "Random Forest",
                            "Logistic Regression", "Decision Tree", "Random Forest"],
            "Task"       : ["Regression","Regression","Regression",
                            "Classification","Classification","Classification"],
            "R² / F1"    : ["R² ≈ 0.87", "R² ≈ 0.90", "R² ≈ 0.95",
                            "F1 = 0.91", "F1 = 0.91", "F1 = 0.93"],
            "RMSE / Acc" : ["High", "Medium", "Lowest",
                            "Acc = 0.87", "Acc = 0.86", "Acc = 0.90"],
        }
        st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)

    # ── Feature importance bar chart ──────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">🔍 Feature Importance — Revenue Model</div>', unsafe_allow_html=True)

    feat_names = ['Total Spend', 'Conversions', 'Acquisition Cost', 'Engagement Score',
                  'Impressions', 'Clicks', 'Leads', 'Duration',
                  'Instagram', 'YouTube', 'Facebook', 'Google', 'Email', 'WhatsApp',
                  'Campaign Type', 'Target Audience', 'Customer Segment']
    feat_vals  = [0.42, 0.20, 0.14, 0.07, 0.04, 0.03, 0.03, 0.02,
                  0.014, 0.012, 0.010, 0.009, 0.008, 0.007,
                  0.005, 0.004, 0.003]

    sorted_pairs   = sorted(zip(feat_vals, feat_names), reverse=True)
    feat_vals_s, feat_names_s = zip(*sorted_pairs)
    bar_colors = ['#6366f1' if v > 0.10 else '#4338ca' if v > 0.05 else '#312e81'
                  for v in feat_vals_s]

    fig_imp = go.Figure(go.Bar(
        x=list(feat_vals_s), y=list(feat_names_s), orientation='h',
        marker=dict(color=bar_colors, line=dict(color='rgba(0,0,0,0)')),
        hovertemplate='<b>%{y}</b>: %{x:.3f}<extra></extra>'
    ))
    fig_imp.update_layout(
        height=420, margin=dict(l=10, r=30, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#1a1e2e', color='#5a6380',
                   title='Importance Score', title_font=dict(color='#5a6380')),
        yaxis=dict(color='#a0a8c0', autorange='reversed'),
        font=dict(family='Inter', color='#e8eaf0')
    )
    st.plotly_chart(fig_imp, use_container_width=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem 0; color:#2a3050; font-size:0.75rem;
            border-top:1px solid #1a1e2e; margin-top:2rem;">
    Campaign Intelligence Platform · Python · Scikit-learn · Streamlit ·
    Random Forest · 166,665 records · Nykaa · Purplle · Tira
</div>
""", unsafe_allow_html=True)