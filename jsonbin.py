import requests

BIN_API_URL = r'https://api.jsonbin.io/v3/b'

# Funktionen für den "sick"-Teil

def load_data(api_key_sick, bin_id_sick):
    """
    Lädt den gesamten Bin
    """
    url_sick = BIN_API_URL + '/' + bin_id_sick + '/latest'
    headers_sick = {'X-Master-Key': api_key_sick}
    response_sick = requests.get(url_sick, headers=headers_sick).json()
    return response_sick['record']


def save_data(api_key_sick, bin_id_sick, data_sick):
    """
    Speichert den gesamten Bin
    """
    url_sick = BIN_API_URL + '/' + bin_id_sick
    headers_sick = {'X-Master-Key': api_key_sick, 'Content-Type': 'application/json'}
    response_sick = requests.put(url_sick, headers=headers_sick, json=data_sick).json()
    return response_sick


def load_key(api_key_sick, bin_id_sick, key_sick, empty_value=[]):
    """
    Lädt den Wert für einen bestimmten Schlüssel aus dem Bin
    """
    url_sick = BIN_API_URL + '/' + bin_id_sick + '/latest'
    headers_sick = {'X-Master-Key': api_key_sick}
    response_sick = requests.get(url_sick, headers=headers_sick).json()
    record_sick = response_sick['record']
    if key_sick in record_sick:
        return record_sick[key_sick]
    else:
        return empty_value


def save_key(api_key_sick, bin_id_sick, key_sick, data_sick):
    """
    Speichert den Wert für einen bestimmten Schlüssel im Bin
    """
    url_sick = BIN_API_URL + '/' + bin_id_sick
    headers_sick = {'X-Master-Key': api_key_sick, 'Content-Type': 'application/json'}
    response_sick = requests.get(url_sick, headers=headers_sick).json()
    record_sick = response_sick['record']
    if type(record_sick) != dict:
        record_sick = {key_sick: data_sick}  # erzeuge ein neues Dictionary
    else:
        record_sick[key_sick] = data_sick
    response_sick = requests.put(url_sick, headers=headers_sick, json=record_sick).json()
    return response_sick


# Funktionen für den "med"-Teil

def load_data(api_key_med, bin_id_med):
    """
    Lädt den gesamten Bin
    """
    url_med = BIN_API_URL + '/' + bin_id_med + '/latest'
    headers_med = {'X-Master-Key': api_key_med}
    response_med = requests.get(url_med, headers=headers_med).json()
    return response_med['record']


def save_data(api_key_med, bin_id_med, data_med):
    """
    Speichert den gesamten Bin
    """
    url_med = BIN_API_URL + '/' + bin_id_med
    headers_med = {'X-Master-Key': api_key_med, 'Content-Type': 'application/json'}
    response_med = requests.put(url_med, headers=headers_med, json=data_med).json()
    return response_med


def load_key(api_key_med, bin_id_med, key_med, empty_value=[]):
    """
    Lädt den Wert für einen bestimmten Schlüssel aus dem Bin
    """
    url_med = BIN_API_URL + '/' + bin_id_med + '/latest'
    headers_med = {'X-Master-Key': api_key_med}
    response_med = requests.get(url_med, headers=headers_med).json()
    record_med = response_med['record']
    if key_med in record_med:
        return record_med[key_med]
    else:
        return empty_value


def save_key(api_key_med, bin_id_med, key_med, data_med):
    """
    Speichert den Wert für einen bestimmten Schlüssel im Bin
    """
    url_med = BIN_API_URL + '/' + bin_id_med
    headers_med = {'X-Master-Key': api_key_med, 'Content-Type': 'application/json'}
    response_med = requests.get(url_med, headers=headers_med).json()
    record_med = response_med['record']
    if type(record_med) != dict:
        record_med = {key_med: data_med}  # generate new dict
    else:
        record_med[key_med] = data_med
    response_med = requests.put(url_med, headers=headers_med, json=record_med).json()
    return response_med
