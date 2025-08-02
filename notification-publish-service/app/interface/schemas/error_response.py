from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Erro ao enviar notificação.")
