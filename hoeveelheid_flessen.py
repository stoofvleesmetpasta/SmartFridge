import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Stap 1: Data inladen en voorbereiden
CSV_FILE = './Data-process/smart refrigerator data.csv'


def load_and_prepare_data(file_path):
    """Laad de CSV en bereid de features en labels voor."""
    # Lees het CSV-bestand
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8-sig')

    # Zorg ervoor dat de kolom 'temperature' aanwezig is
    if 'temperature' not in df.columns or 'Bottle  number' not in df.columns:
        raise ValueError(
            "De vereiste kolommen 'temperature' en 'Bottle  number' ontbreken in de dataset.")

    # Features (X): alleen de temperatuur
    X = df[['temperature']]

    # Labels (y): aantal flesjes
    y = df['Bottle  number']

    return X, y

# Stap 2: Data preprocessing en model training


def train_model(X, y):
    """Train een Random Forest-model en evalueer het."""
    # Verdeel de data in train- en testsets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Initialiseer en train het model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Voorspel op de testset
    y_pred = model.predict(X_test)

    # Evaluatie
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(
        f"Model Evaluatie:\nMean Squared Error: {mse:.2f}\nR² Score: {r2:.2f}")

    return model

# Stap 3: Model opslaan


def save_model(model, filename='bottle_predictor_model.pkl'):
    """Sla het getrainde model op."""
    joblib.dump(model, filename)
    print(f"Model opgeslagen als: {filename}")

# Hoofdfunctie


def main():
    X, y = load_and_prepare_data(CSV_FILE)
    model = train_model(X, y)
    save_model(model)


if __name__ == "__main__":
    main()
