from common.db import create_db_and_tables, get_session
from common.analysis import run_condition_count_analysis, run_keyword_count_analysis 

def run_all_analysis():
    create_db_and_tables()
    
    try:
        with get_session() as session:
                        
            print("Starting all analysis tasks...")

            print("-> Running Keyword Count Analysis...")
            run_keyword_count_analysis(session)
            
            print("-> Running Grouping and Filtering Analysis...")
            run_condition_count_analysis(session)
            
            session.commit()
            
            print("All analysis tasks completed and committed successfully.")
            
    except Exception as e:
     
        print(f"A critical error occurred during analysis. ROLLED BACK.")
        print(f"Error details: {e}")
        raise 


if __name__ == "__main__":
    run_all_analysis()