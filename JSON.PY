import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// ==========================================
// MIDDLEWARE
// ==========================================
app.use(cors());
app.use(express.json()); // Parses incoming JSON requests
app.use(express.urlencoded({ extended: true })); // Parses URL-encoded data

// Request logging middleware (Custom)
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} request to ${req.url}`);
  next();
});

// ==========================================
// ROUTES
// ==========================================
// In-memory mock database
let items = [
  { id: 1, name: 'Item One', description: 'This is the first item' },
  { id: 2, name: 'Item Two', description: 'This is the second item' }
];

// Health Check Route
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date() });
});

// GET: Fetch all items
app.get('/api/items', (req, res) => {
  res.status(200).json({ success: true, count: items.length, data: items });
});

// GET: Fetch single item by ID
app.get('/api/items/:id', (req, res) => {
  const item = items.find(i => i.id === parseInt(req.params.id));
  if (!item) {
    return res.status(404).json({ success: false, message: 'Item not found' });
  }
  res.status(200).json({ success: true, data: item });
});

// POST: Create a new item
app.post('/api/items', (req, res) => {
  const { name, description } = req.body;
  
  if (!name) {
    return res.status(400).json({ success: false, message: 'Name field is required' });
  }

  const newItem = {
    id: items.length > 0 ? items[items.length - 1].id + 1 : 1,
    name,
    description: description || ''
  };

  items.push(newItem);
  res.status(201).json({ success: true, message: 'Item created successfully', data: newItem });
});

// PUT: Update an item
app.put('/api/items/:id', (req, res) => {
  const itemId = parseInt(req.params.id);
  const { name, description } = req.body;

  const itemIndex = items.findIndex(i => i.id === itemId);
  if (itemIndex === -1) {
    return res.status(404).json({ success: false, message: 'Item not found' });
  }

  items[itemIndex] = {
    ...items[itemIndex],
    name: name !== undefined ? name : items[itemIndex].name,
    description: description !== undefined ? description : items[itemIndex].description
  };

  res.status(200).json({ success: true, message: 'Item updated successfully', data: items[itemIndex] });
});

// DELETE: Remove an item
app.delete('/api/items/:id', (req, res) => {
  const itemId = parseInt(req.params.id);
  const itemIndex = items.findIndex(i => i.id === itemId);

  if (itemIndex === -1) {
    return res.status(404).json({ success: false, message: 'Item not found' });
  }

  const deletedItem = items.splice(itemIndex, 1);
  res.status(200).json({ success: true, message: 'Item deleted successfully', data: deletedItem[0] });
});

// ==========================================
> **Error Handling Middleware:** Placed at the very end of the middleware stack to gracefully handle unhandled errors or invalid routes across the backend service.
// ==========================================

// 404 Not Found Handler
app.use((req, res, next) => {
  res.status(404).json({ success: false, message: 'Endpoint not found' });
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, message: 'Internal Server Error', error: err.message });
});

// ==========================================
// START SERVER
// ==========================================
app.listen(PORT, () => {
  console.log(`Server is running smoothly on port ${PORT} in ${process.env.NODE_ENV || 'development'} mode.`);
});
