from fastapi import UploadFile, File
from pydantic import BaseModel


class MlResponse(BaseModel):
    result: str


class MlFileRequest(BaseModel):
    grammar: bool
    html_formatting: bool


class MlTextRequest(BaseModel):
    text: str
    grammatic: bool
    html_formatting: bool
