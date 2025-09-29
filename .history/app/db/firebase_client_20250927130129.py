"""
firebase_client.py
------------------
Centralized Firebase Admin SDK client with logging support.

- Supports both normal development and PyInstaller exe builds.
- Provides a clean singleton wrapper for Firestore and Storage.
"""

import os
import sys
import logging
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Default level: INFO (change to DEBUG for dev)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource.
    Works for both development and PyInstaller exe builds.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FirebaseClient:
    """
    Singleton wrapper for Firebase Admin SDK.
    Ensures only one Firebase app is initialized across the project.
    """

    _initialized = False

    def __init__(self, cred_filename: str = "firebase_config.json"):
        if not FirebaseClient._initialized:
            self._initialize_firebase(cred_filename)
            FirebaseClient._initialized = True

        self.db = firestore.client()
        self.bucket = storage.bucket()

    def _initialize_firebase(self, cred_filename: str):
        """Initialize Firebase with service account credentials."""
        try:
            cred_path = resource_path(cred_filename)
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Service account file not found: {cred_path}")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(
                cred,
                {
                    "storageBucket": "<your-project-id>.appspot.com"  # replace with your bucket
                },
            )
            logger.info(f"Firebase initialized with {cred_path}")

        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise RuntimeError(f"Failed to initialize Firebase: {e}")


# Create a single global instance
firebase_client = FirebaseClient()

# Shortcuts for easy import
db = firebase_client.db
bucket = firebase_client.bucket
