from flask import Flask, redirect, request, jsonify, send_file
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from selenium import webdriver
import tempfile
import os

import hashlib
import base64
import re

import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/flask_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


#Model 
class InfoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mainlink = db.Column(db.String())
    shortlink = db.Column(db.String())
    screenshot = db.Column(db.LargeBinary(length=(2**32)-1))
 
    def __init__(self, mainLink, shortLink, screenshot):
        self.mainlink = mainLink
        self.shortlink = shortLink
        self.screenshot = screenshot

class InfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'mainlink', 'shortlink', 'screenshot')        

info_schema = InfoSchema()
info_schema = InfoSchema(many=True) 


#Methods
def getShortedLink(mainLink):
    # определяем строку, для которой нужно создать хеш-код
    input_string = mainLink

    # создаем объект хеша blake2b
    hash_object = hashlib.blake2b(digest_size=6)

    # обновляем объект хеша строкой
    hash_object.update(input_string.encode())

    # получаем хеш-код строки
    hash_code = hash_object.hexdigest()

    # кодируем хеш-код в Base64
    encoded_hash_code = base64.b64encode(bytes.fromhex(hash_code)).decode()

    # удаляем символы /, = и +
    encoded_hash_code = re.sub('[/+=]', '', encoded_hash_code)
    
    count = 1
    while count<9:
        hash = (encoded_hash_code)[:count]
        shortLink = InfoModel.query.filter_by(shortlink=hash).first()
        if not shortLink:
            return hash
        count+=1
    return "collision"


def getScreensot(url):    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')

    browser = webdriver.Firefox()
    browser.get(url)
    browser.save_screenshot(temp_file.name)
    
    browser.quit()
    return temp_file


#Routes
@app.route('/putimage/<id>', methods=['PUT'])
def put_image(id):
    row = InfoModel.query.get(id)
    if row.screenshot != None:
        return send_file(io.BytesIO(row.screenshot), mimetype='image/png')
    else:
        file = getScreensot(row.mainlink)
        screenshot = file.read()
        file.close()
        os.remove(file.name)

        row.screenshot = screenshot
        db.session.commit()

        return send_file(io.BytesIO(screenshot), mimetype='image/png')


@app.route('/send', methods = ['POST'])
def send():
    mainLink = request.json['mainLink']
    foundLink = InfoModel.query.filter_by(mainlink=mainLink).first()
    if foundLink:            
        return jsonify({'id':foundLink.id, 'shortlink':foundLink.shortlink})
    else:
        shortLink = getShortedLink(mainLink)        
            
        new_row = InfoModel(mainLink, shortLink, None)

        db.session.add(new_row)
        db.session.commit()

        return jsonify({'id': new_row.id, 'shortlink': shortLink})        


@app.route('/r/<shorthash>')
def redirection(shorthash):
    mainLink = InfoModel.query.filter_by(shortlink=shorthash).first()
    print(mainLink)
    if mainLink:
        return redirect(mainLink.mainlink)
    else:
        return redirect('http://192.168.3.2:3000/404')


@app.route('/404')
def error_page():    
    return f"Ссылка недействительна, такой страницы нет, обратитесь в поддержку!"

@app.route('/collision')
def collision_page():    
    return f"Коллизия хэш кода, обратитесь в поддержку!"

 
if __name__ == '__main__':
    app.run(host='192.168.3.2', port=3000, debug=True)