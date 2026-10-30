import os
from pathlib import Path
def detect(image_path):
    weights=os.getenv("DAMAGE_MODEL_PATH")
    if not weights or not Path(weights).exists(): return [],"not_configured"
    from ultralytics import YOLO
    model=YOLO(weights); results=model.predict(image_path,verbose=False)
    rows=[]
    for r in results:
        for box in r.boxes or []:
            cid=int(box.cls.item())
            rows.append({"label":str(r.names.get(cid,cid)),"confidence":float(box.conf.item()),
                         "bbox_xyxy":[float(x) for x in box.xyxy[0].tolist()]})
    return rows,"configured"
def estimate(detections):
    path=os.getenv("COST_MODEL_PATH")
    if not path or not Path(path).exists() or not detections:return None
    import joblib,pandas as pd
    from sklearn.pipeline import Pipeline
    top=max(detections,key=lambda x:x["confidence"])
    label=top["label"] if top["label"] in {"scratch","dent","crack","broken_glass","missing_part"} else "dent"
    row={"damage_type":label,"component":"bumper","severity":"moderate","panels_affected":1,
         "labour_hours":3.0,"parts_required":int(label in {"broken_glass","missing_part"}),
         "paint_required":int(label in {"scratch","dent","crack"}),"vehicle_age_years":5,
         "image_damage_area_ratio":None,"image_model_confidence":top["confidence"]}
    return round(float(joblib.load(path).predict(pd.DataFrame([row]))[0]),2)
