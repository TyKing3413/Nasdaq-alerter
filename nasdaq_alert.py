
import os
import yfinance as yf
from twilio.rest import Client
import schedule
import time
from datetime import datetime
# Get credentials securely from environment variables
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
MY_NUMBER = os.environ.get("MY_NUMBER")

def send_text(message):
    """Send SMS using Twilio"""
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(body=message, from_=TWILIO_NUMBER, to=MY_NUMBER)

def check_nasdaq():
    """Check if Nasdaq hits a new all-time high"""
    nasdaq = yf.Ticker("^IXIC")
    data = nasdaq.history(period="1y")

    current_price = data["Close"][-1]
    all_time_high = data["High"].max()

    print(f"{datetime.now()} — Current: {current_price:.2f}, ATH: {all_time_high:.2f}")

    if current_price >= all_time_high:
        send_text(f"🚀 Nasdaq hit a new all-time high! ({current_price:.2f})")
        print("✅ Alert sent via SMS.")
    else:
        print("No alert — below all-time high.")

# Run every 15 minutes
schedule.every(15).minutes.do(check_nasdaq)

print("📈 Nasdaq alert service running... (Ctrl+C to stop)")
check_nasdaq()  # Run once immediately

while True:
    schedule.run_pending()
    time.sleep(60)
