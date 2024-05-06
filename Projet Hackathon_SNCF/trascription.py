import pyaudio
import wave
import keyboard
import pip
from openai import OpenAI  # for making OpenAI API calls
import urllib  # for downloading example audio files
import os
from deep_translator import GoogleTranslator

# define a wrapper function for seeing how prompts affect transcriptions
def transcribe(audio_filepath, prompt: str) -> str:
    """Given a prompt, transcribe the audio file."""
    transcript = client.audio.transcriptions.create(
        file=open(audio_filepath, "rb"),
        model="whisper-1",
        prompt=prompt,
    )
    return transcript.text

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


#Prompte pour guider le model whisper dans sa transcription 
prompt = """Voie 22, 24. voie 43. Flash info trafic Je vous rappelle que le prochain train à destination de Paris 
se trouve actuellement à quai à la voie 21. Mesdames Messieurs Voie numéro 6 le TER situé à l accès aux quais 
ne prend pas de  voyageurs. Mesdames Messieurs je vous invite à consulter les applications Île-de-France 
mobilités, les sites de transilien.com, ratp.fr, SNCF Connect ou votre application de Mobilités. 
Madame Monsieur, je vous remercie de votre écoute. Flash INFO trafic, ligne B. Le TER à destination 
de Beauvais, départ 19h37 entrera en gare dans quelques minutes. Voie 1 votre train entre en gare. 
Ladies and gentlemans, the Bording of you OUIGO train .Voie 12 ce train ne prend pas de voyageurs. 
Pour le service pour le service essai de sonorisation . Voie numéro 9, voie numéro 9, votre train rentre en gare. 
Mesdames Messieurs, les TGV 6995 et 6923  """


# Paramètres d'enregistrement audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 60  # Durée de l'enregistrement (en secondes)

# Initialise PyAudio
audio = pyaudio.PyAudio()

# Ouvre le flux d'entrée audio depuis le microphone
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Enregistrement en cours. Appuyez sur 'Echap' pour arrêter l'enregistrement.")

frames = []

# Enregistre les données audio en chunks
while True:
    data = stream.read(CHUNK)
    frames.append(data)
    if keyboard.is_pressed('esc'):
        break

print("Enregistrement terminé.")

# Ferme le flux d'entrée audio
stream.stop_stream()
stream.close()
audio.terminate()

# Écrit les données enregistrées dans un fichier WAV
wf = wave.open("enregistrement.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

"""la voie est enregistré sous format wav apres avoir parlé"""

#recuperer le fichier audio 
up_first_filepath = "C:/Users/hp/Desktop/SNCF/enregistrement.wav"

#transcription du fichier audio
transcription = transcribe(up_first_filepath, prompt=prompt)
print()
print("--------------------------------------------------------")
print(transcription)


print("--------------------------------------------------------")
print()

#traduction du fichier audio en anglais
translated_to_english = GoogleTranslator(source='auto', target='en').translate(transcription)
print(translated_to_english)
print("--------------------------------------------------------")
print()
#traduction du fichier audio en espagnole

translated_to_spanich = GoogleTranslator(source='auto', target='es').translate(transcription)
print(translated_to_spanich)