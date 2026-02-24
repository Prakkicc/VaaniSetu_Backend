// Node.js Main Backend - schemeRoutes.js
const express = require('express');
const router = express.Router();
const schemeController = require('../controllers/schemeController');

// The endpoint React will call
router.post('/recommend', schemeController.getRecommendations);

module.exports = router;