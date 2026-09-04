# ⚡ Collaborative Real-Time Whiteboard

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://collaborative-realtime-whiteboard.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://collaborative-realtime-whiteboard.vercel.app](https://collaborative-realtime-whiteboard.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Multi-room collaborative HTML5 canvas engine synchronizing vector strokes with coordinate broadcasting, room isolation, and bounded memory buffers.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** HTML5 Canvas, FastAPI WebSockets, Redis pub/sub
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Bounded Frame Buffer:** 1,000-stroke buffer cap per room eliminates memory leaks under rapid drawing.
* **Room Isolation:** Scoped WebSocket rooms prevent cross-session message leaks.
* **Resilient Decoding:** Drops invalid coordinates without disconnecting active peers.

---

## 🚀 API Contracts
```http
WS /ws/whiteboard/{room_id}

Client Inbound Frame:
{
  "type": "DRAW_STROKE",
  "data": {"x0": 12, "y0": 45, "x1": 80, "y1": 120, "color": "#38bdf8"}
}

Broadcast Event:
{
  "event": "PEER_DRAW",
  "client_id": "client_942",
  "stroke": {"x0": 12, "y0": 45, "x1": 80, "y1": 120, "color": "#38bdf8"}
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v