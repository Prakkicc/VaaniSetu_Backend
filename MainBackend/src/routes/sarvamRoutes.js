const express = require('express');
const router = express.Router();
const upload = require('../config/multerConfig');
const sarvamController = require('../controllers/sarvamController');

router.post('/speech-to-text', upload.single('speech'), sarvamController.handleSpeechToText);

router.post('/text-to-speech', sarvamController.handleTextToSpeech);

module.exports = router;