
import spacy
import re
import ipaddress

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


# 1. Text preprocessing
def preprocess_text(text):

    text = str(text).lower()

    text = re.sub(r'<[^>]+>', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# 2. Tokenization
def tokenize_text(text):

    doc = nlp(text)

    tokens = [
        token.text
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
    ]

    return tokens


# 3. Named Entity Recognition
def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({
            "entity": ent.text,
            "type": ent.label_
        })

    return entities


# 4. IOC Extraction
def extract_iocs(text):

    patterns = {

        "IP Address":
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',

        "Email":
        r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b',

        "CVE":
        r'\bCVE-\d{4}-\d{4,7}\b',

        "Hash":
        r'\b(?:[a-fA-F0-9]{32}|'
        r'[a-fA-F0-9]{40}|'
        r'[a-fA-F0-9]{64})\b',

        "Domain":
        r'\b(?:[a-zA-Z0-9-]+\.)+'
        r'[a-zA-Z]{2,}\b'
    }

    results = {}

    for category, pattern in patterns.items():

        matches = re.findall(pattern, text)

        if category == "IP Address":

            valid = []

            for ip in matches:
                try:
                    ipaddress.ip_address(ip)
                    valid.append(ip)
                except ValueError:
                    pass

            matches = valid

        results[category] = list(set(matches))

    return results


# 5. Threat Classification
def classify_threat(text):

    categories = {

        "Ransomware": [
            "ransomware", "encrypted files",
            "ransom demand"
        ],

        "Data Breach": [
            "stolen data", "data leak",
            "database stolen"
        ],

        "Credential Theft": [
            "stolen credentials", "passwords",
            "login credentials"
        ],

        "Phishing": [
            "phishing", "fake login",
            "malicious email"
        ],

        "Malware": [
            "malware", "trojan",
            "spyware"
        ],

        "DDoS": [
            "ddos", "denial of service"
        ]
    }

    detected = []

    for category, keywords in categories.items():

        if any(keyword in text for keyword in keywords):
            detected.append(category)

    return detected if detected else ["Unclassified"]


# 6. Risk Assessment
def calculate_risk(threats, iocs):

    high_risk = [
        "Ransomware",
        "Data Breach",
        "Credential Theft"
    ]

    medium_risk = [
        "Phishing",
        "Malware",
        "DDoS"
    ]

    score = 0

    for threat in threats:

        if threat in high_risk:
            score += 30

        elif threat in medium_risk:
            score += 15

    ioc_count = sum(
        len(values) for values in iocs.values()
    )

    score += min(ioc_count * 5, 20)

    if score >= 50:
        return "High"

    elif score >= 20:
        return "Medium"

    return "Low"


# 7. Complete NLP Analysis
def analyze_text(text):

    cleaned = preprocess_text(text)

    tokens = tokenize_text(cleaned)

    entities = extract_entities(cleaned)

    iocs = extract_iocs(cleaned)

    threats = classify_threat(cleaned)

    risk = calculate_risk(threats, iocs)

    return {
        "tokens": tokens,
        "entities": entities,
        "iocs": iocs,
        "threats": threats,
        "risk": risk
    }
