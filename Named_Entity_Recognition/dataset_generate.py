import random
import pandas as pd
import json
import string
from collections import Counter, defaultdict

# SETUP YOUR LISTS 

crops = [
    # Cereals & Millets
    "Rice", "Wheat", "Maize", "Jowar", "Bajra", "Ragi", "Barley", "Sorghum", "Pearl Millet", "Finger Millet", "Paddy",
    
    # Pulses (Dal)
    "Tur Dal", "Arhar", "Moong Dal", "Urad Dal", "Masoor Dal", "Gram", "Chana", "Chickpea", "Horse Gram", "Lentils", "Peas", "Kidney Beans", "Rajma",
    
    # Oilseeds
    "Groundnut", "Mustard", "Soybean", "Sunflower", "Sesame", "Castor", "Linseed", "Safflower", "Niger Seed",
    
    # Cash Crops & Fibers
    "Sugarcane", "Cotton", "Jute", "Tobacco", "Rubber", "Tea", "Coffee", "Arecanut", "Coconut", "Bamboo",
    
    # Spices
    "Chilli", "Turmeric", "Ginger", "Garlic", "Cumin", "Coriander", "Cardamom", "Black Pepper", "Cloves", "Fenugreek", "Fennel",
    
    # Vegetables
    "Potato", "Onion", "Tomato", "Brinjal", "Eggplant", "Okra", "Bhindi", "Cabbage", "Cauliflower", "Spinach", "Carrot", "Radish", "Bottle Gourd", "Bitter Gourd",
    
    # Fruits
    "Mango", "Banana", "Apple", "Guava", "Papaya", "Pomegranate", "Orange", "Lemon", "Grapes", "Pineapple", "Jackfruit", "Watermelon"
]

land_sizes = [
    # --- STANDARD / METRIC UNITS (Used Nationally) ---
    "1 acre", "2 acres", "5 acres", "10 acres", "1.5 acres", "2.5 acres",
    "0.5 acre", "half an acre", "quarter acre",
    "1 hectare", "2 hectares", "5 hectares", "0.5 hectare", "10 hectares",
    "1000 square meters", "5000 sq ft", "10000 sq ft", "2000 sq yards",
    
    # --- NORTH INDIA (Punjab, Haryana, UP, Rajasthan, HP) ---
    # Common: Bigha, Biswa, Killa, Kanal
    "1 bigha", "2 bighas", "4 bighas", "5 kachha bighas", "1 pucca bigha",
    "10 biswas", "5 biswas", "12 biswas", "20 biswas",
    "1 killa", "2 killas", "5 killas", "10 killas", # (Popular in Punjab/Haryana)
    "1 kanal", "2 kanals", "4 kanals", "8 kanals", "10 kanals",
    "5 marlas", "10 marlas", "15 marlas", # (Small units in North)
    "1 ghumaon", "2 ghumaons", # (Old Punjabi unit)
    "1 sarsahi", "5 sarsahis",
    
    # --- EAST INDIA (Bihar, West Bengal, Odisha, Assam, Jharkhand) ---
    # Common: Katha, Dhur, Decimal, Chatak, Lecha
    "1 katha", "2 kathas", "5 kathas", "10 kathas", "20 kathas",
    "1 kattha", "2 katthas", # (Spelling variation often found in Bihar)
    "10 decimals", "5 decimals", "25 decimals", "50 decimals", "1 decimal",
    "1 dhur", "5 dhurs", "10 dhurs", "20 dhurs",
    "1 chatak", "2 chataks", "5 chataks", "16 chataks",
    "1 lecha", "5 lechas", "10 lechas", # (Assam specific)
    
    # --- WEST INDIA (Maharashtra, Gujarat, Rajasthan) ---
    # Common: Guntha, Vigha, Are
    "1 guntha", "2 gunthas", "5 gunthas", "10 gunthas", "20 gunthas", "40 gunthas",
    "1 gunta", "2 guntas", "5 guntas", # (Spelling variation)
    "1 vigha", "2 vighas", "5 vighas", # (Gujarati variation of Bigha)
    "1 are", "5 ares", "10 ares", "100 ares",
    "5 vasas", "10 vasas", # (Rare but used in Gujarat)
    
    # --- SOUTH INDIA (TN, Kerala, Karnataka, AP, Telangana) ---
    # Common: Cent, Ground, Ankanam, Kuncham
    "1 cent", "2 cents", "5 cents", "10 cents", "50 cents", "100 cents",
    "1 ground", "2 grounds", "5 grounds", "10 grounds", # (Tamil Nadu real estate/farm)
    "1 ankanam", "5 ankanams", "10 ankanams", # (Andhra/Telangana)
    "1 kuncham", "5 kunchams", "10 kunchams",
    
    # --- COMPLEX/MIXED PHRASING (How people actually speak) ---
    "2 acres and 5 gunthas",
    "1 bigha 4 biswa",
    "5 kanals and 10 marlas",
    "3 acres 20 cents",
    "1000 gaj", # (Gaj = Square Yard, common in Hindi belt)
    "200 gaj"
]

land_types = [
    # --- IRRIGATION STATUS (Crucial for Loan Eligibility) ---
    "Irrigated", "Rain-fed", "Dry land", "Wetland", 
    "Partially irrigated", "Assurred irrigation", "Unirrigated",
    "Canal irrigated", "Tube-well irrigated", "Tank irrigated", 
    "Well irrigated", "Drip irrigated", "Sprinkler irrigated",
    
    # --- SOIL TYPES (Determines Crop Suitability) ---
    "Black soil", "Red soil", "Alluvial soil", "Sandy loam", 
    "Clayey soil", "Saline soil", "Alkaline soil", "Laterite soil",
    "Loamy soil", "Silt", "Desert soil", "Marshy", "Rocky",
    "Kali mitti", "Lal mitti", "Regur soil", # (Hindi/Local terms)
    
    # --- TOPOGRAPHY & ELEVATION ---
    "Hilly", "Sloped", "Plains", "Lowland", "Highland", "Upland", 
    "Terraced", "Valley", "Riverbed", "Coastal", "Forest land",
    "Dhipa", "Khal", # (Common terms for High/Low land in East India)
    
    # --- CULTIVATION STATUS ---
    "Barren", "Fallow", "Current fallow", "Cultivable waste", 
    "Pasture", "Grazing land", "Arable", "Orchard", "Garden land", 
    "Double cropped", "Single cropped", "Homestead",
    
    # --- REGIONAL REVENUE TERMS (Verbatim from Land Records) ---
    "Barani",   # Rainfed (Common in North India/Punjab/Haryana)
    "Chahi",    # Irrigated by Well (North)
    "Nahri",    # Irrigated by Canal (North)
    "Banjar",   # Wasteland (North)
    "Khushki",  # Dry land (Deccan/South)
    "Tari",     # Wet land (Deccan/South)
    "Baghayat", # Garden/Orchard land (West India/Maharashtra)
    "Jirayat",  # Dry crop land (Maharashtra/Gujarat)
    "Nanjai",   # Wet land (Tamil Nadu)
    "Punjai",   # Dry land (Tamil Nadu)
    "Magani"    # Wetland (Karnataka)
]

seasons = [
    # --- SCIENTIFIC AGRICULTURAL SEASONS ---
    "Kharif", "Rabi", "Zaid",
    "Kharif season", "Rabi season", "Zaid season",
    "Early Kharif", "Late Kharif", "Late Rabi",

    # --- WEATHER-BASED TERMS (Common in colloquial speech) ---
    "Monsoon", "Rainy season", "Winter", "Summer", 
    "Dry season", "Wet season", "Post-monsoon", "Pre-monsoon",
    "Cold season", "Hot season",

    # --- MONTH-BASED (Farmers often use Hindi/English months) ---
    "June-July", "October-November", "March-April",
    "Sawan", "Bhadon", "Kartik", "Magh", "Chaitra", "Baisakh", # (Hindi Months)
    "Ashadh", "Phalguna",

    # --- CROP-SPECIFIC PHRASING (Implicit Season) ---
    "Paddy season", "Wheat season", "Sowing season", "Harvesting season",
    "Planting time", "Cutting time"
]

terrestrial_livestock = [
    # --- DAIRY & CATTLE (Bovines) ---
    "Cows", "Buffaloes", "Jersey Cow", "Holstein Friesian", "HF Cow",
    "Gir Cow", "Sahiwal", "Red Sindhi", "Tharparkar",
    "Murrah Buffalo", "Surti Buffalo", "Mehsana Buffalo",
    "Bullocks", "Oxen", "Calves", "Heifers", "Milch animals",
    "Cross-bred cows", "Desi cows",

    # --- GOAT & SHEEP (Small Ruminants) ---
    "Goats", "Sheep", "Buck", "Doe", "Lamb", "Ram",
    "Jamunapari", "Beetal", "Barbari", "Black Bengal", "Sirohi",
    "Nellore", "Mandya", "Marwari",

    # --- POULTRY (Birds) ---
    "Poultry", "Chickens", "Hens", "Broilers", "Layers", "Chicks",
    "Desi Murgh", "Kadaknath", "Vanaraja",
    "Ducks", "Quails", "Turkeys", "Guinea Fowl",
    "Egg laying birds", "Meat birds",

    # --- PIGGERY ---
    "Pigs", "Swine", "Boar", "Piglets",

    # --- APICULTURE ---
    "Honey Bees", "Beehives", "Apiary",

    # --- SERICULTURE ---
    "Silkworms", "Cocoons",

    # --- OTHER TERRESTRIAL / REGIONAL ---
    "Camels", "Mithun", "Yak"
]

