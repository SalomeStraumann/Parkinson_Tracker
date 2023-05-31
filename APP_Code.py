# Import der benötigten Bibliotheken
import streamlit as st
import pandas as pd
import json
import datetime
from PIL import Image
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Laden der Secrets für jsonbin.io
jsonbin_secrets = st.secrets["jsonbin"]
api_key_med = jsonbin_secrets["api_key_med"]
bin_id_med = jsonbin_secrets["bin_id_med"]
api_key_sick = jsonbin_secrets["api_key_sick"]
bin_id_sick = jsonbin_secrets["bin_id_sick"]

# Benutzerlogin
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialisierung des Authenticators
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Durchführung des Logins
fullname, authentication_status, username = authenticator.login('Login', 'main')

# Überprüfung des Login-Status
if authentication_status == True:   # Login erfolgreich
    show_logout_button = True
elif authentication_status == False:
    st.error('Benutzername/Passwort ist falsch')
    st.stop()
elif authentication_status == None:
    st.warning('Bitte Benutzername und Passwort eingeben')
    st.stop()

# Hauptseite der App
st.title("Parkinson Tracker")
# Begrüßungsnachricht
text_before = "Hallo,"
text_after = "!"
st.header("{} {}{}".format(text_before, username, text_after))
# Hinweis für den Benutzer
st.warning("Bitte beantworte die Fragen in der Seitenleiste")

# Seitenleiste
# Eingabefelder für Datum und Uhrzeit
date = st.sidebar.date_input("Datum", datetime.date(2023, 5, 20))
time = st.sidebar.time_input("Uhrzeit", datetime.time(12, 00))
# Kombination von Datum und Uhrzeit zu einem DateTime-Objekt
datetime_obj = datetime.datetime.combine(date, time)
# Formatierung des DateTime-Objekts als String
datetime_string = datetime_obj.strftime('%Y-%m-%d, %H:%M')

# Untertitel Seitenleiste - Befinden
st.sidebar.header(':blue[Befinden]')
# Liste der verfügbaren Symptome
symptoms = [
    'Taubheitsgefühl in den Beinen',
    'Taubheitsgefühl in den Armen',
    'Kribbeln in den Beinen',
    'Kribbeln in den Armen',
    'Tremor (Zittern)',
    'Steifheit der Muskeln',
    'Langsame Bewegungen',
    'Rasche Erschöpfung',
    'Probleme bei der Darmentleerung',
    'Probleme bei der Blasenentleerung',
    'Gangstörungen',
    'Gleichgewichtsstörungen',
    'Sehstörungen',
    'Lähmungserscheinungen',
    'Globale Schmerzen',
    'Keine Symptome'
]

selected_symptoms = st.sidebar.multiselect('Wähle deine aktuellen Symptome aus', symptoms)

severity_levels = {}
for symptom in selected_symptoms:
    if symptom != 'Keine Symptome':
        severity_level = st.sidebar.number_input(
            f'Wie stark ist das Symptom "{symptom}" auf einer Skala? 0 = Nicht vorhanden, 10 = Extrem stark.',
            min_value=0,
            max_value=10,
            value=5
        )
        severity_levels[symptom] = severity_level

if selected_symptoms:
    st.write(':blue[Ausgewählte Symptome und Schweregrade:]')
    for symptom in selected_symptoms:
        if symptom != 'Keine Symptome':
            severity_level = severity_levels[symptom]
            st.write(f'- {symptom}: {severity_level}')
            symptoms_and_severity = {symptom: severity_levels[symptom] for symptom in selected_symptoms if symptom != 'Keine Symptome'}
        else:
            st.write ('Keine Symptome')
            symptoms_and_severity = "Keine Symptome"
else:
    st.write('Keine Symptome ausgewählt')

# Seitenleiste
# Slider für Stärke der Limitation in der Gesamtheit
feeling = st.sidebar.slider('Wie stark limitieren dich die Symptome gerade im Alltag?', 0, 10, 1)
# Dictionary, das jedem Schweregrad eine Beschreibung zuordnet
severity_levels_lim = {
    0: 'Überhaupt nicht',
    1: 'Kaum',
    2: 'Geringfügig',
    3: 'Leicht',
    4: 'Etwas',
    5: 'Mässig',
    6: 'Deutlich',
    7: 'Stark',
    8: 'Sehr stark',
    9: 'Äusserst',
    10:'Extrem'
}
# Beschreibungen der Schweregrade werden unter dem Slider angezeigt
st.sidebar.write(severity_levels_lim[feeling])
# Untertitel Seitenleiste - Kommentare
st.sidebar.header(':blue[Kommentare]')
# Eingabefeld, um Kommentare hinzuzufügen
comment = st.sidebar.text_input('Hast du noch weitere relevante Bemerkungen?')
# Einschub auf der Hauptseite
# Anzeige der Kommentare auf der Hauptseite, falls Eingabefeld ausgefüllt
if comment:
    st.write('Kommentar:')
    st.write(comment)
else:
    st.write('Kein Kommentar hinzugefügt')


# Button zum Speichern der Daten
submit = st.sidebar.button('Speichern')
delete = st.sidebar.button("letzter Eintrag löschen")


# Darstellung der Daten auf der Hauptseite - Daten aus dem Abschnitt "Befinden" und "Medikamente"

