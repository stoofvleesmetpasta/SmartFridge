import time
import random
import joblib

class FridgeSimulation:
    def __init__(self):
        # Laad de modellen die eerder zijn getraind
        self.bottle_model_path = './models/trained_bottle_model.pkl'
        self.cooling_model_path = './models/trained_random_forest_model.pkl'

        try:
            self.bottle_model = joblib.load(self.bottle_model_path)
            self.cooling_model = joblib.load(self.cooling_model_path)
        except Exception as e:
            print(f"Fout bij het laden van modellen: {e}")
            exit()

    def simulate_cooling(self):
        while True:
            try:
                # Genereer een temperatuur tussen 0 en 5 graden
                temperature = random.randint(0, 5)

                # Voorspel het aantal flesjes op basis van de temperatuur
                bottle_number = self.bottle_model.predict([[temperature]])[0]

                # Gebruik de temperatuur en het aantal flesjes om het koelvermogen te voorspellen
                cooling_power = self.cooling_model.predict([[0, temperature, bottle_number]])[0]  # '0' als timestamp placeholder

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