aquaculture_livestock = [
    "Fish", "Rohu", "Catla", "Mrigal", "Carp",
    "Prawns", "Shrimp", "Vannamei", "Tiger Prawns",
    "Crabs", "Catfish", "Pangasius"
]

templates = [
    # --- SECTION A: COMPLEX SYNTAX & CONDITIONAL CLAUSES (Positional Diversity) ---
    # Strategies: Start with subordinate clauses, use passive voice.
    "If the rain continues, my {crop} harvest will be delayed.",
    "Although I own {land_size}, the soil quality is poor.",
    "Since the market price for {crop} dropped, I am switching to {terrestrial_livestock}.",
    "Unless I receive the {scheme} benefit, I cannot afford new seeds.",
    "Because of the drought, {crop} cultivation on my {land_size} has stopped.",
    "While {name} manages the accounts, I handle the {terrestrial_livestock}.",
    "Whenever the {season} arrives, we prepare the {land_size} for sowing.",
    "Given that my income is {income_amount}, I qualify for the {category} quota.",
    "Should the bank approve my loan of {loan_amount}, I will buy a {resource}.",
    "Before planting {crop}, we must test the soil.",

    # --- SECTION B: PASSIVE VOICE & OBJECT-FIRST STRUCTURES ---
    # Strategies: Move entities to the start or very end of sentences[cite: 3].
    "{crop} is what we primarily cultivate in this region.",
    "The {scheme} was applied for by my father last month.",
    "A loan of {loan_amount} is being processed by the {bank}.",
    "{land_size} of land is owned by my family in {village}.",
    "The {resource} was purchased using the subsidy from {scheme}.",
    "{terrestrial_livestock} rearing is considered profitable by many here.",
    "By the end of {season}, the {crop} will be ready for harvest.",
    "Into the {bank} account, the {income_amount} was deposited.",
    "Under the {category} category, my application was accepted.",
    "From {village}, {name} has requested a meeting.",

    # --- SECTION C: HIGH DENSITY CO-OCCURRENCE (Multiple Entities) ---
    # Strategies: Force distinct entity types (Crop + Land + Scheme) together.
    "I grow {crop_1} and {crop_2} on my {land_size} of {land_type} land.",
    "To improve my {crop} yield, I need a {resource} through the {scheme}.",
    "My {terrestrial_livestock} and {aquaculture_livestock} require a loan of {loan_amount}.",
    "{name} from {village} applied for {scheme_1} and {scheme_2}.",
    "We use {resource_1} and {resource_2} for farming {crop} in the {season}.",
    "My {land_size} produces {crop}, which earns me {income_amount} annually.",
    "I need {loan_amount} from {bank} to buy {resource} for my {land_type} farm.",
    "Does the {scheme} cover both {crop_1} and {crop_2} damages?",
    "With {income_amount} income, can I afford {resource} and {terrestrial_livestock}?",
    "{season} farming of {crop} requires {resource} and reliable irrigation.",

    # --- SECTION D: FINANCIAL & BANKING SPECIFIC (Semantic Separation) ---
    # Strategies: Distinct contexts for money to avoid confusing Income vs. Loan[cite: 13].
    "The {bank} has sanctioned a credit limit of {loan_amount}.",
    "I am repaying the {loan_amount} borrowed for my tractor.",
    "My total annual earnings from agriculture are {income_amount}.",
    "Is a family income of {income_amount} eligible for this waiver?",
    "I have a pending debt of {loan_amount} with the cooperative.",
    "The subsidy amount credited to my account is distinct from my {income_amount} earnings.",
    "Can {bank} provide a top-up on my existing {loan_amount}?",
    "We struggle because our household income is only {income_amount}.",
    "The installments for the {loan_amount} loan are becoming a burden.",
    "I declared {income_amount} on my income certificate.",

    # --- SECTION E: NEGATIVE SAMPLES (No Entities) ---
    # Strategies: Sentences with NO placeholders to teach the model when NOT to tag.
    "The weather has been very unpredictable lately.",
    "Farming is hard work but it is honest work.",
    "I need to go to the market tomorrow morning.",
    "Please tell me the procedure to meet the officer.",
    "Is the office open on Saturdays?",
    "We are waiting for the monsoon to arrive.",
    "Water scarcity is a major issue in our village.",
    "Transportation costs have gone up significantly.",
    "The village meeting is scheduled for next week.",
    "My son is studying in the city college.",
    "Agriculture is the backbone of our economy.",
    "Can you help me fill out this form?",
    "The road to the farm is in bad condition.",
    "We need better electricity supply during the day.",
    "Who is the current sarpanch of this area?",

    # --- SECTION F: DISTRACTORS & AMBIGUITY (Shortcut Risk Reduction) ---
    # Strategies: Use trigger words (bank, season, seeds) without the actual entities.
    "I went to the bank to update my passbook.", 
    "This season has been very difficult for us.",
    "I need to buy some seeds from the local shop.",
    "The field needs to be plowed before the rains.",
    "Is there any government help available for us?",
    "The animals are grazing in the open field.",
    "I want to ask about the interest rates.",
    "My application was rejected due to missing documents.",
    "We usually harvest in the early morning.",
    "The cooperative society meeting is at noon.",

    # --- SECTION G: DEMOGRAPHIC & SOCIAL CONTEXT ---
    "As a {gender} farmer, I face unique challenges in {village}.",
    "My family belongs to the {caste} community in {district}.",
    "I am {name}, a {age}-year-old resident of {state}.",
    "We are a {family_size} living in a small house.",
    "Being from the {category} category, do I get extra benefits?",
    "{name}, {relation}, is the legal heir to this property.",
    "Our {religion} customs are strictly followed in the village.",
    "I am the head of a {family_size} in {village}.",
    "Is there a special quota for {caste} farmers?",
    "My identity as a {category} member is stated in the card.",

    # --- SECTION H: RESOURCE & REQUEST INTENT ---
    "I am looking to purchase a {resource} for my farm.",
    "Is there a subsidy available for {resource}?",
    "My request is regarding the {scheme} application.",
    "I want to register for {req_type} under the new guidelines.",
    "Please process my {req_type} as soon as possible.",
    "I need information about {scheme_1} and {scheme_2}.",
    "How do I apply for {scheme} online?",
    "The {resource} I bought last year is not working.",
    "Can you check the status of my {req_type}?",
    "I require a {resource} to manage the harvest efficiently.",

    # --- SECTION I: LIVESTOCK & AQUACULTURE SPECIFIC ---
    "I am planning to start {aquaculture_livestock} farming.",
    "My pond is stocked with {aquaculture_livestock} and local fish.",
    "Feeding {terrestrial_livestock} costs me {income_amount} per year.",
    "The {terrestrial_livestock} need vaccination urgently.",
    "Is {aquaculture_livestock} covered under the insurance scheme?",
    "I sell milk from my {terrestrial_livestock} to the dairy.",
    "We are expanding our {aquaculture_livestock} business.",
    "The {terrestrial_livestock} shed was damaged in the storm.",
    "Prices for {aquaculture_livestock} are high in the local market.",
    "I need a loan to buy more {terrestrial_livestock}."

    # --- SECTION J: INCOME STATUS SPECIFIC (New Entity) ---
    "I belong to the {income_status} category and need financial help.",
    "As a {income_status} farmer, am I eligible for the {scheme}?",
    "My family is classified as {income_status} in the government records.",
    "Is there any special subsidy on {resource} for {income_status} households?",
    "We are a {income_status} family living in {village}.",
    "I have attached my {income_status} certificate with the application.",
    "Since I fall under the {income_status} group, I cannot pay high interest.",
    "Does the bank offer lower interest rates for {income_status} applicants?",
    "My application was rejected because I am not considered {income_status}.",
    "With a family of {family_size}, we are struggling as a {income_status} household.",
    "The {scheme} is exclusively for {income_status} farmers.",
    "Please update my status from APML to {income_status} in the passbook.",
    "Only {income_status} beneficiaries can apply for this {req_type}.",
    "I possess a valid card proving my {income_status} status.",
    "Government benefits for {income_status} families have not reached me yet.",
]

