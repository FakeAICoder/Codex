const express = require('express');
const fetch = require('node-fetch');
const app = express();
app.use(express.json());

app.post('/search', async (req, res) => {
  const { query } = req.body;
  const response = await fetch('http://localhost:8000/api/search/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  const data = await response.json();
  res.json(data);
});

app.post('/generate', async (req, res) => {
  const response = await fetch('http://localhost:8000/api/generate/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req.body)
  });
  const data = await response.json();
  res.json(data);
});

app.listen(3000, () => console.log('Node frontend listening on port 3000')); 
