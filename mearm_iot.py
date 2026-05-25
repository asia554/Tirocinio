import paho.mqtt.client as mqtt
import pigpio
import time

PIN_BASE = 4
PIN_LEFT = 17
PIN_RIGHT = 22
PIN_CLAW = 23

pi = pigpio.pi()
if not pi.connected:
        exit()

#traduzione tra client e broker
def al_ricevimento_messaggio(client, userdata, msg):
    topic = msg.topic
    valore = int(float(msg.payload.decode()))           #decode prende il messaggio in byte e lo traduce leggibile a p>

#identifico il topic
    if topic == "mearm/base":
            pi.set_servo_pulsewidth(PIN_BASE, valore)
            
    elif topic == "mearm/pinza":
            pi.set_servo_pulsewidth(PIN_CLAW, valore)

    elif topic == "mearm/left":
            pi.set_servo_pulsewidth(PIN_LEFT, valore)
    
    elif topic == "mearm/right":
            pi.set_servo_pulsewidth(PIN_RIGHT, valore)

#configurazione client e collegamento
client = mqtt.Client()
client.on_message = al_ricevimento_messaggio

client.connect("localhost", 1883, 60)
client.subscribe("mearm/#")

#fine programma
try:
    client.loop_forever()
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(PIN_BASE, 0)
    pi.set_servo_pulsewidth(PIN_CLAW, 0)
    pi.set_servo_pulsewidth(PIN_LEFT, 0)
    pi.set_servo_pulsewidth(PIN_RIGHT, 0)
    pi.stop()