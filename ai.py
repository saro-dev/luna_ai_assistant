import tkinter as tk
from tkinter import ttk  # Import the ttk module for themed widgets
import pyttsx3
import speech_recognition as sr
import mysql.connector
from datetime import datetime
import psutil
import webbrowser
import pyautogui
import wikipedia
from PIL import Image, ImageTk
import threading
import sys
import time
import requests


class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert("end", message)
        self.text_widget.see("end")  # Scroll to the end to always show the latest messages

    def flush(self):
        pass

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'english+f3')
        self.engine.setProperty('rate', 150)
        self.root.title("Voice Assistant")

        self.label = tk.Label(self.root, text="Welcome to LUNA", font=('Helvetica', 20, 'bold'))
        self.label2 = tk.Label(self.root, text="Your Personal Voice Assistant", font=('Helvetica', 18))
        self.label.pack(pady=20)
        self.label2.pack(pady=10)

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the position to center the window
        x_position = (screen_width - 600) // 2
        y_position = (screen_height - 600) // 2

        # Set the window geometry
        self.root.geometry(f"600x600+{x_position}+{y_position}")

       # Load and resize the logo image
        self.logo_image = Image.open("./logo.png")  # Replace "logo.png" with your logo file path
        self.logo_image = self.logo_image.resize((300, 300)) # Set width and height to 300 pixels
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.root, image=self.logo_photo)
        self.logo_label.pack(pady=10)

        # Style for buttons using ttk
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), foreground='white', background='#4CAF50',
                             borderwidth='3', relief='raised', padding=10)
        
        # Create and style buttons using ttk

        self.login_button = ttk.Button(self.root, text="Login", command=self.login_page, style='TButton')
        self.login_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.signup_button = ttk.Button(self.root, text="Sign Up", command=self.signup_page, style='TButton')
        self.signup_button.pack(pady=10, padx=20, ipadx=10, ipady=5)
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), foreground='white', background='#4CAF50', borderwidth='3', relief='raised', padding=10)
        self.style.map('TButton',
                    background=[('active', '#008000')])  # Set the background color to dark green when active (hovered)


        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sarorosy@12",
            database="ai"
        )
        self.db_cursor = self.db_connection.cursor()

        # Bind the close event of the window to the on_close method
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Close the MySQL connection before exiting the program
        self.db_cursor.close()
        self.db_connection.close()
        self.root.destroy()  # Destroy the tkinter window


    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_coordinate = int((screen_width - width) / 2)
        y_coordinate = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    
        

    def start_voice_assistant_thread(self):
        voice_thread = threading.Thread(target=self.voice_assistant)
        voice_thread.daemon = True
        voice_thread.start()

    def voice_access_page(self, username):
        self.root.withdraw()  # Hide the current window
        voice_window = tk.Toplevel(self.root)
        voice_window.title("Voice Access Page")

        # Set window size and position
        self.center_window(voice_window, 600, 600)

        

        # Create a style object
        style = ttk.Style()
        style.configure('TLabel', padx=10, pady=5)  # Set padding for all labels

        # Create the username label
        username_label = ttk.Label(voice_window, text=f"User: {username}", font=('Helvetica', 14), style='TLabel')
        username_label.place(relx=1, x=-10, y=10, anchor="ne")  # Position at top right corner

        # Configure other label properties
        username_label.config(background='#4CAF50', foreground='white', relief=tk.RAISED, borderwidth=2)

        # Add a bold title "LUNA" at the top
        title_label = tk.Label(voice_window, text="LUNA", font=('Helvetica', 20, 'bold'))
        title_label.pack(pady=10)
        # Load and display the logo image
        logo_label = tk.Label(voice_window, image=self.logo_photo)
        logo_label.pack(pady=20)

        response_label = tk.Label(voice_window, text="Assistant Response:", font=('Helvetica', 14))
        response_label.pack(pady=(20, 5))

        self.response_text = tk.Text(voice_window, height=6, width=50)
        self.response_text.pack()
        sys.stdout = StdoutRedirector(self.response_text)
        self.start_voice_assistant_thread()



       





    def login_page(self):
        self.root.withdraw()  # Hide the current window
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        login_window.geometry("400x400+250+150")  # Increase the height to 400

        # Set window size and position
        self.center_window(login_window, 400, 400)

        # Heading
        ttk.Label(login_window, text="Login to your account", font=('Helvetica', 16)).pack(pady=(70, 10))

        # Create login page elements
        ttk.Label(login_window, text="Email").pack(pady=5)
        self.login_email_entry = ttk.Entry(login_window)
        self.login_email_entry.pack(pady=5)

        # Display label for user not found message
        self.user_not_found_label = tk.Label(login_window, text="", fg="red")
        self.user_not_found_label.pack(pady=5)

        ttk.Label(login_window, text="Password").pack(pady=5)
        self.login_password_entry = ttk.Entry(login_window, show="*")
        self.login_password_entry.pack(pady=5)

        # Style for buttons
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), foreground='white', background='#4CAF50',
                            borderwidth='3', relief='raised', padding=10)

        login_button = ttk.Button(login_window, text="Login", command=self.login, style='TButton')
        login_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        # Back button
        back_button = ttk.Button(login_window, text="Back", command=lambda: self.show_home_page(login_window),
                                style='Back.TButton')
        back_button.place(x=10, y=10)

        # Configure style for the back button
        self.style.configure('Back.TButton', foreground='black', background='lightgrey', padding=5,
                            borderwidth=2, relief='raised', font=('Helvetica', 10), width=8,
                            bordercolor='black', borderrelief='sunken')

    def signup_page(self):
        self.root.withdraw()  # Hide the current window
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")

        # Set window size and position
        self.center_window(signup_window, 400, 400)

        # Heading
        ttk.Label(signup_window, text="Create a new account", font=('Helvetica', 16)).pack(pady=(70, 10))

        # Create signup page elements
        ttk.Label(signup_window, text="Name").pack(pady=5)
        self.signup_name_entry = ttk.Entry(signup_window)
        self.signup_name_entry.pack(pady=5)

        ttk.Label(signup_window, text="Email").pack(pady=5)
        self.signup_email_entry = ttk.Entry(signup_window)
        self.signup_email_entry.pack(pady=5)

        ttk.Label(signup_window, text="Password").pack(pady=5)
        self.signup_password_entry = ttk.Entry(signup_window, show="*")
        self.signup_password_entry.pack(pady=5)

        # Configure style for the back button
        self.style.configure('Back.TButton', foreground='black', background='lightgrey', padding=5,
                            borderwidth=2, relief='raised', font=('Helvetica', 10), width=8,
                            bordercolor='black', borderrelief='sunken')

        signup_button = ttk.Button(signup_window, text="Sign Up", command=self.signup)
        signup_button.pack(pady=10, padx=20, ipadx=10, ipady=5)
        signup_button.configure(style='TButton')

        # Back button
        back_button = ttk.Button(signup_window, text="Back", command=lambda: self.show_home_page(signup_window), style='Back.TButton')
        back_button.place(x=10, y=10)

        
    def show_home_page(self,window):
        window.withdraw()  # Hide the current window
        self.root.deiconify()  # Show the main window


    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        # Check if the user exists in the database
        query = "SELECT name FROM users WHERE email = %s AND password = %s"
        user_data = (email, password)
        self.db_cursor.execute(query, user_data)
        user = self.db_cursor.fetchone()

        if user:
            print("User found. Logging in...")
            username = user[0]
            # Close the login window after successful login
            self.root.withdraw()  # Hide the login window
            self.voice_access_page(username)
            wishMe(self.app)
            self.root.destroy()
            
            
        else:
            print("User not found.")
            self.user_not_found_label.config(text="User not found.")

    def signup(self):
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        password = self.signup_password_entry.get()
        print("Sign up with:", name, email, password)

        # Insert user data into the database
        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        user_data = (name, email, password)
        self.db_cursor.execute(insert_query, user_data)
        self.db_connection.commit()
        print("User signed up and data inserted into database")

        # After successful signup, navigate to the voice assistant interface
        self.root.deiconify()  # Show the main window
        self.voice_access_page(name)
        wishMe(self.app)
        self.root.destroy()

    def voice_assistant(self):
        while True:  # Continuous loop for listening
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                print("Listening...")
                try:
                    audio = self.recognizer.listen(source, timeout=4)  # Set a timeout of 5 seconds

                    print("Processing...")
                    query = self.recognizer.recognize_google(audio)

                    print("You said:", query)
                    self.process_query(query)

                except sr.WaitTimeoutError:
                    print("Timeout reached. No speech detected.")
                    self.engine.runAndWait()

                except sr.UnknownValueError:
                    print("Sorry, I could not understand. Please try again.")
                    self.engine.say("Sorry, I could not understand. Please try again.")
                    self.engine.runAndWait()

                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    self.engine.say("Could not connect to the speech recognition service. Please try again later.")
                    self.engine.runAndWait()

    def process_query(self, query):
        if "the time" in query:
            current_time = datetime.now().strftime("%I:%M %p")
            print("Current time is:", current_time)
            self.engine.say(f"The current time is {current_time}")

        elif "battery" in query:
            battery_percentage = int(psutil.sensors_battery().percent)
            print("Battery percentage:", battery_percentage)
            self.engine.say(f"The current battery percentage is {battery_percentage} percent")

        elif "hello" in query:
            print("Hello! How can I assist you?")
            self.engine.say("Hello! How can I assist you?")

        elif "how are you" in query or "hi" in query:
            print("I'm fine, Thank you")
            self.engine.say("I'm fine, Thank you")

        elif "who made you" in query or "who created you" in query:
            self.engine.say("i have been created by miss Sandhyaa and Team")

        elif "who are you" in query:
            self.engine.say("I am your virtual assistant created by Sandhyaa and team")

        elif "what is" in query or "who is" in query:
            search_query = query.replace("what is", "").replace("who is", "").strip()
            print("Searching Wikipedia for:", search_query)
            self.engine.say(f"Searching Wikipedia for {search_query}")
            try:
                summary = wikipedia.summary(search_query, sentences=1)
                print("Summary from Wikipedia:", summary)
                self.engine.say(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                print("Disambiguation Error:", e)
                self.engine.say("There are multiple results for this query. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                print("Page Error:", e)
                self.engine.say("Sorry, I could not find any relevant information on Wikipedia.")

        elif "open google" in query or "open Google" in query:
            print("Opening Google...")
            self.engine.say("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in query or "open YouTube" in query:
            print("Opening YouTube...")
            self.engine.say("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open whatsapp" in query or "open Whatsapp" in query  or "open WhatsApp" in query:
            print("Opening Whatsapp...")
            self.engine.say("Opening Whatsapp")
            webbrowser.open("https://web.whatsapp.com")

        elif "calculate" in query:
        # Perform math calculation
        # You need to extract the mathematical expression and evaluate it
            expression = query.replace("calculate", "").strip()
            try:
                result = eval(expression)
                self.engine.say(f"The answer of {expression} is {result}")
                self.engine.runAndWait()
            except Exception as e:
                print("Error occurred during calculation:", e)
                self.engine.say("Sorry, I couldn't perform the calculation. Please try again.")
                self.engine.runAndWait()

        elif "stop listening" in query:
        # Stop listening to further commands temporarily
            self.engine.say("I'll stop listening for 10 seconds.")
            self.engine.runAndWait()
            time.sleep(10)
            self.engine.say("I'm listening again.")
            self.engine.runAndWait()

        elif any(word.isdigit() for word in query.split()) and "sleep" in query:
        # Sleep for the specified duration
            duration = [int(s) for s in query.split() if s.isdigit()][0]
            self.engine.say(f"Okay, I'll sleep for {duration} seconds.")
            self.engine.runAndWait()
            time.sleep(duration)
            self.engine.say("I'm awake now!")
            self.engine.runAndWait()

        elif "search" in query:
            search_query = query.replace("search", "")
            print("Searching for:", search_query)
            self.engine.say(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif "close" in query or "single" in query:
            # Close the current tab or window in the web browser
            pyautogui.hotkey('ctrl', 'w')

        elif "scroll down" in query:
            # Scroll down the web page
            pyautogui.scroll(-100)

        elif "scroll up" in query:
            # Scroll up the web page
            pyautogui.scroll(100)

        elif "weather in" in query:
            api_key = "b4837b29b69aec432e772e736da6e5a4"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city_name = query.replace("weather in", "").strip()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature_kelvin = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]

                # Convert temperature from Kelvin to Celsius
                current_temperature_celsius = int(current_temperature_kelvin - 273.15)

                weather_info = f"Temperature: {current_temperature_celsius:.2f} °C\nPressure: {current_pressure} hPa\nHumidity: {current_humidity}%\nDescription: {weather_description}"
                print(weather_info)
                self.engine.say(f"The weather in {city_name} is {current_temperature_celsius:.2f} degrees Celsius.")

            else:
                print("City not found.")
                self.engine.say("City not found.")


        elif "where is" in query:
            query=query.replace("where is","")
            location = query
            self.engine.say("Locating ")
            self.engine.say(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")

        elif "open Gmail" in query or "open mail" in query:
            self.engine.say("opening Gmail")
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

        elif "open spotify" in query or "open Spotify" in query:
            self.engine.say("opening Spotify")
            webbrowser.open("https://open.spotify.com/playlist/4DWNg46fjViQBWM2kwbPvF")

        elif "take a note" in query or "write a note" in query or "take notes" in query:
            # Extract the content of the note
            note_content = query.replace("take a note", "").replace("write a note", "").replace("take notes", "").strip()

            # Open a file to write the note
            with open("notes.txt", "a") as file:
                # Write the note content to the file
                file.write(note_content + "\n")

            # Confirm to the user
            print("Note taken successfully.")
            self.engine.say("Note taken successfully.")

        elif "read notes" in query:
            try:
                # Open the file to read the notes
                with open("notes.txt", "r") as file:
                    # Read the contents of the file
                    notes_content = file.read()

                if notes_content:
                    # Speak the contents of the notes
                    print("Reading notes:")
                    print(notes_content)
                    self.engine.say("Here are your notes:")
                    self.engine.say(notes_content)
                else:
                    print("No notes found.")
                    self.engine.say("You don't have any notes.")

            except FileNotFoundError:
                print("No notes found.")
                self.engine.say("You don't have any notes.")


        elif "luna" in query or "Luna" in query:  # Add a condition to exit the loop
            print("I'm Listening madam")
            self.engine.say("Yes mam., I'm listening")

        elif "exit" in query:  # Add a condition to exit the loop
            print("Exiting voice assistant...")
            exit()

        else:
            print("Sorry, I couldn't understand. Please try again.")
            self.engine.say("Sorry, I couldn't understand. Please try again.")

        self.engine.runAndWait()

def wishMe():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        app.engine.say("Good Morning!")

    elif hour >= 12 and hour < 18:
        app.engine.say("Good Afternoon!")   

    else:
        app.engine.say("Good Evening!")  

    assname = "Loonaaa"
    app.engine.say("I am your Assistant")
    app.engine.say(assname)

    app.engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
