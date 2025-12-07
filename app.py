import streamlit as st
import redis
import time
import json
from prometheus_client import start_http_server, Counter

# --- METRICS CONFIGURATION ---
# Use cache_resource to ensure metrics are initialized only once
@st.cache_resource
def init_metrics():
    hits = Counter('news_cache_hits_total', 'Total number of cache hits')
    misses = Counter('news_cache_misses_total', 'Total number of cache misses')
    
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    return hits, misses

CACHE_HITS, CACHE_MISSES = init_metrics()

# --- DATABASE CONNECTION ---
# Connect to Redis service defined in docker-compose
r = redis.Redis(host='redis-db', port=6379, decode_responses=True)

# --- UI SETUP ---
st.title("📰 Lanka News Dashboard")
st.caption("Microservices Architecture Demo with Prometheus Monitoring")

# Mock API Data
news_data = {
    "headline": "DevOps adoption rising in Sri Lankan tech sector",
    "breaking": "Weather Sentinel issues heavy rain alert for Western Province",
    "sports": "Cricket: Sri Lanka secures series victory!"
}

def fetch_news():
    # Attempt to retrieve data from Redis cache
    cached_data = r.get("lanka_news")
    
    if cached_data:
        CACHE_HITS.inc()
        st.success("⚡ Cache HIT: Loaded from Redis (Latency: <10ms)")
        return json.loads(cached_data)
    
    else:
        CACHE_MISSES.inc()
        st.warning("🐢 Cache MISS: Fetching from upstream API...")
        
        # Simulate API latency
        time.sleep(2) 
        
        # Store in Redis with 10-second TTL (Time To Live)
        r.set("lanka_news", json.dumps(news_data), ex=10)
        return news_data

# Main Execution
if st.button('Refresh Feed'):
    data = fetch_news()
    st.divider()
    st.markdown(f"### {data['headline']}")
    st.error(f"🚨 **BREAKING:** {data['breaking']}")
    st.info(f"🏏 **Sports:** {data['sports']}")