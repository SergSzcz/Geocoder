from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
import pandas

app = Flask(__name__)
UPLOAD_FOLDER = '/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
coder = Nominatim()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #methos is necessary for code to be working with HTML code
def success():
    if request.method == 'POST':
        file = request.files['myFile']
        if file.filename == '':
            return render_template("index.html", text = "Nie wybrałeś pliku!")
        if '.csv' not in file.filename:
            return render_template("index.html", text = "Nie wybrałeś pliku .csv!")
        df = pandas.read_csv(file.filename)
        count = 0
        for item in df.columns.values:
            if item == 'Address' or item == 'address':
                count = count + 1
            else:
                continue
        if count == 0:
            return render_template("index.html", text = "Brak kolumny <i>Address</i> lub <i>address</s>!")
        if "Address" in df.columns.values:
            adres = "Address"
        elif "address" in df.columns.values:
            adres = "address"
        df["Coordinates"]=df[adres].apply(coder.geocode)
        df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
        df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
        df = df.drop('Coordinates',1)
        df.to_csv('uploads\Coordinates.csv')
        g=df.to_html()
        return render_template('success.html',tabela = g)

@app.route("/indexy", methods=['POST'])
def indexy():
    return render_template("index.html")

if __name__ == '__main__':
    app.debug=True
    app.run()
