import requests
import pandas as pd
import zipfile
import io
import re
import os

#Basis-URL für die DWD Wetterdaten
base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/"

#URL Endungen
data_types = {
    "temperature_historical": "air_temperature/historical/",
    "temperature_recent": "air_temperature/recent/",
    "cloudiness_historical": "cloudiness/historical/",
    "cloudiness_recent": "cloudiness/recent/",
    "pressure_historical": "pressure/historical/",
    "pressure_recent": "pressure/recent/",
    "sun_historical": "sun/historical/",
    "sun_recent": "sun/recent/",
    "wind_historical": "wind/historical/",
    "wind_recent": "wind/recent/",
}

#Liste der Stations-IDs
#station_ids = ["00722", "01262", "01975", "02667", "02932"]
station_ids = ["00722"]

#Speicherort
output_folder = "./Data/Weather/autoweather"

#Funktion zur Suche und Herunterladen der Wetterdaten pro Station
def get_weather_data_for_station(station_id):
    for data_type, endpoint in data_types.items():

        #URL erstellen
        url = base_url + endpoint
        
        #Esrtellt Liste von Dateien im Verzeichnis
        response = requests.get(url)
        response.raise_for_status()

        #Suche nach passender ZIP-Datei
        for line in response.text.splitlines():
            if station_id in line and "zip" in line:
                filename = re.search(r'href="(.*?)"', line).group(1)
                file_url = url + filename
                
                #Lade ZIP-Datei herunter
                print(f"Lade herunter: {file_url}")
                file_response = requests.get(file_url)
                file_response.raise_for_status()
                
                #Entpacke ZIP-Datei und suche passender TXT-Datei in der ZIP
                with zipfile.ZipFile(io.BytesIO(file_response.content)) as z:
                    if data_type == "cloudiness_historical" or data_type == "cloudiness_recent":
                        txt_files = [name for name in z.namelist() if re.match(r'produkt_n_stunde_\d{8}_\d{8}_' + station_id + r'\.txt', name)]
                    elif data_type == "pressure_historical" or data_type == "pressure_recent":
                        txt_files = [name for name in z.namelist() if re.match(r'produkt_p0_stunde_\d{8}_\d{8}_' + station_id + r'\.txt', name)]
                    elif data_type == "sun_historical" or data_type == "sun_recent":
                        txt_files = [name for name in z.namelist() if re.match(r'produkt_sd_stunde_\d{8}_\d{8}_' + station_id + r'\.txt', name)]
                    elif data_type == "wind_historical" or data_type == "wind_recent":
                        txt_files = [name for name in z.namelist() if re.match(r'produkt_ff_stunde_\d{8}_\d{8}_' + station_id + r'\.txt', name)]
                    else:
                        txt_files = [name for name in z.namelist() if re.match(r'produkt_tu_stunde_\d{8}_\d{8}_' + station_id + r'\.txt', name)]
                    
                    if not txt_files:
                        print(f"Keine TXT-Datei im erwarteten Format für Station {station_id} gefunden.")
                        continue  

                    #Wenn TXT-Datei gefunden wurde, lade sie in pandas
                    txt_filename = txt_files[0]
                    with z.open(txt_filename) as f:
                        #Test ob ladbar
                        try:
                            df = pd.read_csv(f, sep=";", encoding="utf-8")
                            if df.empty:
                                print(f"Warnung: Die Datei {txt_filename} ist leer.")
                            else:
                                print("Daten geladen für:", txt_filename)

                                #Ausgabeordener checken
                                os.makedirs(output_folder, exist_ok=True)
                                
                                #Dateinamen nach Datenart setzen
                                if data_type == "temperature_historical":
                                    new_filename = f"temp_{station_id}_hist.txt"
                                elif data_type == "temperature_recent":
                                    new_filename = f"temp_{station_id}_recent.txt"
                                elif data_type == "cloudiness_historical":
                                    new_filename = f"clouds_{station_id}_hist.txt"
                                elif data_type == "cloudiness_recent":
                                    new_filename = f"clouds_{station_id}_recent.txt"
                                elif data_type == "pressure_historical":
                                    new_filename = f"pressure_{station_id}_hist.txt"
                                elif data_type == "pressure_recent":
                                    new_filename = f"pressure_{station_id}_recent.txt"
                                elif data_type == "sun_historical":
                                    new_filename = f"sun_{station_id}_hist.txt"
                                elif data_type == "sun_recent":
                                    new_filename = f"sun_{station_id}_recent.txt"
                                elif data_type == "wind_historical":
                                    new_filename = f"wind_{station_id}_hist.txt"
                                elif data_type == "wind_recent":
                                    new_filename = f"wind_{station_id}_recent.txt"
                                
                                
                                #Speichere TXT-Datei im angegebenen Ordner
                                output_filepath = os.path.join(output_folder, new_filename)
                                df.to_csv(output_filepath, sep=";", encoding="utf-8", index=False)
                                print(f"Wetterdaten gespeichert unter: {output_filepath}")
                                
                                
                                print(f"Die Datei wurde erfolgreich gespeichert unter: {os.path.abspath(output_filepath)}")
                        except Exception as e:
                            print(f"Fehler beim Laden der Datei {txt_filename}: {e}")

    return None  #Rückgabe, wenn keine Datei gefunden wird

#Funktion zum Herunterladen der Wetterdaten für alle angegebenen Stationen
def download_weather_data_for_all_stations(station_ids):
    for station_id in station_ids:
        print(f"Starte den Download für Station {station_id}...")
        get_weather_data_for_station(station_id)
        print()

#Starte Download
download_weather_data_for_all_stations(station_ids)
