import psycopg2
import csv
import time
from datetime import datetime

# Databaseverbinding
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

# Verwijder bestaande gegevens uit de tabel
cursor.execute("DELETE FROM smart_fridge_data;")
print("Bestaande gegevens verwijderd.")

# Lees en voeg gegevens in van de CSV
with open('smart refrigerator data.csv', mode='r', encoding='utf-8-sig') as file:
    # Aangezien de CSV gescheiden is met een puntkomma, stellen we de delimiter in op ';'
    reader = csv.DictReader(file, delimiter=';')

    for row in reader:
        # Strip leading/trailing spaces from the keys
        row = {key.strip(): value for key, value in row.items()}

        try:
            # Verwerk de 'timestamp', 'temperature', 'Bottle number', en 'Heating element'
            # Zorg voor het juiste datumnotatie
            timestamp = datetime.strptime(row['timestamp'], '%H:%M:%S').time()
            temperature = int(row['temperature'].strip())  # Verwijder spaties en converteer naar integer
            bottle_number = int(row['Bottle  number'])  # Note the extra space here
            heating_element = int(row['Heating element'])

            cursor.execute(""" 
                INSERT INTO smart_fridge_data (timestamp, temperature, bottle_number, heating_element) 
                VALUES (%s, %s, %s, %s)
            """, (timestamp, temperature, bottle_number, heating_element))

            print(f"Ingevoegde rij: {timestamp}, {temperature}, {bottle_number}, {heating_element}")
        except Exception as e:
            print(f"Fout bij het invoeren van rij: {row}. Fout: {e}")
            continue  # Sla de probleemrij over

# Veranderingen bevestigen en verbinding sluiten
conn.commit()
cursor.close()
conn.close()