loan_amounts = [
    # --- STANDARD NUMERIC (with & without commas) ---
    "50,000 rupees", "10,000 rupees", "25,000 rupees", "80,000 rupees",
    "50000", "10000", "20000", "15000", "25000", "30000",
    "40000", "45000", "60000", "75000", "80000", "90000",
    "100000", "150000", "200000", "300000", "500000",
    "1,00,000", "1,50,000", "2,00,000", "3,00,000", "5,00,000",
    "7,50,000", "10,00,000", "12,00,000", "25,00,000",

    # --- TEXTUAL "LAKH" & "CRORE" (Standard Indian English) ---
    "1 lakh", "2 lakhs", "5 lakhs", "10 lakhs", 
    "1.5 lakhs", "2.5 lakhs", "3.5 lakhs", "7.5 lakhs",
    "1.6 lakhs", "1.60 lakhs", # (Specific KCC limit often cited)
    "one lakh", "two lakhs", "five lakhs", "ten lakhs",
    "half a lakh", "quarter lakh", # (Rare but possible in speech)
    "12 lakhs", "15 lakhs", "20 lakhs", "25 lakhs", "50 lakhs",
    "1 crore", "1.5 crores", # (For large machinery/groups)

    # --- "THOUSAND" VARIATIONS ---
    "50 thousand", "fifty thousand", "20 thousand", "twenty thousand",
    "10 thousand", "ten thousand", "five thousand", "two thousand",
    "25 thousand", "75 thousand", "80 thousand", "90 thousand",
    "1 lakh 50 thousand", "2 lakhs 10 thousand",

    # --- SHORT HAND / SLANG (Common in chat/notes) ---
    "50k", "10k", "20k", "25k", "100k", "5k", "2k",
    "1.5L", "2L", "5L", "10L", "50L", "1Cr",

    # --- CURRENCY PREFIXES/SUFFIXES ---
    "Rs 50000", "Rs. 10,000", "INR 50,000", "Rs. 1 lakh",
    "Rupees 5 lakhs", "Rupees fifty thousand",
    "INR 2 lakhs", "Rs. 1.6 lakhs", "Rs 15000",

    # --- SPECIFIC / ODD AMOUNTS (To prevent model memorizing "000" endings) ---
    "49,000", "99,000", "1,60,000", "3,20,000",
    "12,500", "17,500", "22,500", "27,000",
    "55,000", "65,000", "85,000", "95,000"
]

income_amounts = [
    # --- YEARLY INCOME ---
    "2 lakhs per year", "3 lakhs per year", "5 lakhs per year",
    "1.5 lakhs per year", "2.5 lakhs per year", "4 lakhs per year",
    "60,000 per year", "80,000 per year", "90,000 per year",
    "1 lakh per annum", "2 lakhs per annum", "5 lakhs per annum",
    "Rs. 2 lakhs annually", "Rs. 1.2 lakhs per year",
    "50,000 yearly", "75,000 yearly", "1,20,000 per year",

    # --- MONTHLY INCOME ---
    "10,000 per month", "5,000 per month", "15,000 per month",
    "20,000 per month", "8,000 per month", "12,000 per month",
    "25,000 per month", "3,000 per month", "2,000 per month",
    "Rs. 6000 pm", "Rs. 10000 pm", "Rs. 15000 pm",
    "5k per month", "10k per month", "15k per month",
    "earning 10000 monthly", "earning 20000 monthly",

    # --- PRECISE / IRREGULAR ---
    "48,000 per year", "72,000 per year", "96,000 per year",
    "1,44,000 per year", "1,80,000 per year",
    "4500 per month", "8500 per month", "12500 per month"
]

income_statuses = [
    "BPL",
    "below poverty line",
    "low income",
    "middle income",
    "economically weaker section",
    "EWS",
    "marginal farmer income",
    "small farmer income",
    "no regular income",
    "seasonal income",
    "daily wage earner",
    "meager income",
    "sufficient income",
    "high income",
    "average income",
    "family income of 1 lakh",
    "household income of 2 lakhs"
]

banks = [
    # --- MAJOR PUBLIC SECTOR BANKS (PSBs) ---
    "SBI", "State Bank of India", "State Bank", 
    "PNB", "Punjab National Bank", 
    "BoB", "Bank of Baroda", 
    "Canara Bank", "Union Bank", "Union Bank of India",
    "Bank of India", "BoI", "Central Bank of India", "CBI",
    "Indian Bank", "Indian Overseas Bank", "IOB",
    "UCO Bank", "Bank of Maharashtra", "Punjab & Sind Bank",

    # --- REGIONAL RURAL BANKS (RRBs - Crucial for Agriculture) ---
    "Odisha Gramya Bank", "OGB", 
    "Utkal Grameen Bank", "UGB", # (Specific to Odisha)
    "Andhra Pradesh Grameena Vikas Bank", "APGVB",
    "Kerala Gramin Bank", "Karnataka Vikas Grameena Bank",
    "Prathama UP Gramin Bank", "Aryavart Bank",
    "Baroda UP Gramin Bank", "Sarva Haryana Gramin Bank",
    "Rajasthan Marudhara Gramin Bank", "Bihar Gramin Bank",
    "Paschim Banga Gramin Bank", "Telangana Grameena Bank",

    # --- COOPERATIVE BANKS & SOCIETIES (PACS/DCCB) ---
    "Cooperative Bank", "Co-op Bank", "District Cooperative Bank",
    "DCCB", "District Central Cooperative Bank",
    "OSCB", "Odisha State Cooperative Bank",
    "Apex Bank", "State Cooperative Bank",
    "PACS", "Primary Agricultural Credit Society", "The Society",
    "Land Development Bank", "Urban Cooperative Bank",

    # --- PRIVATE SECTOR BANKS (Rural Branches) ---
    "HDFC Bank", "HDFC", 
    "ICICI Bank", "ICICI", 
    "Axis Bank", "Kotak Mahindra Bank", "Kotak Bank",
    "IndusInd Bank", "IDFC First Bank", "Bandhan Bank",
    "Federal Bank", "South Indian Bank", "Yes Bank",

    # --- SMALL FINANCE BANKS (Rising in Rural Areas) ---
    "AU Small Finance Bank", "Ujjivan Small Finance Bank",
    "Equitas Small Finance Bank", "Jana Small Finance Bank",
    "ESAF Small Finance Bank",

    # --- INSTITUTIONAL / REGULATORY BODIES ---
    "NABARD", "National Bank for Agriculture and Rural Development",
    "RBI", "Reserve Bank of India",
    "SIDBI", "Mudra Bank",

    # --- COLLOQUIAL / GENERIC TERMS ---
    "Gramin Bank", "Village Bank", "Local Bank", 
    "Sarkari Bank", "Government Bank", "Private Bank",
    "The Branch", "Main Branch", "Lead Bank"
]

debt_status = [
    # --- CLEAR / NO DEBT ---
    "I have no due loans", "I have paid off all my debts", "my loan is cleared",
    "no outstanding dues", "I am debt free", "my account is clean",
    "I have a No Dues Certificate", "previous loan is fully paid",
    "I have closed my KCC account", "all installments are paid",
    
    # --- ACTIVE DEBT (Standard) ---
    "I have an existing loan", "my KCC loan is active", "I have a running loan",
    "I have a debt", "my crop loan is still pending", 
    "I have an active loan with the cooperative society",
    "I have taken a gold loan", "my tractor loan is ongoing",
    "I am paying my EMIs regularly", "I have a loan limit of 1 lakh",

    # --- OVERDUE / DEFAULT (Negative Status) ---
    "I am a defaulter", "my loan is overdue", "I missed the last installment",
    "my account has become NPA", "my previous loan is pending",
    "I could not pay due to crop failure", "bank has sent a notice",
    "interest is piling up", "I have a bad repayment history",
    "my CIBIL score is low", "loan is in default",

    # --- PARTIAL / SPECIFIC STATUS ---
    "I paid the principal but interest is left", "only one EMI is remaining",
    "my loan renewal is pending", "I have renewed my KCC",
    "I settled the loan through OTS", # (One Time Settlement)
    "my loan limit is exhausted", "I have a debt from the moneylender",
    "half the loan is paid", "I need to renew my account"
]

male_names = [
    # --- North India ---
    "Ram", "Shyam", "Kishan", "Mohan", "Sohan", "Gopal",
    "Ramesh", "Suresh", "Mahesh", "Dinesh", "Rajesh",
    "Amit", "Sumit", "Anil", "Sunil", "Manoj", "Deepak",
    "Sanjay", "Vijay", "Ajay", "Pradeep", "Sandeep",
    "Alok", "Vikas", "Ashish", "Naveen", "Praveen",
    "Brijesh", "Kamlesh", "Om Prakash", "Shiv Kumar",
    "Ram Lal", "Sohan Lal", "Kanhaiya", "Raghubir",
    "Babu Lal", "Chhote Lal", "Girdhari Lal", "Deen Dayal",
    "Rameshwar Prasad", "Suresh Kumar", "Mahadev Prasad",

    # --- Punjab & Haryana ---
    "Manpreet", "Gurpreet", "Harpreet", "Jasbir", "Daljeet",
    "Kuldeep", "Balwinder", "Sukhwinder", "Jatinder",
    "Rajinder", "Surinder", "Harjit", "Avtar", "Joginder",
    "Satnam", "Amrik", "Balbir", "Karnail", "Gurcharan",
    "Hardeep",

    # --- East India ---
    "Bijay", "Sanjib", "Pradipta", "Manas", "Sapan",
    "Ranjan", "Biswajit", "Satyajit", "Tapan", "Gagan",
    "Deepankar", "Subhash", "Gouranga", "Balaram",
    "Aditya", "Sameer", "Sudipta", "Debasish",
    "Manoj Kumar", "Ashok", "Rabi Narayan", "Bhagirathi",

    # --- Tribal / Indigenous ---
    "Budhu", "Somra", "Mangal", "Sukra", "Budhwa",
    "Laxman", "Birsa", "Sidhu", "Kanhu", "Mogal",
    "Dambaru", "Chaitan", "Haria", "Guru", "Bhima",
    "Mahadev", "Kanku", "Joga", "Rupa",

    # --- South India ---
    "Venkatesh", "Subramaniam", "Murugan", "Ravi", "Kumar",
    "Krishna", "Srinivas", "Nagaraj", "Reddy", "Rao",
    "Muthu", "Velu", "Perumal", "Chinnasamy", "Ramasamy",
    "Gowda", "Appanna", "Thimmayya", "Narayana",
    "Ananth", "Balaji", "Karthik", "Saravanan",
    "Muniswamy", "Chandrashekar",

    # --- Muslim (non-famous) ---
    "Mohammed", "Abdul", "Ahmed", "Ibrahim", "Ismail",
    "Yusuf", "Rahim", "Karim", "Mustafa", "Ali",
    "Saddam", "Hussain", "Ansari", "Rashid", "Firoz",
    "Javed", "Salim", "Imran", "Farooq", "Nasir",

    # --- Christian (non-famous) ---
    "Joseph", "Thomas", "Mathew", "George", "John",
    "Anthony", "David", "Philip", "Varghese", "Chacko",
    "Paul", "Peter", "Samuel", "Andrew",

    # --- West India ---
    "Patel", "Pawar", "Jadav", "Shinde", "Deshmukh",
    "Mukesh", "Nitin", "Vilas", "Ganesh", "Jignesh",
    "Hardik", "Dhiraj", "Ramesh Patil", "Vijay Patil",

    # --- North East ---
    "Bipul", "Mukul", "Haren", "Dipen", "Jintu",
    "Manab", "Pranjal", "Gogoi", "Boro", "Sangma",
    "Lyngdoh", "Khyriem", "Lalram", "Thangboi"
]

