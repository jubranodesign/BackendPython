from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from common.db import get_session
from common.models import AnalysisResult, RawClinicalTrial
from sqlalchemy.sql import func 

app = FastAPI()

@app.get(
    "/analysis/results/",
    response_model=List[AnalysisResult]  
)
def get_analysis_results(
    session: Session = Depends(get_session),
    result_type: Optional[str] = Query(None)
):
   
    statement = select(AnalysisResult)
    if result_type:
        statement = statement.where(func.lower(AnalysisResult.result_type) == result_type.lower())
    statement = statement.order_by(AnalysisResult.result_value.desc())
    results = session.exec(statement).all()
    return results


@app.get(
    "/trials/",
    response_model=List[RawClinicalTrial]
)
def read_raw_trials(
    session: Session = Depends(get_session),
    nct_id: Optional[str] = Query(None)
):
    
    statement = select(RawClinicalTrial)
    if nct_id:
        statement = statement.where(RawClinicalTrial.nct_id == nct_id)
    trials = session.exec(statement).all()
    return trials