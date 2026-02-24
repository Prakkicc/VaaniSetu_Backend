const sarvamService = require('../services/sarvamService');

const audioCache = new Map();

const handleSpeechToText = async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: "No audio file provided" });
        }

        const translatedText = await sarvamService.translateAudioToEnglish(
            req.file.buffer, 
            req.file.originalname
        );

        res.json({
            text: translatedText
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

const handleTextToSpeech = async (req, res) => {
    try {
        const { text, language } = req.body;

        if (!text) return res.status(400).json({ error: "Text is required" });

        const languageMap = {
            'hi-in': 'hi-IN',
            'en-in': 'en-IN',
            'bn-in': 'bn-IN',
            'kn-in': 'kn-IN',
            'ml-in': 'ml-IN',
            'mr-in': 'mr-IN',
            'od-in': 'od-IN', 
            'pa-in': 'pa-IN',
            'ta-in': 'ta-IN',
            'te-in': 'te-IN',
            'gu-in': 'gu-IN'
        };

        const targetLangCode = languageMap[language?.toLowerCase()];

        if (!targetLangCode) {
            return res.status(400).json({ error: "Unsupported or invalid language" });
        }

        // 2. Create a unique key for this exact text and language combo
        const cacheKey = `${text}-${targetLangCode}`;

        // 3. Check if we already have this audio saved in our cache
        if (audioCache.has(cacheKey)) {
            console.log(`Serving cached audio for: ${cacheKey}`);
            const cachedAudio = audioCache.get(cacheKey);
            
            res.set({
                'Content-Type': 'audio/wav',
                'Content-Length': cachedAudio.length,
            });
            return res.send(cachedAudio); // Return instantly!
        }

        console.log(`Generating new audio for: ${cacheKey}`);

        // Translate the English text to the Target Language
        let textToSpeak = text;
        if (targetLangCode !== 'en-IN') {
             textToSpeak = await sarvamService.translateText(text, targetLangCode);
        }

        // Convert the Translated Text to Speech
        const audioBuffer = await sarvamService.convertTextToSpeech(textToSpeak, targetLangCode);

        // 4. Save the newly generated audio to the cache for next time
        audioCache.set(cacheKey, audioBuffer);

        res.set({
            'Content-Type': 'audio/wav',
            'Content-Length': audioBuffer.length,   
        });

        res.send(audioBuffer);

    } catch (error) {
        console.log("TTS Route Error:", error);
        res.status(500).json({ error: error.message });
    }
};

module.exports = { handleSpeechToText, handleTextToSpeech };