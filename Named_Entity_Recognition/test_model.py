import spacy
import re

# Load the model
nlp = spacy.load("./Google_Colab")

def clean_entity(text, label):
    clean_text = text.replace(" and", "").replace(" but", "").strip().lower()

    # FAMILY CLEANING    
    family_keywords = ["member", "people", "person", "family", "dependent"]
    if label == "FAMILY_SIZE" or any(word in clean_text for word in family_keywords):
        digits = "".join([s for s in clean_text if s.isdigit()])
        if digits:
            return digits, "FAMILY_SIZE"

    # LOCATION CLEANING
    if label not in ["FARMER_NAME", "BANK_NAME", "SCHEME"]:
        
        known_villages = [
            # --- Odisha ---
                "balipatna", "sakhigopal", "pipili", "jatni", "khordha",
                "raghurajpur", "hirapur", "nuapatna", "maniabandha",
                "bhingarpur", "balianta", "gop", "kakatpur", "nimapara",
                "banpur", "chilika", "brahmagiri", "satyabadi", "delang",
                "begunia", "bolagarh", "tangi", "khandapara", "ranpur",
                "banki", "athagarh", "tigiria", "badamba", "niali",
                "kendupatna", "talapada", "chandaneswar", "jaleswar",
                "daspalla", "buguda", "asika",
            # --- Punjab ---
                "badal", "lambi", "attari", "wagah",
                "khera", "majra", "dera", "chak",
                "rajpura", "bahadurpur", "islamnagar",
            # --- Haryana / Western UP belt ---
                "kalan", "khurd", "patti", "gaon",
                "nagla", "sarai", "baragaon",
                "bada gaon", "chhota gaon",
            # --- Uttar Pradesh ---
                "rampur", "sultanpur", "fatehpur", "govindpur",
                "kishanpur", "raghunathpur", "ramnagar",
                "shahpur", "sheikhpura", "nawada",
                "kalyanpur", "inderpur", "laxmipur",
                "narayanpur", "sitarampur",
            # --- Bihar ---
                "gopalpur", "bishnupur", "hariharpur",
                "champaran", "ramchandrapur", "bhagwanpur",
                "mahadevpur", "hanumanpur", "shivpur",
            # --- West Bengal ---
                "plassey", "bishnupur", "krishnapur",
                "shyampur", "shyamnagar", "ramchandrapur",
                "haripur", "raghunathpur", "chak",
            # --- Maharashtra ---
                "ralegan siddhi", "hiware bazar", "shirdi",
                "sevagram", "manchar", "pimpri", "chinchwad",
                "rajgurunagar", "narayangaon", "alephata",
                "otur", "morgaon", "jeur", "vadgaon",
                "karjat", "khopoli", "alibag", "dahanu", "talasari",
            # --- Gujarat ---
                "bardoli", "sabarmati", "rajpur",
                "vadgaon", "kalyanpur",
            # --- Telangana ---
                "pochampally", "shamirpet",
                "ramapuram", "venkatapuram",
                "kothapalli", "kothapeta", "kothur",
            # --- Andhra Pradesh ---
                "krishnapuram", "narasapuram",
                "annavaram", "kandukur",
                "yerraguntla", "proddatur", "pulivendula",
            # --- Tamil Nadu ---
                "chidambaram", "sriperumbudur",
                "tiruvallur", "hosur", "denkanikottai",
            # --- Karnataka ---
                "yelahanka", "nelamangala",
                "dodballapur", "mandya", "srirangapatna",
            # --- Madhya Pradesh ---
                "rewa", "satna", "sidhi", "singrauli",
                "amarpatan", "maiher", "katni",
                "umaria", "shahdol", "anuppur",
                "burhar", "sehore", "ashta", "ichhawar",
            # --- Assam / Northeast ---
                "haflong", "diphu", "bokajan", "lumding",
                "karimganj", "hailakandi", "badarpur",
                "kokrajhar", "bilasipara", "rangapara", "doomdooma",
        ]
        known_villages.sort(key=len, reverse=True)
        for village in known_villages:
            if village in clean_text:
                return village.title(), "VILLAGE"
             
        known_districts = [
            # --- Odisha ---
            "khordha", "cuttack", "puri", "ganjam", "balasore", "bhadrak", "jajpur",
            "jagatsinghpur", "kendrapara", "nayagarh", "sundargarh", "sambalpur",
            "bargarh", "jharsuguda", "deogarh", "bolangir", "sonepur", "subarnapur",
            "boudh", "kandhamal", "kalahandi", "nuapada", "koraput", "rayagada",
            "nabarangpur", "malkangiri", "mayurbhanj", "keonjhar", "dhenkanal",
            "angul", "gajapati",
            # --- Punjab ---
            "ludhiana", "amritsar", "patiala", "jalandhar", "bathinda", "ferozepur",
            "moga", "barnala", "sangrur", "kapurthala", "hoshiarpur",
            "pathankot", "fazilka", "tarn taran",
            # --- Uttar Pradesh ---
            "lucknow", "varanasi", "gorakhpur", "prayagraj", "agra", "meerut",
            "kanpur nagar", "kanpur dehat", "ghaziabad", "noida", "gautam buddh nagar",
            "bareilly", "aligarh", "moradabad", "saharanpur", "muzaffarnagar",
            "shamli", "bijnor", "bulandshahr", "mathura", "firozabad",
            "ayodhya", "faizabad", "ambedkar nagar", "sultanpur", "jaunpur",
            "azamgarh", "ballia", "mau", "deoria", "kushinagar",
            "bahraich", "shravasti", "sitapur", "lakhimpur kheri", "hardoi",
            "unnao", "rae bareli", "pratapgarh", "chitrakoot", "banda",
            "mahoba", "jhansi", "lalitpur",
            # --- Bihar ---
            "patna", "gaya", "muzaffarpur", "darbhanga", "samastipur",
            "begusarai", "khagaria", "bhagalpur", "banka", "munger",
            "lakhisarai", "jamui", "nalanda", "nawada", "aurangabad",
            "arwal", "bhojpur", "buxar", "rohtas", "kaimur",
            "siwan", "saran", "gopalganj", "motihari", "east champaran",
            "west champaran", "sitamarhi", "sheohar", "madhepura",
            "saharsa", "supaul", "araria", "kishanganj", "katihar", "purnia",
            # --- Maharashtra ---
            "pune", "nashik", "nagpur", "aurangabad", "jalgaon",
            "dhule", "nandurbar", "ahmednagar", "solapur", "satara",
            "sangli", "kolhapur", "ratnagiri", "sindhudurg",
            "raigad", "thane", "palghar", "mumbai city", "mumbai suburban",
            "bhandara", "gondia", "chandrapur", "gadchiroli",
            "wardha", "yavatmal", "akola", "washim", "buldhana",
            "amravati", "parbhani", "hingoli", "nanded", "latur",
            "osmanabad", "beed", "jalna",
            # --- Gujarat ---
            "ahmedabad", "surat", "vadodara", "rajkot", "jamnagar",
            "junagadh", "porbandar", "bhavnagar", "amreli",
            "anand", "kheda", "mehsana", "patan", "banaskantha",
            "sabarkantha", "aravalli", "gandhinagar",
            "bharuch", "narmada", "valsad", "navsari",
            "dang", "kachchh", "morbi", "surendranagar",
            # --- Andhra Pradesh ---
            "guntur", "krishna", "visakhapatnam", "vizianagaram",
            "srikakulam", "east godavari", "west godavari",
            "prakasam", "nellore", "chittoor", "tirupati",
            "kadapa", "kurnool", "anantapur",
            # --- Telangana ---
            "warangal", "hanamkonda", "hyderabad", "rangareddy",
            "medchal", "sangareddy", "nizamabad", "kamareddy",
            "adilabad", "mancherial", "karimnagar", "peddapalli",
            "jagtial", "sircilla", "khammam", "bhadradri kothagudem",
            "mahabubnagar", "nagarkurnool", "wanaparthy",
            # --- Tamil Nadu ---
            "chennai", "coimbatore", "madurai", "salem", "tiruchirappalli",
            "thanjavur", "nagapattinam", "cuddalore", "villupuram",
            "viluppuram", "kallakurichi", "vellore", "ranipet",
            "tiruvannamalai", "erode", "namakkal", "karur",
            "dindigul", "theni", "virudhunagar", "thoothukudi",
            "tirunelveli", "tenkasi", "kanyakumari",
            # --- Karnataka ---
            "bengaluru urban", "bengaluru rural", "mysore", "mandya",
            "hassan", "chamarajanagar", "tumkur", "chitradurga",
            "davangere", "shivamogga", "udupi", "dakshina kannada",
            "uttara kannada", "belagavi", "bagalkot", "vijayapura",
            "bidar", "kalaburagi", "yadgir", "koppal", "raichur",
            "ballari",
            # --- Madhya Pradesh ---
            "indore", "bhopal", "jabalpur", "gwalior", "morena",
            "bhind", "datia", "shivpuri", "guna", "ashoknagar",
            "vidisha", "sagar", "damoh", "katni", "satna",
            "rewa", "sidhi", "singrauli", "shahdol", "anuppur",
            "mandsaur", "neemuch", "ratlam", "ujjain",
            "khandwa", "burhanpur", "khargone", "barwani",
            "betul", "chhindwara", "seoni", "balaghat",
            # --- Rajasthan ---
            "jaipur", "jodhpur", "kota", "udaipur", "ajmer",
            "alwar", "bharatpur", "dhaulpur", "karauli",
            "sawai madhopur", "tonk", "bhilwara",
            "chittorgarh", "pratapgarh", "banswara",
            "dungarpur", "sirohi", "pali", "jalore",
            "barmer", "jaisalmer", "bikaner", "churu",
            "jhunjhunu", "sikar", "nagaur", "hanumangarh",
            "sri ganganagar",
            # --- Chhattisgarh ---
            "raipur", "bilaspur", "durg", "rajnandgaon",
            "korba", "janjgir champa", "baloda bazar",
            "mahasamund", "dhamtari", "kanker",
            "bastar", "kondagaon", "narayanpur",
            "bijapur", "sukma"
            # --- Assam ---
            "baksa", "barpeta", "biswanath", "bongaigaon", "cachar",
            "charaideo", "chirang", "darrang", "dhemaji", "dhubri",
            "dibrugarh", "dima hasao", "goalpara", "golaghat",
            "hailakandi", "hojai", "jorhat", "kamrup",
            "kamrup metropolitan", "karbi anglong", "karimganj",
            "kokrajhar", "lakhimpur", "majuli", "morigaon",
            "nagaon", "nalbari", "sivasagar", "sonitpur",
            "south salmara mancachar", "tinsukia", "udalguri",
            "west karbi anglong",
            # --- Jharkhand ---
            "bokaro", "chatra", "deoghar", "dhanbad", "dumka",
            "east singhbhum", "garhwa", "giridih", "godda",
            "gumla", "hazaribagh", "jamtara", "khunti",
            "koderma", "latehar", "lohardaga", "pakur",
            "palamu", "ramgarh", "ranchi", "sahibganj",
            "seraikela kharsawan", "simdega", "west singhbhum",
            # --- Haryana ---
            "ambala", "bhiwani", "charkhi dadri", "faridabad",
            "fatehabad", "gurugram", "hisar", "jhajjar",
            "jind", "kaithal", "karnal", "kurukshetra",
            "mahendragarh", "nuh", "palwal", "panchkula",
            "panipat", "rewari", "rohtak", "sirsa",
            "sonipat", "yamunanagar",
            # --- Kerala ---
            "alappuzha", "ernakulam", "idukki", "kannur",
            "kasaragod", "kollam", "kottayam", "kozhikode",
            "malappuram", "palakkad", "pathanamthitta",
            "thiruvananthapuram", "thrissur", "wayanad",
            # --- West Bengal ---
            "alipurduar", "bankura", "birbhum",
            "cooch behar", "dakshin dinajpur",
            "darjeeling", "hooghly", "howrah",
            "jalpaiguri", "jhargram", "kalimpong",
            "kolkata", "malda", "murshidabad",
            "nadia", "north 24 parganas",
            "paschim bardhaman", "paschim medinipur",
            "purba bardhaman", "purba medinipur",
            "purulia", "south 24 parganas",
            "uttar dinajpur"
        ]
        known_districts.sort(key=len, reverse=True)
        for dist in known_districts:
            if dist in clean_text:
                return dist.title(), "DISTRICT" 

        known_states = [
            "andhra pradesh",
            "arunachal pradesh",
            "assam",
            "bihar",
            "chhattisgarh",
            "goa",
            "gujarat",
            "haryana",
            "himachal pradesh",
            "jharkhand",
            "karnataka",
            "kerala",
            "madhya pradesh",
            "maharashtra",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "odisha",
            "punjab",
            "rajasthan",
            "sikkim",
            "tamil nadu",
            "telangana",
            "tripura",
            "uttar pradesh",
            "uttarakhand",
            "west bengal"
        ]
        known_states.sort(key=len, reverse=True)
        for state in known_states:
            if state in clean_text: 
                return state.capitalize(), "STATE"
        
    # SEASONS CLEANING
    if label not in ["FARMER_NAME", "BANK_NAME", "SCHEME"]:
        known_seasons = [
            "summer",
            "monsoon",
            "autumn",
            "winter",
            "spring",
            "kharif",
            "rabi",
            "zaid",
            "vasant",
            "grishma",
            "varsha",
            "sharad",
            "hemant",
            "shishir"
        ]
        known_seasons.sort(key=len, reverse=True)
        for season in known_seasons:
            if season in clean_text: 
                return season.capitalize(), "SEASON"
    
    # CROPS CLEANING
    if label == "CROP":
        known_crops = [
            # cereals & millets
            "rice", "wheat", "maize", "jowar", "bajra", "ragi", "barley", "sorghum", "pearl millet", "finger millet", "paddy",
            # pulses (dal)
            "tur dal", "arhar", "moong dal", "urad dal", "masoor dal", "gram", "chana", "chickpea", "horse gram", "lentils",
            "peas", "kidney beans", "rajma",
            # oilseeds
            "groundnut", "mustard", "soybean", "sunflower", "sesame", "castor", "linseed", "safflower", "niger seed",
            # cash crops & fibers
            "sugarcane", "cotton", "jute", "tobacco", "rubber", "tea", "coffee", "arecanut", "coconut", "bamboo",
            # spices
            "chilli", "turmeric", "ginger", "garlic", "cumin", "coriander", "cardamom", "black pepper", "cloves",
            "fenugreek", "fennel",
            # vegetables
            "potato", "onion", "tomato", "brinjal", "eggplant", "okra", "bhindi", "cabbage", "cauliflower", "spinach",
            "carrot", "radish", "bottle gourd", "bitter gourd",
            # fruits
            "mango", "banana", "apple", "guava", "papaya", "pomegranate", "orange", "lemon", "grapes", "pineapple",
            "jackfruit", "watermelon"
        ]
        known_crops.sort(key=len, reverse=True)
        for crop in known_crops:
            if crop in clean_text: 
                return crop.capitalize(), "CROP"
    
    # AGE CLEANING
    if label == "AGE" or (label == "LAND_SIZE" and ("year" in clean_text or "old" in clean_text)):
        digits = "".join([s for s in clean_text if s.isdigit()])
        if digits:
            return digits, "AGE"
        
    # MONEY CLEANING
    if label in ["INCOME_AMOUNT", "LOAN_AMOUNT"]:

        multiplier = 1
        if "lakh" in clean_text:
            multiplier = 100000
        elif "k" in clean_text:
            multiplier = 1000
        elif "crore" in clean_text or "cr" in clean_text:
            multiplier = 10000000

        number_match = re.search(r"(\d+(\.\d+)?)", clean_text)
        
        if number_match:
            try:
                raw_val = float(number_match.group(1))
                final_val = int(raw_val * multiplier)
                return str(final_val), label
            except ValueError:
                pass 

        return clean_text, label
        
    # GENDER CLEANING
    if label == "GENDER":
        male_terms = [
            "male",
            "man",
            "boy",
            "gentleman",
            "gents",
            "purush",       
            "widower"
        ]
        female_terms = [
            "female",
            "woman",
            "girl",
            "lady",
            "ladies",
            "mahila",        
            "widow",
            "housewife",
            "homemaker"
        ]
        if any(x in clean_text for x in male_terms):
            return "Male", "GENDER"
        if any(x in clean_text for x in female_terms):
            return "Female", "GENDER"
    
    # LAND CLEANING
    if label not in ["FARMER_NAME", "BANK_NAME", "SCHEME"]:
        valid_units = [
            # standard / metric
            "acre",
            "hectare",
            "square meter",
            "sq ft",
            "sq yard",
            # north india
            "bigha",
            "biswa",
            "killa",
            "kanal",
            "marla",
            "ghumaon",
            "sarsahi",
            # east india
            "katha",
            "kattha",
            "decimal",
            "dhur",
            "chatak",
            "lecha",
            # west india
            "guntha",
            "gunta",
            "vigha",
            "are",
            "vasa",
            # south india
            "cent",
            "ground",
            "ankanam",
            "kuncham",
            # colloquial / mixed
            "gaj"
        ]
        
        found_unit = None
        for unit in valid_units:
            if unit in clean_text:
                found_unit = unit
                break
                
        if label == "LAND_SIZE" or found_unit:
            number_match = re.search(r"(\d+(\.\d+)?)", clean_text)
            if number_match and found_unit:
                return f"{number_match.group(1)} {found_unit}", "LAND_SIZE"
            elif number_match and label == "LAND_SIZE": 
                # Only return raw number if the model was ALREADY sure it's Land
                return clean_text, "LAND_SIZE"

    return clean_text.capitalize(), label

    

# Test Sentence
text = "My anual income is 5 lakh rupees"
doc = nlp(text)

print(f"--- Input: {text} ---")

for ent in doc.ents:
    final_text, final_label = clean_entity(ent.text, ent.label_)    
    print(f"  🔹 {final_text} \t-> {final_label}")