import json
from main import main

Cities = {'Brno':(49.19564, 16.60895),
          'Jihlava': (49.39933, 15.58344),
          'Prague': (50.08144, 14.424088),
          'Beroun': (49.964855, 14.07005),
          'Hradec Kralove': (50.20604, 15.83271)
}

Test_pool = {'Munich':(48.13743, 11.57549),
          'Monaco': (43.72687, 7.41766),
          'Lviv': (49.83826, 24.02324),
          'Zagreb': (45.81444, 15.97798),
          'Bratislava': (48.14816, 17.10674),
          'Venice':(45.43713, 12.33265),
          'Barcelona': (41.38879, 2.15899),
          'Amsterdam': (52.37403, 4.88969),
          'Colchester': (51.88921, 0.90421),
          'Oslo': (59.91273, 10.74609)
}

def create(cities):
    cit = []
    with open('new.json', 'w') as f:
        for city, coordinates in cities.items():
            jsoned = {'name': city, 'latitude': coordinates[0], 'longitude': coordinates[1]}
            cit.append(jsoned)
        f.write(json.dumps(cit))
    return True

def test_basic():
    if create(Cities):
        assert main("new.json") == 458.6746904624481

test_basic()