female_names = [
    # --- Common Rural / Pan-India ---
    "Kamla", "Vimala", "Sunita", "Anita", "Geeta", "Sita",
    "Radha", "Meera", "Rani", "Pooja", "Rekha",
    "Savitri", "Gayatri", "Laxmi", "Parvati", "Durga",
    "Shanti", "Suman", "Kusum", "Sheela", "Usha",
    "Saroj", "Manju", "Bimala", "Phoolwati",
    "Basanti", "Champa", "Gauri", "Indu", "Nirmala",
    "Kanta", "Shobha", "Kalpana", "Asha", "Kiran",

    # --- Punjab & Haryana ---
    "Simran", "Paramjeet", "Gurpreet Kaur", "Harpreet Kaur",
    "Baljit Kaur", "Jaswinder Kaur", "Manjit Kaur",

    # --- East India ---
    "Nalini", "Damayanti", "Sanju", "Mamta",
    "Binodini", "Suchitra", "Madhuri", "Rashmita",
    "Pratima", "Minati", "Lalita", "Sabita",

    # --- Tribal / Indigenous ---
    "Raima", "Sombari", "Shani", "Budri", "Hirani",
    "Laxmi Tudu", "Sukri", "Phuli", "Janki",
    "Manki", "Dulari",

    # --- South India ---
    "Lakshmi", "Padma", "Amma", "Mallika", "Vasanthi",
    "Meenakshi", "Chitra", "Saroja", "Bhavani",
    "Kavitha", "Anusuya", "Selvi", "Rajalakshmi",

    # --- Muslim (non-famous) ---
    "Fatima", "Ayesha", "Salma", "Reshma", "Noor",
    "Shabnam", "Yasmin", "Farida", "Nazma",
    "Rukhsana", "Sultana",

    # --- Christian (non-famous) ---
    "Mary", "Rose", "Daisy", "Annamma", "Theresa",
    "Mariam", "Elsa", "Lucy", "Agnes",

    # --- West India ---
    "Bhavna", "Sheetal", "Rupal", "Kavita",
    "Hemlata", "Chandrika", "Sarita", "Neeta",

    # --- North East ---
    "Devi", "Lalrin", "Zothanpuii", "Meban",
    "Mimi", "Ankita"
]

male_relations = [
    # --- Direct gendered ---
    "Son of",
    "Husband of",
    "Father of",
    "Widower of",

    # --- Abbreviations ---
    "S/O", "s/o",      # Son of
    "H/O", "h/o",      # Husband of

    # --- Family roles ---
    "Brother of",
    "Grandson of",
    "Nephew of",
    "Uncle of",

    # --- Explicitly male grammar ---
    "elder brother of",
    "younger brother of"
]

female_relations = [
    # --- Direct gendered ---
    "Daughter of",
    "Wife of",
    "Mother of",
    "Widow of",

    # --- Abbreviations ---
    "D/O", "d/o",      # Daughter of
    "W/O", "w/o",      # Wife of

    # --- Family roles ---
    "Sister of",
    "Granddaughter of",
    "Aunt of"
]

neutral_relations = [
    # --- Marital / parental neutral ---
    "Spouse of",
    "married to",
    "child of",

    # --- Care / representation ---
    "Care of",
    "C/O", "c/o",
    "Guardian of",
    "dependent of",

    # --- Legal / administrative ---
    "Legal heir of",
    "Nominee of",
    "acting on behalf of",
    "representative of"
]

categories = [
    # --- MAJOR CONSTITUTIONAL CATEGORIES ---
    "SC", "Scheduled Caste", "S.C.",
    "ST", "Scheduled Tribe", "S.T.",
    "OBC", "Other Backward Class", "O.B.C.", "Backward Class", "BC",
    "General", "GEN", "General Category", "UR", "Unreserved",
    
    # --- SPECIFIC SUB-CATEGORIES (State & Economic) ---
    "SEBC", "Socially and Educationally Backward Classes", # (Common in Odisha/Maharashtra)
    "EWS", "Economically Weaker Section",
    "MBC", "Most Backward Class", # (Common in Tamil Nadu/South)
    "DNC", "Denotified Communities",
    "PVTG", "Particularly Vulnerable Tribal Group", # (For special tribal schemes)
    "EBC", "Economically Backward Class",

    # --- MINORITY & SPECIAL STATUS ---
    "Minority", "Religious Minority",
    "PwD", "Person with Disability", "Divyang", "Handicapped", # (Often gets special subsidies)
    "Ex-Serviceman", "Defense Personnel", # (often has land allotments)
    "Woman Beneficiary", "Female Headed Household", # (Special status in schemes like PM Awas)
    
    # --- COLLOQUIAL / REGIONAL TERMS ---
    "Adivasi", "Tribal", "Vanvasi", # (For ST)
    "Dalit", "Harijan", # (Social terms found in speech, though official use varies)
    "Open Category", "OC",
    "Reserved Category", "Non-Reserved"
]

castes = [
    # --- NORTH INDIA (UP, Bihar, Haryana, Punjab) ---
    "Jat", "Yadav", "Ahir", "Gujjar", "Gurjar",
    "Brahmin", "Pandit", "Tyagi", "Bhumihar",
    "Rajput", "Thakur", "Kshatriya",
    "Kurmi", "Koeri", "Kushwaha", "Maurya",
    "Saini", "Mali", "Lohar", "Kumhar",
    "Chamar", "Jatav", "Valmiki", "Paswan", "Dusadh",

    # --- EAST INDIA (Odisha, Bengal, Assam) ---
    "Khandayat", "Chasa", "Karan", # (Major agricultural castes in Odisha)
    "Mahishya", "Sadgop", "Aguri", # (Bengal)
    "Kayastha", "Brahmin", "Baishya",
    "Gop", "Goud", "Teli", "Sahu",
    "Santal", "Munda", "Oraon", # (Tribal groups often self-identify by tribe name)
    "Kol", "Bhil", "Gond",

    # --- WEST INDIA (Maharashtra, Gujarat, Rajasthan) ---
    "Maratha", "Kunbi", "Dhangar", "Agri", # (Maharashtra)
    "Patel", "Patidar", "Leuva Patel", "Kadva Patel",
    "Koli", "Thakore", "Rabari", "Bharwad", # (Gujarat)
    "Meena", "Bishnoi", "Jat Sikh", "Rajpurohit", # (Rajasthan)

    # --- SOUTH INDIA (Andhra, Telangana, Karnataka, TN, Kerala) ---
    "Reddy", "Kamma", "Kapu", "Velama", "Raju",
    "Gowda", "Vokkaliga", "Lingayat", "Kuruba", # (Karnataka)
    "Gounder", "Vanniyar", "Thevar", "Nadar", "Chettiar", # (Tamil Nadu)
    "Nair", "Ezhava", "Menon", "Pillai", "Syrian Christian", # (Kerala)
    "Shetty", "Rai", "Bunt",

    # --- GENERAL / GENERIC TERMS ---
    "Savarna", "Avarna", "Dalit", "Adivasi",
    "Upper Caste", "Lower Caste", "Backward Caste",
    "Trading Community", "Farming Community",
    "Weaver Community", "Fisherman Community"
]

religions = [
    # --- MAJOR RELIGIONS ---
    "Hindu", "Hinduism", "Sanatan Dharma",
    "Muslim", "Islam", "Musalman",
    "Christian", "Christianity",
    "Sikh", "Sikhism",
    "Buddhist", "Buddhism", "Navayana", # (Neo-Buddhism common in Maharashtra)
    "Jain", "Jainism",

    # --- SECTS & DENOMINATIONS (Often used in identity) ---
    "Sunni", "Shia",
    "Catholic", "Roman Catholic", "Protestant", "Baptist", # (Baptist is common in Nagaland/Mizoram)
    "Syrian Christian", # (Kerala)
    "Digambar", "Shvetambar", # (Jain sects)
    "Vaishnav", "Shaiva",

    # --- TRIBAL & INDIGENOUS FAITHS (Crucial for East/NE India) ---
    "Sarna", "Sarnaism", # (Common in Jharkhand/Odisha/Bengal tribal belts)
    "Donyi-Polo", # (Arunachal Pradesh)
    "Sanamahi", "Sanamahism", # (Manipur)
    "Bathou", # (Assam - Bodo community)
    "Animist", "Nature Worshipper",

    # --- MINORITY / OTHER ---
    "Parsi", "Zoroastrian",
    "Bahai",
    "Jew", "Jewish" # (Tiny communities in Kochi/Mumbai/Manipur)
]

