from fastapi import FastAPI, UploadFile, File, HTTPException, Response

import json
import pandas as pd
import sys

sys.path = [
  "/home/abhishek/Documents/Study/dmml_assignment/group_4_dmml",
]
from config import RAW_API_DIR


app = FastAPI()

RAW_API_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    dest = RAW_API_DIR / "products_api.json"

    filename = file.filename.lower()

    try:
        # -----------------------------
        # Case 1: CSV uploaded
        # -----------------------------
        if filename.endswith(".csv"):
            contents = await file.read()

            # Read CSV into DataFrame
            df = pd.read_csv(pd.io.common.BytesIO(contents))

            # Convert to list of dicts (JSON)
            data = df.to_dict(orient="records")

            with open(dest, "w") as f:
                json.dump(data, f, indent=2)

        # -----------------------------
        # Case 2: JSON uploaded
        # -----------------------------
        elif filename.endswith(".json"):
            contents = await file.read()
            data = json.loads(contents)

            with open(dest, "w") as f:
                json.dump(data, f, indent=2)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only CSV or JSON files are supported"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "uploaded_file": file.filename,
        "saved_as": str(dest)
    }

@app.get("/products")
async def get_products():
    dest = RAW_API_DIR / "products_api.json"
    if not dest.exists():
        raise HTTPException(status_code=404, detail="No data")

    df = pd.read_json(dest)
    
    json_str = df.to_json(orient="records")
    
    return Response(content=json_str, media_type="application/json")
