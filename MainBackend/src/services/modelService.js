const axios = require('axios');

const recommendSchemes = async (profileData) => {
    try {
        // Sends the profile data to the Django API endpoint
        const response = await axios.post('http://localhost:8001/api/recommend/', profileData);
        return response.data;
    } catch (error) {
        console.error("Django Recommendation Service Error:", error.message);
        throw new Error("Failed to fetch recommendations from the model");
    }
};

module.exports = { recommendSchemes };