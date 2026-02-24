require('dotenv').config();
const express = require('express');
const cors = require('cors');
const sarvamRoutes = require('./src/routes/sarvamRoutes');
const nlpRoutes = require('./src/routes/nlpRoutes');
const modelRoutes = require('./src/routes/modelRoutes');
const ocrRoutes = require('./src/routes/ocrRoutes');
const schemeRoutes = require('./src/routes/schemeRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(cors());

app.use('/sarvam', sarvamRoutes);

app.use('/nlp', nlpRoutes);

app.use('/model', modelRoutes);

app.use('/ocr', ocrRoutes);

app.use('/schemes', schemeRoutes);

app.get('/api/ping', (req, res) => res.send('pong'));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});