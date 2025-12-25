#!/bin/bash

# Anjoman Environment Setup Script

echo "🔧 Anjoman Environment Setup"
echo "=============================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file."
        exit 0
    fi
fi

# Create .env file
echo "Creating .env file..."
cat > .env << 'EOF'
# LLM Provider API Keys
# Add at least one key to use Anjoman

# OpenAI (GPT-4, GPT-3.5)
OPENAI_API_KEY=

# Anthropic (Claude)
ANTHROPIC_API_KEY=

# Mistral
MISTRAL_API_KEY=

# Optional: Additional providers
COHERE_API_KEY=
TOGETHER_API_KEY=
EOF

echo "✅ .env file created!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your API key(s)"
echo "   nano .env"
echo ""
echo "2. Get API keys from:"
echo "   - OpenAI: https://platform.openai.com/api-keys"
echo "   - Anthropic: https://console.anthropic.com/"
echo "   - Mistral: https://console.mistral.ai/"
echo ""
echo "3. Run Anjoman:"
echo "   docker-compose up -d"
echo ""
echo "   OR (manual setup):"
echo "   ./start-backend.sh"
echo "   ./start-frontend.sh"
echo ""

# Offer to open editor
read -p "Do you want to edit .env now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo "No text editor found. Please edit .env manually."
    fi
fi

echo ""
echo "Happy deliberating! 🎯"

