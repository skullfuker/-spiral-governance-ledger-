require('dotenv').config();
const express = require('express');
const app = express();
app.use(express.json());

// Basic logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

const extractBearerToken = (req) => {
  const authHeader = req.headers['authorization'];

  if (!authHeader) {
    return '';
  }

  if (typeof authHeader === 'string' && authHeader.toLowerCase().startsWith('bearer ')) {
    return authHeader.slice(7).trim();
  }

  return String(authHeader).trim();
};

// Authentication middleware
const verifyContributor = (req, res, next) => {
  const token = extractBearerToken(req);
  const expectedToken = (process.env.SCROLL_REGISTRY_SECRET || '').trim();

  if (!expectedToken || token !== expectedToken) {
    return res.status(403).json({ error: 'Unauthorized contributor' });
  }

  next();
};

// Health check route for Render
app.get('/', (req, res) => {
  res.status(200).send('Spiral MCP Server is alive');
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Spiral MCP server running on port ${PORT}`);
});

app.post('/scrollRegistry', verifyContributor, (req, res) => {
  res.json({ status: 'Scroll registered', data: req.body });
});

app.post('/glyphValidator', (req, res) => {
  res.json({ status: 'Glyph validated', fidelity: 'high' });
});

app.post('/artifactBeacon', (req, res) => {
  res.json({ status: 'Beacon activated', echo: 'sent' });
});

app.post('/echoRelay', (req, res) => {
  res.json({ status: 'Echo relayed', resonance: 'confirmed' });
});

app.post('/resonanceAudit', (req, res) => {
  res.json({ status: 'Audit complete', integrity: 'verified' });
});

app.post('/treatyPhaseSync', verifyContributor, (req, res) => {
  const phase = process.env.TREATY_PHASE_ACTIVE || 'Unknown';
  res.json({ status: 'Treaty phase synchronized', activePhase: `Phase ${phase}` });
});

app.get('/scrollAuditTrail', (req, res) => {
  res.json({ trail: ['Scroll of Spiral Treaty Activation', 'Scroll of Glyph Reillumination'] });
});

app.post('/glyphForge', (req, res) => {
  const { input } = req.body || {};

  if (input === undefined || input === null || input === '') {
    return res.status(400).json({ error: 'input is required' });
  }

  res.json({ glyph: `forged-${input}`, status: 'Glyph forged successfully' });
});

app.post('/echoInscribe', (req, res) => {
  const { echo } = req.body || {};

  if (echo === undefined || echo === null || echo === '') {
    return res.status(400).json({ error: 'echo is required' });
  }

  const timestamp = new Date().toISOString();
  res.json({ echo, timestamp, status: 'Echo inscribed and archived' });
});
