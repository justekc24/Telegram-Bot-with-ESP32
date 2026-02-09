import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from pydub import AudioSegment
import speech_recognition as sr


# --- CONFIGURATION ---
TOKEN = "8202841278:AAGNKB30nbk9k3Aa9G9EEUkhA8ASQg1RYzc"
ADAFRUIT_USER = "justekc24io"
ADAFRUIT_KEY = "aio_ZrLa85XNqrq3pwM4SyeHf2cOeXSL"
FEED_NAME = "telegramcommand"
MY_CHAT_ID = 6988460478

# --- FONCTION D'ENVOI VERS ADAFRUIT (HTTPS) ---
def send_to_adafruit(valeur):
    try:
        # URL de l'API REST d'Adafruit (Port 443 standard)
        url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_USER}/feeds/{FEED_NAME}/data"
        headers = {"X-AIO-Key": ADAFRUIT_KEY}
        payload = {"value": valeur}

        # Envoi de la requete POST
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"Succes : {valeur} envoye a Adafruit")
        else:
            print(f"Erreur Adafruit code {response.status_code}")
    except Exception as e:
        print(f"Erreur de connexion : {e}")

# --- GESTIONNAIRE UNIQUE (VOIX ET TEXTE) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != MY_CHAT_ID:
        await update.message.reply_text("Accès interdit.")
        return # On arrête tout ici pour cet utilisateu
    # CAS 1 : C'EST UN MESSAGE VOCAL

    if update.message.voice:
        print("Vocal reçu, démarrage de la transcription...")
        try:
            # Téléchargement et conversion
            new_file = await context.bot.get_file(update.message.voice.file_id)
            await new_file.download_to_drive("vocal.ogg")

            sound = AudioSegment.from_ogg("vocal.ogg")
            sound.export("vocal.wav", format="wav")

            # Transcription
            recognizer = sr.Recognizer()
            with sr.AudioFile("vocal.wav") as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="fr-FR")

            print(f"Vocal transcrit : {text}")
            await update.message.reply_text(f"🎙 (Vocal) : {text}")
            send_to_adafruit(text) # Envoi du texte obtenu par la voix
            os.remove("vocal.ogg")
            os.remove("vocal.wav")

        except Exception as e:
            print(f"Erreur vocal : {e}")
            await update.message.reply_text("Désolé, je n'ai pas pu analyser ta voix.")

    # CAS 2 : C'EST UN MESSAGE TEXTE
    elif update.message.text:
        commande_texte = update.message.text
        print(f"Texte direct reçu : {commande_texte}")

        await update.message.reply_text(f"✉️ (Texte) : {commande_texte}")
        send_to_adafruit(commande_texte) # Envoi du texte direct

# --- LANCEMENT DU BOT ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # On utilise un filtre qui accepte TEXTE ou VOIX
    core_handler = MessageHandler(filters.TEXT | filters.VOICE, handle_message)
    application.add_handler(core_handler)

    print("Bot hybride (Voix/Texte) prêt sur PythonAnywhere !")
    application.run_polling()