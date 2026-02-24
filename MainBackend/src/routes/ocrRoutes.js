const express = require('express');
const router = express.Router();
const upload = require('../config/multerConfig');
const ocrController = require('../controllers/ocrController');

// 'files' is the field name expected by both Multer and the FastAPI backend
// The number 10 is the maximum number of files allowed per request (adjust as needed)
// The route React is calling:
router.post('/process-documents', upload.single('files'), ocrController.processDocuments);

module.exports = router;    