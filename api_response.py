# api_response.py
from datetime import datetime

class ApiResponse:
    def __init__(self, success, data=None, error=None, meta=None):
        self.success = success
        self.data = data
        self.error = error
        self.meta = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **(meta or {})
        }

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "meta": self.meta,
        }

    @staticmethod
    def success(data=None, meta=None):
        return ApiResponse(True, data=data, error=None, meta=meta).to_dict()

    @staticmethod
    def error(code, message, meta=None):
        return ApiResponse(False, data=None, error={"code": code, "message": message}, meta=meta).to_dict()
