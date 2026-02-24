const multer = require('multer');

// store file in memory as a Buffer
const storage = multer.memoryStorage();

const upload = multer({ storage: storage });

module.exports = upload;