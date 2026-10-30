import os,uuid,sys
from pathlib import Path
from fastapi import FastAPI,UploadFile,File,Form,HTTPException
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from inspection.models import detect,estimate
from inspection.storage import save,recent
app=FastAPI(title="AI Vehicle Inspection API",version="0.1.0")
UPLOAD=Path(os.getenv("UPLOAD_DIR","data/uploads")); DB=os.getenv("DB_PATH","data/inspections.sqlite3")
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/inspections")
async def create(image:UploadFile=File(...),vehicle_reference:str=Form(default="")):
    suffix=Path(image.filename or "").suffix.lower()
    if suffix not in {".jpg",".jpeg",".png",".webp"}: raise HTTPException(400,"Upload JPG, PNG or WEBP.")
    content=await image.read()
    if len(content)>15*1024*1024: raise HTTPException(413,"Image exceeds 15 MB.")
    UPLOAD.mkdir(parents=True,exist_ok=True); target=UPLOAD/(uuid.uuid4().hex+suffix);target.write_bytes(content)
    try:
        with Image.open(target) as im: im.verify()
    except Exception:
        target.unlink(missing_ok=True);raise HTTPException(400,"Invalid image.")
    detections,status=detect(str(target));cost=estimate(detections)
    iid=save(DB,vehicle_reference,str(target),detections,cost,status)
    return {"inspection_id":iid,"vehicle_reference":vehicle_reference,"detections":detections,
            "estimate_gbp":cost,"model_status":status,
            "disclaimer":"Research output only; qualified assessor review is mandatory."}
@app.get("/inspections")
def list_records(limit:int=100):
    if not 1<=limit<=500: raise HTTPException(400,"limit must be 1..500")
    return recent(DB,limit)
