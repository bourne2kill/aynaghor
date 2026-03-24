
# 🌙 AYNAGH0R - Dark Fantasy AI Storyteller

A sophisticated AI-powered storytelling platform that weaves dark fantasy tales using advanced language models. Built with a modular architecture featuring the KH4NK1 AI agent for automated deployment and management.

## ✨ Features

- 🎭 **Dark Fantasy AI Storytelling** - Generate immersive gothic and fantasy narratives
- 🤖 **Dual AI Provider Support** - Google Gemini API or Local AI models
- 🎨 **Rich Interactive UI** - Beautiful Streamlit interface with dark theme
- 📚 **Story History** - Track and revisit your generated tales
- ⚙️ **Configurable Settings** - Customize story length, mood, and style
- 🔮 **Real-time Status** - Monitor AI engine health and connectivity
- 🏰 **Quick Prompts** - Pre-built story starters for instant inspiration

## 🚀 Quick Start

### Option 1: Direct Python Setup (Recommended)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and preferences
   ```

3. **Run the application**
   ```bash
   streamlit run ui/app.py --server.port=8501 --server.host=0.0.0.0
   ```

4. **Access the UI**
   - Open http://localhost:8501 in your browser

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   cd ../KH4NK1
   docker-compose -f docker-compose.aynaghor.yml up --build
   ```

2. **Access the services**
   - AYNAGH0R UI: http://localhost:8501
   - KH4NK1 Agent API: http://localhost:3000

## ⚙️ Configuration

### Environment Variables (.env file)

```bash
# AI Provider Configuration
USE_GEMINI=true                    # Use Gemini API (true) or Local AI (false)
GEMINI_API_KEY=your_key_here      # Get from https://makersuite.google.com/app/apikey
GEMINI_MODEL=gemini-1.5-flash     # Gemini model to use

# Local AI Configuration (if USE_GEMINI=false)
LLM_HOST=http://localhost:8080    # Local AI server URL
LLM_MODEL=llama2-7b-chat         # Local model name

# Application Settings
ENVIRONMENT=development
DEBUG=true
STREAMLIT_PORT=8501
STREAMLIT_HOST=0.0.0.0

# Story Generation Settings
DEFAULT_STORY_LENGTH=medium
DEFAULT_GENRE=dark_fantasy
DEFAULT_MOOD=mysterious
ENABLE_CONTENT_FILTER=true
MAX_STORY_LENGTH=2000
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file as `GEMINI_API_KEY`

## 🏗️ Architecture

```
aynaghor/
├── ui/app.py              # Streamlit interface
├── core/engine.py         # AI routing engine
├── modules/               # AI provider modules
│   ├── gemini.py          # Google Gemini integration
│   ├── localai.py         # Local AI integration
│   ├── voice.py           # Voice processing (future)
│   ├── image.py           # Image generation (future)
│   └── memory.py          # Conversation memory (future)
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
└── .env.example           # Environment configuration template
```

## 🎮 Usage

### Basic Story Generation

1. **Open the AYNAGH0R interface**
2. **Enter your story prompt** in the text area
3. **Customize settings** in the sidebar:
   - Story length (Short/Medium/Long)
   - Mood & atmosphere
   - Include dialogue and descriptions
4. **Click "Generate Story"** to create your tale
5. **View your story** in the formatted output area

### Quick Prompts

Use the sidebar quick prompts for instant inspiration:
- 🏰 **Haunted Castle** - Gothic horror setting
- 🌲 **Dark Forest** - Mysterious woodland adventure
- 🗡️ **Cursed Artifact** - Archaeological horror
- 👻 **Ghostly Encounter** - Supernatural mystery

### Story History

- All generated stories are saved in your session
- Access previous stories via the "Story History" panel
- Stories include timestamp and character count
- History persists during your browser session

## 🧪 Testing

### Manual Testing

1. **Test AI Integration**
   ```bash
   python -c "from core.engine import Engine; e = Engine(); print(e.route('Test story'))"
   ```

2. **Health Check**
   ```bash
   python -c "from core.engine import Engine; e = Engine(); print(e.health_check())"
   ```

3. **UI Testing**
   - Start the Streamlit app
   - Test story generation with various prompts
   - Verify sidebar controls work correctly
   - Check story history functionality

## 🔒 Security

### AI Content Filtering

- Built-in safety settings for Gemini API
- Content filtering for inappropriate requests
- Rate limiting to prevent abuse
- Secure API key management

## 🚨 Troubleshooting

### Common Issues

**"Gemini model not initialized"**
- Check your `GEMINI_API_KEY` in `.env`
- Verify the API key is valid
- Ensure you have internet connectivity

**"Rate limit exceeded"**
- Wait a minute before generating another story
- Check your Gemini API quota usage

**"Module import errors"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path configuration

**UI not loading**
- Check if Streamlit is running on the correct port
- Verify no other services are using port 8501

### Debug Mode

Enable debug logging by setting `DEBUG=true` in your `.env` file.

## 🛣️ Roadmap

### Phase 1: Core Functionality ✅
- [x] Gemini API integration
- [x] Streamlit UI
- [x] Story generation
- [x] Configuration management

### Phase 2: Enhanced Features 🚧
- [ ] Voice input/output integration
- [ ] Image generation for story scenes
- [ ] Conversation memory system
- [ ] Story export functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

*🌙 AYNAGH0R - Where darkness meets imagination 🌙*