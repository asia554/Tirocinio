import paho.mqtt.client as mqtt

client = mqtt.Client()          #inizializiamo il ricevitore

#decido a chi collegarsi e dove collegarsi
client.connect("localhost", 1883, 60)           #1883 numero standard, 60 sono i secondi di attesa prima di dichiarare la connessione caduta
client.subscribe("mearm/#")                     #indirizzate a mearm, e # è per indicare qualsiasi nome dietro

#ricezione del messaggio
def al_ricevimento_messaggio(client, userdata, msg):
    argomento = msg.topic                               #legge l'etichetta del messaggio
    contenuto_grezzo = msg.payload                      #è il contenuto del messaggio
    contenuto_leggibile = contenuto_grezzo.decode()     #è il traduttore, prende i byte e li trasforma in stringa
    
    print(f"Ricevuto {contenuto_leggibile} su {argomento}")

#lettura messaggi
client.on_message = al_ricevimento_messaggio
client.loop_forever()