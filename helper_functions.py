import csv
import sys
import datetime


def clean_string(string_sample):
    return str(string_sample).replace("{", "").replace("}", "")

def evaluate_staging(parameter, average, recommendation, cutoffs):
    """Evaluate the staging status and return explanation and status level."""
    if average > cutoffs[1]:
        text = (
            f"{parameter}-Status kann aus den Angaben adäquat bestimmt werden. "
            "Keine Korrekturen notwendig!"
        )
        status = "good"
    elif cutoffs[0] < average <= cutoffs[1]:
        text = (
            f"Angaben bzgl. des {parameter}-Status sind etwas uneindeutig."
            f"Bitte überprüfe, ob du den Befund auf Basis der folgenden Empfehlung korrigieren kannst:\n\"{recommendation}\""
        )
        status = "medium"
    else:
        text = (
            f"Angaben bzgl. des {parameter}-Status erscheinen insuffizient. "
            f"Befund bitte anhand der folgenden LLM-generierten Empfehlung verbessern:\n\"{recommendation}\""
        )
        status = "bad"
    return text, status

def save_text_to_file(text):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"\n=== {timestamp} ===\n{text.strip()}\n"
    with open("submitted_reports.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
