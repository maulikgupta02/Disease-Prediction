from flask import Flask,jsonify
import bluetooth
from flask import request
import time


app = Flask(__name__)

@app.route("/",methods=['POST','GET'])

def bluetooth_sweep():
    
    device_bluetoth_mac={"70:5E:55:31:86:AA":"Simardeep"}
    employee=list(device_bluetoth_mac.keys())

    available_services=bluetooth.find_service()

    nearby_devices={}
    temp=[]
    count=1
    for i in available_services:
        d={}
        if i['host'] in employee:
            emp_mac=i['host']
            emp_name=device_bluetoth_mac[i['host']]
            if emp_name not in temp:
                d["name"]=emp_name
                d["mac-address"]=emp_mac
                d["position"]=None
                temp.append(emp_name)
                nearby_devices[count]=d
                count+=1

    print(nearby_devices)
    return jsonify(nearby_devices)

if __name__ == '__main__':
    app.run()




# device_bluetoth_mac={'F0:65:AE:0E:7B:C7':"Maulik Gupta","70:5E:55:31:86:AA":"Simardeep",'48:74:12:85:A7:40':'Rachit Budhiraja'}
# employee=list(device_bluetoth_mac.keys())
# while True:
#     available_services=bluetooth.find_service()

#     nearby_devices={}
#     temp=[]
#     count=1
#     for i in available_services:
#         d={}
#         if i['host'] in employee:
#             emp_mac=i['host']
#             emp_name=device_bluetoth_mac[i['host']]
#             if emp_name not in temp:
#                 d["name"]=emp_name
#                 d["mac-address"]=emp_mac
#                 d["position"]=None
#                 temp.append(emp_name)
#                 nearby_devices[count]=d
#                 count+=1
#     print(nearby_devices)