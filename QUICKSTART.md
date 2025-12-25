# Anjoman Quick Start

Get up and running in 5 minutes.

## Prerequisites

**Choose one:**
- **Option A (Recommended)**: Docker and Docker Compose
- **Option B**: Python 3.10+ and Node.js 18+

Plus: At least one LLM API key (OpenAI, Anthropic, or Mistral)

## Option A: Docker Setup (Easiest) 🐳

### Setup (First Time Only)

```bash
# 1. Create environment file
cp .env.example .env

# 2. Edit .env and add your API key(s)
nano .env  # or use any text editor
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Running Anjoman

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

**That's it!** Open http://localhost:3000

See [DOCKER.md](DOCKER.md) for more Docker commands and options.

---

## Option B: Manual Setup (First Time Only)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file with your API key(s):

```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
echo "SESSIONS_DIR=../data/sessions" >> .env
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

## Running Anjoman

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Or use the startup scripts:**
```bash
./start-backend.sh   # Terminal 1
./start-frontend.sh  # Terminal 2
```

## Using Anjoman

1. Open http://localhost:3000 in your browser
2. Enter your issue/question
3. Set a budget (start with $1-2 for testing)
4. Click "Begin Deliberation"
5. Dana proposes agents - review them
6. Click "Next Iteration" to start the discussion
7. Each agent provides their perspective
8. Dana summarizes after each round
9. Provide guidance or let it continue
10. Click "Complete" when satisfied

## Example Issues to Try

**Technical Decision:**
> "Should we migrate our monolithic application to microservices? We have 100k LOC, 20 engineers, and tight deadlines."

**Product Strategy:**
> "We're a B2B SaaS with 1000 customers. Should we add a freemium tier or focus on enterprise?"

**Career Decision:**
> "I have two job offers: a startup with equity or an established company with higher salary. How should I decide?"

**Architecture Review:**
> "Review this API design: REST vs GraphQL for a mobile app with 1M users and complex data relationships."

## Tips

- Start with a small budget ($1-2) to understand costs
- More iterations = deeper analysis (3-5 is usually good)
- Provide guidance between iterations to steer discussion
- Different models bring different perspectives
- Check the budget display frequently

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.10+)
- Activate venv: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**"API key not found":**
- Verify `.env` file exists in `backend/` directory
- Check API key format (no quotes needed)
- Restart backend after adding keys

**Frontend can't connect:**
- Verify backend is running on http://localhost:8000
- Check browser console for errors
- Try visiting http://localhost:8000 directly

**"Budget exceeded":**
- This is working as designed!
- Increase budget for the session
- Or complete the current session and start a new one

## Getting API Keys

**OpenAI (GPT-4, GPT-3.5):**
- https://platform.openai.com/api-keys
- $5-10 free credit for new accounts

**Anthropic (Claude):**
- https://console.anthropic.com/
- Free tier available

**Mistral:**
- https://console.mistral.ai/
- Pay as you go

You only need ONE provider to start!

## Cost Estimates

Approximate costs per iteration (3-5 agents):

- **GPT-3.5 Heavy**: ~$0.01 - $0.03
- **GPT-4 + Claude Mix**: ~$0.05 - $0.15  
- **GPT-4 Heavy**: ~$0.10 - $0.30

A typical 3-iteration session: **$0.15 - $0.50**

Budget recommendations:
- Testing: $1-2
- Simple issues: $2-5
- Complex analysis: $5-10
- Deep deliberation: $10-20

## Docker Commands (If Using Docker)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Remove everything
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

## Next Steps

- Read [README.md](README.md) for project philosophy
- See [DOCKER.md](DOCKER.md) for detailed Docker usage
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Open issues on GitHub for questions

## Common Workflows

**Quick Decision:**
1. Create session with $2 budget
2. Run 2-3 iterations
3. Review Dana's summaries
4. Make decision

**Deep Analysis:**
1. Create session with $5-10 budget
2. Run 4-5 iterations
3. Provide guidance between rounds
4. Focus on specific aspects
5. Export session for reference

**Compare Options:**
1. Create separate sessions for each option
2. Same budget and agent setup
3. Compare summaries
4. Identify trade-offs

## Need Help?

- **Setup Issues**: See [SETUP.md](SETUP.md)
- **How It Works**: See [ARCHITECTURE.md](ARCHITECTURE.md)  
- **Bugs**: Open a GitHub issue
- **Questions**: Check existing issues or open a new one

---

**You're ready to go! Start with a simple question and see how Anjoman helps you think through it. 🚀**