# Funktion, um Daten der Tabelle "Krankheitsverlauf" hizuzufügen
if submit:
    st.sidebar.write('Deine Daten wurden gespeichert.')
    st.balloons()   
    new_feeling = {
        "Datum und Zeit" : datetime_string,
        "Stärke der Limitation": feeling,
        "Symptome und Schweregrade" : symptoms_and_severity,
        "Kommentare" :comment
    }
    feeling_list = load_key(api_key_sick, bin_id_sick, username)
    feeling_list.append(new_feeling)
    record_sick = save_key(api_key_sick, bin_id_sick, username, feeling_list)
    if 'message' in record_sick:
        st.error(record_sick['message'])

else:
    st.sidebar.write('Deine Daten wurden noch nicht gespeichert.')
     
 
# Löschen des letzten Eintrags
if delete:
    feeling_list = load_key(api_key_sick, bin_id_sick, username)
    feeling_list.pop()
    record_sick = save_key(api_key_sick, bin_id_sick, username, feeling_list)
    if 'message' in record_sick:
        st.error(record_sick['message'])       
        


# Einschub auf der Seitenleiste - Medikamente zur regelmässigen Einnahme

# Eingabefelder, um regelmässig einzunehmende Medikamente hinzuzufügen
add_current_medication = st.sidebar.text_input("Medikament hinzufügen :blue[regelmässige Einnahme]")
add_current_medication_dose = st.sidebar.text_input("Dosierung")
add_current_medication_time = st.sidebar.text_input("Einnahmezeiten")  

# Zweiter Button zum Speichern der Medikamente
submit_med = st.sidebar.button("zur Medikamentenliste hinzufügen")
delete_med = st.sidebar.button("letztes Medikament löschen")

# Darstellung der Daten auf der Hauptseite - Daten aus dem Abschnitt "Medikamente hinzufügen regelmässige Einnahme"

# Funktion, um Daten der Tabelle "Medikamente" hizuzufügen
if submit_med:
    st.sidebar.write('Das Medikament wurde zur Liste hinzugefügt.')
    st.balloons()   
    current_medication = {
    "Medikament" : add_current_medication,
    "Dosierung" : add_current_medication_dose,
    "Einnahmezeiten" : add_current_medication_time
    }
    medi_list = load_key(api_key_med, bin_id_med, username)
    medi_list.append(current_medication)
    record_med = save_key(api_key_med, bin_id_med, username, medi_list)
    if 'message' in record_med:
        st.error(record_med['message'])

else:
    st.sidebar.write('Deine Daten wurden noch nicht gespeichert.')
     
 
# Löschen des letzten Eintrags
if delete_med:
    medi_list = load_key(api_key_med, bin_id_med, username)
    medi_list.pop()
    record_med = save_key(api_key_med, bin_id_med, username, medi_list)
    if 'message' in record_med:
        st.error(record_med['message'])
      
        
    
# Überschrift  Diagram
st. header(':blue[Limitation im Verlauf der Zeit]')

# Lade die Daten und konvertiere sie in ein DataFrame
feeling_list = load_key(api_key_sick, bin_id_sick, username)

if not feeling_list:
    st.warning('Es sind noch keine Daten vorhanden.')
    if show_logout_button:
        # Logout-Button am Ende der Seite platzieren
        authenticator.logout('Logout', 'main')
    st.stop()

new_feeling_data = pd.DataFrame(feeling_list)
# Index auf Datum setzen
new_feeling_data = new_feeling_data.set_index('Datum und Zeit')

# Benutzereingabe für die Zeitspanne
time_periods = ['Heute', 'Letzte Woche', 'Letzter Monat']
selected_time_period = st.selectbox('Zeitspanne auswählen:', time_periods)

# Filtere die Daten basierend auf der ausgewählten Zeitspanne
if selected_time_period == 'Heute':
    filtered_data = new_feeling_data.tail(5)  # Filtert die letzten 5 Einträge
elif selected_time_period == 'Letzte Woche':
    filtered_data = new_feeling_data.tail(35)  # Filtert die letzten 35 Einträge
elif selected_time_period == 'Letzter Monat':
    filtered_data = new_feeling_data.tail(140)  # Filtert die letzten 140 Einträge
else:
    filtered_data = new_feeling_data  # Kein Filter angewendet

# Darstellung der Daten in einem Diagramm
# Liniendiagramm "Limitation durch die Symptome im Verlauf der Zeit" anzeigen
st.line_chart(filtered_data['Stärke der Limitation'])

# Konvertieren der Daten in ein Pandas DataFrame - Daten aus dem Abschnitt "Medikamente hinzufügen regelmässige Einnahme"

medi_list = load_key(api_key_med, bin_id_med, username)
medi_list_data = pd.DataFrame(medi_list)


# Anpassung der Darstellung auf der Hauptseite

# Überschrift
st. header(":blue[Deine Daten auf einen Blick]")

# Darstellung der Daten auf der Hauptseite in zwei Tabs
tab1, tab2 = st.tabs(["Krankheitsverlauf", "Medikamente"])

with tab1:
   st.header("Krankheitsverlauf")
   st.write(new_feeling_data)



with tab2:
    st.header("Medikamente")
    if not medi_list:
        st.warning('Du hast noch kein Medikamente eingetragen')
    else:
        st.write(medi_list_data)

if show_logout_button:
    # Logout-Button am Ende der Seite platzieren
    authenticator.logout('Logout', 'main')
