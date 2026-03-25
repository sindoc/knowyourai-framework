// #KnowYourAI Framework - Neo4j Cypher Import Script
// Source: https://github.com/sindoc/knowyourai-framework
// Description: Graph representation of AI-human relationship risk profiles

// ─────────────────────────────────────────────────────────────
// CONSTRAINTS & INDEXES
// ─────────────────────────────────────────────────────────────

CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT resource_url IF NOT EXISTS FOR (r:Resource) REQUIRE r.url IS UNIQUE;

// ─────────────────────────────────────────────────────────────
// PARENT CONCEPT
// ─────────────────────────────────────────────────────────────

MERGE (parent:Concept {id: 'ai-systems'})
SET parent.prefLabel   = 'AI Systems',
    parent.description = 'An overarching concept for all AI categories';

// ─────────────────────────────────────────────────────────────
// AI RELATIONSHIP CONCEPTS
// ─────────────────────────────────────────────────────────────

// AI as a Tool
MERGE (c1:Concept {id: 'ai-as-a-tool'})
SET c1.prefLabel      = 'AI as a Tool',
    c1.altLabel       = 'Human-Controlled AI',
    c1.description    = 'AI acts purely as a tool that is fully controlled by humans, enhancing human capabilities by automating routine tasks or providing analytical insights.',
    c1.examples       = 'AI-powered data analytics tools, Predictive text or grammar checkers, Image enhancement software',
    c1.humanRole      = 'Decision-maker, supervisor',
    c1.aiRole         = 'Supporting tool, augmenting human tasks',
    c1.notes          = 'Humans retain full control over the process, AI assists by offering speed and efficiency, AI operates under strict parameters set by humans',
    c1.riskLikelihood = 'Low',
    c1.riskImpact     = 'Low';

MERGE (rp1:RiskProfile {id: 'risk-ai-as-a-tool'})
SET rp1.likelihood = 'Low',
    rp1.impact     = 'Low';

MERGE (c1)-[:HAS_RISK_PROFILE]->(rp1);
MERGE (c1)-[:BROADER]->(parent);

// AI as an Assistant
MERGE (c2:Concept {id: 'ai-as-an-assistant'})
SET c2.prefLabel      = 'AI as an Assistant',
    c2.altLabel       = 'Collaborative AI',
    c2.description    = 'AI works alongside humans in a collaborative capacity, making recommendations and helping to solve problems. Humans retain the final decision-making authority.',
    c2.examples       = 'Virtual assistants (e.g., Siri, Alexa), AI in customer service (chatbots), Decision support systems',
    c2.humanRole      = 'Partner, guide, decision-maker',
    c2.aiRole         = 'Assistant, advisor, providing inputs and recommendations',
    c2.notes          = 'Collaborative interaction, AI learns from human feedback, Humans and AI co-create solutions',
    c2.riskLikelihood = 'Medium',
    c2.riskImpact     = 'Medium';

MERGE (rp2:RiskProfile {id: 'risk-ai-as-an-assistant'})
SET rp2.likelihood = 'Medium',
    rp2.impact     = 'Medium';

MERGE (c2)-[:HAS_RISK_PROFILE]->(rp2);
MERGE (c2)-[:BROADER]->(parent);

// AI as an Augmenter
MERGE (c3:Concept {id: 'ai-as-an-augmenter'})
SET c3.prefLabel      = 'AI as an Augmenter',
    c3.altLabel       = 'Human-AI Symbiosis',
    c3.description    = 'AI augments human capabilities, allowing humans to extend their cognitive, physical, or sensory abilities beyond natural limits.',
    c3.examples       = 'AI-enhanced creativity tools, Wearable AI devices, AI in personalized learning platforms',
    c3.humanRole      = 'Co-creator, augmented operator',
    c3.aiRole         = 'Cognitive or physical augmenter, enabler',
    c3.notes          = 'AI enhances human performance in real time, Seamless integration between human intuition and AI processing',
    c3.riskLikelihood = 'Medium',
    c3.riskImpact     = 'High';

MERGE (rp3:RiskProfile {id: 'risk-ai-as-an-augmenter'})
SET rp3.likelihood = 'Medium',
    rp3.impact     = 'High';

MERGE (c3)-[:HAS_RISK_PROFILE]->(rp3);
MERGE (c3)-[:BROADER]->(parent);

