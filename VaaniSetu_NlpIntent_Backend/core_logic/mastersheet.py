# Mapping based on the 20 intents in NLPINTENT.ipynb 
# and the labels in 03 Entities.pdf

INTENT_ENTITY_MAP = {
    # --- Discovery & Queries ---
    "AGRI_LOAN_QUERY": ["CROP", "LAND_SIZE", "STATE", "DISTRICT", "LOAN_AMOUNT"],
    "AGRI_SUBSIDY_QUERY": ["RESOURCE", "CROP", "STATE", "CATEGORY"],
    "EDU_SCHOLARSHIP_QUERY": ["CATEGORY", "STATE", "GENDER", "INCOME"],
    "BANK_ACCOUNT_OPEN": ["BANK_NAME", "STATE", "DISTRICT"],
    "AGRI_INSURANCE_QUERY": ["CROP", "SEASON", "STATE", "DISTRICT"],
    "AGRI_PENSION_QUERY": ["AGE", "STATE", "INCOME"],
    "EDU_LOAN_QUERY": ["LOAN_AMOUNT", "STATE"],
    "BUSINESS_LOAN_QUERY": ["RESOURCE", "LOAN_AMOUNT", "STATE"],
    "SKILL_TRAINING_QUERY": ["RESOURCE", "STATE", "GENDER"],
    
    # --- Action & Tracking ---
    "CHECK_ELIGIBILITY_QUERY": ["SCHEME", "STATE", "CATEGORY", "INCOME"],
    "DOCUMENTS_REQUIRED_QUERY": ["SCHEME"],
    "HOW_TO_APPLY_QUERY": ["SCHEME"],
    "CHECK_STATUS_QUERY": ["FARMER_NAME", "STATE", "REQ_TYPE"],
    
    # --- System & Support (No Entities Required) ---
    "GREETING_CHIT_CHAT": [],
    "OUT_OF_SCOPE": [],
    "CONFIRMATION_YES": [],
    "CONFIRMATION_NO": [],
    "PROVIDE_DATA_PERSONAL": [],
    "PROVIDE_DATA_AGRI": [],
    "PROVIDE_DATA_FINANCIAL": []
}

def get_required_entities(primary_intent):
    """
    Returns the list of mandatory entities for the detected intent.
    """
    return INTENT_ENTITY_MAP.get(primary_intent, [])