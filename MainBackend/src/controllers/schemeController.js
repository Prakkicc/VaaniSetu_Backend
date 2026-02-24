// Node.js Main Backend - schemeController.js
const axios = require('axios');

const getRecommendations = async (req, res) => {
    try {
        // Forward the exact payload from React to Django Scheme Backend (Port 8001)
        const djangoResponse = await axios.post('http://localhost:8001/api/recommend/', req.body);
        
        // Send the Django response back to React
        res.json(djangoResponse.data);
    } catch (error) {
        console.error("Scheme Proxy Error:", error?.response?.data || error.message);
        res.status(500).json({ error: "Failed to fetch recommendations from Scheme backend." });
    }
};

module.exports = { getRecommendations };