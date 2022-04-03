# https://cloud.google.com/text-to-speech/docs/libraries?hl=JA

import os

"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech

class Txt2Speech(object):
    def __init__(self) -> None:
        self.lang_code = {
            '日本語': 'ja-JP',
            'English': 'en-US'
        }

        self.gender_type = {
            'default': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
            'male': texttospeech.SsmlVoiceGender.MALE,
            'female': texttospeech.SsmlVoiceGender.FEMALE,
            'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
        }

        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, lang='日本語', gender='default'):

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang_code[lang],
            ssml_gender=self.gender_type[gender]
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        self.response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

    def save_audio(self, fpth_output='./data/output.mp3'):
        # The response's audio_content is binary.
        with open(fpth_output, "wb") as out:
            # Write the response to the output file.
            out.write(self.response.audio_content)
            print(f'Audio content written to file {fpth_output}.')

def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './data/secret.json'


    text = "こんにちは，わたしは山田太郎です"
    lang = '日本語'
    gender = 'default'

    txt2speech = Txt2Speech()
    txt2speech.synthesize_speech(text, lang, gender)
    txt2speech.save_audio()


if __name__ == '__main__':
    main()