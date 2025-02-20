from library import *
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")

    USER = os.environ.get("GMAIL_USER")
    PASSWORD = os.environ.get("GMAIL_PASSWORD")
    RECIPIENT = os.environ.get("RECIPIENT")
    subscriptions = ["quant-ph", ]

    HTML = renderer(subscriptions)
    sender(HTML, RECIPIENT, USER, PASSWORD)
