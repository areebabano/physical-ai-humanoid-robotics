#!/usr/bin/env python3
"""
Script to run the content ingestion pipeline for the Physical AI Humanoid Robotics book.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Starting content ingestion pipeline...")

    try:
        # Import and run the ingestion module
        from content_ingestion import ingest_book

        print("Beginning book ingestion process...")
        ingest_book()

        print("Content ingestion completed successfully!")

    except ImportError as e:
        print(f"Error importing content_ingestion module: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during content ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()