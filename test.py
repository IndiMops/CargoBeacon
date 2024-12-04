import json
import math
import requests as req
import logging
import requests


# Завантаження даних про міста з JSON
with open("cities.json", "r") as f:
    cities = json.load(f)


# Функція для отримання даних про вантажівку
def get_data():
    try:
        response = requests.get("http://localhost:25555/api/ets2/telemetry")
        raw_data = json.loads(response.content)
        return raw_data
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\n")
        print("\nFatal error: Please make sure that the ETS 2 / ATS Telemetry server is open before "
              "running this application.\n")
        input("Press enter key to exit....")
        exit(1)

def find_nearest_city(x, z):
    nearest_city = None
    min_distance = float("inf")

    for city in cities:
        city_x = city["X"]
        city_y = city["Y"]
        distance = math.sqrt((city_x - x)**2 + (city_y - z)**2)
        if distance < min_distance:
            min_distance = distance
            nearest_city = city

    return nearest_city

def main():
    # Отримуємо координати вантажівки з API
    data = get_data()
    truck_x = data['truck']['placement']['x']
    truck_z = data['truck']['placement']['z']
    
    # Знаходимо найближче місто
    nearest_city = find_nearest_city(truck_x, truck_z)
    
    if nearest_city:
        print(f"Найближче місто: {nearest_city['LocalizedNames']['uk_uk']} ({nearest_city['Country']})")
    else:
        print("Не вдалося знайти найближче місто.")

if __name__ == "__main__":
    main()
