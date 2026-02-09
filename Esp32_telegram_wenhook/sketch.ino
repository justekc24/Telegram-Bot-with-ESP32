#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// --- CONFIGURATION WIFI ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// --- CONFIGURATION ADAFRUIT IO ---
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "" 
#define AIO_KEY         "" 

// --- INITIALISATION DES CLIENTS ---
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// Souscription au flux (Feed) nommé "commande" tu dois changer le nom de la commane par le nom de ton feeds en miniscule
Adafruit_MQTT_Subscribe sub_commande = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/telegramcommand");

void setup() {
  pinMode(4, OUTPUT);
  Serial.begin(115200);

  // Connexion WiFi
  Serial.print("Connexion au WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connecte !");

  // Enregistrement de la souscription
  mqtt.subscribe(&sub_commande);
}

void loop() {
  // Maintenir la connexion MQTT active
  MQTT_connect();

  // Lecture des messages entrants
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &sub_commande) {
      String message = (char *)sub_commande.lastread;
      Serial.print("Message recu : ");
      Serial.println(message);

      // Logique de commande
      if ((message.indexOf("allume") != -1) || message.indexOf("on") != -1){
        digitalWrite(4, HIGH);
        Serial.println("-> ACTION : LED ALLUMEE");
      }
      else if (message.indexOf("éteins") != -1 || message.indexOf("eteins") != -1 || message.indexOf("off") != -1) {
        digitalWrite(4, LOW);
        Serial.println("-> ACTION : LED ETEINTE");
      }
    }
  }
}

// Fonction pour gérer la connexion et reconnexion automatique
void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) return;

  Serial.print("Connexion au MQTT Adafruit... ");
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Nouvelle tentative dans 5 secondes...");
    mqtt.disconnect();
    delay(5000);
    retries--;
    if (retries == 0) while (1); // Stop si echec critique
  }
  Serial.println("Connecte !");
}