// AI as a Manager
MERGE (c4:Concept {id: 'ai-as-a-manager'})
SET c4.prefLabel      = 'AI as a Manager',
    c4.altLabel       = 'AI-Led Decision Making',
    c4.description    = 'AI takes on more responsibility by making decisions within defined areas, with limited human oversight.',
    c4.examples       = 'Autonomous vehicles, Algorithmic trading in finance, AI-driven supply chain management',
    c4.humanRole      = 'Supervisor, parameter setter',
    c4.aiRole         = 'Manager, decision-maker within constraints',
    c4.notes          = 'AI operates with a high degree of autonomy, Humans set parameters but rely on AI for execution',
    c4.riskLikelihood = 'High',
    c4.riskImpact     = 'High';

MERGE (rp4:RiskProfile {id: 'risk-ai-as-a-manager'})
SET rp4.likelihood = 'High',
    rp4.impact     = 'High';

MERGE (c4)-[:HAS_RISK_PROFILE]->(rp4);
MERGE (c4)-[:BROADER]->(parent);

// AI as an Autonomous Agent
MERGE (c5:Concept {id: 'ai-as-an-autonomous-agent'})
SET c5.prefLabel      = 'AI as an Autonomous Agent',
    c5.altLabel       = 'AI Independence',
    c5.description    = 'AI systems function with full autonomy, requiring little to no human intervention.',
    c5.examples       = 'AI in military drones, Fully autonomous research systems, Autonomous self-improving AI',
    c5.humanRole      = 'Observer, designer',
    c5.aiRole         = 'Fully autonomous entity, decision-maker',
    c5.notes          = 'AI operates independently and adapts to new situations, Minimal to no human intervention after deployment',
    c5.riskLikelihood = 'High',
    c5.riskImpact     = 'High';

MERGE (rp5:RiskProfile {id: 'risk-ai-as-an-autonomous-agent'})
SET rp5.likelihood = 'High',
    rp5.impact     = 'High';

MERGE (c5)-[:HAS_RISK_PROFILE]->(rp5);
MERGE (c5)-[:BROADER]->(parent);

// ─────────────────────────────────────────────────────────────
// RESOURCES — AI as a Tool
// ─────────────────────────────────────────────────────────────

MERGE (r1:Resource:Course {url: 'https://www.coursera.org/learn/ai-for-everyone'})
SET r1.title = 'AI for Everyone by Andrew Ng';
MERGE (c1)-[:HAS_RESOURCE]->(r1);

MERGE (r2:Resource:Course {url: 'https://learn.microsoft.com/en-us/training/paths/ml-for-beginners/'})
SET r2.title = 'Machine Learning for Beginners';
MERGE (c1)-[:HAS_RESOURCE]->(r2);

MERGE (r3:Resource:Book {url: 'https://www.amazon.com/dp/1250770742'})
SET r3.title = 'Artificial Intelligence: A Guide for Thinking Humans';
MERGE (c1)-[:HAS_RESOURCE]->(r3);

MERGE (r4:Resource:Tool {url: 'https://cloud.google.com/products/ai'})
SET r4.title = 'Google Cloud AI Tools';
MERGE (c1)-[:HAS_RESOURCE]->(r4);

MERGE (r5:Resource:Movie {url: 'https://www.imdb.com/title/tt0371746/'})
SET r5.title = 'Iron Man';
MERGE (c1)-[:HAS_RESOURCE]->(r5);

// ─────────────────────────────────────────────────────────────
// RESOURCES — AI as an Assistant
// ─────────────────────────────────────────────────────────────

MERGE (r6:Resource:Course {url: 'https://www.futurelearn.com/courses/collaborative-ai'})
SET r6.title = 'AI and Robotics: Collaborative Systems';
MERGE (c2)-[:HAS_RESOURCE]->(r6);

MERGE (r7:Resource:Book {url: 'https://www.amazon.com/dp/1633693864'})
SET r7.title = 'Human + Machine: Reimagining Work in the Age of AI';
MERGE (c2)-[:HAS_RESOURCE]->(r7);

MERGE (r8:Resource:Platform {url: 'https://www.ibm.com/cloud/watson-assistant'})
SET r8.title = 'IBM Watson Assistant';
MERGE (c2)-[:HAS_RESOURCE]->(r8);

