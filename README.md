# Micro-SaaS Architect 🏗️

An AI-powered application that generates comprehensive technical blueprints for SaaS applications, complete with database schemas, API designs, frontend architectures, and deployment plans - all visualized in real-time with interactive Mermaid diagrams.

## Features

- **AI-Powered Blueprint Generation**: Transforms business ideas into detailed technical specifications
- **Multi-Provider LLM Support**: Choose from OpenAI GPT-4, DeepSeek, Groq, or Kimi for 60-97% cost savings
- **Multi-Agent Architecture**: Specialized agents for database, API, frontend, and deployment design
- **Real-Time Visualization**: Live Mermaid diagrams that update as the blueprint generates
- **Flexible Detail Levels**: Choose from high-level overview, detailed specification, or production-ready plans
- **Multi-Platform Deployment**: Generate deployment plans for AWS, GCP, Azure, DigitalOcean, and more
- **Export Options**: Download blueprints as Markdown or JSON
- **Cost Transparency**: See estimated costs for each LLM provider before generation

## Tech Stack

- **Backend**: Python 3.13+
- **AI Framework**: PydanticAI with multi-provider support
- **LLM Providers**: OpenAI, DeepSeek, Groq, Kimi (MoonshotAI)
- **Frontend**: Streamlit
- **Visualization**: Mermaid.js
- **Data Validation**: Pydantic v2

## Installation

### Prerequisites

