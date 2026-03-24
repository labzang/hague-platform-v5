"""경기 일정(Schedule) Pydantic DTO."""

from typing import Optional

from pydantic import BaseModel, Field


class ScheduleDTO(BaseModel):
    """경기 일정 정보를 전송하기 위한 Pydantic DTO.

    SQLAlchemy ScheduleModel과 매핑되는 응답/전달 객체입니다.
    """

    id: Optional[int] = Field(None, description="경기 일정 고유 식별자")
    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    hometeam_id: Optional[int] = Field(None, description="홈팀 ID")
    awayteam_id: Optional[int] = Field(None, description="원정팀 ID")
    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    sche_date: Optional[str] = Field(None, description="경기 일자", max_length=10)
    gubun: Optional[str] = Field(None, description="구분", max_length=10)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    awayteam_code: Optional[str] = Field(None, description="원정팀 코드", max_length=10)
    home_score: Optional[int] = Field(None, description="홈팀 점수")
    away_score: Optional[int] = Field(None, description="원정팀 점수")

    class Config:
        """Pydantic 설정."""

        from_attributes = True


class ScheduleCreateDTO(BaseModel):
    """경기 일정 생성 요청 DTO."""

    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    hometeam_id: Optional[int] = Field(None, description="홈팀 ID")
    awayteam_id: Optional[int] = Field(None, description="원정팀 ID")
    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    sche_date: Optional[str] = Field(None, description="경기 일자", max_length=10)
    gubun: Optional[str] = Field(None, description="구분", max_length=10)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    awayteam_code: Optional[str] = Field(None, description="원정팀 코드", max_length=10)
    home_score: Optional[int] = Field(None, description="홈팀 점수")
    away_score: Optional[int] = Field(None, description="원정팀 점수")


class ScheduleUpdateDTO(BaseModel):
    """경기 일정 수정 요청 DTO."""

    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    hometeam_id: Optional[int] = Field(None, description="홈팀 ID")
    awayteam_id: Optional[int] = Field(None, description="원정팀 ID")
    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    sche_date: Optional[str] = Field(None, description="경기 일자", max_length=10)
    gubun: Optional[str] = Field(None, description="구분", max_length=10)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    awayteam_code: Optional[str] = Field(None, description="원정팀 코드", max_length=10)
    home_score: Optional[int] = Field(None, description="홈팀 점수")
    away_score: Optional[int] = Field(None, description="원정팀 점수")
