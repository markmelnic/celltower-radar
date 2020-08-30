
import json

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