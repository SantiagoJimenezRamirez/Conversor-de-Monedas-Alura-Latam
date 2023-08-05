from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open('data.json', 'r') as json_file:
            data = json_file.read()
            return data, 200
    except FileNotFoundError:
        return 'Archivo no encontrado', 404

if __name__ == '__main__':
    app.run()