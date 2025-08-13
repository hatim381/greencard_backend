const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const Product = require('../models/Product');

// Set up multer for image uploading
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

// @route   POST api/products
// @desc    Create a new product
// @access  Public
router.post('/', upload.single('image'), async (req, res) => {
  const image_url = req.file ? `/uploads/${req.file.filename}` : null;

  try {
    const product = new Product({
      name: req.body.name,
      price: req.body.price,
      image_url: image_url,
      // ...existing code...
    });

    await product.save();
    res.status(201).json(product);
  } catch (err) {
    res.status(500).json({ message: 'Server error' });
  }
});

// ...existing code...

module.exports = router;