import requests
import os

from healthcheck import HealthCheck
from flask import Response, request
from app import app

HEALTH = HealthCheck()
PSKEY = os.getenv('PSKEY')
RUNAS = os.getenv('RUNAS')
BASE = os.getenv('BASE')

# Flask routes to expose app information
app.add_url_rule("/healthcheck",
                 "healthcheck", view_func=HEALTH.run)

@app.route('/vault/v1.0/<systemName>/<accountName>')
def get_credentials(systemName,accountName):
    header = {'Authorization': 'PS-Auth key=' + str(PSKEY) + '; runas=' + str(RUNAS) + ';'}

    session = requests.Session()

    session.headers.update(header)

    response = session.post(str(BASE) + '/Auth/SignAppin', verify=False)

    print(response.status_code)

    accounts = session.get(str(BASE) + '/ManagedAccounts?systemName='+ str(systemName), verify=False)

    envelopes = accounts.json()

    if not envelopes:
        print("El sobre no se encuentra, por favor contacte a Seguridad Unix-Oracle")
        return Response("El sobre del usuario: " + str(accountName) + " no se encuentra, por favor contacte a Seguridad Unix-Oracle", status=404, mimetype='application/json')

    index = 0

    while index < len(envelopes):
        for key in envelopes[index]:
            if envelopes[index][key] == str(accountName):
                print(envelopes[index]["AccountName"])
                api_body = {
                    "AccessType": "View",
                    "SystemId": envelopes[index]["SystemId"],
                    "AccountId": envelopes[index]["AccountId"],
                    "DurationMinutes": 5,
                    "TicketNumber": "N/A",
                    "ConflictOption": "reuse",
                    "Reason": "Test"
                }
        index += 1

    try:
       requestcred = session.post(str(BASE) + '/Requests', data=api_body)
    except UnboundLocalError:
       print("El sobre no se encuentra, por favor contacte a Seguridad")
       return Response("El sobre del usuario: "+ str(username) +" no se encuentra, por favor contacte a Seguridad", status=404, mimetype='application/json')

    print("RequestID: " + str(requestcred.json()))

    passwd = session.get(str(BASE) + '/Credentials/' + str(requestcred.json()))

    session.put(str(BASE) + '/Requests/' + str(requestcred.json()) + '/Checkin')

    return passwd.json()


@app.route('/api/v1.0/<systemname>')
def credentials_ad(systemname):
    header = {'Authorization': 'PS-Auth key=' + str(PSKEY) + '; runas=' + str(RUNAS) + ';'}

    session = requests.Session()

    session.headers.update(header)

    response = session.post(str(BASE) + '/Auth/SignAppin', verify=False)

    print(response.status_code)

    accounts = session.get(str(BASE) + '/ManagedAccounts?systemName=' + str(systemname), verify=False)

    print(accounts.content)

    api_body = {
        "AccessType": "View",
        "SystemId": accounts.json()[0]["SystemId"],
        "AccountId": accounts.json()[0]["AccountId"],
        "DurationMinutes": 45,
        "TicketNumber": "N/A",
        "ConflictOption": "reuse",
        "Reason": "Test"
    }

    requestcred = session.post(str(BASE) + '/Requests', data=api_body)

    print("RequestID: " + str(requestcred.json()))

    passwd = session.get(str(BASE) + '/Credentials/' + str(requestcred.json()))

    session.put(str(BASE) + '/Requests/' + str(requestcred.json()) + '/Checkin')

    return passwd.json()

