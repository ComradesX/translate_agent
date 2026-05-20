from pydantic import BaseModel, Field, field_validator


class TranslationReviewResponse(BaseModel):
    score: int = Field(description="AI 给用户翻译的评分，范围 0~100")
    comment: str = Field(description="AI 对用户翻译的点评")

    @field_validator("score")
    @classmethod
    def validate_score(cls, value: int) -> int:
        if value < 0 or value > 100:
            raise ValueError("score must be in range 0~100")
        return value

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("comment must not be empty")
        return value
