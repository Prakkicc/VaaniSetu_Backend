const axios = require('axios');

const getEntitiesFromPython = async (text) => {
    try {
        const response = await axios.post('http://localhost:5000/ner/ask', {
            text: text
        });

        return response.data;
    } catch (error) {
        console.error("Python NER Service Error:", error.message);
        throw new Error("Failed to process text with NER service");
    }
};

const getIntentFromPython = async (text) => {
    try {
        const response = await axios.post('http://localhost:8000/api/nlp/process-intent/', {
            text: text
        });

        return response.data.intent_data;
        
    } catch (error) {
        console.error("Python Intent Service Error:", error.message);
        throw new Error("Failed to process text with Intent service");
    }
};

module.exports = { 
    getEntitiesFromPython,
    getIntentFromPython
};