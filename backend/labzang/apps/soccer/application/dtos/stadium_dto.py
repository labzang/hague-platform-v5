"""경기장(Stadium) Pydantic DTO."""

from typing import Optional

from pydantic import BaseModel, Field


class StadiumDTO(BaseModel):
    """경기장 정보를 전송하기 위한 Pydantic DTO.

    SQLAlchemy StadiumModel과 매핑되는 응답/전달 객체입니다.
    """

    id: Optional[int] = Field(None, description="경기장 고유 식별자")
    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    stadium_name: Optional[str] = Field(None, description="경기장 이름", max_length=40)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    seat_count: Optional[int] = Field(None, description="좌석 수")
    address: Optional[str] = Field(None, description="주소", max_length=60)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)

    class Config:
        """Pydantic 설정."""

        from_attributes = True


class StadiumCreateDTO(BaseModel):
    """경기장 생성 요청 DTO."""

    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    stadium_name: Optional[str] = Field(None, description="경기장 이름", max_length=40)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    seat_count: Optional[int] = Field(None, description="좌석 수")
    address: Optional[str] = Field(None, description="주소", max_length=60)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)


class StadiumUpdateDTO(BaseModel):
    """경기장 수정 요청 DTO."""

    stadium_code: Optional[str] = Field(None, description="경기장 코드", max_length=10)
    stadium_name: Optional[str] = Field(None, description="경기장 이름", max_length=40)
    hometeam_code: Optional[str] = Field(None, description="홈팀 코드", max_length=10)
    seat_count: Optional[int] = Field(None, description="좌석 수")
    address: Optional[str] = Field(None, description="주소", max_length=60)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)
