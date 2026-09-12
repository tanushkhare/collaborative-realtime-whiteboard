# ⚡ Collaborative Real-Time Whiteboard

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://collaborative-realtime-whiteboard.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://collaborative-realtime-whiteboard.vercel.app](https://collaborative-realtime-whiteboard.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Multi-room collaborative HTML5 canvas engine synchronizing vector strokes with coordinate broadcasting and bounded memory buffers.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** HTML5 Canvas, FastAPI WebSockets, Broadcast Manager
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🚀 API Contracts
```http
WS /ws/whiteboard/{room_id}
GET /api/v1/rooms
```

---

## 💻 Local Quickstart
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v
```
