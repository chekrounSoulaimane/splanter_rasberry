from models.porte import Porte
import time
import pytz
import threading
import firebase_admin
# import Adafruit_DHT
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime


serreID = 's5TkSYTVsVX2yB2mW5VD'

cred = credentials.Certificate(
    "C:/Users/Lenovo/Downloads/splanter-e8fe6-firebase-adminsdk-vbyus-3b921d3aa0.json")

default_app = firebase_admin.initialize_app(cred)
print(default_app.name)

db = firestore.client()

etat_serre_collection_ref = db.collection("etat_serre_test")
etat_plante_collection_ref = db.collection("date_heure_test")
serre_collection_ref = db.collection("serre")

callback_done = threading.Event()

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        dict = doc.to_dict()
        portes = Porte.fromDoc(dict['portes'])
        luminosite = dict['luminosite']
        print(f'luminosite est active: {luminosite}')
        print(f'{portes[0].libelle} is open: {portes[0].isOpen}\n')
    callback_done.set()

doc_ref = serre_collection_ref.document(serreID)

doc_watch = doc_ref.on_snapshot(on_snapshot)

while (True):
    # get sensors data
    # sensor = Adafruit_DHT.DHT11
    # gpio = 17

    # get a sensor reading (waiting 2 seconds between each retry).
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

    # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

    temperature_serre = 16.0
    humidite_serre = 58

    utc_datetime = datetime.now()
    local_timezone = pytz.timezone("Africa/Casablanca")
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc)
    local_datetime = local_datetime.astimezone(local_timezone)

    etat_serre_collection_ref.document().set({
        "timestamp": local_datetime,
        "temperature": temperature_serre,
        "humidite": humidite_serre,
        "serreID": serreID,
    })

    etat_plante_collection_ref.document().set({
        "timestamp": local_datetime,
        "serreID": serreID,
        "planteID": 1,
        "etat_plante": {
            "id": 1,
            "humiditeSol": 12.9,
        },
        "irrigation": {
            "id": 1,
            "duree": 1.2,
        },
    })

    time.sleep(15.0)  # sleep for 5 secondes
