import json
import logging
import math
import time

import requests as req
from pypresence import Presence


with open("cities.json", "r") as f:
    cities = json.load(f)
    
START_TIME = int(time.time())


def get_data():
    try:
        response = req.get("http://localhost:25555/api/ets2/telemetry")
        raw_data = json.loads(response.content)
        return raw_data
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\n")
        print("\nFatal error: Please make sure that the ETS 2 / ATS Telemetry server is open before "
              "running this application.\n")
        input("Press enter key to exit....")
        exit(1)


def start():
    raw_data = get_data()
    game_data = raw_data["game"]
    if game_data["gameName"]:
        if game_data["gameName"] == "ETS2":
            client_id = "1313236581859201074"  # App client ID from discord developer portal
        elif game_data["gameName"] == "ATS":
            client_id = "1313236581859201074"  # App client ID from discord developer portal
        print(f'{game_data["gameName"]} connected...')
        run(client_id)
    else:
        print("Waiting for game to connect...")
        time.sleep(3.5)
        start()
    
def get_city_translation(name: str) -> str:
    for city in cities:
        if city["Name"] == name:
            return city["LocalizedNames"]["uk_uk"]
    return "Translation not found"

def get_country(name: str) -> str:
    for city in cities:
        if city["Name"] == name:
            return city["Country"]
    return "Country not found"

def find_nearest_city(x, z):
    nearest_city = None
    min_distance = float("inf")

    for city in cities:
        city_x = city["X"]
        city_z = city["Z"]
        distance = math.sqrt((city_x - x)**2 + (city_z - z)**2)
        if distance < min_distance:
            min_distance = distance
            nearest_city = city

    return nearest_city


def calculate_distance(x1, z1, x2, z2):
    return math.sqrt((x2 - x1) ** 2 + (z2 - z1) ** 2)

def get_details():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        details = "Симуляція не розпочата"
    else:
        if game_data["paused"]:
            details = "На павзі"
        else:
            player_x = truck_data["placement"]["x"]
            player_z = truck_data["placement"]["z"]
            city = find_nearest_city(player_x, player_z)
            city_x = city["X"]
            city_z = city["Z"]
            distance = calculate_distance(player_x, player_z, city_x, city_z)

            print(f"Різниця дистанція між гравцем та найближчим містом({city['LocalizedNames']['uk_uk']}): {distance} м.")
            if distance <= 500:
                details = f"Відвідує місто: {city['LocalizedNames']['uk_uk']} ({city['Country']})"
            else:
                details = f"Поблизу міста: {city['LocalizedNames']['uk_uk']} ({city['Country']})"
    return details

def get_small_image():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        small_image = "None"
    else:
        if game_data["paused"]:
            small_image = "Pause"
        else:
            countries = {
                "Угорщина": "flag_hu",
                "Швейцарія": "flag_ch",
                "Естонія": "flag_ee",
                "Німеччина": "flag_de",
                "Фінляндія": "flag_fi",
                "Австрія": "flag_at",
                "Люксембург": "flag_lu",
                "Румунія": "flag_ro",
                "Бельгія": "flag_be",
                "Велика Британія": "flag_gb",
                "Болгарія": "flag_bg",
                "Словаччина": "flag_sk",
                "Латвія": "flag_lv",
                "Швеція": "flag_se",
                "Іспанія": "flag_es",
                "Чехія": "flag_cz",
                "Данія": "flag_dk",
                "Норвегія": "flag_no",
                "Нідерланди": "flag_nl",
                "Італія": "flag_it",
                "Польща": "flag_pl",
                "Франція": "flag_fr",
                "Туреччина": "flag_tk",
                "Литва": "flag_lt",
                "росія": "flag_ru",
                "Косово": "flag_xk",
                "Північна македонія": "flag_mk",
                "Греція": "flag_gr",
            }
            
            country = find_nearest_city(truck_data["placement"]["x"], truck_data["placement"]["z"])["Country"]
            small_image = countries.get(country, "logo")
            # print(f"Країна: {country}", f"Прапор: {small_image}")
    return small_image

def get_small_text():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        small_text = "None"
    else:
        country = find_nearest_city(truck_data["placement"]["x"], truck_data["placement"]["z"])["Country"]
        small_text = country
    return small_text


def get_state():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]
    job_data = raw_data["job"]
    trailer_data = raw_data["trailer"]

    if not game_data["connected"]:
        state = "Очікування завантаження симулятора"
    else:
        if game_data["paused"]:
            state = "Водій п'є каву"
        else:
            if job_data["income"] != 0:
                goods = trailer_data["name"]
                
                sourceCity = get_city_translation(job_data["sourceCity"])
                destinationCity = get_city_translation(job_data["destinationCity"])
                
                if goods:
                    if sourceCity != "Translation not found" or destinationCity != "Translation not found":
                        state = f"Перевозить: {goods} з {job_data["sourceCompany"]}({sourceCity}) до {job_data['destinationCompany']}({destinationCity})"
                    else:
                        state = f"Перевозить: {goods}"
                else:
                    state = "Доставляє вантаж."
            else:
                state = "Вільний, як вітер."
    return state


def run(client_id):
    try:
        RPC = Presence(client_id)
        RPC.connect()
        print("Running...\n"
              "NOTE:\n"
              "If you are playing ETS 2 and want to start playing ATS (or vice-versa) then "
              "after closing ETS 2 and before starting ATS you must RESTART this application ALONG WITH the ETS 2 "
              "TELEMETRY SERVER also.\n"
              "Close this window once you are done playing the game...")
        while True:
            # Image section needs to be updated
            
            RPC.update(state=get_state(), details=get_details(),
                       start=START_TIME, large_image="logo",
                       large_text="Euro Truck Simulator 2",
                       small_image=get_small_image(),
                       small_text=get_small_text())
            time.sleep(1)
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\nPlease make sure that Discord is open and running...")
        print("\nFatal error: Please make sure that Discord is open before "
              "running this application.\n")
        input("Press enter key to exit....")
        exit(1)


start()