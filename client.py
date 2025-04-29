import requests
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes
import pyautogui

REMOTE_URL = 'https://flask-volume-control.onrender.com'  # 🔁 À modifier selon ton URL Render

def get_volume_interface():
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)
    return interface.QueryInterface(IAudioEndpointVolume)

while True:
    try:
        r = requests.get(REMOTE_URL)
        cmd = r.json().get('command')

        interface = get_volume_interface()

        if cmd == 'volume_up':
            v = interface.GetMasterVolumeLevelScalar()
            interface.SetMasterVolumeLevelScalar(min(v + 0.1, 1.0), None)
        elif cmd == 'volume_down':
            v = interface.GetMasterVolumeLevelScalar()
            interface.SetMasterVolumeLevelScalar(max(v - 0.1, 0.0), None)
        elif cmd == 'mute':
            interface.SetMute(1, None)
        elif cmd == 'unmute':
            interface.SetMute(0, None)
        elif cmd == 'pause':
            pyautogui.press('space')

    except Exception as e:
        print("Erreur :", e)

    time.sleep(2)