male_gender_terms = [
    # --- Standard ---
    "Male",
    "Man",
    "Boy",

    # --- Conversational / Indian usage ---
    "Gentleman",
    "Gents",
    "Purush",        # Hindi: Man

    # --- Status-based ---
    "Widower"
]

female_gender_terms = [
    # --- Standard ---
    "Female",
    "Woman",
    "Girl",

    # --- Conversational / Indian usage ---
    "Lady",
    "Ladies",
    "Mahila",        # Hindi: Woman

    # --- Status-based ---
    "Widow",
    "Housewife",
    "Homemaker"
]

family_sizes = [
    # --- NUMERIC COUNTS (Standard) ---
    "3 members", "4 members", "5 members", "6 members", "7 members",
    "8 members", "10 members", "12 members", "15 members",
    "family of 3", "family of 4", "family of 5", "family of 6",
    "household of 5", "household of 8",
    "3 people", "4 people", "5 people", "6 persons",

    # --- FAMILY STRUCTURE (Crucial for Land Division Context) ---
    "Joint family", "Joint household", "Undivided family",
    "Nuclear family", "Small family", "Large family",
    "Extended family", "Big family",

    # --- COMPOSITION DESCRIPTIONS (Conversational) ---
    "4 adults and 2 children", "2 adults and 3 kids",
    "husband, wife and 2 children", "living with my parents",
    "living with in-laws", "me and my mother",
    "3 generations living together",
    "5 brothers and their families", # (implies large land holding/dispute risk)
    "sole earner for 6 people",
    
    # --- DEPENDENCY FOCUS (Economic Context) ---
    "5 dependents", "3 dependents", "no dependents",
    "8 mouths to feed", "large number of dependents",
    "supporting a family of 6", "supporting my old parents"
]

schemes = [
    # --- CENTRAL FLAGSHIP SCHEMES (Income & Insurance) ---
    "PM-Kisan", "Pradhan Mantri Kisan Samman Nidhi", "PM Kisan Yojana",
    "PMFBY", "Pradhan Mantri Fasal Bima Yojana", "Fasal Bima", "Crop Insurance Scheme",
    "KCC", "Kisan Credit Card", "Kisan Credit Card Scheme",
    "PMKSY", "Pradhan Mantri Krishi Sinchai Yojana", "Har Khet Ko Pani",
    "PKVY", "Paramparagat Krishi Vikas Yojana", "Organic Farming Scheme",
    "Soil Health Card", "Soil Health Card Scheme", "SHC",
    "e-NAM", "National Agriculture Market", "Mandi Scheme",
    "PM-KMY", "Pradhan Mantri Kisan Maandhan Yojana", "Kisan Pension Scheme",
    "PM-AASHA", "Annadata Aay Sanrakshan Abhiyan",
    "AIF", "Agriculture Infrastructure Fund",

    # --- STATE-SPECIFIC SCHEMES (East & South - High Volume) ---
    # Odisha
    "KALIA", "Kalia Scheme", "Krushak Assistance for Livelihood and Income Augmentation",
    "Balaram Scheme", "Bhoomiheen Kisan Loan", "Odisha Millet Mission",
    "Mo Badi", "Ama Krushi", "SAFAL", "Mukhyamantri Krishi Udyog Yojana",
    # Telangana & Andhra Pradesh
    "Rythu Bandhu", "Farmers Investment Support Scheme",
    "YSR Rythu Bharosa", "YSR Free Crop Insurance", "Jagananna Thodu",
    "YSR Sunna Vaddi", "Zero Interest Loan",
    # West Bengal
    "Krishak Bandhu", "Krishak Bandhu Death Benefit",
    # Maharashtra & MP
    "Shetkari Sanman Yojana", "Namo Shetkari Maha Sanman Nidhi",
    "Bhavantar Bhugtan Yojana", "Mukhya Mantri Solar Pump Yojana",
    "Jalyukt Shivar", "Magel Tyala Shettale", # (Farm pond on demand)
    # North India (Punjab/Haryana/UP)
    "Mera Pani Meri Virasat", "Bhavantar Bharpayee Yojana",
    "Pashu Kisan Credit Card", "Kisan Uday Yojana",

    # --- LIVESTOCK, DAIRY & FISHERIES (The "Blue/White" Revolution) ---
    "PMMSY", "Pradhan Mantri Matsya Sampada Yojana", "Blue Revolution",
    "Kisan Sampada Yojana", "Dairy Entrepreneurship Development Scheme", "DEDS",
    "National Livestock Mission", "NLM",
    "Gopal Ratna Award", "Rashtriya Gokul Mission",
    "Pashu Dhan Bima Yojana", "Livestock Insurance",
    "MGNREGA", "NREGA", "Job Card", # (Often used for farm labor/fencing work)

    # --- ENERGY & SUSTAINABILITY ---
    "PM-KUSUM", "Kusum Yojana", "Solar Pump Subsidy",
    "Gobar-Dhan Yojana", "Biogas Scheme",
    "Sub-Mission on Agricultural Mechanization", "SMAM", "Tractor Subsidy",
    "Micro Irrigation Fund", "Drip Irrigation Subsidy",

    # --- COMPONENT / SPECIFIC SUBSIDIES (How farmers ask) ---
    "Fertilizer Subsidy", "Urea Subsidy",
    "Seed Subsidy", "Certified Seed Scheme",
    "Farm Mechanization Scheme", "Combine Harvester Subsidy",
    "Godown Construction Subsidy", "Cold Storage Subsidy",
    "Borewell Subsidy", "Diggi Scheme", # (Canal water storage)
    "Fencing Subsidy", "Tarbandi Yojana", # (Popular in Rajasthan)
    "Bamboo Mission", "National Bamboo Mission"
]

req_types = [
    # --- 1. FINANCIAL REQUESTS (Loans & Credit) ---
    "loan", "credit", "financial help", "financial assistance",
    "crop loan", "term loan", "soft loan", "interest-free loan",
    "KCC limit", "credit limit", "fresh loan", "renewal of loan",
    "top-up loan", "limit enhancement", "working capital",
    "loan sanction", "disbursement", "cash credit",
    "loan against land", "tractor loan", "dairy loan",

    # --- 2. SUBSIDY & GRANTS (Government Benefits) ---
    "subsidy", "grant", "government support", "financial aid",
    "back-ended subsidy", "capital subsidy", "interest subvention",
    "DBT", "Direct Benefit Transfer", "installment", "money transfer",
    "margin money", "seed funding", "input subsidy",
    "financial benefit", "first installment", "next installment",

    # --- 3. INSURANCE & COMPENSATION (Risk Coverage) ---
    "insurance", "claim", "compensation", "relief",
    "insurance claim", "damage assessment", "survey request",
    "premium subsidy", "claim settlement", "payment for damage",
    "drought relief", "flood relief", "crop loss compensation",
    "famine relief", "pest attack compensation",

    # --- 4. WAIVERS & DEBT RELIEF ---
    "waiver", "loan waiver", "debt relief", "interest waiver",
    "restructuring", "moratorium", "extension of time",
    "settlement", "one time settlement", "OTS",
    "loan write-off", "interest rebate",

    # --- 5. INFORMATION & STATUS CHECKS (Query Intent) ---
    "information", "status check", "application status", "payment status",
    "beneficiary status", "eligibility check", "list of names",
    "reason for rejection", "details", "guidelines",
    "account statement", "passbook update", "balance check",
    "inquiry", "scheme details", "loan eligibility",

    # --- 6. ADMINISTRATIVE & TECHNICAL ACTIONS ---
    "registration", "enrollment", "new application", "correction",
    "update", "KYC", "e-KYC", "Aadhar linking", "mobile linking",
    "grievance", "complaint", "technical support",
    "soil testing report", "land record verification",
    "bank account linking", "NPCI mapping" # (Crucial for DBT failure issues)
]

