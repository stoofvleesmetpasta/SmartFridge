import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Load the dataset
data_path = "Data-process/smart refrigerator data.csv"  # Update with your actual file path
data = pd.read_csv(data_path)
print(data)

# Define features (X) and target (y)
X = data[['timestamp', 'temperature', 'Bottle  number']]
y = data['Heating element']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a random forest classifier
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importances = model.feature_importances_
feature_names = ['seconds', 'temperature', 'Bottle  number']
importance_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importances})
print("Feature Importances:")
print(importance_df.sort_values(by="Importance", ascending=False))
