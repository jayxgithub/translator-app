# Import required libraries
import speech_recognition as sr
from tkinter import *
from tkinter import ttk, messagebox
import pyperclip
from googletrans import Translator as GoogleTranslator, LANGUAGES
from deep_translator import (
    GoogleTranslator,
    MicrosoftTranslator,
    PonsTranslator,
    LingueeTranslator,
    MyMemoryTranslator
)

# Global variables to store translation history and the Listbox for displaying history
translation_history = []
history_listbox = None


def change(text, src="english", dest="marathi", translator_choice="MyMemory"):
    """
    Handles the translation process based on the selected translator.

    Args:
    text (str): The text to be translated
    src (str): The source language
    dest (str): The destination language
    translator_choice (str): The chosen translation service

    Returns:
    str: The translated text
    """
    try:
        if translator_choice == "Google (googletrans)":
            translator = GoogleTranslator()
            translated = translator.translate(text, dest=dest, src=src)
            return translated.text
        elif translator_choice == "Google (deep-translator)":
            translated = GoogleTranslator(source=src, target=dest).translate(text)
        elif translator_choice == "Microsoft":
            translated = MicrosoftTranslator(source=src, target=dest).translate(text)
        elif translator_choice == "Pons":
            translated = PonsTranslator(source=src, target=dest).translate(text)
        elif translator_choice == "Linguee":
            translated = LingueeTranslator(source=src, target=dest).translate(text)
        elif translator_choice == "MyMemory":
            translated = MyMemoryTranslator(source=src, target=dest).translate(text)
        else:
            raise ValueError("Invalid translator choice")
        return translated
    except Exception as e:
        # Show error message if translation fails
        messagebox.showerror("Translation Error", str(e))
        return ""


def data():
    """
    Handles the translation button click event.
    Retrieves input, performs translation, and updates the UI.
    """
    s = combo_txt.get()  # Get the source language
    d = dest_combo.get()  # Get the destination language
    masg = sor_txt.get(1.0, END).strip()  # Get the text to be translated
    translator_choice = translator_var.get()  # Get the selected translator

    if not masg:
        # Show warning if no text is entered
        messagebox.showwarning("Empty Input", "Please enter text to translate.")
        return

    # Perform the translation
    textget = change(text=masg, src=s, dest=d, translator_choice=translator_choice)
    resul_txt.delete(1.0, END)
    resul_txt.insert(END, textget)

    # Add the translation to the history
    translation_history.append({
        "source": s,
        "destination": d,
        "original": masg,
        "translated": textget,
        "translator": translator_choice
    })

    # Update the history Listbox if it exists
    if history_listbox:
        update_history_listbox()


def swap_languages():
    """
    Swaps the source and destination languages and their corresponding texts.
    """
    src = combo_txt.get()
    dest = dest_combo.get()
    combo_txt.set(dest)
    dest_combo.set(src)

    # Swap the text in the source and result Text widgets
    src_text = sor_txt.get(1.0, END).strip()
    dest_text = resul_txt.get(1.0, END).strip()
    sor_txt.delete(1.0, END)
    resul_txt.delete(1.0, END)
    sor_txt.insert(END, dest_text)
    resul_txt.insert(END, src_text)


def clear_text():
    """
    Clears the text from both the source and result Text widgets.
    """
    sor_txt.delete(1.0, END)
    resul_txt.delete(1.0, END)


def copy_text():
    """
    Copies the translated text to the clipboard.
    """
    text_to_copy = resul_txt.get(1.0, END).strip()
    pyperclip.copy(text_to_copy)
    messagebox.showinfo("Copied", "Translated text copied to clipboard!")


def update_history_listbox():
    """
    Updates the Listbox that displays the translation history.
    """
    # Check if the history_listbox widget exists before trying to update it
    if history_listbox and history_listbox.winfo_exists():
        history_listbox.delete(0, END)  # Clear the Listbox
        for i, item in enumerate(reversed(translation_history), 1):
            # Insert each translation history item into the Listbox
            history_listbox.insert(END, f"{i}. {item['original'][:30]}... -> {item['translated'][:30]}...")


