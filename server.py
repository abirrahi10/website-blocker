from flask import Flask, jsonify, request
import time
from urllib.parse import unquote
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url_timestamp = {}
url_viewtime = {}
prev_url = ""

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_url', methods=['GET', 'POST'])
def send_url():
    if request.method == 'POST':
        data = request.form.to_dict()
        url = unquote(data.get("url", ""))

        print("currently viewing: " + url_strip(url))
        parent_url = url_strip(url)

        global url_timestamp
        global url_viewtime
        global prev_url

        print("initial db prev tab: ", prev_url)
        print("initial db timestamp: ", url_timestamp)
        print("initial db viewtime: ", url_viewtime)

        if parent_url not in url_timestamp.keys():
            url_viewtime[parent_url] = 0

        if prev_url != '':
            time_spent = int(time.time() - url_timestamp[prev_url])
            url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

        x = int(time.time())
        url_timestamp[parent_url] = x
        prev_url = parent_url
        print("final timestamps: ", url_timestamp)
        print("final viewtimes: ", url_viewtime)

        return jsonify({'message': 'success!'}), 200
    
    # Return a response for GET request
    return jsonify({'message': 'GET request received.'}), 200

@app.route('/quit_url', methods=['GET', 'POST'])
def quit_url():
    if request.method == 'POST':
        data = request.form.to_dict()
        url = unquote(data.get("url", ""))
        print("Url closed: " + url)
        return jsonify({'message': 'quit success!'}), 200
    
    # Return a response for GET request
    return jsonify({'message': 'GET request received.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
