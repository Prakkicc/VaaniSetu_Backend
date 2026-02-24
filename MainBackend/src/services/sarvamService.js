const axios = require("axios");
const FormData = require("form-data");

const translateAudioToEnglish = async (fileBuffer, fileName) => {
  try {
    const formData = new FormData();
    formData.append("file", fileBuffer, fileName);

    const response = await axios.post(
      "https://api.sarvam.ai/speech-to-text-translate",
      formData,
      {
        headers: {
          "api-subscription-key": process.env.SARVAM_API_KEY,
          ...formData.getHeaders(),
        },
      },
    );

    return response.data.transcript;
  } catch (error) {
    console.error("Sarvam API Error:", error.response?.data || error.message);
    throw new Error("Failed to process audio with Sarvam AI");
  }
};

const translateText = async (inputText, targetLangCode) => {
    try {
        const response = await axios.post(
            'https://api.sarvam.ai/translate',
            {
                input: inputText,
                source_language_code: "en-IN", 
                target_language_code: targetLangCode,
                model: "mayura:v1"
            },
            {
                headers: {
                    'api-subscription-key': process.env.SARVAM_API_KEY,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        return response.data.translated_text;
    } catch (error) {
        console.error("Sarvam Translation Error:", error.response?.data || error.message);
        throw new Error('Failed to translate text');
    }
};

const convertTextToSpeech = async (text, languageCode) => {
    try {
        const response = await axios.post(
            'https://api.sarvam.ai/text-to-speech',
            {
                inputs: [text],
                target_language_code: languageCode,
                speaker: "anushka" 
            },
            {
                headers: {
                    'api-subscription-key': process.env.SARVAM_API_KEY,
                    'Content-Type': 'application/json'
                }
            }
        );

        const base64Audio = response.data.audios[0];
        return Buffer.from(base64Audio, 'base64');

    } catch (error) {
        console.error("Sarvam TTS Error:", error.response?.data || error.message);
        throw new Error('Failed to convert text to speech');
    }
};

module.exports = { 
    translateAudioToEnglish, 
    translateText,      
    convertTextToSpeech 
};
