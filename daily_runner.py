from library import *
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")

    USER = os.environ.get("GMAIL_USER")
    PASSWORD = os.environ.get("GMAIL_PASSWORD")
    RECIPIENTS = os.environ.get("RECIPIENTS")
    subscriptions = {
        "quant-ph": ["cs.LG", "cs.CV", "cs.AI", "cs.GR", ],
    }

    HTML = renderer(subscriptions)
    for RECIPIENT in RECIPIENTS:
        sender(HTML, RECIPIENT, USER, PASSWORD)
