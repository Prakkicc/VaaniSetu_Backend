const axios = require('axios');
const FormData = require('form-data');

const processDocuments = async (files) => {
    try {
        const formData = new FormData();

        // The FastAPI endpoint expects a list of files under the key "files"
        files.forEach(file => {
            formData.append('files', file.buffer, file.originalname);
        });

        // Replace 8002 with the actual port your FastAPI OCR server is running on
        const response = await axios.post('http://localhost:8002/process-documents', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        return response.data;
    } catch (error) {
        console.error("OCR Service Error:", error.response?.data || error.message);
        throw new Error("Failed to process documents with the OCR service");
    }
};

module.exports = { processDocuments };