MERGE (r9:Resource:Movie {url: 'https://www.imdb.com/title/tt1798709/'})
SET r9.title = 'Her';
MERGE (c2)-[:HAS_RESOURCE]->(r9);

// ─────────────────────────────────────────────────────────────
// RESOURCES — AI as an Augmenter
// ─────────────────────────────────────────────────────────────

MERGE (r10:Resource:Course {url: 'https://www.linkedin.com/learning/cognitive-technologies'})
SET r10.title = 'Cognitive Technologies: The Real Opportunities for Augmenting Human Abilities';
MERGE (c3)-[:HAS_RESOURCE]->(r10);

MERGE (r11:Resource:Book {url: 'https://www.amazon.com/dp/0316349135'})
SET r11.title = 'Superminds by Thomas W. Malone';
MERGE (c3)-[:HAS_RESOURCE]->(r11);

MERGE (r12:Resource:Tool {url: 'https://openai.com/gpt-4'})
SET r12.title = 'OpenAI\'s GPT-4';
MERGE (c3)-[:HAS_RESOURCE]->(r12);

MERGE (r13:Resource:Movie {url: 'https://www.imdb.com/title/tt0113568/'})
SET r13.title = 'Ghost in the Shell';
MERGE (c3)-[:HAS_RESOURCE]->(r13);

// ─────────────────────────────────────────────────────────────
// RESOURCES — AI as a Manager
// ─────────────────────────────────────────────────────────────

MERGE (r14:Resource:Course {url: 'https://www.edx.org/course/artificial-intelligence-for-decision-making'})
SET r14.title = 'Artificial Intelligence for Decision Making';
MERGE (c4)-[:HAS_RESOURCE]->(r14);

MERGE (r15:Resource:Book {url: 'https://www.amazon.com/dp/1633695670'})
SET r15.title = 'Prediction Machines';
MERGE (c4)-[:HAS_RESOURCE]->(r15);

MERGE (r16:Resource:Tool {url: 'https://www.tesla.com/autopilot'})
SET r16.title = 'Tesla Autopilot';
MERGE (c4)-[:HAS_RESOURCE]->(r16);

MERGE (r17:Resource:Movie {url: 'https://www.imdb.com/title/tt0343818/'})
SET r17.title = 'I, Robot';
MERGE (c4)-[:HAS_RESOURCE]->(r17);

// ─────────────────────────────────────────────────────────────
// RESOURCES — AI as an Autonomous Agent
// ─────────────────────────────────────────────────────────────

MERGE (r18:Resource:Course {url: 'https://www.udacity.com/course/robotics-and-autonomous-systems--nd209'})
SET r18.title = 'Robotics and Autonomous Systems';
MERGE (c5)-[:HAS_RESOURCE]->(r18);

MERGE (r19:Resource:Book {url: 'https://www.amazon.com/dp/1789954532'})
SET r19.title = 'Architects of Intelligence by Martin Ford';
MERGE (c5)-[:HAS_RESOURCE]->(r19);

MERGE (r20:Resource:Platform {url: 'https://www.bostondynamics.com/'})
SET r20.title = 'Boston Dynamics';
MERGE (c5)-[:HAS_RESOURCE]->(r20);

MERGE (r21:Resource:Movie {url: 'https://www.imdb.com/title/tt0470752/'})
SET r21.title = 'Ex Machina';
MERGE (c5)-[:HAS_RESOURCE]->(r21);

// ─────────────────────────────────────────────────────────────
// EXAMPLE QUERIES
// ─────────────────────────────────────────────────────────────
//
// List all AI relationship concepts with their risk profiles:
//   MATCH (c:Concept)-[:HAS_RISK_PROFILE]->(rp:RiskProfile)
//   WHERE c.id <> 'ai-systems'
//   RETURN c.prefLabel, rp.likelihood AS likelihood, rp.impact AS impact
//   ORDER BY c.prefLabel;
//
// Find all high-impact concepts and their resources:
//   MATCH (c:Concept)-[:HAS_RISK_PROFILE]->(rp:RiskProfile {impact: 'High'})
//   MATCH (c)-[:HAS_RESOURCE]->(r:Resource)
//   RETURN c.prefLabel, collect(r.title) AS resources;
//
// Show the full concept hierarchy:
//   MATCH path = (c:Concept)-[:BROADER*]->(parent:Concept)
//   RETURN path;
