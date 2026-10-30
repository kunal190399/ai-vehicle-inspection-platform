import requests,streamlit as st,pandas as pd
st.title("AI Vehicle Inspection")
st.warning("Research prototype. AI outputs are not repair approvals or customer quotations.")
api=st.sidebar.text_input("API URL","http://127.0.0.1:8000")
ref=st.text_input("Vehicle / job reference","DEMO-001")
img=st.file_uploader("Vehicle image",type=["jpg","jpeg","png","webp"])
if img and st.button("Run inspection"):
    try:
        r=requests.post(api+"/inspections",data={"vehicle_reference":ref},
          files={"image":(img.name,img.getvalue(),img.type)},timeout=120)
        r.raise_for_status();st.json(r.json())
    except requests.RequestException as e: st.error(str(e))
if st.button("Refresh inspection history"):
    try:
        data=requests.get(api+"/inspections",timeout=15).json()
        st.dataframe(pd.DataFrame(data),use_container_width=True) if data else st.info("No records yet.")
    except requests.RequestException as e: st.error(str(e))
