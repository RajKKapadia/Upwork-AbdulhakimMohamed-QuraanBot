import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
FROM = os.getenv('FROM')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

ERROR_MESSAGE = 'We are facing technical issue at this moment.'
CONSENT_MESSAGE = "As-Salamu 'Alaikum wa Rahmatullahi wa Barakatuh,\n\nThanks for trying out Deen Duo,\n\nDrawing from Tafsir Ibn Kathir, this chat allows easy access to a deeper understanding of Islam through the teachings of the Quran.\n\nWant to try it out for free?"
FINAL_MESSAGE = "Thank you!\n\nAs your scholarly companion, I am here to provide guidance, impart wisdom, and lend support for both life's trials and its blessings.\n\nI kindly request your patience, as it may take me a few moments for me to respond.\n\nTo ensure a smooth conversation, please send one message at a time.\n\nNow, what would you like to talk about first?"

DATABASE_NAME = 'QuranaWhatsApp'
COLLECTION_NAME = 'Users'
