from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Column, Field, JSON, SQLModel


class RawClinicalTrial(SQLModel, table=True):
    __tablename__ = "raw_clinical_trials"

    id: str = Field(
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"name": "nct_id"},
    )
    source_url: str = Field(nullable=False)
    time_pulled: datetime = Field(nullable=False)
    json_data: dict = Field(default={}, sa_column=Column(JSON))


class AnalysisResult(SQLModel, table=True):
    __tablename__ = "analysis_results"
   
    __table_args__ = (
        UniqueConstraint("result_type", "result_key", name="uq_analysis_result_key"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_time: datetime = Field(nullable=False, default_factory=datetime.utcnow)
    result_type: str = Field(nullable=False, index=True)
    result_key: str = Field(nullable=False)
    result_value: float = Field(nullable=False)
