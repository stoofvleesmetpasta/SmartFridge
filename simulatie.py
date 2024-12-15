import time
import random
import joblib

# Laad de modellen die eerder zijn getraind
bottle_model_path = './models/trained_bottle_model.pkl'
cooling_model_path = './models/trained_random_forest_model.pkl'

try:
    bottle_model = joblib.load(bottle_model_path)
    cooling_model = joblib.load(cooling_model_path)
except Exception as e:
    print(f"Fout bij het laden van modellen: {e}")
    exit()

# Simulatie functie
def simulate_cooling():
    while True:
        try:
            # Genereer een temperatuur tussen 0 en 5 graden
            temperature = random.randint(0, 5)

            # Voorspel het aantal flesjes op basis van de temperatuur
            bottle_number = bottle_model.predict([[temperature]])[0]

            # Gebruik de temperatuur en het aantal flesjes om het koelvermogen te voorspellen
            cooling_power = cooling_model.predict([[0, temperature, bottle_number]])[0]  # '0' als timestamp placeholder

            # Toon de resultaten
            print(f"Temperatuur: {temperature:.2f} °C | Flesjes: {int(bottle_number)} | Koelvermogen: {cooling_power}")

            # Wacht 5 seconden voordat de volgende iteratie begint
            time.sleep(5)

        except KeyboardInterrupt:
            print("Simulatie gestopt.")
            break
        except Exception as e:
            print(f"Fout tijdens simulatie: {e}")
            break

if __name__ == "__main__":
    print("Starten met simulatie van de koelkast...")
    simulate_cooling()
