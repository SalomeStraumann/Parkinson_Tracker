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


# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key_med = jsonbin_secrets["api_key_med"]
bin_id_med = jsonbin_secrets["bin_id_med"]
api_key_sick = jsonbin_secrets["api_key_sick"]
bin_id_sick = jsonbin_secrets["bin_id_sick"]


# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

# Hauptseite

# Titel der App
st.title("Parkinson Tracker")
# Begrüssung
text_before = "Hallo,"
text_after = "!"
st.header("{} {}{}".format(text_before, username, text_after))
# Information für den Nutzer
st.warning("Bitte beantworte die Fragen in der Seitenleiste")

# Bild
if username == "sara":
    image_sara = Image.open("sara.jpg")
    st.image(image_sara, width = 400)
else:
    image = Image.open("Maya.jpg")
    st.image(image, width = 400)


# Seitenleiste
# Eingabefelder für Datum und Uhrzeit
date = st.sidebar.date_input("Datum", datetime.date(2023, 5, 20))
time = st.sidebar.time_input("Uhrzeit", datetime.time(12, 00))
# Kombination von Datum und Uhrzeit zu einem Datetime-Objekt
datetime_obj = datetime.datetime.combine(date, time)
# Formation des Datetime-Objekts zum String
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
    'Langsame Bewegungen'
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
# Multiselect-Widget für die verfügbaren Symptome
selected_symptoms = st.sidebar.multiselect(
    'Symptome', 
    symptoms
    )
# Eingabefelder für die Schweregrade der ausgewählten Symptome
severity_levels = {}
for symptom in selected_symptoms:
    severity_level = st.sidebar.number_input(
        f'Wie stark ist das Symptom "{symptom}" auf einer Skala? 0 = Nicht vorhanden, 10 = Extrem stark.', 
        min_value=0, 
        max_value=10, 
        value=5
    )
    severity_levels[symptom] = severity_level
# Einschub auf der Hauptseite
# Anzeige der ausgewÃ¤hlten Symptome und Schweregrade auf der Hauptseite, falls Eingabefeld ausgefüllt
if selected_symptoms:
    st.write(':blue[Ausgewählte Symptome und Schweregrade:]')
    for symptom in selected_symptoms:
        severity_level = severity_levels[symptom]
        st.write(f'- {symptom}: {severity_level}')
# Speichern der ausgewählten Symptome und Schweregrade in einem Dictionary
    symptoms_and_severity = {symptom: severity_levels[symptom] for symptom in selected_symptoms}
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
    5: 'MÃ¤ssig',
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
# Untertitel Seitenleiste - Medikamente
st.sidebar.header(':blue[Medikamente]')
# Eingabefeld, um einmalige Medikamenteneinnahme hinzuzufügen
add_medication = st.sidebar.text_input(
    'Medikament inklusive Dosierung hinzufügen :blue[einmalige Einnahme]'
    )

# Button zum Speichern der Daten
submit = st.sidebar.button('Speichern')
delete = st.sidebar.button("Lezter Eintrag löschen")








# Darstellung der Daten auf der Hauptseite - Daten aus dem Abschnitt "Befinden" und "Medikamente"

# Funktion, um Daten der Tabelle "Krankheitsverlauf" hizuzufÃ¼gen
if submit:
    st.sidebar.write('Deine Daten wurden gespeichert.')
    st.balloons()   
    new_feeling = {
        "Datum und Zeit" : datetime_string,
        "Stärke der Limitation": feeling,
        "Symptome und Schweregrade" : symptoms_and_severity,
        "Medikament und Dosierung" : add_medication,
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
    # delete last entry
    feeling_list = load_key(api_key_sick, bin_id_sick, username)
    feeling_list.pop()
    record_sick = save_key(api_key_sick, bin_id_sick, username, feeling_list)
    if 'message' in record_sick:
        st.error(record_sick['message'])

 
    
# Überschrift  Diagram
st. header(':blue[Limitation im Verlauf der Zeit]')
 

# Konvertieren der Daten in ein Pandas DataFrame - Daten aus dem Abschnitt "Befinden" und "Medikamente"
feeling_list = load_key(api_key_sick, bin_id_sick, username)
new_feeling_data = pd.DataFrame(feeling_list)


# Index auf Datum setzen
new_feeling_data = new_feeling_data.set_index('Datum und Zeit')


# Darstellung der Daten in einem Diagram

# Liniendiagramm "Limitation durch die Symptome im Verlauf der Zeit" anzeigen
st.line_chart(new_feeling_data['Stärke der Limitation'])





# Einschub auf der Seitenleiste - Medikamente zur regelmässigen Einnahme

# Eingabefeld, um regelmässig einzunehmende Medikamente hinzuzufügen
add_current_medication = st.sidebar.text_input(
    "Medikament hinzufügen :blue[regelmÃ¤ssige Einnahme]"
    )


# Eingabefeld, um Einnahmezeiten der regelmässig einzunehmenden Medikamente hinzuzufügen
add_current_medication_dose = st.sidebar.text_input(
     "Dosierung"
     )


# Eingabefeld, um Einnahmezeiten der regelmässig einzunehmenden Medikamente hinzuzufügen
add_current_medication_time = st.sidebar.text_input(
     "Einnahmezeiten"
     )
    

# Zweiter Button zum Speichern der Medikamente
submit_med = st.sidebar.button("zur aktuellen Medikamentenliste hinzufügen")
delete_med = st.sidebar.button("Leztes Medikament löschen")




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
    # delete last entry
    medi_list = load_key(api_key_med, bin_id_med, username)
    medi_list.pop()
    record_med = save_key(api_key_med, bin_id_med, username, medi_list)
    if 'message' in record_med:
        st.error(record_med['message'])



# Konvertieren der Daten in ein Pandas DataFrame - Daten aus dem Abschnitt "Medikamente hinzufügen regelmässige Einnahme"

medi_list = load_key(api_key_med, bin_id_med, username)
medi_list_data = pd.DataFrame(medi_list)


# Index auf Medikament setzen
medi_list_data = medi_list_data.set_index('Medikament')



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
    st.write(medi_list_data)
