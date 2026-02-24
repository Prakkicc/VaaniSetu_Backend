const axios = require('axios');
const FormData = require('form-data');

const processDocuments = async (req, res) => {
    try {
        // 1. Check if multer successfully caught the file from React
        const file = req.file || (req.files && req.files[0]);
        if (!file) {
            return res.status(400).json({ error: "No document file provided" });
        }

        // 2. Repackage the file to send to Python FastAPI
        const formData = new FormData();
        // The Python FastAPI expects the key to be "files" based on your api.py
        formData.append('files', file.buffer, file.originalname);

        // 3. Send to Python OCR Server (Change 8002 if your FastAPI runs on a different port)
        const response = await axios.post('http://localhost:8002/process-documents', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        // 4. Send the Python result back to React
        res.json(response.data);

    } catch (error) {
        console.error("OCR Proxy Error:", error?.response?.data || error.message);
        res.status(500).json({ error: "Failed to process document with OCR backend" });
    }
};

module.exports = { processDocuments /*, ... keep your other exports like extract */ };