import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import wikipedia  

recognizer = sr.Recognizer()  
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def fetch_wikipedia_answer(question):
    try:
        
        summary = wikipedia.summary(question, sentences=2)
        return summary
    
    except wikipedia.exceptions.DisambiguationError:
        return f"Multiple results found for {question}. Please be more specific."
    
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def processCommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")

    elif c.lower().startswith("find"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)

        if link:
            webbrowser.open(link)

        else:
            speak("Sorry, I couldn't find that song.")

    elif c.lower().startswith("who") or c.lower().startswith("what") or c.lower().startswith("when") or c.lower().startswith("where"):
        
        speak("Let me search for the answer.")
        answer = fetch_wikipedia_answer(c)
        speak(answer)
        print(f"Answer: {answer}")

    else:
        speak("Sorry, I didn't understand the command.")
        print(f"Unrecognized command: {c}")

if __name__ == "__main__":

    speak("Initializing Chiku...")

    while True:

        print("Recognizing activation keyword...")

        try:

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(source)  
                print("Listening for the keyword 'Chiku'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  

            
            keyword = recognizer.recognize_google(audio)
            print(f"Detected: {keyword}")

            if keyword.lower() == "chiku":

                speak("Yes, I'm here. What do you want me to do?")
                print("Chiku is active, listening for command...")

                with sr.Microphone() as source:
                    
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  
                command = recognizer.recognize_google(audio)
                print(f"Command detected: {command}")

                
                processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")



