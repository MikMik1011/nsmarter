import requests
import json
import utils

with open("./config.json") as f:
    config = json.load(f)
try:
    with open("./data/stations.json") as f:
        stations = json.load(f)
except:
    stations = {}


def checkStation(id):
    arrivals = []

    resp = requests.get(
            f"{config['stationEndpointURL']}{id}",
            headers={"X-Api-Authentication": config["apikey"], "User-Agent": "nsmarter"},
    ).json()

    if (resp[0]['just_coordinates'] != "1"):

        for arr in resp:
            arrivals.append({
                "line": arr['line_number'],
                "eta": arr['seconds_left'],
                "lastStation": arr['vehicles'][0]['station_name']
            })
    return arrivals

def getArrivals(id):
    station = stations[str(id)]
    print(f"\n\nStanica {station['name']}: ")

    try:
        lines = checkStation(id)
    except requests.exceptions.ConnectionError:
        print("Proverite internet konekciju!")
        return

    if lines:
        for arrival in lines:
            print(f"\nLinija: {arrival['line']}")
            print(f"Procenjeno vreme do dolaska: {utils.secondsToTimeString(arrival['eta'])}")
            print(f"Trenutna stanica autobusa: {arrival['lastStation']}")
    else:
        print("Nema dolazaka!")

def searchStation(uuid):
    resp = requests.get(
            config['allStationsEndpointURL'],
            headers={"X-Api-Authentication": config["apikey"], "User-Agent": "nsmarter"},
    ).json()

    for station in resp['stations']:
        if station['station_id'] == uuid:
            st = dict()

            st['name'] = station['name']
            st['coords'] = station['coordinates']
            st['sid'] = station['station_id']

            return (station['id'], st)

def addStation(uuid):
    try:
        id, station = searchStation(uuid)
    except TypeError:
        print("Tražena stanica nije nađena!")
        return

    
    if stations.get(str(id)):
        print("Tražena stanica je već sačuvana!")
        return
    stations[str(id)] = station

    with open("./data/stations.json", "w") as f:
        json.dump(stations, f)
    
    print(f"Stanica {station['name']} je dodata!")


def printStations():
    print("\n")
    for index, id in enumerate(stations):
        print(f"{index} : {stations[id]['name']}")

    choice = input("Unesite broj ispred stanice ili ID stanice: ")

    try:
        choice = int(list(stations.keys())[int(choice)])
    except:
        pass

    if type(choice) == int:
        getArrivals(choice)
    else:
        addStation(choice)



if __name__ == "__main__":
    print("Dobrodošli u NSmarter!")
    
    while 1 < 2:
        printStations()
