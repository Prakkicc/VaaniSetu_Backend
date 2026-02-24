from django.apps import AppConfig
import joblib
import os
import sys

class NlpEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nlp_engine'
    
    # Global variable to store the model
    model = None

    def ready(self):
        # Prevent running this twice (Django reloader issue)
        if 'runserver' not in sys.argv:
            return
            
        print("🧠 Loading NLP Intent Model...")
        
        # Path to: backend/nlp_engine/ml_models/intent_model_full.pkl
        model_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'intent_model_full.pkl')
        
        try:
            if os.path.exists(model_path):
                NlpEngineConfig.model = joblib.load(model_path)
                print("✅ NLP Intent Model loaded successfully!")
            else:
                print(f"⚠️ Warning: Model file not found at {model_path}")
                print("   (This is expected if you haven't uploaded the .pkl file yet)")
        except Exception as e:
            print(f"❌ Error loading model: {e}")