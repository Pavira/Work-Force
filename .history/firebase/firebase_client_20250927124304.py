import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json


class FirebaseClient:

    def _initialize(self):
        """Initialize Firebase Admin SDK with service account credentials."""
        try:
            # Get the path to the config file
            config_path = Path(__file__).parent.parent / "firebase_config.json"

            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(str(config_path))
            firebase_admin.initialize_app(cred)

            # Initialize Firestore client
            self.db = firestore.client()
            print("Firebase connection initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize Firebase: {str(e)}")
