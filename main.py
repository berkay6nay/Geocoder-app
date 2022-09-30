from flask import Flask,request,render_template,send_file
import pandas
from werkzeug.utils import secure_filename
from geopy.geocoders import ArcGIS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/success",methods = ["POST"])
def success():
    if request.method == "POST":
        file = request.files["file"]
        file.save(secure_filename("file_to_work_on"+".csv"))
        global data
        data=pandas.read_csv("file_to_work_on"+".csv")
        print(data)

        if "Address"  in data.columns:
            nom = ArcGIS()
            address_list = data["Address"]
            print(address_list)
            latitude_list = []
            longitude_list = []
            for address in address_list:
                print(address)
                try:
                    latitude_list.append(nom.geocode(address).latitude)

                except:
                    latitude_list.append("Null")
                try:
                    longitude_list.append(nom.geocode(address).longitude)

                except:
                    longitude_list.append("Null")
            data["Longitude"] = longitude_list
            data["Latitude"] = latitude_list
            print(data["Longitude"])
            return render_template("index.html", btn = "download.html",text = data.to_html())
        if "address"  in data.columns:
            nom = ArcGIS()
            address_list = data["address"]
            latitude_list = []
            longitude_list = []
            for address in address_list:
                try:
                    latitude_list.append(nom.geocode(address).latitude)

                except:
                    latitude_list.append("Null")
                try:
                    longitude_list.append(nom.geocode(address).longitude)

                except:
                    longitude_list.append("Null")
            data["Longitude"] = longitude_list
            data["Latitude"] = latitude_list
            return render_template("index.html", btn = "download.html",text = data.to_html())
        else:
            return render_template("error.html")



@app.route("/download")
def download():
    data.to_csv("yourfile.csv",index = False)
    return send_file("yourfile.csv" ,attachment_filename  = "yourfile.csv",as_attachment = True)




if __name__ == "__main__":
    app.debug = True
    app.run()