resources = [
    # --- HEAVY MACHINERY (Loan/Subsidy Targets) ---
    "Tractor", "Power Tiller", "Rotavator", "Cultivator", "Plough",
    "Combine Harvester", "Harvester", "Thresher", "Reaper",
    "Happy Seeder", "Super Seeder", "Zero Till Drill", # (Crucial for stubble management schemes)
    "Potato Planter", "Paddy Transplanter", "Sugarcane Harvester",
    "Laser Land Leveler", "Straw Baler", "JCB", "Excavator",
    "Mini Tractor", "4WD Tractor",

    # --- IRRIGATION EQUIPMENT (High Priority for subsidies) ---
    "Borewell", "Tube well", "Open well", "Dug well",
    "Solar Pump", "Electric Pump", "Diesel Pump", "Submersible Pump",
    "Monoblock Pump", "Motor", "Starter",
    "Drip Irrigation System", "Drip Kit", "Lateral pipes",
    "Sprinkler System", "Sprinkler Set", "Rain Gun",
    "PVC Pipes", "HDPE Pipes", "Pipeline",

    # --- AGRI-INPUTS: FERTILIZERS & CHEMICALS ---
    "Urea", "DAP", "Di-ammonium Phosphate", "MOP", "Potash",
    "NPK", "Complex Fertilizer", "SSP", "Single Super Phosphate",
    "Zinc", "Sulphur", "Micronutrients", "Bio-fertilizer", "Compost",
    "Pesticides", "Insecticides", "Herbicides", "Weedicides", "Fungicides",
    "Neem Oil", "Organic Manure", "Growth Promoter",

    # --- SEEDS & PLANTING MATERIAL ---
    "Seeds", "Certified Seeds", "Hybrid Seeds", "Foundation Seeds",
    "HYV Seeds", "High Yielding Variety Seeds",
    "Bt Cotton Seeds", "Soya Seeds", "Paddy Seeds", "Wheat Seeds",
    "Saplings", "Seedlings", "Nursery Plants", "Grafts",
    "Tissue Culture Plants", # (Common for Banana/Bamboo)

    # --- INFRASTRUCTURE & PROTECTION ---
    "Greenhouse", "Polyhouse", "Net House", "Shade Net",
    "Cold Storage", "Warehouse", "Godown", "Onion Chawl",
    "Cattle Shed", "Poultry Shed", "Goat Shed",
    "Fencing", "Barbed Wire Fencing", "Solar Fencing", "Chain Link",
    "Tarpaulin", "Tripal", "Plastic Sheet", # (For covering harvest)
    "Mulching Sheet", "Anti-hail Net",

    # --- SMALL MACHINERY & TOOLS ---
    "Chaff Cutter", "Fodder Cutter", "Milking Machine",
    "Knapsack Sprayer", "Battery Sprayer", "Power Sprayer", "Boom Sprayer",
    "Brush Cutter", "Weeder", "Cono Weeder",
    "Sickle", "Spade", "Pickaxe", "Crowbar",
    "Crates", "Plastic Crates", "Grain Bins"
]

states = [
    # --- NORTH INDIA ---
    "Punjab", "Haryana", "Himachal Pradesh", "HP",
    "Uttar Pradesh", "UP", "Uttarakhand", "UK", "Uttaranchal",
    "Rajasthan", "Delhi", "New Delhi",
    "Jammu and Kashmir", "J&K", "Ladakh",
    "Chandigarh",

    # --- EAST INDIA ---
    "Odisha", "Orissa", # (Old spelling often found in legacy docs)
    "West Bengal", "WB", "Bengal",
    "Bihar", "Jharkhand",
    "Andaman and Nicobar Islands",

    # --- WEST INDIA ---
    "Maharashtra", "MH",
    "Gujarat",
    "Goa",
    "Dadra and Nagar Haveli and Daman and Diu", "Daman and Diu",

    # --- SOUTH INDIA ---
    "Andhra Pradesh", "AP", "Andhra",
    "Telangana", "TS",
    "Karnataka",
    "Tamil Nadu", "TN",
    "Kerala",
    "Puducherry", "Pondicherry",
    "Lakshadweep",

    # --- CENTRAL INDIA ---
    "Madhya Pradesh", "MP",
    "Chhattisgarh", "CG",

    # --- NORTH EAST INDIA (The "Seven Sisters" + Sikkim) ---
    "Assam",
    "Arunachal Pradesh", "Arunachal",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Tripura",
    "Sikkim"
]

districts = [
    # --- ODISHA (Detailed coverage for your context) ---
    "Khordha", "Cuttack", "Puri", "Ganjam", "Balasore", "Bhadrak",
    "Jajpur", "Jagatsinghpur", "Kendrapara", "Nayagarh",
    "Sundargarh", "Sambalpur", "Bargarh", "Jharsuguda", "Deogarh",
    "Bolangir", "Sonepur", "Subarnapur", "Boudh", "Kandhamal",
    "Kalahandi", "Nuapada", "Koraput", "Rayagada", "Nabarangpur", "Malkangiri",
    "Mayurbhanj", "Keonjhar", "Dhenkanal", "Angul",

    # --- PUNJAB & HARYANA (The "Granary of India") ---
    "Ludhiana", "Amritsar", "Patiala", "Jalandhar", "Bathinda",
    "Ferozepur", "Gurdaspur", "Hoshiarpur", "Sangrur", "Mansa",
    "Karnal", "Hisar", "Kurukshetra", "Ambala", "Panipat",
    "Sirsa", "Fatehabad", "Rohtak", "Bhiwani", "Jind", "Kaithal",

    # --- UTTAR PRADESH (Sugar & Wheat Belt) ---
    "Lucknow", "Varanasi", "Gorakhpur", "Prayagraj", "Allahabad",
    "Agra", "Meerut", "Ghaziabad", "Muzaffarnagar", "Saharanpur",
    "Bareilly", "Moradabad", "Aligarh", "Jhansi", "Kanpur",
    "Ayodhya", "Faizabad", "Basti", "Gonda", "Bahraich",
    "Lakhimpur Kheri", "Sitapur", "Hardoi", "Unnao", "Barabanki",

    # --- BIHAR & EAST INDIA ---
    "Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga",
    "Purnia", "Katihar", "Madhubani", "Samastipur", "Begusarai",
    "Burdwan", "Purba Bardhaman", "Paschim Bardhaman", # (Rice bowl of Bengal)
    "Murshidabad", "Nadia", "Hooghly", "Birbhum", "Bankura",
    "Ranchi", "Jamshedpur", "Dhanbad", "Hazaribagh", "Bokaro",

    # --- MAHARASHTRA & GUJARAT (Cotton, Onion, Dairy) ---
    "Pune", "Nashik", "Nagpur", "Aurangabad", "Ahmednagar",
    "Solapur", "Satara", "Kolhapur", "Sangli", "Jalgaon",
    "Amravati", "Yavatmal", "Akola", "Latur", "Nanded",
    "Ahmedabad", "Rajkot", "Surat", "Vadodara", "Baroda",
    "Banaskantha", "Sabarkantha", "Mehsana", "Anand", "Kheda",
    "Bhavnagar", "Jamnagar", "Junagadh", "Amreli", "Kutch",

    # --- SOUTH INDIA (Spices, Paddy, Cash Crops) ---
    "Guntur", "Krishna", "East Godavari", "West Godavari", "Prakasam",
    "Nellore", "Chittoor", "Kurnool", "Anantapur", "Visakhapatnam",
    "Warangal", "Nalgonda", "Karimnagar", "Nizamabad", "Khammam",
    "Thanjavur", "Tanjore", "Madurai", "Coimbatore", "Salem", "Erode",
    "Tiruchirappalli", "Trichy", "Tirunelveli", "Villupuram",
    "Mandya", "Mysore", "Belagavi", "Belgaum", "Vijayapura", "Bijapur",
    "Hassan", "Shimoga", "Tumkur", "Raichur", "Koppal",
    "Palakkad", "Wayanad", "Idukki", "Thrissur", "Malappuram",

    # --- MADHYA PRADESH & RAJASTHAN (Soybean, Pulses, Mustard) ---
    "Indore", "Bhopal", "Ujjain", "Jabalpur", "Gwalior",
    "Sagar", "Satna", "Rewa", "Ratlam", "Mandsaur",
    "Sehore", "Hoshangabad", "Vidisha", "Raisen",
    "Jaipur", "Jodhpur", "Kota", "Bikaner", "Udaipur",
    "Sri Ganganagar", "Hanumangarh", # (Irrigated belt of Rajasthan)
    "Alwar", "Bharatpur", "Nagaur", "Sikar", "Barmer", "Jaisalmer",

    # --- CHHATTISGARH ("Rice Bowl of Central India") ---
    "Raipur", "Durg", "Bhilai", "Bilaspur", "Rajnandgaon",
    "Korba", "Raigarh", "Janjgir-Champa", "Bastar", "Jagdalpur"
]

