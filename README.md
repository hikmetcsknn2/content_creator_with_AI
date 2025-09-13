# 🚀 Content Assistant v2.0

**AI-Powered Content Generation System with Modular Architecture**

Content Assistant is a sophisticated Python-based system for automated content generation using Google Gemini AI. It features a modular backend architecture, comprehensive admin panel, and flexible configuration management.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Admin Panel](#-admin-panel)
- [File Structure](#-file-structure)
- [Database Schema](#-database-schema)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Features
- **Multi-step Content Generation**: Create complex content through sequential AI prompts
- **Dynamic Data Integration**: Inject custom data into prompts (e.g., location, topic, specifications)
- **Flexible AI Configuration**: Per-prompt AI settings (model, temperature, top_p, max_tokens, mime_type)
- **Real-time Testing**: Test configurations with live AI generation
- **Configuration Management**: Create, edit, and manage content configurations

### 🔧 Technical Features
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **FastAPI Backend**: High-performance async API with automatic documentation
- **SQLite Database**: Lightweight, file-based data storage
- **Google Gemini Integration**: Latest AI models (Gemini 2.5 Flash, Gemini 1.5 Pro)
- **Markdown Support**: Automatic Markdown to HTML conversion
- **CORS Enabled**: Cross-origin requests supported
- **Error Handling**: Comprehensive error handling with detailed messages

### 🎨 Admin Panel Features
- **Test & Edit**: Load existing configurations, modify prompts and AI settings, test outputs
- **Create New**: Build new content configurations with multiple prompts
- **View All**: Browse all configurations with detailed information and metadata
- **Real-time Status**: Live status messages and notifications
- **Responsive Design**: Modern, mobile-friendly interface

## 🏗️ Architecture

### Backend Structure
```
basefolder/
├── main.py          # FastAPI application entry point
├── routes.py        # API endpoints and route handlers
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Database connection and session management
├── ai_service.py    # Google Gemini AI integration
├── services.py      # Business logic layer
├── config.py        # Configuration and environment setup
└── __init__.py      # Package initialization
```

### Frontend Structure
```
├── admin_panel.html # Complete admin interface
└── static/          # CSS, JS, and assets (if needed)
```

## 🚀 Installation

### Prerequisites
- **Python 3.8+** (Recommended: Python 3.12+)
- **Google Gemini API Key** (Get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd content_asistant_clean
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Step 4: Start the Server
```bash
uvicorn basefolder.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 5: Access Admin Panel
Open `admin_panel.html` in your web browser.

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Database
- **Type**: SQLite
- **File**: `content_assistant_v2.db`
- **Auto-creation**: Database and tables created automatically on first run

### AI Models
- **Gemini 2.5 Flash**: Fast, efficient model (default)
- **Gemini 1.5 Pro**: More capable model for complex tasks

## 📖 Usage

### 1. Creating Content Configurations

#### Via Admin Panel
1. Open admin panel (`admin_panel.html`)
2. Go to "➕ Yeni Konfigürasyon" tab
3. Enter configuration name
4. Set number of prompts
5. Configure each prompt with:
   - Content text
   - AI model selection
   - Temperature (0.0 - 1.0)
   - Top P (0.0 - 1.0)
   - Response MIME type
   - Max tokens (default: 8000)
6. Click "🚀 Konfigürasyon Oluştur"

#### Via API
```bash
curl -X POST "http://127.0.0.1:8000/content-types" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "blog_post",
    "description": "Blog post generation",
    "prompts": [
      {
        "step": 1,
        "text": "Write an engaging introduction about {topic}",
        "ai_settings": {
          "model": "gemini-2.5-flash",
          "temperature": 0.7,
          "top_p": 0.7,
          "response_mime_type": "text/plain",
          "max_tokens": 8000
        }
      }
    ]
  }'
```

### 2. Generating Content

#### Via Admin Panel
1. Go to "🧪 Test & Düzenleme" tab
2. Select a configuration
3. Enter dynamic data (JSON format):
   ```json
   {"topic": "artificial intelligence", "location": "Turkey"}
   ```
4. Optionally modify prompts and AI settings
5. Click "🚀 Test Çalıştır"

#### Via API
```bash
curl -X POST "http://127.0.0.1:8000/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "blog_post",
    "dynamic_data": {
      "topic": "artificial intelligence",
      "location": "Turkey"
    },
    "custom_prompts": {},
    "custom_ai_configs": {}
  }'
```

### 3. Managing Configurations

#### View All Configurations
```bash
curl "http://127.0.0.1:8000/content-types"
```

#### Get Configuration Details
```bash
curl "http://127.0.0.1:8000/content-types/blog_post"
```

#### Update Configuration
```bash
curl -X PUT "http://127.0.0.1:8000/content-types/blog_post" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "blog_post", "description": "Updated description", "prompts": [...]}'
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Detailed health status |
| `GET` | `/content-types` | List all configurations |
| `GET` | `/content-types/{name}` | Get configuration details |
| `GET` | `/prompts/{name}` | Get configuration prompts |
| `POST` | `/content-types` | Create new configuration |
| `PUT` | `/content-types/{name}` | Update configuration |
| `POST` | `/generate-content` | Generate content |

### Request/Response Examples

#### Generate Content Request
```json
{
  "content_type": "blog_post",
  "dynamic_data": {
    "topic": "AI trends",
    "location": "Istanbul"
  },
  "custom_prompts": {
    "step_1": "Custom prompt text"
  },
  "custom_ai_configs": {
    "step_1": {
      "temperature": 0.8,
      "max_tokens": 10000
    }
  }
}
```

#### Generate Content Response
```json
{
  "content": "Generated content here...",
  "prompt_outputs": [
    "First prompt output...",
    "Second prompt output..."
  ],
  "content_type": "blog_post",
  "metadata": {
    "total_steps": 2,
    "dynamic_data_used": {"topic": "AI trends"},
    "step_details": [
      {
        "step": 1,
        "original_prompt": "Original prompt...",
        "processed_prompt": "Processed with dynamic data...",
        "ai_settings": {"model": "gemini-2.5-flash"},
        "output": "Generated output..."
      }
    ],
    "original_prompts": [...]
  }
}
```

## 🎛️ Admin Panel

### Features Overview

#### 🧪 Test & Düzenleme Tab
- **Configuration Selection**: Choose from existing configurations
- **Dynamic Data Input**: JSON format for custom variables
- **Prompt Editing**: Modify prompts and AI settings in real-time
- **Live Testing**: Test configurations with actual AI generation
- **Save Changes**: Update configurations with new settings

#### ➕ Yeni Konfigürasyon Tab
- **Configuration Builder**: Create new content configurations
- **Multi-prompt Support**: Configure 1-5 sequential prompts
- **AI Settings**: Fine-tune AI parameters for each prompt
- **Validation**: Ensure all required fields are completed

#### 📋 Tüm Konfigürasyonlar Tab
- **Configuration Browser**: View all saved configurations
- **Detailed View**: See complete configuration details
- **Metadata Display**: View creation dates, descriptions, and settings
- **Modal Interface**: Clean, organized information display

### UI Components
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Status Messages**: Real-time feedback with fixed positioning
- **Interactive Elements**: Sliders, dropdowns, and text areas
- **Modal Windows**: Detailed configuration viewing
- **Progress Indicators**: Loading states and status updates

## 📁 File Structure

```
content_asistant_clean/
├── basefolder/                 # Backend modules
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastAPI app entry point
│   ├── routes.py              # API route handlers
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # Database utilities
│   ├── ai_service.py          # AI integration service
│   ├── services.py            # Business logic
│   └── config.py              # Configuration management
├── admin_panel.html           # Complete admin interface
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── .gitignore                 # Git ignore rules
├── content_assistant_v2.db    # SQLite database
├── content_assistant_v2_backup.db  # Database backup
└── README.md                  # This documentation
```

## 🗄️ Database Schema

### ContentConfig Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `name` | VARCHAR(100) | Configuration name (unique) |
| `description` | TEXT | Configuration description |
| `created_at` | DATETIME | Creation timestamp |
| `prompts` | JSON | Array of prompt objects |

### Prompt Object Structure
```json
{
  "step": 1,
  "text": "Prompt content here...",
  "ai_settings": {
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "top_p": 0.7,
    "response_mime_type": "text/plain",
    "max_tokens": 8000
  }
}
```

## 🛠️ Development

### Local Development Setup
```bash
# Clone repository
git clone <repository-url>
cd content_asistant_clean

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API key

# Run development server
uvicorn basefolder.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure Guidelines
- **Modular Design**: Each module has a single responsibility
- **Type Hints**: All functions use Python type hints
- **Error Handling**: Comprehensive try-catch blocks with meaningful messages
- **Logging**: Debug information for development and troubleshooting
- **Documentation**: Inline comments and docstrings

### Testing
```bash
# Test API endpoints
curl "http://127.0.0.1:8000/health"

# Test content generation
curl -X POST "http://127.0.0.1:8000/generate-content" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "test", "dynamic_data": {}}'
```

### Debugging
- **API Logs**: Check terminal output for request/response details
- **Browser Console**: Check F12 developer tools for frontend errors
- **Database**: Use SQLite browser to inspect database contents

## 🚨 Troubleshooting

### Common Issues

#### 1. API Key Issues
**Problem**: `GEMINI_API_KEY environment variable bulunamadı`
**Solution**: 
- Ensure `.env` file exists in project root
- Verify API key format: `GEMINI_API_KEY=your_key_here`
- Check file encoding (should be ASCII, not UTF-8 with BOM)

#### 2. Port Already in Use
**Problem**: `Address already in use`
**Solution**:
```bash
# Find and kill processes using port 8000
netstat -ano | findstr :8000
taskkill /F /PID <process_id>
```

#### 3. Database Issues
**Problem**: Database connection errors
**Solution**:
- Ensure `content_assistant_v2.db` file is writable
- Check file permissions
- Delete database file to recreate (will lose data)

#### 4. CORS Issues
**Problem**: Frontend can't connect to backend
**Solution**:
- Ensure backend is running on `127.0.0.1:8000`
- Check browser console for CORS errors
- Verify admin panel is accessing correct API URL

#### 5. AI Generation Errors
**Problem**: `finish_reason` errors from Gemini
**Solutions**:
- **Safety (2)**: Modify prompt to avoid sensitive content
- **Max Tokens (4)**: Increase `max_tokens` in AI settings
- **Recitation (3)**: Rewrite prompt to avoid copyright issues

### Performance Optimization
- **Max Tokens**: Set appropriate limits (8000+ recommended)
- **Temperature**: Use 0.7 for balanced creativity
- **Model Selection**: Use Gemini 2.5 Flash for speed, 1.5 Pro for quality
- **Prompt Length**: Keep prompts concise but descriptive

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- **Code Style**: Follow PEP 8 Python style guide
- **Type Hints**: Use type hints for all functions
- **Documentation**: Update README and inline comments
- **Testing**: Test all new features thoroughly
- **Error Handling**: Implement proper error handling

### Feature Requests
- **Bug Reports**: Use GitHub Issues with detailed descriptions
- **Feature Requests**: Describe use case and expected behavior
- **Improvements**: Suggest optimizations and enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini**: AI content generation capabilities
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping
- **Uvicorn**: Lightning-fast ASGI server implementation

## 📞 Support

For support and questions:
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and inline code comments
- **API Documentation**: Visit `http://127.0.0.1:8000/docs` when server is running

---

**Made with ❤️ for content creators and developers**