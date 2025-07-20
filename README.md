# Kulturly POC

A Streamlit application for cultural trend analysis and customer insights.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key (for AI assistant features):
```bash
# Copy the example secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml and add your OpenAI API key
# Get your API key from: https://platform.openai.com/api-keys
```

3. Run the application:
```bash
streamlit run app.py
```

## Features

- Customer-specific cultural trend analysis
- Interactive data visualization
- Customizable geographic regions
- Narrative-driven insights
- AI-powered cultural strategy assistant (Puma customer)
