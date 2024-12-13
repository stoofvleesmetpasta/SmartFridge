import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import os

class SmartFridgeModel:
    def __init__(self):
        """
        Initialiseer de klasse met database configuratie.
        :param db_config: Database configuratie als dictionary.
        """
        self.db_config = {
            "dbname": "smart_fridge",
            "user": "admin",
            "password": "admin123",
            "host": os.getenv("DB_HOST", "localhost"),  # In Docker Compose kan de hostnaam 'db' zijn
            "port": "5432"
        }
        self.engine = self.create_db_engine()
    
    def create_db_engine(self):
        """
        Maak een verbinding met de PostgreSQL database.
        :return: SQLAlchemy engine object.
        """
        try:
            engine = create_engine(f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}")
            return engine
        except Exception as e:
            print(f"Fout bij het maken van de databaseverbinding: {e}")
            return None

    def load_data(self):
        """
        Laad de gegevens uit de database.
        :return: Pandas DataFrame met de gegevens.
        """
        if self.engine:
            try:
                query = "SELECT * FROM smart_fridge_data;"
                df = pd.read_sql(query, self.engine)
                return df
            except Exception as e:
                print(f"Fout bij het laden van data: {e}")
                return None
        else:
            print("Geen geldige databaseverbinding.")
            return None

    def preprocess_data(self, df):
        """
        Verwerk de data door ontbrekende waarden te verwijderen en 'timestamp' te converteren.
        :param df: Pandas DataFrame met de gegevens.
        :return: Verwerkte Pandas DataFrame.
        """
        # Ensure the column names match those in your database
        if 'timestamp' in df.columns and 'temperature' in df.columns and 'bottle_number' in df.columns and 'heating_element' in df.columns:
            # Verwijder rijen waar ontbrekende waarden zijn
            df = df.dropna(subset=['temperature', 'bottle_number', 'heating_element'])

            # Preprocess de 'timestamp' naar een numerieke waarde (aantal seconden)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S').dt.second

            return df
        else:
            print("De vereiste kolommen zijn niet aanwezig in de dataset.")
            return None


    def train_model(self, df):
        """
        Train the model with the given data.
        :param df: Processed Pandas DataFrame.
        """
        # Features (X) and target (y)
        X = df[['timestamp', 'temperature', 'bottle_number']]  # Correct column name here
        y = df['heating_element']  # Target (label)

        # Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Split the data into a training and test set
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Train a Random Forest Classifier
        model = RandomForestClassifier(random_state=42, n_estimators=100)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Model evaluation
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Feature importance
        feature_importances = model.feature_importances_
        feature_names = ['seconds', 'temperature', 'bottle_number']  # Correct feature names here
        importance_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importances})
        print("Feature Importances:")
        print(importance_df.sort_values(by="Importance", ascending=False))

        # Save the model as a .pkl file
        joblib.dump(model, './models/trained_random_forest_model.pkl')


    def run(self):
        """
        Voer het volledige proces uit: laad data, verwerk data, train het model en evalueer.
        """
        df = self.load_data()
        if df is not None:
            df = self.preprocess_data(df)
            if df is not None:
                self.train_model(df)