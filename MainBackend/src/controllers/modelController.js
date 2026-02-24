const modelService = require('../services/modelService');

const handlePredict = async (req, res) => {
    try {
        const profileData = req.body;

        // Validating the fields required by the UserProfileSerializer in Django
        const requiredFields = ['age', 'income', 'gender', 'caste', 'state'];
        const missingFields = requiredFields.filter(field => !profileData[field]);

        if (missingFields.length > 0) {
            return res.status(400).json({ 
                error: `Missing required fields: ${missingFields.join(', ')}` 
            });
        }

        const result = await modelService.recommendSchemes(profileData);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

module.exports = { handlePredict };