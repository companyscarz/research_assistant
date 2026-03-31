import flet as ft
import random
import time
import math
import speech_recognition as sr
import pyttsx3
import threading
import requests
import re

#______________________________________________________________________________________________________________________
def main(page: ft.Page):
    # Track the current engine globally within main
    tts_control = {"engine": None}

    page.title = "AI Legal Assistant"
    page.bgcolor = "#0B0F1A"
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #############################################
    #___________________FUNCTIONALITY___________
        #a user may want to save the result 
    def report_file(file_path):
        def read_content():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                speaker_on(f"Error: {file_path} does not exist.")

        def write_content(data, append=False):
            # 'a' mode appends to the end, 'w' overwrites the file
            mode = 'a' if append else 'w'
            try:
                with open(file_path, mode, encoding='utf-8') as f:
                    f.write(data)
                #Successfully written"
                speaker_on(f"Successfully written to {file_path}.")
            except Exception as e:
                print(f"Failed to write!..{e}")
                speaker_on(f"Failed to write!")

        #detects text and numbers from images, text, pdfs and attaches a prompt of and sends to the sever
    def open_camera():
        try:
            speaker_on("Sorry, Camera is not yet functional")
        except Exception as e:
            speaker_on("Sorry, an error occured. Please try again.")

    #detects text and numbers from images, text, pdfs and attaches a prompt of and sends to the sever
    def read_media_text():
        try:
            print("the speaker is working")
            speaker_on("Sorry, add media is not yet functional")
        except Exception as e:
            speaker_on("Sorry, an error occured. Please try again.")

    #detects voice, convert to text automatically sends to the sever
    def voice_to_text():
        try:
            recognizer =  sr.Recognizer() #initialize microphone
            microphone = sr.Microphone()
            with microphone as source: #audio source is microphone
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            #detect and return response
            speech_response = recognizer.recognize_google(audio)
            input_field.value = speech_response
            page.update()
            send_appeal()
        except Exception as e:
            print("Error when converting voice to speech")
            speaker_on("Sorry, I couldn't understand that. Please try again.")

    def toggle_ui_on_off_speaking(speaking: bool):
        """Helper to switch visibility between Input and Mute controls."""
        # When speaking: hide input, show mute
        # When silent: show input, hide mute
        input_container.visible = not speaking
        microphone_off.visible = speaking
        page.update()

    def speaker_off(e=None):
            """Stops the current engine if it exists."""
            if tts_control["engine"]:
                try:
                    tts_control["engine"].stop()
                    tts_control["engine"] = None
                except Exception as ex:
                    print(f"Mute Error: {ex}")
            # Once stopped, bring back the input field
            toggle_ui_on_off_speaking(speaking=True)

    def speaker_on(text: str):
        # 1. Switch UI to "Mute Mode" immediately
        toggle_ui_on_off_speaking(speaking=False)

        """Starts a new speech thread, stopping any existing one first."""
        speaker_off() # Stop current speech if any

        def talk():
            try:
                engine = pyttsx3.init() 
                tts_control["engine"] = engine #save reference for muting

                engine.say(text)
                engine.runAndWait()

                #cleanup after finishing naturally
                toggle_ui_on_off_speaking(speaking=False)
                tts_control["engine"] = None
            except Exception as e:
                print(f"TTS Error: {e}")
                toggle_ui_on_off_speaking(speaking=False)

        # Run this in a separate thread so it doesn't freeze your Flet UI
        threading.Thread(target=talk, daemon=True).start()

    # function to clean up the json response from the server for better text to speech and display formatting
    def clean_ai_response(data):
        #1. handle dict vs string
        if isinstance(data, dict):
            text = data.get("research_results", "")
        else:
            text = str(data)
        
        #2. (clean text) Remove bullet points and other unwanted characters
        text = text.replace("•", "")
        text = re.sub(r'\s*\n\s*', ' ', text)
        text = re.sub(r'\s+', ' ', text) #.strip()
        
        #3. Sentence cleanup 
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        clean_text = ". ".join(sentences)

        return clean_text
    
    # function to return chunks of text for better tts performance and display formatting
    def split_for_speech(text, max_len=200):
        words = text.split()
        chunks = []
        current = []
        for word in words:
            current.append(word)
            if len(" ".join(current)) > max_len:
                chunks.append(" ".join(current))
                current = []
        if current:
            chunks.append(" ".join(current))
        return chunks
    
    def toggle_loading(is_loading: bool):
        """Swaps the send button for a loading ring."""
        send_appeal_button.visible = not is_loading
        loading_indicator.visible = is_loading
        page.update()

    #send the message to the server
    def send_appeal(e=None):
        user_query = input_field.value
        if not user_query:
            return
    
        #show loading state
        toggle_loading(True)

        def make_request():
            try:
                res = requests.post(
                    url="http://127.0.0.1:5000/user_query",
                    timeout = 120,
                    json={
                        "user_query": user_query
                    }
                )
                if res.status_code == 200:
                    response = res.json()
                    
                    results = response.get("research_results", {})

                    clean_text = clean_ai_response(results)


                    input_field.value = ""
                    toggle_loading(False)

                    clean_text = split_for_speech(clean_text)
                    
                    speaker_on(clean_text)

                    #raw_response = response.get("research_results", f"Sorry, I couldn't get a response for {user_query}.")
                    #input_field.value = ""
                    #toggle_loading(False)
                    #speaker_on(raw_response)
                else:
                    toggle_loading(False)
                    speaker_on("Sever error. Please try again.")
            except Exception as e:
                print(f"Request Error: {e}")
                toggle_loading(False)
                speaker_on("connection lost. Check your server")
        # Run request in thread so it doesn't freeze the wave animation
        threading.Thread(target=make_request, daemon=True).start()


    ###################################################
    #___________________CONTROLS___________________
    # ---------- HEADER ----------
    header = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            margin=ft.Margin.only(bottom=20),
            controls=[
                ft.Container(
                    content=ft.Text(
                        "TROVE AI",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        italic=True,
                    ),
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
    )

# ---------- SOUND WAVE (SIMULATED) ----------
    bars = []
    for i in range(20):
        bar = ft.Container(
            width=4,
            height=20,
            border_radius=2,
            gradient=ft.LinearGradient(
                colors=["#00C6FF", "#7F00FF"]
            ),
        )
        bars.append(bar)

    wave_row = ft.Row(
        controls=bars,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=4,
    )

    def animate_wave():
        while True:
            for i, bar in enumerate(bars):
                new_height = 10 + abs(math.sin(time.time() * 2 + i)) * 40
                bar.height = new_height
            page.update()
            time.sleep(0.05)

    threading.Thread(target=animate_wave, daemon=True).start()

    animated_sound_wave = ft.Row(
        controls=wave_row,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=4,
    )


    microphone_off = ft.IconButton( 
        icon=ft.Icons.MIC_OFF, 
        icon_size=30, 
        align=ft.Alignment.CENTER, 
        icon_color=ft.Colors.GREY_600,
        visible=False,
        on_click=speaker_off
    )

    loading_indicator = ft.ProgressRing(
                        width=20, 
                        height=20, 
                        stroke_width=2, 
                        visible=False)
    
    # ---------- INPUT FIELD ----------
    input_field = ft.TextField(
        hint_text="ASK Trove...",
        border=ft.InputBorder.NONE,
        expand=True,
        text_size=14,
        color=ft.Colors.WHITE,
        multiline=True,
        max_lines=6
    )

    input_container = ft.Container(
        visible=True,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=-10,
                    controls=[
                        add_media_btn := ft.IconButton(
                            icon=ft.Icons.ATTACH_FILE,
                            icon_color="#5D41F7",
                            on_click=read_media_text
                        ),
                        camera_btn := ft.IconButton(
                            icon=ft.Icons.CAMERA_ALT,
                            icon_color="#5D41F7",
                            on_click=open_camera
                        ),
                        microphone_btn := ft.IconButton(
                            icon=ft.Icons.MIC,
                            icon_color="#5D41F7",
                            on_click=voice_to_text
                        ),
                    ]
                ),
                input_field,
                #use stack to swap send button with loading indicator
                ft.Stack(controls=[
                        send_appeal_button := ft.IconButton(
                        icon=ft.Icons.SEND,
                        icon_color="#00C6FF",
                        on_click = send_appeal
                    ),
                    ft.Container(
                        content=loading_indicator,
                        padding=10, #match button spacing
                    )
                ])
            
            ],
        ),
        padding=10,
        margin=ft.Margin.symmetric(horizontal=20),
        border_radius=30,
        bgcolor="#1A1F2E",
    )

    # ---------- MAIN LAYOUT ----------
    page.add(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                header,
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        animated_sound_wave
                    ],
                ),
                ft.Column(
                    controls=[
                        microphone_off,
                        input_container,
                        ft.Divider()
                    ],
                ),
            ],
        )
    )


ft.run(main)