#Author: Noname
#Date: 19.12.2020
#Purpose: This is a Scrpit to log the Time, Programms are used on a PC

print("importing...")
from flask import Flask, render_template, Markup, request
import os
import datetime
import calendar
import json
from packaging.version import Version

print("loading...")

app = Flask(__name__)

datapath = "C:\\Users\\Nutzer\\Desktop\\Tools\\TimeLogger2.0\\TimeLogs\\"



@app.route("/")
def main():
    return render_template("main.html")


@app.route("/times/")
def times():
    found = readTimes(datapath)
    data = found[0]
    d_on = found[2]
    d_off = found[3]

    amount = float(0.1)

    if request.method == "GET":
        if "amount" in request.args:
            amount = request.args["amount"]
            amount = amount

    return render_template("graph.html",
                           PY_DATA=Markup(data),
                           PY_DATA_UNDERTITLES=Markup(found[1]),
                           PY_DATA_D_ON=round(d_on, 2),
                           PY_DATA_D_OFF=round(d_off, 2),
                           PY_SETTINGS_AMOUNT=amount
                           )


def readTimes(datapath):
    datelist = []

    result_list = []

    #values uesd to calculate average On/Off Times
    durchschnitt_on = 0
    durchschnitt_off = 0
    howmany_files_found = 0

    files = []
    file_list = os.listdir(datapath)
    for qpmva in file_list:
        if str(qpmva).startswith("date"):
            files.append(str(qpmva).replace("date@", "").replace(".json", "").replace("-", "."))

    files = sorted(files, key=lambda elt: Version(elt))
    print("-------------------------------------------------" + "Processment" + "-------------------------------------------------")
    for cf in files:
        cf = "date@"+cf.replace(".", "-")+".json"
        if str(cf).startswith("date"):
            howmany_files_found += 1
            with open(datapath+"/"+cf, "r") as infile:
                data = json.load(infile)
                #--------------------------------------------------------------Work Here--------------------------------------------------------------

                result_list.append(data)
                
                offtime = 0
                ontime = 0
                for ct in data:         #Interation durch die An diesem Tag geloggten Programme
                    tag = ct
                    time = data[ct][0]
                    lastTitle = data[ct][1]

                    if tag == "OFF-TIME":     #Offline
                        offtime += time
                    else:                   #Online
                        ontime += time

                durchschnitt_on += ontime
                durchschnitt_off += offtime

                datelist.append(str(cf).replace("date@", "").replace(".json", "").replace("-", "."))


    if howmany_files_found != 0:
        durchschnitt_on /= howmany_files_found
        durchschnitt_off /= howmany_files_found


    if request.method == "GET":
        if "days" in request.args:
            days = int(request.args["days"])
            return [result_list[-days:], datelist[-days:], durchschnitt_on / 60 / 60, durchschnitt_off / 60 / 60]


    return [result_list, datelist, durchschnitt_on/60/60, durchschnitt_off/60/60]




if(__name__=="__main__"):
    app.run(host="0.0.0.0", port=34567, debug=True)