- Python 3.9 or higher
- At least one LLM provider API key:
  - **DeepSeek** (Recommended - 97% cheaper): [Get API key](https://platform.deepseek.com/)
  - **OpenAI** (Premium quality): [Get API key](https://platform.openai.com/api-keys)
  - **Groq** (Fast & Free - has compatibility issues): [Get API key](https://console.groq.com/)
  - **Kimi/MoonshotAI** (60% cheaper): [Get API key](https://platform.moonshot.cn/)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/architect-blueprint.git
   cd architect-blueprint
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** from the example:
   ```bash
   cp .env.example .env
   ```

6. **Add your API key(s)** to the `.env` file:
   ```env
   # Choose your provider (recommended: deepseek for cost savings)
   DEFAULT_PROVIDER=deepseek

   # Add API key for your chosen provider
   DEEPSEEK_API_KEY=sk-your-deepseek-key-here
   # OPENAI_API_KEY=sk-your-openai-key-here
   # GROQ_API_KEY=gsk-your-groq-key-here
   # MOONSHOT_API_KEY=sk-your-kimi-key-here
   ```

## Usage

1. **Start the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

3. **Select your AI provider**:
   - Choose from DeepSeek (97% cheaper), OpenAI (premium), Groq (has issues), or Kimi (60% cheaper)
   - See real-time cost estimates for each provider
   - Select the specific model you want to use

4. **Enter your SaaS idea**:
   - Describe your business idea in detail in the text area
   - Select your desired detail level (High-level, Detailed, or Production-ready)
   - Choose your preferred deployment platform (AWS, GCP, Azure, etc.)

5. **Generate the blueprint**:
   - Click "Generate Blueprint"
   - Watch as the AI agents analyze your idea and generate each section
   - See diagrams update in real-time as components are designed

6. **Review and export**:
   - Browse through the generated database schema, API design, frontend architecture, and deployment plan
   - Download the blueprint as Markdown or JSON
   - Copy to clipboard for easy sharing

## Project Structure

```
Architect_Blueprint/
├── src/
│   ├── agents/           # PydanticAI agents
│   │   ├── architect_agent.py
│   │   ├── database_agent.py
│   │   ├── api_agent.py
│   │   ├── frontend_agent.py
│   │   ├── deployment_agent.py
│   │   └── prompts.py    # AI prompts
│   ├── models/           # Pydantic data models
│   ├── services/         # Business logic
│   ├── ui/               # Streamlit UI components
│   ├── config/           # Configuration
│   └── utils/            # Utility functions
├── app.py                # Main application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## LLM Provider Comparison

| Provider | Model | Cost (per 1M tokens) | Speed | Quality | Best For |
|----------|-------|---------------------|-------|---------|----------|
| **DeepSeek** | deepseek-chat | $0.27 input / $1.10 output | Fast | Excellent | **Cost savings (97% cheaper)** |
| **Kimi** | moonshot-v1-8k | $2.00 input / $6.00 output | Medium | Very Good | Cost savings (60% cheaper) |
| **OpenAI** | gpt-4-turbo | $10.00 input / $30.00 output | Medium | Excellent | Premium quality |
| **Groq** | llama-3.3-70b | Free | Very Fast | Good | **Has compatibility issues** |

**Cost Example**: Detailed blueprint (~8K tokens)
- DeepSeek: ~$0.01-0.02
- Kimi: ~$0.06-0.10
- OpenAI: ~$0.30-0.50

**Recommendation**: Use **DeepSeek** for 97% cost savings with excellent quality.

## Detail Levels

### High-Level Overview
- Core components and architecture
- **10+ database tables** covering core features
- 10-15 key API endpoints
- Basic frontend structure
- Simple deployment plan

### Detailed Specification (Recommended)
- Comprehensive component design
- **15-20 database tables** with full schemas and relationships
- 30+ API endpoints with request/response details
- Detailed frontend component hierarchy
- Complete deployment architecture with cost estimates

### Production-Ready
- Enterprise-grade specifications
- **25-30+ database tables** with partitioning and replication
- Extensive API documentation with rate limiting and caching
- Optimized frontend with performance considerations
- Production deployment with monitoring, security, and DR

## Supported Deployment Platforms

- **AWS** (Amazon Web Services)
- **GCP** (Google Cloud Platform)
- **Azure** (Microsoft Azure)
- **DigitalOcean**
- **Heroku**
- **Vercel**
- **Render**
- **Railway**
- **Fly.io**

## Configuration

### Environment Variables

```env
# LLM Provider Selection
DEFAULT_PROVIDER=deepseek  # Options: openai, deepseek, groq, kimi

# API Keys (add keys for providers you want to use)
OPENAI_API_KEY=sk-your-openai-key
DEEPSEEK_API_KEY=sk-your-deepseek-key
GROQ_API_KEY=gsk-your-groq-key
MOONSHOT_API_KEY=sk-your-kimi-key

# Model Selection (optional, uses defaults if not set)
OPENAI_MODEL=gpt-4-turbo
DEEPSEEK_MODEL=deepseek-chat
GROQ_MODEL=llama-3.3-70b-versatile
KIMI_MODEL=moonshot-v1-8k

# Agent Configuration
MAX_TOKENS=4096  # Increased for comprehensive outputs
TEMPERATURE=0.3
LOG_LEVEL=INFO
```

### Detail Level Configuration

Edit `src/config/detail_levels.py` to customize what's included at each detail level.

### Platform Configuration

Edit `src/config/deployment_configs.py` to add or modify deployment platform services.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
ruff check src/ tests/
```

## How It Works

1. **Requirements Analysis**: The Architect agent analyzes your business idea and extracts core features, user types, and key entities

2. **Database Design**: The Database agent creates a normalized schema with tables, fields, relationships, and indexes

3. **API Design**: The API agent designs RESTful endpoints based on the database schema and requirements

4. **Frontend Architecture**: The Frontend agent creates a component hierarchy and determines the best framework and state management approach

5. **Deployment Planning**: The Deployment agent designs infrastructure using platform-specific services with security and scalability in mind

6. **Diagram Generation**: Throughout the process, Mermaid diagrams are generated to visualize each layer of the architecture

## Limitations

- Requires at least one LLM provider API key (DeepSeek recommended for low cost)
- Generation time varies (typically 1-3 minutes for detailed blueprints)
- Quality depends on clarity of input - be specific and detailed about your SaaS idea
- Groq provider has known compatibility issues with PydanticAI (use DeepSeek instead)
- Diagrams may need manual adjustment for very complex applications
- Token limits may be reached for extremely complex systems (increase MAX_TOKENS if needed)

## Known Issues

- **Groq Provider**: Returns `service_tier='on_demand'` which causes validation errors in PydanticAI. Use DeepSeek or OpenAI instead.
- **Model Dropdown**: Ensure you select provider before generating blueprint for correct model options

## Future Enhancements

- [ ] Code generation from blueprints (generate actual project files)
- [ ] Blueprint refinement and iteration (modify existing blueprints)
- [ ] Comparison of multiple deployment options side-by-side
- [ ] User accounts and blueprint history/versioning
- [ ] Additional specialist agents (Testing, Security, Monitoring, Documentation)
- [ ] Support for Anthropic Claude and local models (Ollama, LM Studio)
- [ ] Export to other formats (PDF, HTML, Confluence)
- [ ] API endpoint for programmatic blueprint generation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For questions or issues:
1. Check existing GitHub issues
2. Create a new issue with a detailed description
3. Include your Python version, OS, and error messages

## Acknowledgments

- Built with [PydanticAI](https://github.com/pydantic/pydantic-ai)
- Powered by [OpenAI GPT-4](https://openai.com)
- UI with [Streamlit](https://streamlit.io)
- Diagrams with [Mermaid.js](https://mermaid.js.org)
