import requests
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes
import pyautogui

REMOTE_URL = 'https://flask-volume-control-1.onrender.com'  # Remplace par ton URL Render

def get_volume_interface():
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)
    return interface.QueryInterface(IAudioEndpointVolume)

while True:
    try:
        # Récupère la commande depuis le serveur Flask
        r = requests.get(REMOTE_URL + '/next-command')
        command = r.json().get('command')
        print(f"Commande reçue pour traitement : {command}")  # Affiche la commande reçue
        
        # Récupère l'interface de contrôle du volume
        interface = get_volume_interface()

        # Traitement des commandes
        if command == 'volume_up':
            v = interface.GetMasterVolumeLevelScalar()
            interface.SetMasterVolumeLevelScalar(min(v + 0.1, 1.0), None)
            print("Volume augmenté")
        elif command == 'volume_down':
            v = interface.GetMasterVolumeLevelScalar()
            interface.SetMasterVolumeLevelScalar(max(v - 0.1, 0.0), None)
            print("Volume diminué")
        elif command == 'mute':
            interface.SetMute(1, None)
            print("Son coupé")
        elif command == 'unmute':
            interface.SetMute(0, None)
            print("Son rétabli")
        elif command == 'pause':
            pyautogui.press('space')
            print("Lecture mise en pause/reprise")
        else:
            print("Commande non reconnue")

    except Exception as e:
        print(f"Erreur : {e}")

    time.sleep(2)  # Attente de 2 secondes avant de récupérer la prochaine commande
