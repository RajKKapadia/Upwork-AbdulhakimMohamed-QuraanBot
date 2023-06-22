import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
FROM = os.getenv('FROM')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

## Not reading the indexes anymore
# DB_DIR = 'data/db'
# INPUT_FILE_PATH = 'data/input/sample.pdf'
# OUTPUT_DIR = 'data/output'

DATABASE_NAME = 'QuranaWhatsApp'
COLLECTION_NAME = 'Users'
