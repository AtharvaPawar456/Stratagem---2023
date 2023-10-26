from flask import Flask
from PIL import Image
import base64
from io import BytesIO
import requests

app = Flask(__name__)

#By using the <path: url> specifier, we ensure that the string that will come after send-image / is taken as a whole.
@app.route("/send-image/<path:url>")
def image_check(url):
    
    '''
    FUTURE PROCESS
    '''
    
    # When you type http://127.1.0.0:5000/send-image/https://sample-website.com/sample-cdn/photo1.jpg to the browser
    # you will se the whole "https://sample-website.com/sample-cdn/photo1.jpg"
    return url

if __name__ == '__main__':
    app.run(host='0.0.0.0')