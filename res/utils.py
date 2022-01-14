import json, math

_SETTINGSJSON = 'settings.json'


def load_settings() -> dict:
    with open(_SETTINGSJSON, mode='r') as st:
        settings = st.read()
        settings = (json.loads(settings))
        st.close()
    return settings


def change_settings(field: str, value):
    settings = load_settings()
    with open(_SETTINGSJSON, 'w') as setjson:
        settings[field] = value
        json.dump(settings, setjson)
        setjson.close()


def cartesian(latitude, longitude, elevation = 0):
    # Convert to radians
    latitude = latitude * (math.pi / 180)
    longitude = longitude * (math.pi / 180)

    R = 6371 # 6378137.0 + elevation  # relative to centre of the earth
    X = R * math.cos(latitude) * math.cos(longitude)
    Y = R * math.cos(latitude) * math.sin(longitude)
    Z = R * math.sin(latitude)

    return (X, Y, Z)


def trilaterate(dataset: list) -> list:
    # dataset to variables
    x1, y1, r1 = dataset[0]
    x2, y2, r2 = dataset[1]
    x3, y3, r3 = dataset[2]

    # calculate system coefficients
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2

    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # calculate coordinates for system solution
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    return x, y
