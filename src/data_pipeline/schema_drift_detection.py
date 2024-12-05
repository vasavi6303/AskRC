import os
import re
import json
import uuid
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename="schema_drift.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

reference_schema = {
    "id": "string",
    "content": "string",
    # Add other known fields if applicable
}

# Save the reference schema to a JSON file
with open("reference_schema.json", "w") as file:
    json.dump(reference_schema, file, indent=4)


def detect_schema_drift(new_document, reference_schema_path="reference_schema.json"):
    """
    Detect schema drift by comparing the new document's schema with the reference schema.
    """
    # Load the reference schema
    with open(reference_schema_path, "r") as file:
        reference_schema = json.load(file)

    # Extract the keys of the new document
    new_keys = set(new_document.keys())
    reference_keys = set(reference_schema.keys())

    # Detect added or missing keys
    added_keys = new_keys - reference_keys
    missing_keys = reference_keys - new_keys

    if added_keys or missing_keys:
        print(f"Schema drift detected!")
        if added_keys:
            print(f"New keys added: {added_keys}")
        if missing_keys:
            print(f"Keys missing: {missing_keys}")

        # Log the schema drift
        log_schema_drift(added_keys, missing_keys)  # Log drift details

        # Update reference schema (optional, depends on your workflow)
        reference_schema.update({key: "unknown" for key in added_keys})
        with open(reference_schema_path, "w") as file:
            json.dump(reference_schema, file, indent=4)
            print("Reference schema updated.")
        
        return True  # Indicates schema drift
    else:
        print("No schema drift detected.")
        return False  # No drift

def log_schema_drift(added_keys, missing_keys):
    """
    Log schema drift details to a file.
    """
    if added_keys:
        logging.info(f"Schema drift detected: Added keys - {added_keys}")
    if missing_keys:
        logging.info(f"Schema drift detected: Missing keys - {missing_keys}")