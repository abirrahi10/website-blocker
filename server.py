from flask import Flask, jsonify, request, redirect
import time
from urllib.parse import unquote
from flask_cors import CORS
import ctypes

app = Flask(__name__)
CORS(app)

url_timestamp = {}
url_viewtime = {}
to_block_urls = ["www.youtube.com", "www.facebook.com", "www.twitch.tv", "www.twitter.com", "www.instagram.com"]
prev_url = ""
ip = "127.0.0.1"

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

def blocker(url):
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r+") as host:
        content = host.read()
        if url in content:
            print(url + " is already blocked")
            pass
        else:
            url_to_block = ip + "       " + url + "\n"
            host.write(url_to_block)

def unblocker():
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r+") as host:
        content = host.read()
        for i in range(len(to_block_urls)):
            if to_block_urls[i] in content:
                new_content = content.replace(to_block_urls[i], "")
                host.truncate(0)
                host.write(new_content)
            else:
                print(i + " has not been blocked")

def window_refresh_alert():
    WS_EX_TOPMOST = 0x40000
    windowTitle = "Time to Block Some Websites!"
    message = "Please close all your chrome windows. \n\nIf you don't, we cant stop you, but you wont feel great about it will you?"

    ctypes.windll.user32.MessageBoxExW(None, message, windowTitle, WS_EX_TOPMOST)

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

        if parent_url in to_block_urls and url_viewtime[parent_url] > 60:
            blocker(parent_url)
            print("blocked url: " + parent_url)
            window_refresh_alert()
            return jsonify({'message': 'blocked!'}), 403
        else:
            print("url not blocked: " + parent_url)
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
