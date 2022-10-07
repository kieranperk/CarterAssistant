import requests
import pyttsx3
import speech_recognition as sr

# Config
activekeyword = "hello"

# Voice Settings
engine = pyttsx3.init()
engine.setProperty('rate', 200)     # setting up new voice rate
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Speech Recognition
r = sr.Recognizer()
m = sr.Microphone()

# Keys
carter_key = 'YOUR CARTER API KEY' #found in the carter dashboard, under "Access & More"!

# Startup
print("Calibrating ambient noise threshold.")
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(round(r.energy_threshold, 1)))
engine.say("Pie is now active!")
engine.runAndWait()
while True:
    try:
        with m as source: audio = r.listen(source)
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)
        if value == activekeyword:
            convActive = True
            while convActive == True:
                try:
                    print("Listening...")
                    with m as source: audio = r.listen(source)
                    value = r.recognize_google(audio)
                    print(">", value)

                    if value != None and "goodbye" in value:
                        convActive = False
                        engine.say("Okay, goodbye!")
                        print("Pie: Okay, goodbye!")
                        engine.runAndWait()
                    else:
                        # Open Conversation Via CarterAPI
                        carterR = requests.post('https://api.carterapi.com/v0/chat', json={'api_key': carter_key,'query': value,'uuid': "user-id-123",})
                        agent_response = carterR.json()
                        print("Pie:", agent_response['output']['text'])
                        engine.say(agent_response['output']['text'])
                        engine.runAndWait()
                except sr.UnknownValueError:
                    engine.say("Sorry, I couldn't understand that.")
                    engine.runAndWait()
                    continue
                except sr.RequestError:
                    engine.say("Uh oh! Couldn't request results from Google Speech Recognition service!")
                    engine.runAndWait()
                    continue
                
        else:
            continue
    except sr.UnknownValueError:
        continue
    except sr.RequestError:
        continue