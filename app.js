const express = require('express');
const app = express();
const path = require('path');

// ...existing middleware and routes...

app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// ...existing error handling and server start logic...