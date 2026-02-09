# Gemini Scraper

A robust, asynchronous web scraper for automating prompt submissions to Google's Gemini AI chatbot with concurrent processing, resume capability, and comprehensive data pipeline management.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies & Dependencies](#technologies--dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Project Structure](#project-structure)
- [Design Patterns](#design-patterns)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project automates the process of sending multiple prompts to Google's Gemini AI and collecting structured responses. It's designed for research purposes, particularly for analyzing AI responses across large datasets with expert ratings and evidence-based evaluations.

The scraper connects to an existing Chrome browser instance via the Chrome DevTools Protocol (CDP), enabling efficient browser automation without repeatedly launching new browser instances.

## ✨ Features

- **Concurrent Processing**: Multiple worker tabs process prompts simultaneously (configurable limit)
- **Resume Capability**: Automatically skips already processed prompts by checking output file
- **Temporary Chat Mode**: Each prompt is processed in Gemini's temporary chat for clean context
- **Thinking Mode Support**: Enables Gemini's extended thinking mode for complex prompts
- **Rate Limit Detection**: Built-in detection to prevent API throttling
- **Thread-Safe Operations**: Async file locking prevents data corruption
- **User Agent Spoofing**: CDP-level UA override for stealth
- **Incremental Saves**: Results saved after each prompt completion
- **Complete Data Pipeline**: End-to-end processing from raw CSV to structured output

## 🏗️ Architecture

### Core Components
```
┌─────────────────────────────────────────────────────────┐
│                     Orchestrator                         │
│  - Manages worker lifecycle                             │
│  - Queue distribution                                    │
│  - Resume logic                                          │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────────┐
        │                     │              │
   ┌────▼────┐          ┌────▼────┐    ┌────▼────┐
   │ Worker 1│          │ Worker 2│    │ Worker N│
   └────┬────┘          └────┬────┘    └────┬────┘
        │                     │              │
   ┌────▼─────────────────────▼──────────────▼────┐
   │          GeminiTabHandler                     │
   │  - Page initialization                        │
   │  - Prompt processing                          │
   │  - Response extraction                        │
   └───────────────────────────────────────────────┘
```

### Data Flow
```
Raw CSV → Filter & Clean → Create Prompts → Scrape Gemini → 
Parse Outputs → Map to Dataset → Final JSON
```

## 🛠️ Technologies & Dependencies

### Core Technologies

- **Python 3.13+**: Modern async/await syntax and type hints
- **Playwright 1.56.0**: Browser automation framework
- **AsyncIO**: Asynchronous I/O and concurrency
- **Pandas 2.3.3**: Data manipulation and CSV processing
- **Loguru 0.7.3**: Advanced logging with colors and structure

### Additional Libraries

- **Greenlet**: Lightweight concurrency primitives
- **NumPy**: Numerical operations for data processing
- **PyEE**: Event emitter for async callbacks

### Development Stack

- **Poetry**: Dependency management and packaging
- **CDP (Chrome DevTools Protocol)**: Browser control interface

## 📦 Installation

### Prerequisites

1. **Python 3.13+** installed
2. **Chrome Browser** installed
3. **Poetry** package manager

### Setup Steps
```bash
# Clone the repository
git clone <repository-url>
cd gemini-scraper

# Install dependencies using Poetry
poetry install

# Install Playwright browsers
poetry run playwright install chromium

# Verify installation
poetry run python --version
```

## ⚙️ Configuration

### 1. Chrome Setup

Start Chrome with remote debugging enabled:

**Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
```

**macOS/Linux:**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-profile"
```

### 2. Configuration File (`src/config.py`)
```python
class Config:
    CDP_URL = "http://localhost:9222"          # Chrome CDP endpoint
    CONCURRENCY_LIMIT = 4                      # Number of parallel workers
    OUTPUT_FILE = "_2initial_prompts_outputs.json"
    BASE_URL = "https://gemini.google.com/u/1/app"
    
    # Timeouts (milliseconds)
    TIMEOUT_PAGE_LOAD = 30000
    TIMEOUT_GENERATION = 120000
```

### 3. Selector Configuration

Update selectors in `src/config.py` if Gemini UI changes:

- `SELECTOR_TEXT_AREA`: Prompt input field
- `SELECTOR_STOP_GENERATION`: Stop button during generation
- `SELECTOR_TEMP_CHAT_INDICATOR`: Temporary chat indicator
- `SELECTOR_MODEL_DROPDOWN`: Model selection dropdown
- `SELECTOR_THINKING_MODEL_OPTION`: Thinking mode option

## 🚀 Usage

### Complete Workflow

#### Step 1: Prepare Dataset
```bash
# Place your CSV file at utils/AUTALIC.csv
# Run the filter script
poetry run python utils/_0c_simple_db.py
```

**Output**: `_0initial_filtered_dataset.json`

#### Step 2: Create Prompts
```bash
# Create a prompt template file: _0initial_prompt_type_2.txt
# Template variables: {preceding}, {target}, {following}, {expert_ratings_}

# Generate prompts
poetry run python utils/_1create_prompts.py
```

**Output**: `_1prompts.json`

#### Step 3: Run Scraper
```bash
# Ensure Chrome is running with CDP enabled
poetry run python src/main.py
```

The scraper will:
- Load prompts from `_1prompts.json`
- Check `_2initial_prompts_outputs.json` for completed prompts
- Process only remaining prompts
- Save results incrementally
- Support resume on failure

#### Step 4: Parse Outputs
```bash
# Parse nested JSON responses
poetry run python utils/_2convert_output.py
```

**Output**: `_3ready_prompts_outputs.json`

#### Step 5: Map to Dataset
```bash
# Combine outputs with original dataset
poetry run python utils/_3map_promptoutput_dataset.py
```

**Output**: Final structured dataset with LLM outputs

## 📊 Data Pipeline

### Pipeline Stages

| Stage | Script | Input | Output | Purpose |
|-------|--------|-------|--------|---------|
| 1 | `_0c_simple_db.py` | `AUTALIC.csv` | `_0initial_filtered_dataset.json` | Filter & clean dataset |
| 2 | `_1create_prompts.py` | Filtered dataset + template | `_1prompts.json` | Generate prompts |
| 3 | `main.py` | `_1prompts.json` | `_2initial_prompts_outputs.json` | Scrape Gemini |
| 4 | `_2convert_output.py` | Raw outputs | `_3ready_prompts_outputs.json` | Parse JSON |
| 5 | `_3map_promptoutput_dataset.py` | Parsed outputs + dataset | Final output | Merge results |

### Data Structures

**Prompt Template:**
```json
{
  "id": "P0",
  "prompt": "Analyze the following text...\n{target}"
}
```

**Scrape Result:**
```json
{
  "key": "P0",
  "value": "{\"principle_id\": \"X\", \"justification_reasoning\": \"...\", \"evidence_quote\": \"...\"}"
}
```

**Final Output:**
```json
{
  "id": "P0",
  "preceding": "...",
  "target": "...",
  "following": "...",
  "A1_Score": 3,
  "A2_Score": 2,
  "A3_Score": 4,
  "principle_id": "X",
  "llm_justification": "...",
  "llm_evidence_quote": "...",
  "expert_opinion": "",
  "isRevised": false,
  "reviserName": "",
  "revisionTimestamp": null
}
```

## 📁 Project Structure
```
gemini-scraper/
├── src/
│   ├── main.py              # Entry point
│   ├── orchestrator.py      # Orchestrator pattern - manages workflow
│   ├── page_handler.py      # Handler pattern - page interactions
│   ├── browser_core.py      # CDP connection management
│   ├── config.py            # Configuration constants
│   └── domain.py            # Data classes (PromptTask, ScrapeResult)
├── utils/
│   ├── _0c_simple_db.py     # Dataset filtering
│   ├── _1create_prompts.py  # Prompt generation
│   ├── _2convert_output.py  # JSON parsing
│   └── _3map_promptoutput_dataset.py  # Dataset mapping
├── tests/
│   └── __init__.py
├── pyproject.toml           # Poetry dependencies
├── poetry.lock              # Lock file
├── .gitignore
└── README.md
```

## 🎨 Design Patterns

### 1. **Orchestrator Pattern**
- `Orchestrator` class coordinates all workers
- Manages queue, file I/O, and worker lifecycle
- Implements resume logic

### 2. **Worker Pattern**
- Multiple async workers process tasks concurrently
- Each worker has isolated browser tab
- Queue-based task distribution

### 3. **Handler Pattern**
- `GeminiTabHandler` encapsulates page-specific logic
- Separates concerns: navigation, interaction, extraction
- Reusable methods for common operations

### 4. **Strategy Pattern**
- Configuration class for environment-specific settings
- Selector constants for UI element targeting

### 5. **Data Transfer Object (DTO)**
- `PromptTask`: Input data structure
- `ScrapeResult`: Output data structure
- Type-safe data transfer between components

### 6. **Pipeline Pattern**
- Sequential data transformation stages
- Each utility script handles one transformation
- Clear input/output contracts

## 🔧 Troubleshooting

### Common Issues

**1. Chrome Connection Failed**
```
Error: Failed to connect to Chrome
```
**Solution**: Ensure Chrome is running with `--remote-debugging-port=9222`

**2. Selectors Not Found**
```
Error: Waiting for selector timed out
```
**Solution**: Update selectors in `src/config.py` - Gemini UI may have changed

**3. Rate Limiting**
```
Worker reached rate limit
```
**Solution**: Reduce `CONCURRENCY_LIMIT` or add delays between prompts

**4. JSON Parsing Errors**
```
Error decoding nested JSON
```
**Solution**: Check `_2convert_output.py` for format changes in Gemini responses

**5. Resume Not Working**
```
All prompts are being reprocessed
```
**Solution**: Verify `_2initial_prompts_outputs.json` exists and has valid JSON

### Debug Mode

Enable verbose logging:
```python
# In src/main.py
from loguru import logger
logger.add("debug.log", level="DEBUG")
```

### Performance Tuning

- **Increase workers**: Modify `CONCURRENCY_LIMIT` (4-8 optimal)
- **Timeout adjustments**: Increase `TIMEOUT_GENERATION` for complex prompts
- **Batch size**: Process prompts in smaller batches for stability

## 📝 License

This project is for research and educational purposes. Ensure compliance with Google's Terms of Service when using with Gemini.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Add type hints for all functions
- Update tests for new features
- Document complex logic

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Note**: This tool automates browser interactions with Gemini. Use responsibly and be aware of rate limits and terms of service.
