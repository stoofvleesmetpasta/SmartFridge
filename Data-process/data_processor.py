import psycopg2
import csv
import time
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    dbname="smart_fridge",
    user="admin",
    password="admin123",
    host="db",  # Gebruik 'db' als hostnaam in Docker Compose
    port="5432"
)
cursor = conn.cursor()

# Wacht totdat de tabel beschikbaar is (retry-mechanisme)
while True:
    try:
        cursor.execute("SELECT 1 FROM smart_fridge_data LIMIT 1;")
        break  # Als er geen fout is, breek de loop
    except psycopg2.Error as e:
        print("Tabel nog niet klaar, probeer opnieuw...")
        time.sleep(5)  # Wacht 5 seconden en probeer opnieuw

# Lees en voeg gegevens in van de CSV
with open('smart refrigerator data.csv', mode='r', encoding='utf-8-sig') as file:
    # Aangezien de CSV gescheiden is met een puntkomma, stellen we de delimiter in op ';'
    reader = csv.DictReader(file, delimiter=';')

    for row in reader:
        # Verwijder BOM-teken en spaties van de kolomnamen
        row = {key.strip().replace('\ufeff', ''): value for key, value in row.items()}

        try:
            # Verwerk de 'date', 'temperature', 'threshold', en andere velden
            date = datetime.strptime(row['date'], '%d/%m/%Y').strftime('%Y-%m-%d')  # Zorg voor het juiste datumnotatie
            temperature = row['Tempreature'].replace('°C', '').strip()  # Verwijder '°C'
            threshold = float(row['Threashold'].replace('kg', '').strip())  # Verwijder 'kg' en converteer naar float
            bottle_number = int(row['Bottle  number'])  # Converteer bottle_number naar integer
            heating_element = int(row['Heating element'])  # Converteer heating_element naar integer

            cursor.execute(""" 
                INSERT INTO smart_fridge_data (date, temperature, threshold, bottle_number, heating_element) 
                VALUES (%s, %s, %s, %s, %s)
            """, (date, temperature, threshold, bottle_number, heating_element))

            print(f"Ingevoegde rij: {date}, {temperature}, {threshold}, {bottle_number}, {heating_element}")
        except Exception as e:
            print(f"Fout bij het invoeren van rij: {row}. Fout: {e}")
            continue  # Sla de probleemrij over

# Veranderingen bevestigen en verbinding sluiten
conn.commit()
cursor.close()
conn.close()