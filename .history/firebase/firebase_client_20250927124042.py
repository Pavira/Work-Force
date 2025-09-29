import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json

class FirebaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize Firebase Admin SDK with service account credentials."""
        try:
            # Get the path to the config file
            config_path = Path(__file__).parent.parent / 'firebase_config.json'
            
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(str(config_path))
            firebase_admin.initialize_app(cred)
            
            # Initialize Firestore client
            self.db = firestore.client()
            print("Firebase connection initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize Firebase: {str(e)}")

    def get_collection(self, collection_name: str):
        """Get a reference to a Firestore collection.
        
        Args:
            collection_name (str): Name of the collection to access
            
        Returns:
            firestore.CollectionReference: Reference to the specified collection
        """
        return self.db.collection(collection_name)

    def add_document(self, collection_name: str, data: dict):
        """Add a new document to a collection.
        
        Args:
            collection_name (str): Name of the collection
            data (dict): Document data to add
            
        Returns:
            str: ID of the created document
        """
        doc_ref = self.get_collection(collection_name).add(data)
        return doc_ref[1].id

    def get_document(self, collection_name: str, doc_id: str):
        """Get a document by its ID.
        
        Args:
            collection_name (str): Name of the collection
            doc_id (str): ID of the document to retrieve
            
        Returns:
            dict: Document data or None if not found
        """
        doc = self.get_collection(collection_name).document(doc_id).get()
        return doc.to_dict() if doc.exists else None

    def update_document(self, collection_name: str, doc_id: str, data: dict):
        """Update a document by its ID.
        
        Args:
            collection_name (str): Name of the collection
            doc_id (str): ID of the document to update
            data (dict): Updated data
        """
        self.get_collection(collection_name).document(doc_id).update(data)

    def delete_document(self, collection_name: str, doc_id: str):
        """Delete a document by its ID.
        
        Args:
            collection_name (str): Name of the collection
            doc_id (str): ID of the document to delete
        """
        self.get_collection(collection_name).document(doc_id).delete()

    def query_collection(self, collection_name: str, field: str, operator: str, value: any):
        """Query documents in a collection.
        
        Args:
            collection_name (str): Name of the collection
            field (str): Field to query on
            operator (str): Comparison operator ('==', '>', '<', '>=', '<=', 'array_contains')
            value (any): Value to compare against
            
        Returns:
            list: List of matching documents
        """
        docs = self.get_collection(collection_name).where(field, operator, value).stream()
        return [doc.to_dict() for doc in docs]
