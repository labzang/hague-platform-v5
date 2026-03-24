"""팀(Team) Pydantic DTO."""

from typing import Optional

from pydantic import BaseModel, Field


class TeamDTO(BaseModel):
    """팀 정보를 전송하기 위한 Pydantic DTO.

    SQLAlchemy TeamModel과 매핑되는 응답/전달 객체입니다.
    """

    id: Optional[int] = Field(None, description="팀 고유 식별자")
    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    team_code: Optional[str] = Field(None, description="팀 코드", max_length=10)
    region_name: Optional[str] = Field(None, description="지역명", max_length=10)
    team_name: Optional[str] = Field(None, description="팀명", max_length=40)
    e_team_name: Optional[str] = Field(None, description="영문 팀명", max_length=50)
    orig_yyyy: Optional[str] = Field(None, description="창단년도", max_length=10)
    zip_code1: Optional[str] = Field(None, description="우편번호1", max_length=10)
    zip_code2: Optional[str] = Field(None, description="우편번호2", max_length=10)
    address: Optional[str] = Field(None, description="주소", max_length=80)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)
    fax: Optional[str] = Field(None, description="팩스번호", max_length=20)
    homepage: Optional[str] = Field(None, description="홈페이지", max_length=100)
    owner: Optional[str] = Field(None, description="구단주", max_length=50)

    class Config:
        """Pydantic 설정."""

        from_attributes = True


class TeamCreateDTO(BaseModel):
    """팀 생성 요청 DTO."""

    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    team_code: Optional[str] = Field(None, description="팀 코드", max_length=10)
    region_name: Optional[str] = Field(None, description="지역명", max_length=10)
    team_name: Optional[str] = Field(None, description="팀명", max_length=40)
    e_team_name: Optional[str] = Field(None, description="영문 팀명", max_length=50)
    orig_yyyy: Optional[str] = Field(None, description="창단년도", max_length=10)
    zip_code1: Optional[str] = Field(None, description="우편번호1", max_length=10)
    zip_code2: Optional[str] = Field(None, description="우편번호2", max_length=10)
    address: Optional[str] = Field(None, description="주소", max_length=80)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)
    fax: Optional[str] = Field(None, description="팩스번호", max_length=20)
    homepage: Optional[str] = Field(None, description="홈페이지", max_length=100)
    owner: Optional[str] = Field(None, description="구단주", max_length=50)


class TeamUpdateDTO(BaseModel):
    """팀 수정 요청 DTO."""

    stadium_id: Optional[int] = Field(None, description="경기장 ID")
    team_code: Optional[str] = Field(None, description="팀 코드", max_length=10)
    region_name: Optional[str] = Field(None, description="지역명", max_length=10)
    team_name: Optional[str] = Field(None, description="팀명", max_length=40)
    e_team_name: Optional[str] = Field(None, description="영문 팀명", max_length=50)
    orig_yyyy: Optional[str] = Field(None, description="창단년도", max_length=10)
    zip_code1: Optional[str] = Field(None, description="우편번호1", max_length=10)
    zip_code2: Optional[str] = Field(None, description="우편번호2", max_length=10)
    address: Optional[str] = Field(None, description="주소", max_length=80)
    ddd: Optional[str] = Field(None, description="지역번호", max_length=10)
    tel: Optional[str] = Field(None, description="전화번호", max_length=20)
    fax: Optional[str] = Field(None, description="팩스번호", max_length=20)
    homepage: Optional[str] = Field(None, description="홈페이지", max_length=100)
    owner: Optional[str] = Field(None, description="구단주", max_length=50)
