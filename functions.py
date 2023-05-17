import re
import mailparser

def extract_data(subject, body):
    data = {}
    patterns = {
        "case_number": r"OSRTUS(\d{13})",
        "failed_job": r'\"([^\"]+)\"',
        "iti_notes": r"(?i)good (?:morning|afternoon),\s*(.*?)\s*thank you",
        "model_number": r"([A-Za-z0-9]+)$",
    }

    for key, pattern in patterns.items():
        if key == "iti_notes":
            match = re.search(pattern, body, re.DOTALL)
        else:
            match = re.search(pattern, subject)
        
        if match:
            if key == "case_number":    
                data[key] = "US" + match.group(1)[:-2]
            else:
                data[key] = match.group(1).strip()
        else:
            data[key] = "Not Found"

    return data




def generate_message_logic(job_type, model_number):
    task = ""
    job_label = ""

    model_number = int(model_number[:2])

    if job_type == "Replacement":
        job_label = "Failed Job -> Failed On-Site Repair -> Unsuccessful Repair."
        if model_number <= 55:
            task = "Advance Exchange"
        elif model_number <= 65:
            task = "ADTV"
        elif model_number >= 70:
            task = "OSS"
    elif job_type == "Incorrect Diagnosis":
        job_label = "Failed Job -> Failed On-Site Repair -> Incorrect Diagnosis."
        if model_number <= 55:
            task = "Advance Exchange"
        elif model_number <= 65:
            task = "ADTV"
        elif model_number >= 70:
            task = "OSS"
    elif job_type == "Area not Serviceable":
        job_label = "Failed Job -> Failed On-Site Repair -> Area not serviceable."
        if model_number <= 55:
            task = "Advance Exchange"
        elif model_number <= 65:
            task = "ADTV"
        elif model_number >= 70:
            task = "OSS"
    elif job_type == "Repair":
        job_label = "Failed Job -> Failed On-Site Repair -> Unsuccessful Repair."
        task = "Create another OSR"
    elif job_type == "Physical Damage":
        task = "Contact the EU and inform them that physical damage is not covered under our limited 1 year manufactures warranty. There is nothing more we can do for this serial number."
    elif job_type == "Environment Issue":
        task = "Contact the EU and inform them that Environmental issues, including, but not limited to, insect infestation, are not covered by our 1-year limited manufacturer’s warranty. Unfortunately, there is nothing more we can do about this serial number."

    return task, job_label

def parse_eml(filepath):
    mail = mailparser.parse_from_file(filepath)
    subject = mail.subject
    body = mail.body
    data = extract_data(subject, body)
    return data
