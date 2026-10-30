# AI Vehicle Inspection Platform

FastAPI + Streamlit workflow prototype. Uploads a vehicle image, optionally calls
a trained YOLO detector and cost model from Projects 1 and 2, and stores the result
in SQLite. Missing models are explicitly reported; no detections are fabricated.

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.api:app --reload
# second terminal
streamlit run app/ui.py
```
Open http://127.0.0.1:8000/docs for interactive API documentation.

## Optional model integration
Set `DAMAGE_MODEL_PATH` to a trained YOLO `.pt` checkpoint and
`COST_MODEL_PATH` to Project 2's joblib artifact. Ensure the corresponding Python
packages are installed. The default app works without models and returns
`model_status=not_configured`.

## Privacy and production hardening
This local demo stores images and metadata on disk/SQLite. Before real use, implement
authentication, role-based access, encrypted storage, audit logs, retention controls,
secure backups, malware scanning, rate limits, HTTPS, monitoring and data-protection
review. Never commit customer images or credentials. This prototype is not connected
to ABL systems and is not a production deployment.
