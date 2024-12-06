import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load your data (replace 'file_path' with your actual CSV file path)
file_path = "Smartfridge/data/data.csv"
df = pd.read_csv(file_path)
print(df.columns)


# Data preprocessing
df["Bottle number"] = pd.to_numeric(df["Bottle number"], errors="coerce")
df["Threshold"] = df["Threshold"].str.replace('kg', '').astype(float)  # Remove 'kg' and convert to float
df["Temperature"] = df["Temperature"].str.replace('°C', '').astype(float)  # Remove '°C' and convert to float

# Features and target
X = df[["Temperature", "Bottle number", "Threshold"]]  # Features
y = df["Heating element"]  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model (optional, if you want to reuse it)
import joblib
joblib.dump(model, "fridge_heating_model.pkl")

# Example usage: Predict heating element power for new data
new_data = pd.DataFrame({
    "Temperature": [5],
    "Bottle number": [4],
    "Threshold": [4.5],
})
predicted_heating = model.predict(new_data)
print("Predicted Heating Element:", predicted_heating[0])
