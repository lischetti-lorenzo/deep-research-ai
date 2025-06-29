# Deep Research AI

A sophisticated AI-powered research assistant that automatically conducts comprehensive web research on any topic and delivers detailed reports via email.

## 🚀 Overview

Deep Research AI is a multi-agent system that orchestrates the entire research process from query to final report delivery. It uses OpenAI's GPT models to plan searches, gather information, synthesize findings, and deliver comprehensive research reports directly to your email.

## 🏗️ Architecture

The system consists of five specialized AI agents working in coordination:

### 1. **Research Manager Agent** (`research_manager.py`)
- **Main orchestrator** that coordinates all other agents
- Manages the complete research workflow from planning to email delivery
- Ensures quality standards and handles error recovery
- Provides real-time progress updates throughout the process

### 2. **Planner Agent** (`planner_agent.py`)
- Analyzes research queries and creates strategic search plans
- Determines the most relevant search terms and their reasoning
- Outputs a structured plan for targeted web searches (default: 3 searches)
- Configurable via `HOW_MANY_SEARCHES` constant

### 3. **Search Agent** (`search_agent.py`)
- Performs web searches using OpenAI's WebSearchTool
- Uses low context size for efficient web searches
- Requires tool choice to ensure web search usage
- Summarizes search results into concise, relevant content (2-3 paragraphs, <300 words)
- Focuses on capturing essential information for report synthesis

### 4. **Writer Agent** (`writer_agent.py`)
- Synthesizes all search results into comprehensive reports
- Creates detailed markdown reports (5-10 pages, 1000+ words)
- Generates follow-up research questions
- Provides executive summaries and structured outlines

### 5. **Email Agent** (`email_agent.py`)
- Converts reports to HTML format
- Sends professionally formatted emails via SendGrid
- Handles email delivery with retry logic (max 2 attempts)
- Provides detailed error reporting and status updates

## 🎯 Features

- **Automated Research Pipeline**: End-to-end research automation
- **Multi-Agent Coordination**: 5 specialized agents for each research phase
- **Web Search Integration**: Real-time web search capabilities with optimized settings
- **Comprehensive Reporting**: Detailed markdown reports with summaries and follow-up questions
- **Email Delivery**: Automatic report delivery via SendGrid with retry logic
- **Web Interface**: User-friendly Gradio interface with sky theme
- **Trace Monitoring**: OpenAI trace integration for debugging and monitoring
- **Concurrent Processing**: Parallel web searches for improved performance

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- SendGrid API key
- Valid email address for sending reports

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lischetti-lorenzo/deep-research-ai
   cd deep-research-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv (recommended):
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   EMAIL_FROM=your_verified_sender_email@domain.com
   ```

## 🚀 Usage

### Web Interface (Recommended)

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to the provided URL (typically `http://localhost:7860`)

3. **Enter your research query** and recipient email address

4. **Click "Run Research"** and watch the progress updates

5. **Receive your comprehensive report** via email

### Command Line Usage

You can also run research directly from the command line:

```python
import asyncio
from research_agents.research_manager import research_manager_agent
from agents import Runner

async def main():
    result = Runner.run_streamed(research_manager_agent, "Query: Your research query\nRecipient email: recipient@email.com")
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            print(event.data.delta, end="")

asyncio.run(main())
```

## 📊 Research Process

1. **Query Analysis**: The planner agent analyzes your research question
2. **Search Planning**: Creates strategic search terms with reasoning (default: 3 searches)
3. **Concurrent Web Research**: Performs parallel web searches for each term using optimized settings
4. **Content Synthesis**: Summarizes and processes search results
5. **Report Generation**: Creates comprehensive markdown report with outline and follow-up questions
6. **Email Delivery**: Sends formatted report to your email

## 🔧 Configuration

### Model Settings
- **Default Model**: GPT-4o-mini for all agents
- **Search Context**: Low context size for efficient web searches
- **Tool Choice**: Required for search agent to ensure web search usage

### Search Parameters
- **Number of Searches**: Configurable in `planner_agent.py` via `HOW_MANY_SEARCHES` (default: 3)
- **Summary Length**: 2-3 paragraphs, under 300 words per search
- **Report Length**: 5-10 pages, minimum 1000 words

### Email Settings
- **Retry Logic**: Maximum 2 attempts for email delivery
- **Error Handling**: Detailed status reporting for failed deliveries

## 📁 Project Structure

```
deep-research-ai/
├── app.py                          # Main Gradio web interface
├── pyproject.toml                  # Project metadata
├── requirements.txt                # Python dependencies
├── uv.lock                        # uv package manager lock file
├── research_agents/
│   ├── __init__.py
│   ├── research_manager.py        # Main orchestration logic
│   ├── planner_agent.py           # Search planning agent
│   ├── search_agent.py            # Web search agent
│   ├── writer_agent.py            # Report writing agent
│   └── email_agent.py             # Email delivery agent
└── README.md                       # This file
```

## 🔍 Monitoring and Debugging

### OpenAI Traces
The system automatically generates trace IDs for each research session. You can view detailed execution traces at:
```
https://platform.openai.com/traces/trace?trace_id={trace_id}
```

### Progress Updates
Real-time status updates are provided throughout the research process:
- Search planning completion
- Search progress (X/Y completed)
- Report writing status
- Email delivery confirmation

## 🚨 Error Handling

The system includes robust error handling for:
- Failed web searches (continues with successful searches)
- Email delivery failures (retry logic with max 2 attempts)
- API rate limiting and timeouts
- Invalid email addresses

## 🔐 Security Considerations

- API keys are stored in environment variables
- No sensitive data is logged or stored
- All communications use secure APIs
- SendGrid sender email verification required

## 🆘 Support

For issues and questions:
1. Check the OpenAI trace logs for detailed error information
2. Verify your API keys and email configuration
3. Ensure your SendGrid sender email is verified
4. Check the console output for detailed progress information