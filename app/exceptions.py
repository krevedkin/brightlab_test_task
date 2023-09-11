from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = ""
    headers = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
