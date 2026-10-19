import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq

app = Flask(__name__)

# API Key সরাসরি না লিখে এনভায়রনমেন্ট ভেরিয়েবল থেকে নেওয়া হচ্ছে (নিরাপত্তার জন্য)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# বাকি কোড আগের মতোই থাকবে...