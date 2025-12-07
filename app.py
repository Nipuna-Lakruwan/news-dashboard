import streamlit as st
import redis
import time
import json
from prometheus_client import start_http_server, Counter

# --- MONITORING CONFIG ---
# These are the "Sensors" we are installing
CACHE_HITS = Counter('news_cache_hits_total', 'Total number of cache hits')
CACHE_MISSES = Counter('news_cache_misses_total', 'Total number of cache misses')

# Start the Metrics Server on Port 8000 so Prometheus can scrape it
# We use a check to ensure it only starts once
if 'metrics_started' not in st.session_state:
    start_http_server(8000)
    st.session_state['metrics_started'] = True

# --- APP CONFIG ---
r = redis.Redis(host='redis-db', port=6379, decode_responses=True)

st.title("📰 Lanka News (Monitored)")
st.caption("Now with Prometheus Tracking 🕵️‍♂️")

news_data = {
    "headline": "DevOps Engineers in High Demand in Sri Lanka",
    "breaking": "Weather Sentinel Bot saves construction site from rain!",
    "sports": "Cricket: Sri Lanka wins the series!"
}

def get_news():
    cached_news = r.get("lanka_news")
    
    if cached_news:
        # Increment the "Hit" Counter
        CACHE_HITS.inc()
        st.success("⚡ Loaded from Redis Cache (Super Fast!)")
        return json.loads(cached_news)
    
    else:
        # Increment the "Miss" Counter
        CACHE_MISSES.inc()
        st.warning("🐢 Cache Miss! Fetching from 'Internet'...")
        time.sleep(2) 
        r.set("lanka_news", json.dumps(news_data), ex=10) # Reduced to 10s for testing
        return news_data

if st.button('Refresh News'):
    data = get_news()
    st.write(data)