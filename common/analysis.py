from typing import Any, Dict, Iterable, List, Optional
from collections import Counter
from sqlmodel import Session, select
from common.models import RawClinicalTrial
from common.repositories import save_global_analysis_results

CONDITION_COUNT_TYPE = "GLOBAL_CONDITION_COUNT"
GLOBAL_RESULT_TYPE = "GLOBAL_KEYWORD_COUNT"
GLOBAL_KEYWORDS = ["Cancer", "Phase3", "Vaccine"]

def compute_keyword_counts(
    trials: Iterable[RawClinicalTrial],
    keywords: Optional[List[str]] = None,
) -> Dict[str, int]:
    use_keywords = keywords or GLOBAL_KEYWORDS
    counts = {k: 0 for k in use_keywords}

    for trial in trials:
        data: Dict[str, Any] = trial.json_data

        conditions_module = data.get("protocolSection", {}).get("conditionsModule", {})
        design_module = data.get("protocolSection", {}).get("designModule", {})

        keywords_to_check: List[str] = []
        keywords_to_check.extend(conditions_module.get("keywords", []))
        keywords_to_check.extend(conditions_module.get("conditions", []))
        keywords_to_check.extend(design_module.get("phases", []))

        lower_items = [
            item.lower() for item in keywords_to_check if isinstance(item, str)
        ]
        for keyword in use_keywords:
            key_lower = keyword.lower()
            if any(key_lower in item for item in lower_items):
                counts[keyword] += 1

    return counts


def run_keyword_count_analysis(session: Session, keywords: Optional[List[str]] = None):
    raw_trials = session.exec(select(RawClinicalTrial)).all()
    counts = compute_keyword_counts(raw_trials, keywords)
    save_global_analysis_results(session, counts, result_type=GLOBAL_RESULT_TYPE)


def run_condition_count_analysis(session: Session) -> None:
    print("Starting global condition count analysis...")
    
    trials = session.exec(select(RawClinicalTrial)).all()
     
    condition_counter = Counter()

    for trial in trials:
        try:
            trial_data = trial.json_data
            protocol_section = trial_data.get('protocolSection', {})
            conditions_module = protocol_section.get('conditionsModule', {})
            conditions_list = conditions_module.get('conditions', [])           
            print(f"trial_data {conditions_list}")

            condition_counter.update(conditions_list)
                
        except Exception as e:
            print(f"Warning: Could not process trial data for {trial.nct_id if hasattr(trial, 'nct_id') else 'Unknown ID'}. Error: {e}")
            continue

    print(f"Finished counting. Found {len(condition_counter)} unique conditions.")

    save_global_analysis_results(session, dict(condition_counter), CONDITION_COUNT_TYPE)
