const nlpService = require('../services/nlpService');

const handleEntityRecognition = async (req, res) => {
    try {
        const { text } = req.body;

        if (!text) {
            return res.status(400).json({ error: "Text is required" });
        }

        const result = await nlpService.getEntitiesFromPython(text);
        
        res.json(result);

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

const handleIntentRecognition = async (req, res) => {
    try {
        const { text } = req.body;

        if (!text) {
            return res.status(400).json({ error: "Text is required" });
        }

        const result = await nlpService.getIntentFromPython(text);
        
        res.json(result);

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// --- NEW: Gemini Conversational Fallback ---
const handleConversationalFallback = async (req, res) => {
    try {
        const { text, missingEntities } = req.body;

        if (!text) {
            return res.status(400).json({ error: "Text is required" });
        }

        // Use the fast and cost-effective Flash model
        const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

        // The "Smart Glue" Prompt
        const prompt = `
        You are a helpful, polite agricultural assistant chatbot in India.
        The user said: "${text}"
        
        We are currently trying to collect the following missing information from the user for a government scheme application: ${missingEntities && missingEntities.length > 0 ? missingEntities.join(', ') : 'None'}.
        
        Task:
        1. If the user's message is a question or a tangent, answer it briefly and accurately (in 1-2 short sentences).
        2. After answering, politely steer the conversation back and ask the user to provide the FIRST missing piece of information from the list above.
        3. Do not use bolding, asterisks, or complex formatting. Speak naturally as if you are talking out loud.
        `;

        const result = await model.generateContent(prompt);
        const responseText = result.response.text();

        res.json({ reply: responseText });

    } catch (error) {
        console.error("Gemini Fallback Error:", error);
        res.status(500).json({ error: "Failed to generate fallback response." });
    }
};

module.exports = { 
    handleEntityRecognition, 
    handleIntentRecognition, 
    handleConversationalFallback 
};