import csv
import random
import datetime
import time

# Bestandsnaam
CSV_FILE = './Data-process/smart refrigerator data.csv'


def read_last_row(filename):
    """Lees de laatste rij uit het CSV-bestand."""
    try:
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = list(csv.DictReader(file, delimiter=';'))
            if not reader:
                return None
            return reader[-1]  # Retourneer de laatste rij
    except FileNotFoundError:
        return None


def combine_time_with_date(time_str):
    """Combineer de tijdstring (H:M:S) met de huidige datum."""
    current_date = datetime.date.today()
    combined_datetime = datetime.datetime.strptime(
        f"{current_date} {time_str}", "%Y-%m-%d %H:%M:%S")
    return combined_datetime


def generate_next_temperature(current_temp):
    """Genereer een volgende temperatuur met normale of grote variaties."""
    if random.random() < 0.2:  # 20% kans op een grote variatie
        variation = random.uniform(-3.0, 3.0)  # Grote variatie
        print("Grote temperatuurvariatie!")
    else:
        variation = random.uniform(-0.5, 0.5)  # Kleine variatie

    next_temp = round(float(current_temp) + variation, 1)
    next_temp = max(0.0, min(10.0, next_temp))  # Houd het tussen 0°C en 10°C
    return next_temp


def append_new_row(filename, timestamp, new_temp):
    """Voeg een nieuwe rij toe aan het CSV-bestand."""
    new_row = {
        'timestamp': timestamp.strftime("%H:%M:%S"),
        'Tempreature': f"{new_temp}°C",
        # Simuleer realistische waarden
        'Bottle  number': random.randint(0, 6),
        # Simuleer realistische waarden
        'Heating element': random.randint(1, 3)
    }

    with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['timestamp', 'Tempreature',
                      'Bottle  number', 'Heating element']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

        # Voeg header toe als bestand leeg is
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(new_row)
        print(f"Toegevoegde rij: {new_row}")


def main():
    last_row = read_last_row(CSV_FILE)

    if last_row:
        # Combineer tijd met huidige datum en haal de temperatuur
        last_timestamp = combine_time_with_date(last_row['timestamp'])
        last_temp = last_row['Tempreature'].replace('°C', '').strip()
    else:
        # Start met de huidige tijd als er geen data is
        last_timestamp = datetime.datetime.now()
        last_temp = 5.0  # Begin met een standaard temperatuur van 5°C

    for i in range(10):  # Voeg 10 rijen toe als voorbeeld
        next_temp = generate_next_temperature(last_temp)
        # Tel 5 seconden bij de vorige timestamp op
        last_timestamp += datetime.timedelta(seconds=5)
        append_new_row(CSV_FILE, last_timestamp, next_temp)
        last_temp = next_temp

        # Optioneel: Wacht 1 seconde om het script realistischer te maken
        time.sleep(1)


if __name__ == "__main__":
    main()
