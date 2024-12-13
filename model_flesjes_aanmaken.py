import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Laad de dataset
file_path = './Data-process/smart refrigerator data.csv'
df = pd.read_csv(file_path)
print(df)

# Controleer of 'temperature' en 'bottle_number' aanwezig zijn in de dataset
if 'temperature' in df.columns and 'bottle_number' in df.columns:
    # Verwijder rijen waar 'temperature' of 'bottle_number' ontbreekt
    df = df.dropna(subset=['temperature', 'bottle_number'])

    # Features en target
    X = df[['temperature']]  # Alleen 'temperature' gebruiken als feature
    y = df['bottle_number']  # Target is 'bottle_number'

    # Verdeel de data in een training en testset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Maak het model
    model = LinearRegression()

    # Train het model
    model.fit(X_train, y_train)

    # Maak voorspellingen
    y_pred = model.predict(X_test)

    # Evaluatie van het model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")

    # Sla het model op
    joblib.dump(model, 'trained_bottle_model.pkl')
else:
    print("De vereiste kolommen 'temperature' en 'bottle_number' zijn niet aanwezig in de dataset.")