villages = [
    # --- COMMON GENERIC NAMES (Found in almost every state) ---
    "Rampur", "Gopalpur", "Sultanpur", "Madhapur", "Chandipur",
    "Fatehpur", "Govindpur", "Anandpur", "Hariharpur", "Kishanpur",
    "Bishnupur", "Raghunathpur", "Jamalpur", "Dramapur",
    "Narayanpur", "Kamalpur", "Mohanpur", "Shantipur", "Lalpur",

    # --- ODISHA & EAST INDIA SPECIFIC (Your home region context) ---
    # Suffixes: -pur, -patna, -sahi, -jua
    "Balipatna", "Sakhigopal", "Pipili", "Jatni", "Khurdha",
    "Raghurajpur", "Hirapur", "Nuapatna", "Maniabandha",
    "Bhingarpur", "Balianta", "Gop", "Kakatpur", "Nimapara",
    "Banpur", "Chilika", "Brahmagiri", "Satyabadi", "Delang",
    "Begunia", "Bolagarh", "Tangi", "Khandapara", "Ranpur",
    "Banki", "Athagarh", "Tigiria", "Badamba", "Niali",

    # --- NORTH INDIA (Punjab, Haryana, UP) ---
    # Suffixes: -kalan (Big), -khurd (Small), -khera, -wala
    "Badal", "Lambi", "Chapparchiri", "Attari", "Wagah",
    "Rakhra", "Meham", "Manesar", "Sohna", "Palwal",
    "Chauri Chaura", "Kakori", "Dadri", "Jewar", "Hathras",
    "Shahpur", "Alipur", "Khanpur", "Jalalpur", "Sikandar",
    "Dhanas", "Sarangpur", "Khuda Ali Sher", # (Chandigarh villages)
    "Mullanpur", "Zirakpur", "Dera Bassi",

    # --- SOUTH INDIA (AP, Telangana, TN, Karnataka) ---
    # Suffixes: -pally, -oor, -ur, -varam
    "Pochampally", "Shamirpet", "Ghatkesar", "Medchal",
    "Keesara", "Ibrahimpatnam", "Maheshwaram", "Chevella",
    "Sriperumbudur", "Mamallapuram", "Thirukadaiyur",
    "Avadi", "Ambattur", "Tambaram", # (Peri-urban villages)
    "Devvanahalli", "Yelahanka", "Whitefield", "Sarjapur",
    "Marthandam", "Kovalam", "Kumarakom",
    "Gudivada", "Bhimavaram", "Tenali", "Mangalagiri",

    # --- WEST INDIA (Maharashtra, Gujarat) ---
    # Suffixes: -gaon, -wadi, -shed
    "Ralegan Siddhi", "Hiware Bazar", # (Famous model villages)
    "Koregaon", "Malegaon", "Shegaon", "Khamgaon",
    "Shirdi", "Shani Shingnapur",
    "Punsari", "Dharmaj", "Ajrakhpur", "Hodka", "Dhordo", # (Gujarat)
    "Bhosari", "Chakan", "Hinjewadi", "Wakad",

    # --- DISTINCTIVE / HISTORICAL NAMES ---
    "Plassey", "Champaran", "Bardoli", "Sevagram", "Sabarmati",
    "Shantiniketan", "Belur", "Halebidu", "Hampi",
    "Khajuraho", "Konark", "Sanchi", "Bodh Gaya",
    "Kushinagar", "Sarnath", "Vaishali", "Nalanda"
]

ages = [
    "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", 
    "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", 
    "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", 
    "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", 
    "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", 
    "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", 
    "78", "79", "80"
]


# RESTRUCTURED TEMPLATES (Grouped by Intent)
template_groups = {

    # --- 1. MULTI-ENTITY (High Density Co-Occurrence) ---
    # Solves Problem #7: Force the model to separate multiple entities in one sentence.
    "MULTI_ENTITY": [
        "I grow {crop_1} and {crop_2} on my {land_size} of {land_type} land.",
        "To improve my {crop} yield, I need a {resource} through the {scheme}.",
        "My {terrestrial_livestock} and {aquaculture_livestock} require a loan of {loan_amount}.",
        "{name} from {village} applied for {scheme_1} and {scheme_2}.",
        "We use {resource_1} and {resource_2} for farming {crop} in the {season}.",
        "My {land_size} produces {crop}, which earns me {income_amount} annually.",
        "I need {loan_amount} from {bank} to buy {resource} for my {land_type} farm.",
        "Does the {scheme} cover both {crop_1} and {crop_2} damages?",
        "With {income_amount} income, can I afford {resource} and {terrestrial_livestock}?",
        "{season} farming of {crop} requires {resource} and reliable irrigation.",
        "The {bank} sanctioned {loan_amount} for {resource} purchase.",
        "Can I get a subsidy for {resource} if I own {land_size}?",
        "My {terrestrial_livestock} shed needs repair before the {season} starts."
    ],

    # --- 2. NEGATIVE SAMPLES (No Entities) ---
    # Solves Problem #4: Teach the model when NOT to annotate anything.
    "NEGATIVE": [
        "The weather has been very unpredictable lately.",
        "Farming is hard work but it is honest work.",
        "I need to go to the market tomorrow morning.",
        "Please tell me the procedure to meet the officer.",
        "Is the office open on Saturdays?",
        "We are waiting for the monsoon to arrive.",
        "Water scarcity is a major issue in our village.",
        "Transportation costs have gone up significantly.",
        "The village meeting is scheduled for next week.",
        "My son is studying in the city college.",
        "Agriculture is the backbone of our economy.",
        "Can you help me fill out this form?",
        "The road to the farm is in bad condition.",
        "We need better electricity supply during the day.",
        "Who is the current sarpanch of this area?",
        "The bus service to the town is irregular.",
        "I will come back next week to check.",
        "Thank you for your help yesterday."
    ],

    # --- 3. DISTRACTORS (Trigger Words without Entities) ---
    # Solves Problem #5: Prevent the model from just memorizing words like 'bank' or 'seeds'.
    "DISTRACTOR": [
        "I went to the bank to update my passbook.",
        "This season has been very difficult for us.",
        "I need to buy some seeds from the local shop.",
        "The field needs to be plowed before the rains.",
        "Is there any government help available for us?",
        "The animals are grazing in the open field.",
        "I want to ask about the interest rates.",
        "My application was rejected due to missing documents.",
        "We usually harvest in the early morning.",
        "The cooperative society meeting is at noon.",
        "I have an account in the local branch.",
        "The soil is very dry this year.",
        "I need to withdraw money for household expenses.",
        "The fertilizer shop was closed today."
    ],

    # --- 4. INCOME CONTEXT (Specific Focus) ---
    # Solves Problem #10: Teach the distinction between INCOME_AMOUNT and INCOME_STATUS.
    "INCOME_CONTEXT": [
        "I belong to the {income_status} category and need financial help.",
        "As a {income_status} farmer, am I eligible for the {scheme}?",
        "My family is classified as {income_status} in the government records.",
        "Is there any special subsidy on {resource} for {income_status} households?",
        "We are a {income_status} family living in {village}.",
        "I have attached my {income_status} certificate with the application.",
        "Since I fall under the {income_status} group, I cannot pay high interest.",
        "Does the bank offer lower interest rates for {income_status} applicants?",
        "My application was rejected because I am not considered {income_status}.",
        "With a family of {family_size}, we are struggling as a {income_status} household.",
        "The {scheme} is exclusively for {income_status} farmers.",
        "Please update my status from APML to {income_status} in the passbook.",
        "Only {income_status} beneficiaries can apply for this {req_type}.",
        "I possess a valid card proving my {income_status} status.",
        "Government benefits for {income_status} families have not reached me yet.",
        "My total annual earnings from agriculture are {income_amount}.",
        "Is a family income of {income_amount} eligible for this waiver?",
        "I declared {income_amount} on my income certificate.",
        "We struggle because our household income is only {income_amount}."
    ],

    # --- 5. STANDARD (All Original General Templates) ---
    # Solves Problem #6: General coverage of single entities.
    "STANDARD": [
        # Complex Syntax
        "If the rain continues, my {crop} harvest will be delayed.",
        "Although I own {land_size}, the soil quality is poor.",
        "Since the market price for {crop} dropped, I am switching to {terrestrial_livestock}.",
        "Unless I receive the {scheme} benefit, I cannot afford new seeds.",
        "Because of the drought, {crop} cultivation on my {land_size} has stopped.",
        "While {name} manages the accounts, I handle the {terrestrial_livestock}.",
        "Whenever the {season} arrives, we prepare the {land_size} for sowing.",
        "Given that my income is {income_amount}, I qualify for the {category} quota.",
        "Should the bank approve my loan of {loan_amount}, I will buy a {resource}.",
        "Before planting {crop}, we must test the soil.",

        # Passive Voice
        "{crop} is what we primarily cultivate in this region.",
        "The {scheme} was applied for by my father last month.",
        "A loan of {loan_amount} is being processed by the {bank}.",
        "{land_size} of land is owned by my family in {village}.",
        "The {resource} was purchased using the subsidy from {scheme}.",
        "{terrestrial_livestock} rearing is considered profitable by many here.",
        "By the end of {season}, the {crop} will be ready for harvest.",
        "Into the {bank} account, the {income_amount} was deposited.",
        "Under the {category} category, my application was accepted.",
        "From {village}, {name} has requested a meeting.",

        # Financial Specific
        "The {bank} has sanctioned a credit limit of {loan_amount}.",
        "I am repaying the {loan_amount} borrowed for my tractor.",
        "I have a pending debt of {loan_amount} with the cooperative.",
        "Can {bank} provide a top-up on my existing {loan_amount}?",
        "The installments for the {loan_amount} loan are becoming a burden.",

        # Demographic
        "As a {gender} farmer, I face unique challenges in {village}.",
        "My family belongs to the {caste} community in {district}.",
        "I am {name}, a {age}-year-old resident of {state}.",
        "We are a {family_size} living in a small house.",
        "Being from the {category} category, do I get extra benefits?",
        "{name}, {relation}, is the legal heir to this property.",
        "Our {religion} customs are strictly followed in the village.",
        "I am the head of a {family_size} in {village}.",
        "Is there a special quota for {caste} farmers?",
        "My identity as a {category} member is stated in the card.",

        # Resource Request
        "I am looking to purchase a {resource} for my farm.",
        "Is there a subsidy available for {resource}?",
        "My request is regarding the {scheme} application.",
        "I want to register for {req_type} under the new guidelines.",
        "Please process my {req_type} as soon as possible.",
        "How do I apply for {scheme} online?",
        "The {resource} I bought last year is not working.",
        "Can you check the status of my {req_type}?",
        "I require a {resource} to manage the harvest efficiently.",

        # Livestock
        "I am planning to start {aquaculture_livestock} farming.",
        "My pond is stocked with {aquaculture_livestock} and local fish.",
        "Feeding {terrestrial_livestock} costs me {income_amount} per year.",
        "The {terrestrial_livestock} need vaccination urgently.",
        "Is {aquaculture_livestock} covered under the insurance scheme?",
        "I sell milk from my {terrestrial_livestock} to the dairy.",
        "We are expanding our {aquaculture_livestock} business.",
        "The {terrestrial_livestock} shed was damaged in the storm.",
        "Prices for {aquaculture_livestock} are high in the local market.",
        "I need a loan to buy more {terrestrial_livestock}."
    ]
}


