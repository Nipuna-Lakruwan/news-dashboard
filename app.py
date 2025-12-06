import streamlit as st
import redis
import time
import json
import os

# --- CONFIGURATION ---
# "redis-db" is the HOSTNAME. In Docker Compose, this is the name of the service.
# We do not use IP addresses (like 192.168.x.x). We use names.
r = redis.Redis(host='redis-db', port=6379, decode_responses=True)

st.title("📰 Lanka News Dashboard")
st.subheader("DevOps Caching Demo")

# Fake News Data
news_data = {
    "headline": "DevOps Engineers in High Demand in Sri Lanka",
    "breaking": "Weather Sentinel Bot saves construction site from rain!",
    "sports": "Cricket: Sri Lanka wins the series!"
}

def get_news():
    # 1. Check if news is in Redis Cache
    cached_news = r.get("lanka_news")
    
    if cached_news:
        st.success("⚡ Loaded from Redis Cache (Super Fast!)")
        return json.loads(cached_news)
    
    else:
        # 2. If not in cache, simulate a "Slow Fetch"
        st.warning("🐢 Cache Miss! Fetching from 'Internet' (Slow)...")
        time.sleep(3) # Simulates a 3-second delay
        
        # 3. Save to Redis for next time (Expires in 60 seconds)
        r.set("lanka_news", json.dumps(news_data), ex=60)
        return news_data

if st.button('Refresh News'):
    data = get_news()
    st.write("---")
    st.write(f"**Headline:** {data['headline']}")
    st.write(f"**Breaking:** {data['breaking']}")
    st.write(f"**Sports:** {data['sports']}")