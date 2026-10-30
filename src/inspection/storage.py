import sqlite3,json
from pathlib import Path
from datetime import datetime,timezone
def connect(path):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS inspections (id INTEGER PRIMARY KEY, created_at TEXT, vehicle_ref TEXT, image_path TEXT, detections TEXT, estimate REAL, model_status TEXT)")
    db.commit();return db
def save(path,vehicle_ref,image_path,detections,estimate,status):
    with connect(path) as db:
        cur=db.execute("INSERT INTO inspections(created_at,vehicle_ref,image_path,detections,estimate,model_status) VALUES(?,?,?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(),vehicle_ref,image_path,json.dumps(detections),estimate,status))
        return cur.lastrowid
def recent(path,limit=100):
    with connect(path) as db:
        rows=db.execute("SELECT id,created_at,vehicle_ref,image_path,detections,estimate,model_status FROM inspections ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
    return [{"id":r[0],"created_at":r[1],"vehicle_reference":r[2],"image_path":r[3],
             "detections":json.loads(r[4]),"estimate_gbp":r[5],"model_status":r[6]} for r in rows]
