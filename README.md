# Multi-Translator

Multi-Translator is a versatile Python application that provides translation services using multiple translation APIs. It features a user-friendly graphical interface built with Tkinter, allowing users to easily translate text between various languages.

## Features

- Translate text using multiple translation services:
  - Google Translate (using both `googletrans` and `deep-translator`)
  - Microsoft Translator
  - Pons Translator
  - Linguee Translator
  - MyMemory Translator
- Speech-to-text functionality for easy input
- Swap source and destination languages with a single click
- Copy translated text to clipboard
- Clear text fields
- View and load from translation history
- User-friendly GUI built with Tkinter

## Requirements

To run Multi-Translator, you need Python 3.x and the following libraries:

- speech_recognition
- tkinter
- pyperclip
- googletrans
- deep_translator

You can install these dependencies using pip:

```
pip install SpeechRecognition tkinter pyperclip googletrans==3.1.0a0 deep-translator
```

Note: We're using a specific version of `googletrans` (3.1.0a0) as newer versions might have compatibility issues.

## Usage

1. Run the script:
   ```
   python multi_translator.py
   ```
2. The Multi-Translator window will appear.
3. Enter the text you want to translate in the "Source Text" field, or use the "Speech to Text" button to input text by speaking.
4. Select the source and destination languages from the dropdown menus.
5. Choose your preferred translation service.
6. Click the "Translate" button to see the results.

## Additional Features

- **Swap Languages**: Click the "⇄" button to swap source and destination languages.
- **Clear Text**: Remove all text from both input and output fields.
- **Copy Text**: Copy the translated text to your clipboard.
- **History**: View your translation history and load past translations.

## Contributing

Contributions to Multi-Translator are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This application uses various third-party translation services. Please be aware of and comply with the terms of service for each translation API you use.