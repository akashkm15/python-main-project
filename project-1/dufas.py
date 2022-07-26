# import these modules
import pyttsx3  # for speaking
import datetime  # for date-time
import speech_recognition as sr  # for speech- recognition
import wikipedia  # for wikipedia search
import webbrowser  # for open webrowser
import os  # for os realted work
import smtplib  # for sending email

# microsoft speech API(sapi5)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# 0 is set to david voice and 1 is set to zira voice.
engine.setProperty('voices', voices[0].id)


def speak(audio):
    # speak function
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    # wishme function for salutation
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good Morning!')
    elif 12 <= hour < 18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!!')

    speak("Hello sir! Welcome back. I'm DUFAS, your integrated AI , how may I help you today?")


def takeCommand():
    # it takes microphone input from microphone and return a string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f'user said: {query}\n')

    except Exception as e:
        print(e)

        print("Say that again please")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-pass')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == '__main__':
    wishMe()
    while True:  # for keep going
        # if 1:
        query = takeCommand().lower()  # use (.lower) for easily search a lower search
        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('searching wikipedia.....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to wikipedia')
            # print(results) for printing the result(do it at your own risk).
            speak(results)

        elif 'open youTube' in query:
            # opening youTube from line5
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            # opening google from line5
            webbrowser.open("google.com")

        elif 'open stackover' in query:
            # opening stackoverflow from line5
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            # opening the os module from line 6
            music_dir = 'E:\\rings'
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            # for random play:
            #     os.startfile(os.path.join(music_dir,randomfunction(songs)

        elif 'the time' in query:
            # for time
            strTime = datetime.datetime.now().strftime("%H:%H:%S")
            speak(f"the time is {strTime}")

        elif 'open code' in query:
            code_path = "E:\\setups\\VSCodeUserSetup-x64-1.67.2.exe"
            os.startfile(code_path)


        elif 'email to akash' in query:
            try:
                speak('What should i say?')
                content = takeCommand()
                to = "akashnine2012@gmail.com"
                sendEmail(to, content)
                speak('Email has been sent!')
            except Exception as e:
                print(e)
                speak("Sorry sir, I'm not authorised to send this email.")

        elif 'quit' in query:
            quit()
