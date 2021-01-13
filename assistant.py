from data.essentials import *
manual_path = r"data\manual_addition.json"

"""
This whole code is just if-elif-else for checking what the user has said
"""

if __name__=='__main__':
    wishMe()
    notify("Personal Assistant", "Assistant is now running\nTo close say: stop", 3)
    while True:
        speak("How can I help you?")
        statement = voice_input().lower()
        if statement==0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement or "bye" in statement:
            hour=datetime.datetime.now().hour
            if hour>=19:
                speak("ok Bye, and good night")
                print("ok Bye, and good night")
            elif hour < 16 and hour >9:
                speak("ok Bye, and have a nice day!")
                print("ok Bye, and have a nice day!")
            else:
                speak('ok ,Good bye')
                print('ok ,Good bye')
            break
            exit()



        if statement.startswith('wikipedia'):
            try:
                speak('Searching Wikipedia...')
                statement =statement.replace("wikipedia", "")
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Please try to narrow down the topic a bit more")

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif statement.startswith('play'):
            statement = statement.replace('play', '')
            pywhatkit.playonyt(statement)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=voice_input()
            while city_name == "None":
                speak("Can you please say the city name again?")
                city_name=voice_input()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"In {city_name} Temperature in celcius is " +
                      str(round(current_temperature - 273.15, 2)) + "degree celcius" +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in celcius = " +
                      str(round(current_temperature - 273.15, 2)) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")



        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' == statement or 'what can you do' == statement:
            speak('I am your persoanl voice assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif 'search'  in statement:
            pywhatkit.search(statement.replace('search', ''))
            time.sleep(5)

        elif 'ask' in statement:
            try:
                solve()
            except Exception as e:
                speak("An error occured")

        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "change voice" in statement:
            change_voice()

        elif statement == "change engine":
            switch_talker()

        elif "help" in statement:
            help()

        elif "translate" in statement:
            speak("Please, say the sentence you want to translate")
            text = voice_input().lower()
            while text == "none":
                speak("Please say the sentence again")
                text = voice_input().lower()
            speak("Translate to which language?")
            lang = voice_input().lower()
            while lang == "none":
                speak("I did not hear that")
                lang = voice_input().lower()
            try:
                translate(text, lang)
            except:
                speak("An error occured")

        elif statement == "add response":
            add_response()

        elif statement == "remove response":
            remove_response()

        elif statement.startswith("sleep for") and (statement.endswith("minutes") or statement.endswith("minute")):
            statement = statement.replace("sleep for", "")
            notify("Personal Assistant", f"See you after {statement}", 3)
            statement = statement.replace("minutes", "")
            statement = statement.replace("minute", "")
            sleep(int(statement))

        elif statement in manual_addition:
            speak(random.choice(manual_addition[statement]))

        elif statement == "reset all response":
            reset_response()

        elif statement == "load backup response":
            load_backup()

        elif statement.startswith("notify me after") and (statement.endswith("minutes") or statement.endswith("minute")):
            statement = statement.replace("notify me after", "")
            speak("Want to add a description?")
            option = voice_input()
            if option == "yes":
                speak("Please say the description")
                desc = voice_input()
            else:
                desc = "No description"
            notify("Personal Assistant", f"I'll notify you after {statement}", 3)
            statement = statement.replace("minutes", "")
            statement = statement.replace("minute", "")
            timer(int(statement), desc)


time.sleep(3)
