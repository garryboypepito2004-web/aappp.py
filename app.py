import streamlit as st
import smtplib
import pandas as pd
from datetime import datetime
from email.message import EmailMessage

# ═════════════════ CONFIGURATION ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj"
# ailyn_peps0678@yahoo.com has been temporarily removed
RECEIVER_EMAILS = ["garryboypepito2004@gmail.com"] 
# ═════════════════════════════════════════════════

st.set_page_config(page_title="AILYN CONSTRUCTION PRO", layout="centered")

# --- PROFESSIONAL COMMERCIAL STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .pro-header {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }
    .logo-text { font-size: 32px; font-weight: 900; letter-spacing: -1px; text-transform: uppercase; margin: 0; }
    .sub-logo { font-size: 11px; opacity: 0.8; letter-spacing: 4px; font-weight: 400; text-transform: uppercase; }
    
    .stat-card {
        background: #ffffff;
        color: #1b5e20;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        display: flex;
        justify-content: space-around;
        font-weight: bold;
        border: 1px solid #e0e0e0;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; border: 1px solid #e0e0e0; height: 3.5em;
        background-color: white; transition: all 0.3s; font-weight: 600;
    }
    .stButton>button:hover { border-color: #1b5e20; color: #1b5e20; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

if 'records' not in st.session_state: st.session_state.records = []
if 'budget' not in st.session_state: st.session_state.budget = 0.0

# --- CALCULATIONS ---
now = datetime.now()
mat_total = sum(r['Total'] for r in st.session_state.records if "DEDUCT" not in r['Description'] and "SOBRE" not in r['Description'])
ded_total = sum(r['Total'] for r in st.session_state.records if "DEDUCT" in r['Description'] or "SOBRE" in r['Description'])
balance = st.session_state.budget - mat_total - ded_total

# --- EMAIL ENGINE ---
def send_email_report(records, budget, mat_total, ded_total, balance):
    msg = EmailMessage()
    msg["Subject"] = f"AILYN CONSTRUCTION - INVENTORY RECEIPT - {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = f"AILYN PRO SYSTEM <{SENDER_EMAIL}>"
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    budget_row = f"<tr><td style='padding:10px; border-bottom:1px solid #eee;'>{datetime.now().strftime('%b %d, %Y')}</td><td style='padding:10px; border-bottom:1px solid #eee;'>INITIAL PROJECT BUDGET ALLOCATION</td><td style='padding:10px; border-bottom:1px solid #eee; text-align:right;'>PHP {budget:,.2f}</td></tr>"
    
    exp_rows, ded_rows = "", ""
    for r in records:
        if any(word in r['Description'].upper() for word in ["SOBRE", "DEDUCT", "LEFTOVER"]):
            ded_rows += f"<tr><td style='padding:10px; border-bottom:1px solid #1b5e20;'>{r['Date']}</td><td style='padding:10px; border-bottom:1px solid #1b5e20;'>{r['Description']}</td><td style='padding:10px; border-bottom:1px solid #1b5e20; text-align:right; color:#d32f2f;'>- PHP {r['Total']:,.2f}</td></tr>"
        else:
            exp_rows += f"<tr><td style='padding:10px; border-bottom:1px solid #1b5e20;'>{r['Date']}</td><td style='padding:10px; border-bottom:1px solid #1b5e20; text-align:center;'>{r['Qty']}</td><td style='padding:10px; border-bottom:1px solid #1b5e20;'>{r['Description']}</td><td style='padding:10px; border-bottom:1px solid #1b5e20; text-align:right;'>{r['Unit Price']:,.2f}</td><td style='padding:10px; border-bottom:1px solid #1b5e20; text-align:right;'>PHP {r['Total']:,.2f}</td></tr>"

    html = f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 800px; margin: auto; border: 1px solid #eee; padding: 20px; background: #fff;">
            <p style="border-left: 4px solid #1b5e20; padding-left: 15px;"><b>Good Day!</b><br><span style="font-size: 12px; color: #555;">Reviewing material inventory for <b>AILYN CONSTRUCTION</b>.</span></p>
            <div style="background-color: #1b5e20; color: white; padding: 25px;">
                <h1 style="margin: 0;">AILYN CONSTRUCTION <span style="font-weight: 200;">INVENTORY RECEIPT</span></h1>
                <div style="border-top: 1px solid rgba(255,255,255,0.2); margin-top: 10px; padding-top: 10px; font-size: 10px;">DATE: {datetime.now().strftime('%b %d, %Y | %I:%M %p')}</div>
            </div>
            <h4 style="background: #f4f4f4; border-left: 4px solid #1b5e20; padding: 8px; color: #1b5e20; margin-top: 25px;">BUDGET SUMMARY</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">{budget_row}</table>
            <h4 style="background: #f4f4f4; border-left: 4px solid #1b5e20; padding: 8px; color: #1b5e20; margin-top: 25px;">DEDUCTIONS & LEFTOVERS</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">{ded_rows if ded_rows else "<tr><td colspan='3' style='text-align:center; padding:10px;'>No Deductions</td></tr>"}</table>
            <h4 style="background: #f4f4f4; border-left: 4px solid #1b5e20; padding: 8px; color: #1b5e20; margin-top: 25px;">MATERIALS & EXPENSES</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 11px;">{exp_rows}</table>
            <div style="background-color: #1b5e20; color: white; padding: 25px; border-radius: 8px; margin-top: 30px; width: 55%;">
                <div style="font-size: 13px;">Material Total: PHP {mat_total:,.2f}</div>
                <div style="font-size: 13px;">Deduction: PHP {ded_total:,.2f}</div>
                <div style="font-size: 13px;">Budget: PHP {budget:,.2f}</div>
                <div style="border-top: 1px dashed white; margin-top: 10px; padding-top: 10px; font-size: 18px; font-weight: bold;">FINAL BALANCE: PHP {balance:,.2f}</div>
            </div>
        </div>
    </body></html>
    """
    msg.add_alternative(html, subtype='html')
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        st.success("✅ RECEIPT SENT TO CLOUD")
    except Exception as e: st.error(f"❌ ERROR: {e}")

# --- DASHBOARD HEADER ---
st.markdown(f"""
    <div class="pro-header">
        <div class="sub-logo">ENGINEERING & CONSTRUCTION</div>
        <div class="logo-text">AILYN CONSTRUCTION</div>
        <div style="font-size: 13px; margin-top: 5px; opacity: 0.8;">{now.strftime('%B %d, %Y | %I:%M %p')}</div>
        <div class="stat-card">
            <div>ALLOCATION: <span style="color:#2e7d32">PHP {st.session_state.budget:,.2f}</span></div>
            <div style="border-left: 1px solid #ddd; padding-left: 20px;">
                BALANCE: <span style="color:{'#2e7d32' if balance >=0 else '#d32f2f'}">PHP {balance:,.2f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
m1, m2, m3 = st.columns(3)
with m1:
    if st.button("📊 SET BUDGET"): st.session_state.mode = "budget"
with m2:
    if st.button("➕ NEW MATERIAL"): st.session_state.mode = "entry"
with m3:
    if st.button("📉 DEDUCTIONS"): st.session_state.mode = "deduct"

m4, m5, m6 = st.columns(3)
with m4:
    if st.button("💸 OTHER COSTS"): st.session_state.mode = "other"
with m5:
    if st.button("✉️ SEND REPORT"): send_email_report(st.session_state.records, st.session_state.budget, mat_total, ded_total, balance)
with m6:
    if st.button("🔄 RESET SYSTEM"):
        st.session_state.records = []
        st.rerun()

st.divider()

# --- INPUT LOGIC ---
current_mode = st.session_state.get("mode", "entry")

if current_mode == "budget":
    new_b = st.number_input("TOTAL PROJECT BUDGET (PHP):", value=st.session_state.budget)
    if st.button("UPDATE ALLOCATION"):
        st.session_state.budget = new_b
        st.rerun()
else:
    st.subheader(f"📝 {current_mode.upper()} MODE")
    with st.form("entry_form", clear_on_submit=True):
        col_item, col_qty = st.columns([3, 1])
        with col_item:
            item = st.text_input("MATERIAL DESCRIPTION").upper()
        with col_qty:
            q = st.number_input("QTY", min_value=1, value=1)
        
        price = st.number_input("UNIT PRICE (PHP)", min_value=0.0)
        
        if st.form_submit_button("PROCESS TRANSACTION"):
            if item and price >= 0:
                desc = f"DEDUCT: {item}" if current_mode == "deduct" else item
                st.session_state.records.append({
                    "Date": now.strftime("%Y-%m-%d"),
                    "Description": desc,
                    "Qty": q,
                    "Unit Price": price,
                    "Total": q * price
                })
                st.rerun()

# --- LIVE DATA LOG ---
if st.session_state.records:
    st.write("### TRANSACTION LOGS")
    st.dataframe(pd.DataFrame(st.session_state.records), use_container_width=True, hide_index=True)