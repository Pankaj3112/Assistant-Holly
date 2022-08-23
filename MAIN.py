import re
import pyttsx3
import webbrowser
import requests
import time
from datetime import datetime
import speech_recognition as sr
import wikipedia
import os
import json
import ssl
import smtplib
from email.message import EmailMessage
import winshell

#setting the speak engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#you can set voices[0] for male voice
engine.setProperty('voice',voices[1].id)
#you can set rate of speech from below
engine.setProperty('rate',171)

#Function to make our assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Function that will help assistant to listen to our voice
def takeOrder():
    #setting the speech recognition
    with sr.Microphone()as source:
        rec = sr.Recognizer()
        print("listening...")
    #pause threshhold is basically after how many sentence of your sentence completion will it stop recording audio
        rec.pause_threshold = 1
    #dynamic energy is related to frequency of sound ,by default it is 350,and you can set the mic for ambient noise
        rec.dynamic_energy_threshold= 500
        rec.adjust_for_ambient_noise
        audio = rec.listen(source)
    try:
    #audio is then sent to google server for recognition
        print('Recognizing...')
        text = rec.recognize_google(audio,language='en-in')
        print(f'{text}\n')
        return text
    except Exception:
        print('will you please say it again...\n')
        return ("none")

#wishme will help understand assistant what time it is
def Wishme():
    currentHour = int(datetime.now().strftime('%H'))
    if currentHour >=6 and currentHour <12:
        return("Good Morning,Sir")
    elif currentHour >=12 and currentHour <16:
        return("Good afternoon,Sir")
    elif currentHour >=16 and currentHour <20:
        return("Good evening,Sir")

#function to show search result for our query
def fetchytsearch(query):
    speak("searching youtube...")
    url = "https://www.youtube.com/results?search_query="+query
    #playing yt vedio
    speak("Showing search results on Youtube")
    web(url)
    
#function for opening web results on chrome,by default it opens web pages in internet explorer
def web(link):
    chromepath  = "C:\\Program Files (x86)\\Google\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chromepath))
    web = webbrowser.get('chrome')
    web.open(link)
          
#function for fetching results from wikipedia library
def wiki(query):
    try:
        result = wikipedia.summary(query,sentences=2)
        print(result)
        speak("According to Wikipedia")
        speak(result)
    except Exception:
        speak("no results on wikipedia for your query")

