"""
Main Execution Pipeline for Novel RAG System
Generates predictions for test dataset
Submission format: Story ID | Prediction | Rationale
"""

import pandas as pd
from typing import Dict
import time
from src.graph_agent import graph


def extract_short_rationale(final_answer: str) -> str:
    """Limit rationale length to keep CSV clean"""
    text = final_answer.strip()
    
    if not text:
        return ""
    
    # Take first 2 lines if multi-line
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    if non_empty_lines:
        rationale = '. '.join(non_empty_lines[:2])
    else:
        rationale = text
    
    # Limit to 150 characters
    if len(rationale) > 150:
        rationale = rationale[:147] + "..."
    
    return rationale


def run_verification(backstory: str, character: str, book_name: str, max_retries: int = 5) -> Dict:
    """Run graph agent for backstory verification with retry logic"""
    print(f"\n{'='*80}")
    print(f"📖 Book: {book_name}")
    print(f"👤 Character: {character}")
    print(f"📄 Backstory: {backstory[:100]}...")
    print(f"{'='*80}")
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = graph.invoke({
                "backstory": backstory,
                "character": character,
                "book_name": book_name,
                "queries": [],
                "retrieved_docs": [],
                "final_answer": "",
                "verdict": ""
            })
            
            prediction = result.get("verdict", "consistent")
            
            print(f"\n🎯 Prediction: {prediction}")
            print(f"📝 Rationale: {result['final_answer'][:200]}...")
            
            return {
                "prediction": prediction,
                "rationale": result["final_answer"]
            }
        
        except Exception as e:
            last_error = str(e)
            print(f"❌ Error on attempt {attempt + 1}/{max_retries}: {last_error}")
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 3
                print(f"⏳ Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    
    # If all retries failed, return fallback
    print(f"❌ Failed after {max_retries} attempts. Using default prediction.")
    return {
        "prediction": "consistent",
        "rationale": f"Processing failed after {max_retries} attempts. Error: {last_error}"
    }


def main():
    """Main pipeline - generates results.csv in submission format with guaranteed processing of all rows"""
    print("🚀 Starting Novel RAG Verification System")
    print("="*80)
    
    from config.config import TEST_DATA
    test_df = pd.read_csv(TEST_DATA)
    print(f"📊 Loaded {len(test_df)} test cases")
    
    results = []
    processed_count = 0
    failed_count = 0
    
    for idx, row in test_df.iterrows():
        row_num = int(idx) if isinstance(idx, (int, float)) else 0
        print(f"\n{'#'*80}")
        print(f"Processing {row_num + 1}/{len(test_df)} - ID: {row['id']}")
        print(f"{'#'*80}")
        
        # This will retry until success or max retries reached
        verification = run_verification(
            backstory=row["content"],
            character=row["char"],
            book_name=row["book_name"],
            max_retries=5  # Will try 5 times with increasing delays
        )
        
        short_rationale = extract_short_rationale(verification["rationale"])
        
        prediction_numeric = 1 if verification["prediction"] == "consistent" else 0
        
        results.append({
            "story_id": row["id"],
            "prediction": prediction_numeric,
            "rationale": short_rationale
        })
        
        if "failed after" in verification["rationale"].lower():
            failed_count += 1
            print(f"⚠️  Row {row_num + 1} completed with fallback prediction")
        else:
            processed_count += 1
            print(f"✅ Row {row_num + 1} successfully processed")
        
        print(f"📊 Progress: {row_num + 1}/{len(test_df)} | Success: {processed_count} | Fallback: {failed_count}")
    
    results_df = pd.DataFrame(results)
    
    results_file = "results.csv"
    results_df.to_csv(results_file, index=False)
    print(f"\n{'='*80}")
    print(f"✅ Submission file saved: {results_file}")
    print(f"📊 Total predictions: {len(results_df)}")
    print(f"✅ Successfully processed: {processed_count}")
    print(f"⚠️  Fallback predictions: {failed_count}")
    print(f"🎯 All {len(test_df)} rows guaranteed to be in results")
    print(f"{'='*80}")
    
    print(f"\n📋 Sample Predictions:")
    print(results_df.head(5).to_string(index=False))
    
    return results_df


if __name__ == "__main__":
    import requests
    
    from config.config import PATHWAY_HOST, PATHWAY_PORT_CASTAWAYS
    print("🔍 Checking if Pathway Vector Store server is running...")
    try:
        response = requests.post(
            f"http://{PATHWAY_HOST}:{PATHWAY_PORT_CASTAWAYS}/v1/retrieve",
            json={"query": "test", "k": 1},
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Pathway Server is running!")
        else:
            raise Exception(f"Server returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("   Use: python run.py (for automated setup)")
        print("   Or: docker-compose up --build (manual)")
        exit(1)
    except Exception as e:
        print(f"❌ Server error: {e}")
        exit(1)
    
    results = main()
