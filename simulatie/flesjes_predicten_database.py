import pandas as pd
import joblib  # Voor het laden van het model
import numpy as np

# Laad het getrainde model
# Zorg dat dit bestand bestaat
model = joblib.load('bottle_predictor_model.pkl')

# Laad de dataset
file_path = './Data-process/smart refrigerator data.csv'
df = pd.read_csv(file_path)

# Controleer welke rijen geen 'bottle_number' hebben
# We gaan ervan uit dat lege waarden zijn aangegeven als NaN of lege cellen
missing_bottles = df['bottle_number'].isna() | (df['bottle_number'] == '')

# Selecteer alleen de benodigde features voor het model
if 'temperature' in df.columns:
    # Vul ontbrekende waarden tijdelijk op met 0 om problemen te voorkomen
    # Zorg dat we lege waarden goed zien
    df.loc[missing_bottles, 'bottle_number'] = np.nan
    prediction_data = df.loc[missing_bottles, ['temperature']].copy()

    # Zorg dat temperatuur een numerieke waarde heeft (voor de zekerheid)
    prediction_data['temperature'] = pd.to_numeric(
        prediction_data['temperature'], errors='coerce')
    # Vul ontbrekende waarden op voor het model
    prediction_data = prediction_data.fillna(0)

    # Maak voorspellingen
    predictions = model.predict(prediction_data)

    # Voeg voorspellingen toe aan de juiste rijen in de DataFrame
    df.loc[missing_bottles, 'bottle_number'] = predictions.round().astype(
        int)  # Rond af naar integer voor flesjes

    # Schrijf de bijgewerkte dataset terug naar de CSV
    df.to_csv(file_path, index=False)

    print("Voorspellingen zijn toegevoegd aan de dataset en opgeslagen.")
else:
    print("De kolom 'temperature' ontbreekt in de dataset.")
