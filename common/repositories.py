from datetime import datetime
from typing import Dict
from sqlmodel import Session, delete
from common.models import AnalysisResult, RawClinicalTrial


def save_study(session: Session, study_data: dict) -> None:
    nct_id = (
        study_data.get("protocolSection", {})
        .get("identificationModule", {})
        .get("nctId")
    )

    if not nct_id:
        print("Skipping study with no NCT ID.")
        return

    new_trial = RawClinicalTrial(
        id=nct_id,
        source_url=f"https://clinicaltrials.gov/api/v2/studies/{nct_id}",
        time_pulled=datetime.now(),
        json_data=study_data,
    )

    with session.no_autoflush:
        existing_trial = session.get(RawClinicalTrial, nct_id)

    if existing_trial:
        existing_trial.json_data = study_data
        existing_trial.time_pulled = new_trial.time_pulled
        session.add(existing_trial)
        print(f"Updated NCT ID: {nct_id}")
    else:
        session.add(new_trial)
        print(f"Added NCT ID: {nct_id}")


def save_global_analysis_results(
    session: Session,
    counts: Dict[str, int],
    result_type: str
) -> None:

    print(f"Deleting existing results for {result_type}...")
    
    session.exec(
        delete(AnalysisResult).where((AnalysisResult.result_type == result_type))
    )

    now = datetime.utcnow()
    results = [
        AnalysisResult(
            analysis_time=now,
            result_type=result_type,
            result_key=key,
            result_value=float(val),
        )
        for key, val in counts.items()
    ]
    session.add_all(results)
    print(f"Added {len(results)} analysis results ({result_type}).")
