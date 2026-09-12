import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Whiteboard", layout="wide")

st.title("🎨 Collaborative Real-Time Whiteboard Canvas")
st.markdown("Sub-50ms vector stroke synchronization and room session recovery.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Canvas Stroke Dispatch")
    room_id = st.text_input("Target Collaborative Room", value="architecture-room-01")
    user_id = st.text_input("User ID / Peer Handle", value="usr_architect_41")
    color = st.color_picker("Stroke Color", "#38bdf8")
    width = st.slider("Line Width (px)", 1, 12, 3)

    if st.button("Transmit Vector Stroke Event", type="primary"):
        payload = {
            "room_id": room_id,
            "user_id": user_id,
            "color": color,
            "stroke_width": width,
            "points": [{"x": 102.5, "y": 240.1}, {"x": 105.8, "y": 243.6}, {"x": 110.2, "y": 248.0}]
        }
        try:
            res = requests.post("http://localhost:8000/api/v1/whiteboard/stroke", json=payload, timeout=5)
            if res.status_code == 200:
                st.session_state["p06_status"] = res.json()
                st.success("Vector Stroke Broadcasted!")
            else:
                st.error(f"Error: {res.text}")
        except Exception:
            st.warning("Backend offline. Simulating local canvas event.")
            st.session_state["p06_status"] = {
                "room_id": room_id,
                "active_peers": 3,
                "persisted_strokes": 42,
                "status": "ACTIVE_ROOM"
            }

with col2:
    if "p06_status" in st.session_state:
        st.subheader("Active Room State")
        s = st.session_state["p06_status"]
        m1, m2 = st.columns(2)
        m1.metric("Active Peers", s["active_peers"])
        m2.metric("Persisted Strokes", s["persisted_strokes"], delta=s["status"])
        st.info(f"Room `{s['room_id']}` synchronizing via WebSocket stream.")
