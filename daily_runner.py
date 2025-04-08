from library import *
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")

    USER = os.environ.get("GMAIL_USER")
    PASSWORD = os.environ.get("GMAIL_PASSWORD")
    FREELOADERS = os.environ.get("FREELOADERS").split('\n')

    for FREELOADER in FREELOADERS:
        RECIPIENT = FREELOADER.split(':')[0]
        SUBSCRIPTIONS = {
            PART.split(',')[0]: PART.split(',')[1:]
            for PART in FREELOADER.split(':')[1:]
        }

        HTML = renderer(SUBSCRIPTIONS)
        sender(HTML, RECIPIENT, USER, PASSWORD)


    # FREELOADERS variable should be structured like:
    # example0@gmail.com:primary1,secondary11,secondary12:primary2:primary3,secondary31
    # example1@gmail.com:quant-ph,cs.LG,cs.CV,cs.AI,cs.GR:math.AG
    # example2@gmail.com:math.NT
    # The resolution of the above example would be:
    # SUBSCRIPTIONS0 = {
    #     "primary1": ["secondary11", "secondary12", "cs.AI", "cs.GR", ],
    #     "primary2": [],
    #     "primary3": ["secondary31", ],
    # }
    # SUBSCRIPTIONS1 = {
    #     "quant-ph": ["cs.LG", "cs.CV", "cs.AI", "cs.GR", ],
    #     "math.AG": [],
    # }
    # SUBSCRIPTIONS2 = {
    #     "math.NT": [],
    # }
