from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json

app = Flask(__name__)
CORS(app)

def getAddress(lat, long):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        address = data['display_name']
    return address

def sort_array_by_serial(array):
    sorted_array = sorted(array, key=lambda obj: obj['deviceSerialNumber'])
    return sorted_array

def mapArray(array):
    i = 0
    outJSON = []
    for obj in array:
        address = getAddress(obj['latitude'], obj['longitude'])
        obj['address'] = address
        outJSON.append(obj)
        i = i + 1
    sorted_array = sort_array_by_serial(outJSON)
    return sorted_array

@app.route('/api/mapArray', methods=['POST'])

def api_map_array():
    data = request.get_json()
    mapped_array = mapArray(data)
    return jsonify(mapped_array)

if __name__ == '__main__':
    app.run(debug=True)


