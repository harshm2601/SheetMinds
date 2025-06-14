# CSV/Sheet Analyzer with LLM

## Overview

**CSV/Sheet Analyzer with LLM** is a powerful, interactive web application that leverages Large Language Models (LLMs) to analyze, visualize, and extract insights from your CSV or Excel (XLSX) files. With a user-friendly Streamlit interface, you can upload your data, ask natural language questions, and receive instant Python code, visualizations, and AI-generated insights—all without writing a single line of code yourself!

---

## Features & Capabilities

- **Upload CSV/XLSX Files:** Supports both CSV and Excel files for maximum flexibility.
- **Natural Language Queries:** Ask questions or request visualizations in plain English.
- **Automatic Code Generation:** The app uses an LLM (Gemini 2.0 Flash) to generate Python code for your query, using pandas, numpy, matplotlib, and seaborn.
- **Safe Code Execution:** All generated code is executed in a sandboxed environment for security.
- **Instant Data Preview:** View the first 100 rows of your uploaded data.
- **Visualizations & Tables:** Get plots, tables, or text results based on your query.
- **AI-Powered Insights:** For visualizations, the LLM provides concise, context-aware insights about your data and the generated plot.

---

## How It Works

1. **Upload your data:** Choose a CSV or XLSX file to analyze.
2. **Preview:** Instantly see the first 100 rows of your data.
3. **Ask a question:** Type a question or request (e.g., "Show the distribution of sales by region" or "What is the correlation between age and income?").
4. **LLM generates code:** The app sends your query and data context to the LLM, which returns Python code.
5. **Sandboxed execution:** The code is safely executed. Results (plots, tables, or text) are displayed.
6. **Get insights:** For plots, the LLM provides additional insights and observations about the visualization.

---

## Installation & Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/harshm2601/SheetMinds.git
cd SheetMinds
```

### 2. Install Dependencies
Navigate to the `app` directory and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

## File Structure

```
app/
  main.py           # Streamlit app entry point
  llm.py            # Handles LLM API calls and code extraction
  sandbox.py        # Securely executes generated code
  utils.py          # Utility functions for file handling and data overview
requirements.txt  # Python dependencies
```

---

## Requirements
- Python 3.8+
- See `app/requirements.txt` for Python package dependencies

---

## Security & Limitations
- **Code Execution:** All code is executed in a restricted environment, but always review generated code for safety.
- **API Key:** The LLM API key is hardcoded for demonstration. For production, use environment variables or a secure vault.
- **File Size:** Large files may impact performance.

---

## Credits
- Built with [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), and [Gemini LLM](https://ai.google.dev/).

---

## License
This project is for educational and demonstration purposes only.
