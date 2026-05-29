
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Dataset for training
@st.cache_resource
def train_intelligent_model():
    data = {
        'text': [
            # Phishing Examples
            "Your bank account has been flagged for suspicious activity. Click here to verify.",
            "Urgent: Security alert for your account. Update your password immediately at this link.",
            "Congratulations! You won a $500 Amazon gift card. Claim your reward now!",
            "Dear customer, your Netflix subscription has expired. Update payment information now.",
            "Official Notice: PayPal account suspension warning. Click to secure your credentials.",
            "You have received a secure encrypted message from tax administration. Open link to view.",
            "Crypto Alert: Your wallet security phrase has been compromised. Reset it here.",
            "Dear User, verify your login attempt from Russia or terminate your session now.",
            "Get rich quick! Invest $100 in Bitcoin right now and make $10,000 by tomorrow!",
            "Your package delivery failed. Please click here to pay the remaining shipping fee.",
            
            # Safe Examples
            "Hey, are we still meeting for lunch at 1 PM today?",
            "Please review the attached project proposal and give me your feedback.",
            "Hi Mom, just checking in to see how you are doing. Call me later.",
            "The invoice for next month's software subscription is attached.",
            "Can you please send me the schedule for the upcoming team meetings?",
            "Thanks for your email. I will look over the documents and get back to you soon.",
            "Let's reschedule our phone call to Friday afternoon if you are free.",
            "Hi team, just a reminder that the office will be closed this coming Monday.",
            "The notes from yesterday's presentation have been uploaded to the shared folder.",
            "Hey buddy, happy birthday! Hope you have an amazing day ahead."
        ],
        'label': [
            'phishing', 'phishing', 'phishing', 'phishing', 'phishing', 
            'phishing', 'phishing', 'phishing', 'phishing', 'phishing',
            'safe', 'safe', 'safe', 'safe', 'safe', 
            'safe', 'safe', 'safe', 'safe', 'safe'
        ]
    }
    
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    y = df['label']
    
    model = MultinomialNB()
    model.fit(X, y)
    
    return model, cv

model, cv = train_intelligent_model()

# 2. Design the Web Interface
st.set_page_config(page_title="Phishing Shield AI", page_icon="🛡️", layout="centered")

st.title("🛡️ Phishing Shield AI")
st.subheader("School Project Email Security Analyzer")
st.write("Paste the full content of any suspicious email below to run a security risk assessment.")

email_input = st.text_area("Analyze Email Text", height=250, placeholder="Paste email content here...")

if st.button("Run Security Scan", use_container_width=True):
    if email_input.strip() == "":
        st.warning("⚠️ Please paste some email text to analyze.")
    else:
        # Process and predict
        transformed_input = cv.transform([email_input])
        prediction = model.predict(transformed_input)[0]
        probabilities = model.predict_proba(transformed_input)[0]
        
        confidence = max(probabilities) * 100
        
        st.write("### 📊 Scan Results:")
        
        if prediction == 'phishing':
            st.error("🚨 CRITICAL WARNING: Phishing Signature Detected!")
            st.metric(label="AI Threat Certainty", value=f"{confidence:.2f}%")
            st.markdown("""> Security Diagnostics:
            > * This message contains structural patterns highly identical to known social engineering scams.
            > * Action Required: Do NOT click any links, do NOT download attachments, and delete this email immediately.
            """)
        else:
            st.success("✅ Security Clean: Email Appears Safe")
            st.metric(label="AI Safety Confidence", value=f"{confidence:.2f}%")
            st.markdown("""
            > Security Diagnostics:
            > * No immediate malicious phrasing or phishing structures were triggered.
            """)