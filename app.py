from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
last_command = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-command', methods=['POST'])
def send_command():
    global last_command
    data = request.get_json()
    last_command = data.get('command')
    print(f"Commande reçue : {last_command}")  # Affiche la commande reçue dans les logs
    return jsonify({'message': f"Commande '{last_command}' reçue avec succès."})

@app.route('/next-command', methods=['GET'])
def next_command():
    global last_command
    cmd = last_command
    last_command = None  # Réinitialise après lecture
    return jsonify({'command': cmd})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Lancement sur le port 10000