@app.route('/api/v1.0/was/<username>')
def credentials_was(username):
    header = {'Authorization': 'PS-Auth key=' + str(PSKEY) + '; runas=' + str(RUNAS) + ';'}

    session = requests.Session()

    session.headers.update(header)

    response = session.post(str(BASE) + '/Auth/SignAppin', verify=False)

    print(response.status_code)

    accounts = session.get(str(BASE) + '/ManagedAccounts?systemName=DCRIO06', verify=False)

    envelopes = accounts.json()

    if not envelopes:
        print("El sobre no se encuentra, por favor contacte a Seguridad Unix-Oracle")
        return Response("El sobre del usuario: " + str(username) + " no se encuentra, por favor contacte a Seguridad Unix-Oracle", status=404, mimetype='application/json')

    index = 0

    while index < len(envelopes):
        for key in envelopes[index]:
            if envelopes[index][key] == str(username):
                print(envelopes[index]["AccountName"])
                api_body = {
                    "AccessType": "View",
                    "SystemId": envelopes[index]["SystemId"],
                    "AccountId": envelopes[index]["AccountId"],
                    "DurationMinutes": 5,
                    "TicketNumber": "N/A",
                    "ConflictOption": "reuse",
                    "Reason": "Test"
                }
        index += 1

    try:
       requestcred = session.post(str(BASE) + '/Requests', data=api_body)
    except UnboundLocalError:
       print("El sobre no se encuentra, por favor contacte a Seguridad Unix-Oracle")
       return Response("El sobre del usuario: "+ str(username) +" no se encuentra, por favor contacte a Seguridad Unix-Oracle", status=404, mimetype='application/json')

    print("RequestID: " + str(requestcred.json()))

    passwd = session.get(str(BASE) + '/Credentials/' + str(requestcred.json()))

    session.put(str(BASE) + '/Requests/' + str(requestcred.json()) + '/Checkin')

    return passwd.json()

@app.route('/api/v1.0/dbora')
def credentials_db_list():
    header = {'Authorization': 'PS-Auth key=' + str(PSKEY) + '; runas=' + str(RUNAS) + ';'}

    session = requests.Session()

    session.headers.update(header)

    response = session.post(str(BASE) + '/Auth/SignAppin', verify=False)

    print(response.status_code)

    accounts = session.get(str(BASE) + '/ManagedAccounts', verify=False)

    print(accounts.content)

    return Response(accounts.content, status=200, mimetype='application/json')

@app.route('/api/v1.0/dbora/<dbinstance>/<schema>')
def credentials_ora(dbinstance,schema):
    header = {'Authorization': 'PS-Auth key=' + str(PSKEY) + '; runas=' + str(RUNAS) + ';'}

    session = requests.Session()

    session.headers.update(header)

    response = session.post(str(BASE) + '/Auth/SignAppin', verify=False)

    print(response.status_code)

    accounts = session.get(str(BASE) + '/ManagedAccounts?InstanceName=' + str(dbinstance) + '&AccountName=' + str(schema), verify=False)

    print(accounts.content)

    envelopes = accounts.json()

    if not envelopes:
        print("El sobre no se encuentra, por favor contacte a Seguridad Unix-Oracle")
        return Response("El sobre de la Instancia: "+ str(dbinstance) +" y Schema: "+ str(schema) +" no se encuentra, por favor contacte a Seguridad Unix-Oracle", status=404, mimetype='application/json')

    index = 0

    while index < len(envelopes):
        for key in envelopes[index]:
            if envelopes[index][key]==str(dbinstance):
                print(envelopes[index]["InstanceName"] + "," + envelopes[index]["AccountName"])
                api_body = {
                    "AccessType": "View",
                    "SystemId": envelopes[index]["SystemId"],
                    "AccountId": envelopes[index]["AccountId"],
                    "DurationMinutes": 5,
                    "TicketNumber": "N/A",
                    "ConflictOption": "reuse",
                    "Reason": "Test"
                }
        index += 1

    try:
       requestcred = session.post(str(BASE) + '/Requests', data=api_body)
    except UnboundLocalError:
       print("El sobre no se encuentra, por favor contacte a Seguridad Unix-Oracle")
       return Response("El sobre de la Instancia: "+ str(dbinstance) +" y Schema: "+ str(schema) +" no se encuentra, por favor contacte a Seguridad Unix-Oracle", status=404, mimetype='application/json')

    print("RequestID: " + str(requestcred.json()))

    passwd = session.get(str(BASE) + '/Credentials/' + str(requestcred.json()))

    session.put(str(BASE) + '/Requests/' + str(requestcred.json()) + '/Checkin')

    return passwd.json()
