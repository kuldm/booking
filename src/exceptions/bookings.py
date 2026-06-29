from fastapi import HTTPException, status


class BookingException(HTTPException):
    """Базовый класс для исключений, связанных с бронированиями."""

    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BookingFailed(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Нет свободных номеров для создания бронирования."
