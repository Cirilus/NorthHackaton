import io
import os
from docx import Document
from fastapi import UploadFile, HTTPException, APIRouter, File, Depends
from starlette import status

from schemas.ML import MlResponse, MlTextRequest, MlFileRequest

router = APIRouter(prefix="/api/v1/ml", tags=["ml"])


@router.post(
    "/file",
    response_model=MlResponse,
 )
async def get_file(req: MlFileRequest = Depends(), file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in {".txt", ".docx"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a .txt or .docx file")
    text = ""

    if file_extension == ".txt":
        text = await file.read()
        text = text.decode("utf-8")

    if file_extension == ".docx":
        docx_content = await file.read()
        docx_document = Document(io.BytesIO(docx_content))
        text = "\n".join([para.text for para in docx_document.paragraphs])

    if text == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the file must not to be empty")

    return {
        "result": text,
    }


@router.post(
    "/text",
    response_model=MlResponse,
)
async def get_text(req: MlTextRequest):

    if req.text == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the file must not to be empty")
    return {
        "result": req.text,
    }
