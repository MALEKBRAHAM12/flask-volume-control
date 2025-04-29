from flask import Flask, render_template, jsonify
from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume
import comtypes
import pyautogui 

app = Flask(__name__)
app.config['DEBUG'] = True

def get_volume_interface():
     
    comtypes.CoInitialize()

    devices = AudioUtilities.GetSpeakers()

    
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 
        1, 
        None)
    
    
    return interface.QueryInterface(IAudioEndpointVolume)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/volume/up', methods=['POST'])
def volume_up():
    interface = get_volume_interface()
    volume = interface.GetMasterVolumeLevelScalar()
    new_volume = min(volume + 0.1, 1.0)  
    interface.SetMasterVolumeLevelScalar(new_volume, None)
    return jsonify({"message": "Volume augmenté"})


@app.route('/volume/down', methods=['POST'])
def volume_down():
    interface = get_volume_interface()
    volume = interface.GetMasterVolumeLevelScalar()
    new_volume = max(volume - 0.1, 0.0)  
    interface.SetMasterVolumeLevelScalar(new_volume, None)
    return jsonify({"message": "Volume diminué"})


@app.route('/volume/mute', methods=['POST'])
def mute():
    interface = get_volume_interface()
    interface.SetMute(1, None)  
    return jsonify({"message": "Son coupé"})


@app.route('/volume/unmute', methods=['POST'])
def unmute():
    interface = get_volume_interface()
    interface.SetMute(0, None)  
    return jsonify({"message": "Son rétabli"})

@app.route('/audio/pause', methods=['POST'])
def pause_audio():
    pyautogui.press('space') 
    return jsonify({"message": "Lecture audio mise en pause/reprise"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
