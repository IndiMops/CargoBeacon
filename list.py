import json

with open("cities.json", "r") as f:
    cities = json.load(f)

def get_unique_countries(cities_data):
    countries = set()  # Використовуємо set для уникнення дублювання
    
    for city in cities_data:
        countries.add(city["Country"])  # Додаємо країну в set
    
    return countries


countries_set = get_unique_countries(cities)
print(countries_set)