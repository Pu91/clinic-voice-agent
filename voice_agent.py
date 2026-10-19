import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq

app = Flask(__name__)

# Render-এর Environment Variables থেকে নিরাপদভাবে API Key নেওয়া হচ্ছে
groq_api_key = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# ১. কেউ কল করলে Twilio প্রথমে এই লিংকে হিট করবে
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    
    greeting = "নমস্কার! শিলিগুড়ি সিটি ক্লিনিক থেকে বলছি। আজ আপনাকে কীভাবে সাহায্য করতে পারি?"
    resp.say(greeting, language="bn-IN", voice="Polly.Aditi")
    
    resp.gather(input="speech", action="/process_speech", language="bn-IN", timeout=3)
    
    return str(resp)

# ২. রোগীর কথা শুনে Groq-এর মাধ্যমে উত্তর তৈরি করা
@app.route("/process_speech", methods=['GET', 'POST'])
def process_speech():
    user_speech = request.values.get("SpeechResult", "")
    resp = VoiceResponse()

    if user_speech:
        system_prompt = """
        তুমি শিলিগুড়ি সিটি ক্লিনিকের একজন প্রফেশনাল রিসেপশনিস্ট। 
        রোগীর সাথে শুধু বাংলায় কথা বলবে। তোমার উত্তরগুলো হবে খুব ছোট এবং টু-দ্য-পয়েন্ট (১-২ লাইনের মধ্যে), কারণ তুমি ফোনে কথা বলছো।
        রোগীর সমস্যা শুনে তার নাম ও সময় জেনে অ্যাপয়েন্টমেন্ট বুক করতে সাহায্য করো।
        """
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_speech}
            ],
            model="llama3-8b-8192", 
        )
        
        bot_reply = chat_completion.choices[0].message.content
        
        resp.say(bot_reply, language="bn-IN", voice="Polly.Aditi")
        
        resp.gather(input="speech", action="/process_speech", language="bn-IN", timeout=3)
        
    else:
        resp.say("আমি ঠিক বুঝতে পারলাম না, দয়া করে আরেকবার বলবেন?", language="bn-IN", voice="Polly.Aditi")
        resp.gather(input="speech", action="/process_speech", language="bn-IN", timeout=3)

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
