
L’objectif de ce projet est d’allumer / éteindre une lampe à l’aide d’une note vocale ou d’un message texte envoyé sur Telegram.

#Architecture_du_système
 ----------------------------------------------------------|
|Bot Telegram → PythonAnywhere → Adafruit IO → ESP32 (MQTT)|
-----------------------------------------------------------

Ce type d’architecture peut être utile pour la domotique, l’accessibilité ou la supervision à distance.

#Fonctionnement

 un bot Telegram capable de recevoir des messages (vocaux, écrit etc).
Un script Python, hébergé sur PythonAnywhere, récupère ces messages via le token du bot.

 Lorsqu’il s’agit d’un message vocal, le script effectue la transcription grâce à l’API Google Speech Recognition.  Le message (transcrit ou non) est ensuite envoyé vers un feed Adafruit IO à l’aide de l’API REST.

L’ESP32 (simulé sur Wokwi) s’abonne au feed via le protocole MQTT, analyse le message reçu et commande un relais (HIGH / LOW) pour piloter la lampe.

#Matériel_et_logiciels_utilisés
 • Bot Telegram
 • PythonAnywhere (serveur)
 • Adafruit IO
 • ESP32
 • Relais
 • LED
 
Voici le lien vers la simualtion wokwi: Et là il faut faire la configuration avant de lancer
https://wokwi.com/projects/455324172858802177
LinkedIn: juste Kocou
#Note
 +Les serveurs PythonAnywhere  ne permettent pas une communication directe via les ports #MQTT classiques (1883 / 8083), ce qui impose l’utilisation d’un certificat TLS.
 C'est pourquoi il faudrait passer par Adafruit Io pour communiquer via mqtt avec esp32

<img width="1366" height="768" alt="allumage_audio" src="https://github.com/user-attachments/assets/0cca8c90-7ff8-44fb-87bd-1a0b7968efb2" />


#Juste Kocou  
#IoT #ESP32 #MQTT #Python #TelegramBot #Cloud #EmbeddedSystems #HumanAI
