
import json, math

_SETTINGSJSON = 'settings.json'

def load_settings() -> dict:
    with open(_SETTINGSJSON, mode='r') as st:
        settings = st.read()
        settings = (json.loads(settings))
        st.close()
    return settings

def change_settings(field : str, value):
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
