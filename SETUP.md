# Anjoman Setup Guide

Complete setup instructions for running Anjoman locally.

## Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **API Keys** for LLM providers (OpenAI, Anthropic, etc.)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd anjoman
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure API Keys

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=...
```

**Important**: You need at least one LLM provider API key to use Anjoman.

#### Start the Backend Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

You can verify it's running by visiting `http://localhost:8000` in your browser.

### 3. Frontend Setup

In a new terminal:

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment (Optional)

If your backend is not running on `localhost:8000`, create a `.env.local` file:

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Start the Frontend Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### 4. Verify Setup

1. Open `http://localhost:3000` in your browser
2. Create a new session with a test issue
3. You should see Dana propose agents and the discussion begin

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

**"API key not found" errors:**
- Check that your `.env` file exists in the `backend` directory
- Verify your API keys are valid
- Make sure there are no quotes around the API keys in `.env`

**Port already in use:**
- Change the port: `uvicorn main:app --reload --port 8001`
- Update `NEXT_PUBLIC_API_URL` in frontend's `.env.local`

### Frontend Issues

**"Cannot connect to backend" errors:**
- Verify the backend is running on `http://localhost:8000`
- Check the `NEXT_PUBLIC_API_URL` in `.env.local`
- Look for CORS errors in browser console

**Dependencies installation fails:**
- Make sure you have Node.js 18 or higher: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then `npm install` again

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Add billing information if needed

### Anthropic (Claude)
1. Visit https://console.anthropic.com/
2. Go to API Keys section
3. Create a new key

### Mistral
1. Visit https://console.mistral.ai/
2. Create an account and get your API key

## Cost Management

- Start with a small budget ($1-2) to test
- Monitor costs in the UI during sessions
- OpenAI and Anthropic provide free trial credits for new accounts

## Next Steps

Once everything is running:
1. Read the [README.md](README.md) to understand Anjoman's philosophy
2. Try a simple issue first
3. Experiment with different agent configurations
4. Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute

## Need Help?

- Check existing [GitHub Issues](issues)
- Open a new issue with your setup details
- Join our community discussions

