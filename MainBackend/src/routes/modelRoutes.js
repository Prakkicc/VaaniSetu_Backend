const express = require('express');
const router = express.Router();
const modelController = require('../controllers/modelController');

// Defines the POST /predict endpoint
router.post('/predict', modelController.handlePredict);

module.exports = router;