import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

from gen_rpt.review.groq_reviewer import run_groq_review_file


def parse_args():
    parser = argparse.ArgumentParser(description="Run Groq AI Review on an existing text or markdown report.")
    parser.add_argument("--file", required=True, help="Path to the file you want to review (e.g., report.md)")
    parser.add_argument("--out-dir", default="review_output", help="Output directory for the review artifacts (default: review_output)")
    return parser.parse_args()


def main():
    # Load environment variables from .env file (to get GROQ_API_KEY)
    load_dotenv()
    
    args = parse_args()
    file_path = Path(args.file)
    output_dir = Path(args.out_dir)
    
    if not file_path.exists():
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)
        
    if not file_path.is_file():
        print(f"Error: {file_path} is not a valid file.")
        sys.exit(1)
        
    print(f"Starting review for: {file_path}")
    print(f"Output will be saved to: {output_dir}")
    
    review_data = run_groq_review_file(file_path, output_dir)
    
    if review_data:
        print("\nReview completed successfully!")
        print(f"Overall Score: {review_data.get('scores', {}).get('overall_score')}")
        print(f"Grade: {review_data.get('scores', {}).get('grade')}")
        print(f"\nPlease check the following files in '{output_dir}':")
        print("  - review_report.md")
        print("  - review_summary.txt")
        print("  - review_report.json")
    else:
        print("\nReview failed or was skipped. Please check the logs above.")


if __name__ == "__main__":
    main()
