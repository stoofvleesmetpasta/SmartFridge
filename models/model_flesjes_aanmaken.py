import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class ModelFlesjesMaken:
    db_config = {
        "dbname": "smart_fridge",
        "user": "admin",
        "password": "admin123",
        "host": os.getenv("DB_HOST", "localhost"),  # Ensure host is set properly
        "port": "5432"
    }

    @staticmethod
    def create_db_engine():
        try:
            engine = create_engine(f"postgresql://{ModelFlesjesMaken.db_config['user']}:{ModelFlesjesMaken.db_config['password']}@{ModelFlesjesMaken.db_config['host']}:{ModelFlesjesMaken.db_config['port']}/{ModelFlesjesMaken.db_config['dbname']}")
            return engine
        except Exception as e:
            print(f"Fout bij het maken van de databaseverbinding: {e}")
            return None

    @staticmethod
    def train_model_flesjes():
        engine = ModelFlesjesMaken.create_db_engine()
        if engine is None:
            return
        
        try:
            query = "SELECT * FROM smart_fridge_data;"
            df = pd.read_sql(query, engine)

            # Print column names for debugging
            print(f"Columns in DataFrame: {df.columns}")

            # Clean column names (strip leading/trailing spaces)
            df.columns = df.columns.str.strip()

            # Debugging: Check if the required columns are present
            print(f"Checking for 'temperature' and 'bottle_number' columns...")
            if 'temperature' in df.columns and 'bottle_number' in df.columns:
                print("Both 'temperature' and 'bottle_number' columns are present.")
                
                # Drop rows with missing values
                df = df.dropna(subset=['temperature', 'bottle_number'])

                # Features and target
                X = df[['temperature']]  # Using 'temperature' as the feature
                y = df['bottle_number']  # Target is 'bottle_number'

                # Split the data into training and test sets
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Create the model
                model = LinearRegression()

                # Train the model
                model.fit(X_train, y_train)

                # Make predictions
                y_pred = model.predict(X_test)

                # Evaluate the model
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)

                print(f"Mean Squared Error: {mse}")
                print(f"R² Score: {r2}")

                # Save the trained model
                joblib.dump(model, './models/trained_bottle_model.pkl')
            else:
                # Temporarily remove this message
                # print("The required columns 'temperature' and 'bottle_number' are not present in the dataset.")
                print("Skipping error message for missing columns.")
        except Exception as e:
            print(f"Fout bij het uitvoeren van de query of verwerken van data: {e}")