def show_history():
    """
    Displays the translation history in a new window.
    """
    global history_listbox
    history_window = Toplevel(box)
    history_window.title("Translation History")
    history_window.geometry("600x400")

    # Frame to hold the Listbox and Scrollbar
    history_frame = Frame(history_window)
    history_frame.pack(fill=BOTH, expand=True)

    # Listbox to display the history
    history_listbox = Listbox(history_frame, font=("Helvetica", 12))
    history_listbox.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for the Listbox
    scrollbar = Scrollbar(history_frame, orient=VERTICAL)
    scrollbar.config(command=history_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    history_listbox.config(yscrollcommand=scrollbar.set)

    # Populate the Listbox with the current translation history
    update_history_listbox()

    def load_selected_translation():
        """
        Loads a selected translation from history into the main window.
        """
        selection = history_listbox.curselection()
        if selection:
            index = selection[0]
            item = translation_history[-(index + 1)]
            sor_txt.delete(1.0, END)
            sor_txt.insert(END, item["original"])
            resul_txt.delete(1.0, END)
            resul_txt.insert(END, item["translated"])
            combo_txt.set(item["source"])
            dest_combo.set(item["destination"])
            translator_var.set(item["translator"])
        history_window.destroy()

    # Button to load the selected translation
    load_button = Button(history_window, text="Load Selected", command=load_selected_translation)
    load_button.pack(pady=10)


def speech_to_text():
    """
    Converts speech to text using Google's speech recognition API.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Speech Recognition", "Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        sor_txt.delete(1.0, END)
        sor_txt.insert(END, text)
    except sr.UnknownValueError:
        messagebox.showerror("Speech Recognition", "Could not understand audio")
    except sr.RequestError as e:
        messagebox.showerror("Speech Recognition", f"Could not request results; {e}")


# Tkinter GUI setup
box = Tk()
box.geometry('500x900')  # Increased height to accommodate new button
box.title('Multi-Translator')
box.config(bg='black')

# Label for the main title
lab_txt = Label(box, text='Multi-Translator', font="Helvetica 20 bold", bg='black', fg='white')
lab_txt.place(x=100, y=20, width=300, height=50)

# Frame to hold the translation interface
frame = Frame(box, bg='black')
frame.pack(side=BOTTOM, fill=BOTH, expand=True)

# Label for the source text section
lab_txt = Label(frame, text='Source Text', font="Helvetica 15 bold", fg='white', bg='black')
lab_txt.place(x=100, y=80, width=300, height=20)

# Text widget for entering the source text
sor_txt = Text(frame, font="Helvetica 12", wrap=WORD)
sor_txt.place(x=10, y=110, width=480, height=100)

# Button for speech-to-text
speech_button = Button(frame, text='Speech to Text', relief=RAISED, command=speech_to_text, bg='cyan', fg='black')
speech_button.place(x=10, y=220, width=150, height=40)

# List of available languages for translation
list_text = list(LANGUAGES.values())

# Combobox to select the source language
combo_txt = ttk.Combobox(frame, values=list_text)
combo_txt.place(x=10, y=270, width=150, height=40)
combo_txt.set("english")  # Default source language

# Button to trigger the translation
button = Button(frame, text='Translate', relief=RAISED, command=data, bg='blue', fg='white')
button.place(x=170, y=270, width=100, height=40)

# Combobox to select the destination language
dest_combo = ttk.Combobox(frame, values=list_text)
dest_combo.place(x=280, y=270, width=150, height=40)
dest_combo.set("marathi")  # Default destination language

# Button to swap the source and destination languages
swap_button = Button(frame, text='⇄', relief=RAISED, command=swap_languages, bg='green', fg='white')
swap_button.place(x=440, y=270, width=50, height=40)

# Combobox to select the translator (set MyMemory as default)
translator_var = StringVar()
translator_var.set("MyMemory")  # Set MyMemory as the default translator
translator_choices = [
    "Google (googletrans)",
    "Google (deep-translator)",
    "Microsoft",
    "Pons",
    "Linguee",
    "MyMemory"
]
translator_menu = ttk.Combobox(frame, textvariable=translator_var, values=translator_choices)
translator_menu.place(x=10, y=320, width=200, height=40)

# Label for the translated text section
lab_txt = Label(frame, text='Translated Text', font="Helvetica 15 bold", fg='white', bg='black')
lab_txt.place(x=100, y=370, width=300, height=20)

# Text widget to display the translated text
resul_txt = Text(frame, font="Helvetica 12", wrap=WORD)
resul_txt.place(x=10, y=400, width=480, height=100)

# Button to clear the text
clear_button = Button(frame, text='Clear Text', relief=RAISED, command=clear_text, bg='orange', fg='white')
clear_button.place(x=10, y=510, width=100, height=40)

# Button to copy the translated text
copy_button = Button(frame, text='Copy Text', relief=RAISED, command=copy_text, bg='purple', fg='white')
copy_button.place(x=120, y=510, width=100, height=40)

# Button to show the translation history
history_button = Button(frame, text='History', relief=RAISED, command=show_history, bg='brown', fg='white')
history_button.place(x=230, y=510, width=100, height=40)

# Button to exit the application
exit_button = Button(frame, text='Exit', relief=RAISED, command=box.quit, bg='red', fg='white')
exit_button.place(x=340, y=510, width=100, height=40)

# Start the Tkinter event loop
box.mainloop()