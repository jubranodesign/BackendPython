from common.db import create_db_and_tables, get_session
from common.repositories import save_study
from scraper_api import fetch_studies


def run_scraper(page_size: int = 5) -> None:
    create_db_and_tables()

    print("🔗 Starting data pull from API")
    studies = fetch_studies(page_size=page_size)
    print(f"📦 Successfully pulled {len(studies)} studies.")

    try:
        with get_session() as session:
            for study in studies:
                save_study(session, study)
            session.commit()
            print("--- Transaction committed successfully. ---")
    except Exception as e:
        print(f"An error occurred during DB operation: {e}")


if __name__ == "__main__":
    run_scraper()