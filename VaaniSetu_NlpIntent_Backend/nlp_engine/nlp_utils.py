import re
import numpy as np

def predict_intent_backend(user_text, model):
    """
    Takes text + the loaded model.
    Returns a list of intents (e.g., ['AGRI_LOAN_QUERY', 'CHECK_STATUS_QUERY'])
    """
    
    # --- 1. CLEAN INPUT ---
    # Whisper sometimes adds standard punctuation we don't strictly need, 
    # but our logic handles it. Just basic whitespace stripping here.
    clean_text = user_text.strip()
    
    # --- 2. SMART SPLIT (The "Run-on Sentence" Fix) ---
    # Splits on: and, also, but, then, so, &, ., ,
    raw_chunks = re.split(r'\s+(?:and|also|but|then|so|&|\.|,)\s+', clean_text, flags=re.IGNORECASE)
    chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 2] # Ignore tiny chunks
    
    if not chunks: 
        chunks = [clean_text]

    candidates = []
    
    # --- 3. PREDICT ON CHUNKS ---
    for chunk in chunks:
        # Get probabilities from the model
        probs = model.predict_proba([chunk])[0]
        pred_index = np.argmax(probs)
        confidence = probs[pred_index] * 100
        intent = model.classes_[pred_index]
        
        candidates.append({
            "chunk": chunk,
            "intent": intent,
            "conf": confidence
        })

    # --- 4. LOGIC LAYER (The "Brain") ---
    final_intents = set()
    
    # Group candidates by type for easier filtering
    queries = [c for c in candidates if "QUERY" in c['intent'] or "OPEN" in c['intent']]
    data_only = [c for c in candidates if "PROVIDE_DATA" in c['intent']]
    greetings = [c for c in candidates if "GREETING" in c['intent']]
    
    # A. PROCESS QUERIES (Dynamic Thresholds)
    if queries:
        for q in queries:
            word_count = len(q['chunk'].split())
            
            # Status checks are often short ("Where is money?"), so we trust them more
            if "STATUS" in q['intent'] or "ELIGIBILITY" in q['intent']:
                threshold = 30.0 
            # Longer sentences need higher confidence
            else:
                threshold = 35.0 if word_count < 5 else 45.0
            
            if q['conf'] > threshold:
                final_intents.add(q['intent'])
    
    # B. PROCESS DATA (Only if very sure, or if no query found)
    elif data_only:
        best_data = max(data_only, key=lambda x: x['conf'])
        # Data usually supports a query, so we only return it as a primary intent 
        # if it's very distinct (high confidence).
        if best_data['conf'] > 60.0:
            final_intents.add(best_data['intent'])

    # C. GREETINGS (Only if nothing else matches)
    if greetings and not final_intents:
         best_greet = max(greetings, key=lambda x: x['conf'])
         if best_greet['conf'] > 50.0:
             final_intents.add(best_greet['intent'])

    # D. FALLBACK (If logic filtered everything out)
    if not final_intents:
        # Check for any high confidence "Other" intents we might have missed
        other_intents = [c for c in candidates if c['conf'] > 55.0]
        for o in other_intents:
            final_intents.add(o['intent'])
            
    # --- 5. RETURN CLEAN LIST ---
    results = list(final_intents)
    
    # Default safety response
    if not results:
        results = ["OUT_OF_SCOPE"] 
        
    return results