#function to get realtime weather
def weather(query):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":query}
    headers = {
        "X-RapidAPI-Key": "get your api key from rapid api",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    text = json.loads(response.text)

    print(f'Weather is {text["current"]["condition"]["text"]}\nTemprature is {text["current"]["temp_c"]}C\nRain is {text["current"]["precip_in"]} inches')
    
    speak(f'''The weather in patiala is {text["current"]["condition"]["text"]}.
The temprature is {text["current"]["temp_c"]} degree celcius and it feels like {text["current"]["feelslike_c"]} degree celcius
and there is {text["current"]["precip_in"]} inches of rain today.''')

#function for speaking a random joke
def joke():
    url = "https://yo-mama.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": "get your api key from rapid api",
        "X-RapidAPI-Host": "yo-mama.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    text = json.loads(response.text)
    text['joke'] = text['joke'].replace('\\n','\n')
    speak(text['joke'])

#function to send email
def sendemail(receiver,body):
    emailsender = 'pankajbeniwal3112@gmail.com'
    #This password is not your actual email pw,
    # you need to enable 2factor authentication and make a app password from google site
    emailpw = '16 lettered passcode'
    email_receiever = receiver
    subject = "Hi! i am Holly the assistant.I am sending this Email on behalf of cheeku."
    

    em = EmailMessage()
    em['From'] = emailsender
    em['To'] = email_receiever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(emailsender,emailpw)
        smtp.sendmail(emailsender,email_receiever,em.as_string())
    

#calculator function
def calculator(task,num1,num2):
    if 'add' in task or '+' in task:
        print(f"{num1} plus {num2} is equals to {num1+num2}")
        speak(f"{num1} plus {num2} is equals to {num1+num2}")

    elif '-' in task:
        print(f"{num1} minus {num2} is equals to {num1-num2}")
        speak(f"{num1} minus {num2} is equals to {num1-num2}")

    elif 'subtract' in task:
        print(f"{num2} minus {num1} is equals to {num2-num1}")
        speak(f"{num2} minus {num1} is equals to {num2-num1}")

    elif 'multiply' in task or ' X ' in task:
        print(f"{num1} multiplied by {num2} is equals to {num1*num2}")
        speak(f"{num1} multiplied by {num2} is equals to {num1*num2}")

    elif 'divide' in task or '/' in task:
        print(f"{num1} divided by {num2} is equals to {num1/num2}")
        speak(f"{num1} divided by {num2} is equals to {num1/num2}")

#fetching news from News Api
def fetchnews():
    try:
        url = "https://newsapi.org/v2/top-headlines"
        source = "bbc-news"
        key = "your api keys from news api"
        para = {"sources":source,"apiKey":key}
        response = requests.get(url,params=para)
        r = response.text
        
        global parsednews
        parsednews = json.loads(r)
        global articlesnews
        articlesnews = parsednews['articles']
    except Exception:
        print("Sorry sir i am unable to fetch news for you\n")

#function for printing and speaking news
def newsmain():
        fetchnews()
        speak("Reading today's headlines from BBC news")
        speak("The first news is")
        for items in range(1,5):
            title = parsednews['articles'][items]['title']
            news = parsednews['articles'][items]['description']
            newsurl = parsednews['articles'][items]['url']
            print(f"{items}: \n{title}")
            speak(title)
            time.sleep(1)
            print(news)
            speak(news)
            print(newsurl,"\n")
            time.sleep(1)
            speak("the next news is ")




if __name__=="__main__":
    #you need to add contacts here in order to send emails
    contacts = {"xyz":"xyz@gmail.com","abc":"abc@gmail.com"}

    print("-You can say 'help' for help and\n\
-'you need a break' to exit program\n ")

    speak(Wishme())
    speak("How can i help you?")
    while True:
        task = takeOrder().lower()

        if 'on youtube' in task:
            task = task.replace("on youtube","")
            task = task.replace("search","")
            fetchytsearch(task)

        elif 'open youtube' in task:
            web("youtube.com")
        
        elif 'time' in task:
            time = datetime.now().strftime('%H:%S')
            speak(time)
        
        elif 'google' in task:
            web("google.com")

        elif 'spotify' in task:
            os.system('spotify')

        elif 'discord' in task:
            os.system('discord')

        elif 'wikipedia' in task:
            task = task.replace("on wikipedia","")
            wiki(task)
        
        elif 'weather' in task:
            #you can pass name of your city as string in this function
            weather()
        
        elif 'joke' in task:
            joke()
        
        elif 'email' in task:
            task = task.replace('email to','')
            tasklist = task.split(' ')
            #making a list of words in task string and checking any of them is in contacts dictionary
            tasklist = [i for i in tasklist if i!='']
            emailsentto = []

            try:
                for i in tasklist:
                    if i in contacts:
                        receiver = contacts[i]
                            
                        
                        speak(f"What do you want to say to {i}")
                        body = takeOrder().lower()
                        sendemail(receiver=receiver,body=body)
                        emailsentto.append(i)
            except Exception:    
                speak("Sorry Sir! i am unable to send this email right now,due to some technical issues.")

            if len(emailsentto) == 0:
                speak("The person you want to email is not in your contacts")
            elif len(emailsentto) == 1:
                speak(f"Sent Email by you to {emailsentto}")
            else:
                speak(f"sent emails by you to {emailsentto}")

        
        elif 'add' in task or 'subtract' in task or 'multiply' in task or 'divide' in task or '+' in task or '-' in task or ' X ' in task or '/' in task:
            try:
                #using regular expression two find numbers from task string
                list = re.findall('\d+',task)
                num1 = list[0]
                num2 = list[1]
                calculator(task,int(num1),int(num2))
            except Exception:
                print('please try again...')
        
        elif 'recycle bin' in task:
            try:
                speak("Emptying recycle bin for you")
                winshell.recycle_bin().empty(confirm=False,show_progress=True,sound=False)
            except Exception:
                print("\nYou cancelled the operation")

        elif 'news' in task:
            newsmain()

        elif 'you need a break' in task:
            speak("ok sir! have a nice day")
            exit()
        
        elif 'your name' in task:
            speak("my name is Holy, are you drunk? because you know me from a very long time")

        elif 'help' in task or 'what can you do' in task:
            speak(f'I can do the following things for you.')
            print('-I can open Youtube,Google,Discord,Spotify\n\
-Search your query on Youtube,wikipedia\n\
-Tell you a joke\n\
-The realtime Weather\n\
-The latest news.\n\
-Calculate numbers for you\n\
-Empty your recycle bin\n\
-Send email to someone\n')

        input("Press Enter to continue")
        