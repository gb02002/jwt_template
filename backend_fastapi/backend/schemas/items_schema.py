from pydantic import BaseModel


class ParsingItem(BaseModel):
    """Валидация для модели Item"""
    id: int

    title: str
    author_id: str
    views: int
    position: int
    ordered_by: int

    class Config:
        orm_mode = True
