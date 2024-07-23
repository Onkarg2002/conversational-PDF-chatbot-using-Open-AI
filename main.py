from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pdf_handler import extract_text_from_pdf
from llm_handler import get_llm_response

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

class QueryRequest(BaseModel):
    question: str
    pdf_text: str

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    content = await file.read()
    pdf_text = extract_text_from_pdf(content)
    
    return {"pdf_text": pdf_text}

@app.post("/query-pdf/")
async def query_pdf(query_request: QueryRequest):
    response = get_llm_response(query_request.question, query_request.pdf_text)
    return JSONResponse(content={"response": response})

@app.get("/")
async def root():
    return FileResponse('static/index.html')
