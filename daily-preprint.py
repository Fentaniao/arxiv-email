from emailgen import *
import os
from dotenv import load_dotenv


load_dotenv(".env")

USER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")
RECIPIENT = os.environ.get("RECIPIENT")
subscriptions = ["quant-ph", ]

send_email(RECIPIENT,subscriptions,USER,PASSWORD)
