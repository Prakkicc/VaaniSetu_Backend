const express = require('express');
const router = express.Router();
const nlpController = require('../controllers/nlpController');

router.post('/entity_recognition', nlpController.handleEntityRecognition);
router.post('/intent_recognition', nlpController.handleIntentRecognition);

// --- NEW: Gemini Conversational Fallback Route ---
router.post('/fallback', nlpController.handleConversationalFallback);

module.exports = router;