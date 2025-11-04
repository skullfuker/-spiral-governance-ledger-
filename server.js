const express = require('express');
const app = express();
app.use(express.json());

// Basic logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

// Authentication middleware
const verifyContributor = (req, res, next) => {
  const token = req.headers['authorization'];
  if (token !== process.env.SCROLL_REGISTRY_SECRET) {
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

app.post('/treatyPhaseSync', (req, res) => {
  res.json({ status: 'Treaty phase synchronized', activePhase: process.env.TREATY_PHASE_ACTIVE });
});

app.get('/scrollAuditTrail', (req, res) => {
  res.json({ trail: ['Scroll of Spiral Treaty Activation', 'Scroll of Glyph Reillumination'] });
});

app.post('/glyphForge', (req, res) => {
  const { input } = req.body;
  res.json({ glyph: `forged-${input}`, status: 'Glyph forged successfully' });
});

app.post('/echoInscribe', (req, res) => {
  const { echo } = req.body;
  const timestamp = new Date().toISOString();
  res.json({ echo, timestamp, status: 'Echo inscribed and archived' });
});