# --- MAPPING KEYS TO ENTITY LABELS ---
ENTITY_MAP = {
    "crop": "CROP", "crop_1": "CROP", "crop_2": "CROP",
    "land_size": "LAND_SIZE",
    "land_type": "LAND_TYPE",
    "season": "SEASON",
    "terrestrial_livestock": "LIVESTOCK", "aquaculture_livestock": "LIVESTOCK",
    "loan_amount": "LOAN_AMOUNT",
    "income_amount": "INCOME_AMOUNT",
    "income_status": "INCOME_STATUS",
    "debt_status": "DEBT_STATUS",
    "bank": "BANK_NAME",
    "name": "FARMER_NAME",
    "age": "AGE",
    "gender": "GENDER",
    "relation": "RELATION",
    "category": "CATEGORY", "caste": "CASTE", "religion": "RELIGION",
    "family_size": "FAMILY_SIZE",
    "scheme": "SCHEME", "scheme_1": "SCHEME", "scheme_2": "SCHEME",
    "req_type": "REQ_TYPE",
    "resource": "RESOURCE", "resource_1": "RESOURCE", "resource_2": "RESOURCE",
    "state": "STATE", "district": "DISTRICT", "village": "VILLAGE"
}


# ==========================================
# THE GENERATOR CLASS
# ==========================================

class NERDatasetGenerator:
    def __init__(self, target_rows=20000):
        self.target_rows = target_rows
        self.generated_rows = 0
        
        # TRACKERS
        self.entity_counts = Counter()
        self.label_counts = Counter()
        self.template_group_counts = Counter()
        self.context_counts = Counter() 
        
        # CONFIG: Ratios & Caps
        self.ratios = {
            "NEGATIVE": 0.15,      # 15% Negative 
            "DISTRACTOR": 0.15,    # 15% Distractor
            "MULTI_ENTITY": 0.20,  # 20% Complex
            "INCOME_CONTEXT": 0.10,# 10% Income specific
            "STANDARD": 0.40       # 40% Standard
        }
        
        # Calculate exact target numbers for groups
        self.group_targets = {k: int(v * target_rows) for k, v in self.ratios.items()}
        
        # Pre-analyze templates to know which labels they provide
        self.template_label_map = self._map_templates_to_labels()

    def _map_templates_to_labels(self):
        """Helper to see which labels a template produces."""
        mapping = []
        for group, templates in template_groups.items():
            for tmpl in templates:
                labels_in_tmpl = []
                for _, field, _, _ in string.Formatter().parse(tmpl):
                    if field and field in ENTITY_MAP:
                        labels_in_tmpl.append(ENTITY_MAP[field])
                mapping.append({"group": group, "tmpl": tmpl, "labels": set(labels_in_tmpl)})
        return mapping

    def smart_sample(self, key, source_list, max_cap_ratio=0.05):
        """
        Solves Problem #1: Frequency Overloading.
        Prevents any single entity (like 'Rice') from exceeding 5% of total generations for that type.
        """
        # 1. Filter out items that have hit the "Cap"
        # dynamic_cap = max(5, self.label_counts[ENTITY_MAP.get(key, "Unknown")] * max_cap_ratio)
        # Simplified: Just ensure flat distribution
        
        current_counts = self.entity_counts
        
        # Find the minimum usage count in this list
        min_freq = min([current_counts[x] for x in source_list]) if source_list else 0
        
        # Only pick items that are near the minimum frequency (The "Underdogs")
        candidates = [x for x in source_list if current_counts[x] <= min_freq + 2]
        
        # Fallback if candidates is empty (rare)
        if not candidates:
            candidates = source_list
            
        selection = random.choice(candidates)
        self.entity_counts[selection] += 1
        return selection

    def get_template_category(self):
        """
        Solves Problem #3 & #4: Enforces strict ratios for Negative/Distractor samples.
        """
        # Find groups that haven't met their target yet
        available_groups = [g for g, t in self.group_targets.items() if self.template_group_counts[g] < t]
        
        # If all targets met (end of generation), pick any
        if not available_groups:
            return "STANDARD"
            
        return random.choice(available_groups)

    def generate_relation(self):
        """
        Solves Problem #5: Relation Entity Span Integrity.
        Ensures gender logic is consistent and returns ONE string.
        """
        is_male = random.choice([True, False])
        if is_male:
            # Male subject -> "Son of" + (Male Name) OR "Husband of" + (Female Name)
            prefix = random.choice(male_relations)
            relative = random.choice(female_names) if "Husband" in prefix else random.choice(male_names)
        else:
            # Female subject -> "Daughter of" + (Male Name) OR "Wife of" + (Male Name)
            prefix = random.choice(female_relations)
            relative = random.choice(male_names) # Usually relative is father/husband (Male)
            
        # Bind into one string that will be tagged as ONE entity
        full_relation_str = f"{prefix} {relative}"
        return full_relation_str

    def augment_context(self, text):
        """
        Solves Problem #6: Contextual Coverage Tracking.
        Ensures diverse sentence starts/ends.
        """
        prefixes = ["Actually, ", "Basically, ", "Sir, ", "To be honest, ", "Hello, ", ""]
        suffixes = [".", " right now.", " immediately.", " please.", "??", ""]
        
        # Smart selection for context
        p = self.smart_sample("context_prefix", prefixes)
        s = self.smart_sample("context_suffix", suffixes)
        
        return f"{p}{text}{s}"

    def run(self):
        csv_data = []
        json_data = []

        while self.generated_rows < self.target_rows:
            
            # Select Template Group based on Quotas
            category = self.get_template_category()
            self.template_group_counts[category] += 1
            
            # Select specific template
            template = random.choice(template_groups[category])
            
            # Prepare Data Dictionary
            data = {
                "crop": self.smart_sample("crop", crops),
                "crop_1": self.smart_sample("crop", crops),
                "crop_2": self.smart_sample("crop", crops),
                "land_size": self.smart_sample("land_size", land_sizes),
                "land_type": self.smart_sample("land_type", land_types),
                "season": self.smart_sample("season", seasons),
                "terrestrial_livestock": self.smart_sample("terrestrial_livestock", terrestrial_livestock),
                "aquaculture_livestock": self.smart_sample("aquaculture_livestock", aquaculture_livestock),
                "loan_amount": self.smart_sample("loan_amount", loan_amounts),
                "income_amount": self.smart_sample("income_amount", income_amounts),
                "income_status": self.smart_sample("income_status", income_statuses),
                "debt_status": self.smart_sample("debt_status", debt_status),
                "bank": self.smart_sample("bank", banks),
                "scheme": self.smart_sample("scheme", schemes),
                "scheme_1": self.smart_sample("scheme", schemes),
                "scheme_2": self.smart_sample("scheme", schemes),
                "req_type": self.smart_sample("req_type", req_types),
                "resource": self.smart_sample("resource", resources),
                "resource_1": self.smart_sample("resource", resources),
                "resource_2": self.smart_sample("resource", resources),
                "state": self.smart_sample("state", states),
                "district": self.smart_sample("district", districts),
                "village": self.smart_sample("village", villages),
                "caste": self.smart_sample("caste", castes),
                "category": self.smart_sample("category", categories),
                "religion": self.smart_sample("religion", religions),
                "family_size": self.smart_sample("family_size", family_sizes), 
                "name": random.choice(male_names + female_names),
                "relation": self.generate_relation(), 
                "age": random.choice(ages),
                "gender": random.choice(male_gender_terms + female_gender_terms) 
            }
            
            # Fill Template
            try:
                # Basic fill to get text
                base_text = template.format(**data)
                
                # Augment Context
                final_text = self.augment_context(base_text)
                
                # Calculate Indices
                entities = []
                
                if category not in ["NEGATIVE", "DISTRACTOR"]:
                    for key, val in data.items():
                        # We only tag it if the placeholder {key} was actually in the template
                        # OR if the value appears naturally (be careful with this, strict placeholder check is safer)
                        if f"{{{key}}}" in template: 
                            label = ENTITY_MAP.get(key)
                            if not label: continue
                                
                            # Search for value in final_text
                            start = final_text.find(val)
                            if start != -1:
                                end = start + len(val)
                                entities.append([start, end, label])
                                self.label_counts[label] += 1

                csv_data.append(final_text)
                json_data.append([final_text, {"entities": entities}])
                self.generated_rows += 1
                
            except Exception as e:
                # Useful for debugging if a specific template fails
                print(f"Error in template: {template}") 
                print(f"Missing Key: {e}")
                continue

        return csv_data, json_data
    


# ==========================================
# EXECUTION
# ==========================================

generator = NERDatasetGenerator(target_rows=20000)
csv_out, json_out = generator.run()

# Save
df = pd.DataFrame(csv_out, columns=["text"])
df.to_csv("robust_agri_dataset.csv", index=False)

with open("robust_agri_annotations.json", "w", encoding="utf-8") as f:
    json.dump(json_out, f, indent=2)

print("Generation Complete.")
print("Template Distribution:", generator.template_group_counts)
print("Label Distribution:", generator.label_counts)