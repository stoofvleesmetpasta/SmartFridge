import os
import joblib
import pandas as pd
from models import model_flesjes_aanmaken, model

# Bestands- en mappaden
model_dir = './models'
bottle_model_path = os.path.join(model_dir, 'trained_bottle_model.pkl')
rf_model_path = os.path.join(model_dir, 'trained_random_forest_model.pkl')

# Functie om te controleren of modellen bestaan
def check_or_train_models():
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)  # Maak de map 'model' aan als deze niet bestaat

    bottle_model_exists = os.path.exists(bottle_model_path)
    rf_model_exists = os.path.exists(rf_model_path)

    if bottle_model_exists and rf_model_exists:
        print("Modelbestanden bestaan al.")
        # Vraag de gebruiker of ze de modellen willen behouden of opnieuw trainen
        user_input = input("Wil je de bestaande modellen behouden en verder gaan? (y/n): ").strip().lower()

        if user_input == 'y':
            print("De bestaande modellen worden geladen...")
            # Laad de getrainde modellen
            bottle_model = joblib.load(bottle_model_path)
            rf_model = joblib.load(rf_model_path)
            print(f"Model Flesjes: {bottle_model}")
            print(f"Model Fridge: {rf_model}")
            return bottle_model, rf_model
        else:
            print("De modellen zullen opnieuw worden getraind...")
            # Train de modellen opnieuw
            model_flesjes_model = model_flesjes_aanmaken.ModelFlesjesMaken.train_model_flesjes()

            # Maak een instantie van SmartFridgeModel en voer de run() functie uit
            smart_fridge_model = model.SmartFridgeModel()  # Maak een instantie van de SmartFridgeModel
            model_fridge = smart_fridge_model.run()  # Roep de run() methode aan op de instantie

            return model_flesjes_model, model_fridge

    else:
        print("Niet alle modelbestanden bestaan. Modellen zullen worden getraind...")
        # Als de modellen niet bestaan, train ze
        model_flesjes_model = model_flesjes_aanmaken.ModelFlesjesMaken.train_model_flesjes()

        # Maak een instantie van SmartFridgeModel en voer de run() functie uit
        smart_fridge_model = model.SmartFridgeModel()  # Maak een instantie van de SmartFridgeModel
        model_fridge = smart_fridge_model.run()  # Roep de run() methode aan op de instantie

        return model_flesjes_model, model_fridge

if __name__ == "__main__":
    model_flesjes_model, model_fridge = check_or_train_models()