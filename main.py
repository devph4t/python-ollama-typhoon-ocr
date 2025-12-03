from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from api_response import ApiResponse
from typhoon_ocr import prepare_ocr_messages
from openai import OpenAI
import tempfile
import shutil
import json
import re
app = FastAPI()

@app.get("/")
async def root_get():
    return JSONResponse(
        ApiResponse.success(
            data={"message": "OCR API is running"},
            meta={"endpoint": "GET /"}
        )
    )

@app.post("/ocr/upload")
async def ocr_upload(file: UploadFile = File(...)):
    try:
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        # Prepare OCR input
        messages = prepare_ocr_messages(
            pdf_or_image_path=temp_path,
            task_type="default",
            page_num=1
        )

        # OCR Client (Ollama)
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="not-needed"
        )

        response = client.chat.completions.create(
            model="scb10x/typhoon-ocr-3b:latest",
            messages=messages,
            max_tokens=16000,
            extra_body={
                "repetition_penalty": 1.2,
                "temperature": 0.1,
                "top_p": 0.6,
            },
        )

        # Extract OCR text from response
        ocr_text = response.choices[0].message.content
        print("OCR Text:", ocr_text)
        print("OCR Text Type:", type(ocr_text))

        # string to JSON
        ocr_data = json.loads(ocr_text)
        natural_text = ocr_data.get("natural_text", "")
        print("Natural Text:", natural_text)

        # extract license plate info
        lines = natural_text.split("\n")
        plate_line = lines[0] if len(lines) > 0 else ""
        province_line = lines[1] if len(lines) > 1 else ""
        plate_match = re.match(r"([ก-ฮ\d]+)\s*(\d+)", plate_line)
        if plate_match:
            plate_letters = plate_match.group(1)
            plate_number = plate_match.group(2)
        else:
            plate_letters = ""
            plate_number = ""

        province = province_line

        # 5. Print results
        print("Plate Letters:", plate_letters)
        print("Plate Number:", plate_number)
        print("Province:", province)


        # Success response
        return JSONResponse(
            ApiResponse.success(
                data={
                    "ocr_text": ocr_text,
                    "plate":{
                        "plate_letters": plate_letters,
                        "plate_number": plate_number,
                        "province": province
                    }
                },
                meta={"fileName": file.filename}
            )
        )

    except Exception as e:
        return JSONResponse(
            ApiResponse.error(
                code="OCR_ERROR",
                message=str(e)
            ),
            status_code=500
        )
