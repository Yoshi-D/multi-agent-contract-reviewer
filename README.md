
This readme file has been created by my github documentation agent that you can find in my pinned repositories. Gang gang

## 1. What the codebase does

This codebase implements an intelligent system for automated contract analysis, risk identification, and interactive question-answering. It streamlines the process of reviewing legal documents by leveraging Large Language Models (LLMs) to understand, analyze, and extract critical information.

The core functionalities include:

1.  **PDF Content Extraction:** Converts PDF contracts into a structured Markdown format, making the content easily processable.
2.  **Contract Sectioning:** Automatically breaks down the extracted contract content into logical sections, complete with titles, section numbers, and page references, facilitating granular analysis.
3.  **Semantic Indexing:** Stores these structured sections in a vector database, enabling rapid and semantically relevant retrieval of contract clauses based on natural language queries.
4.  **AI-Powered Risk Analysis:** Employs an AI agent to scrutinize each contract section, identifying potential risks, vulnerabilities, or unfavorable clauses. It generates a structured analysis detailing the risk level, type, severity, and an explanation.
5.  **Markdown Risk Report Generation:** Compiles all identified risks into a well-organized Markdown report, providing a clear and actionable summary of the contract's risk profile.
6.  **Interactive Q&A:** Offers an interactive command-line interface where users can ask natural language questions about the contract. An AI agent, powered by the semantic index and an LLM, provides grounded answers, referencing specific page and section numbers from the original contract.

In essence, the codebase transforms a raw PDF contract into an analyzable, queryable knowledge base, significantly reducing manual review effort and enhancing insights.

## 2. Architecture

The system is designed with a modular architecture, separating concerns into distinct processing steps and AI agents. This allows for clear data flow and facilitates potential future enhancements or modifications.

### Core Components:

*   **`main.py`:**
    *   Serves as the orchestrator of the entire workflow.
    *   Initializes and coordinates the `PDF_Manager`, section parsing, `ContractVectorStore`, `RiskAgent`, and `QAAgent`.
    *   Handles the sequential execution of PDF extraction, sectioning, vectorization, risk analysis, report generation, and the interactive Q&A loop.
*   **`processing/pdf_parser.py` (PDF_Manager):**
    *   Utilizes the `pymupdf4llm` library to extract content from PDF files, converting pages into markdown strings.
    *   Responsible for saving the aggregated risk analysis results into a well-formatted Markdown report file (`risk_report.md`).
*   **`processing/section_parser.py` :**
    *   This module (imported as `parse_sections`) takes the raw markdown pages extracted from the PDF.
    *   Its role is to parse and segment the content into logical contract sections, typically identifying headings, subheadings, and associated content, assigning section numbers, titles, content, and original page numbers.
*   **`vector_db/vector_store.py` (ContractVectorStore):**
    *   This module provides the functionality for creating, managing, and querying a vector database.
    *   It's responsible for clearing existing data, adding new contract sections (likely converting them into embeddings before storage), and performing similarity searches to retrieve context relevant to a given query (`get_context`).
*   **`agents/risk_agent.py` (RiskAgent):**
    *   An AI agent designed specifically for analyzing contract sections for risks.
    *   It takes a contract section as input and, presumably using an LLM, identifies and categorizes potential risks, providing a structured output including risk level, type, severity, and explanation.
*   **`agents/qa_agent.py` (QAAgent):**
    *   An AI agent focused on answering user questions about the contract.
    *   It is initialized with an LLM client (Google Gemini) and the `ContractVectorStore`.
    *   When a question is posed, it retrieves the most semantically relevant context from the `ContractVectorStore` and crafts an answer using the LLM, ensuring the answer is grounded in the provided contract context and includes page/section references.

### Data Flow and Interactions:

1.  **PDF Input:** The `main.py` script specifies a `pdf_path` (e.g., `sample_contracts/vendor_contract.pdf`).
2.  **Extraction:** `PDF_Manager.extract_markdown(pdf_path)` reads the PDF and returns a list of markdown-formatted pages.
3.  **Sectioning:** `parse_sections(pages)` processes the markdown pages into a list of structured `section` dictionaries. Each section contains its number, title, content, and start page.
4.  **Vectorization & Storage:** The `ContractVectorStore` is initialized, cleared, and then populated with these structured `sections` using `vector_store.add_sections()`.
5.  **Risk Analysis Loop:** `main.py` iterates through each significant `section`:
    *   A `RiskAgent` (initialized with an API key) is invoked via `risk_agent.analyze_section(section)`.
    *   The results are collected.
6.  **Risk Report Generation:** After all sections are analyzed, `pdf_manager.save_markdown_report(all_risks)` generates `risk_report.md`.
7.  **Interactive Q&A Loop:**
    *   A `QAAgent` is initialized with the API key and the `ContractVectorStore`.
    *   The user inputs a `question`.
    *   `qa_agent.answer(question)` is called:
        *   It uses `self.vector_store.get_context(query=question, top_k=3)` to retrieve the top 3 most relevant contract sections from the vector store.
        *   A detailed prompt, including the user's question and the retrieved context, is sent to the `gemini-2.5-flash` model via `self.client.models.generate_content()`.
        *   The LLM's response, which is a grounded answer with references, is printed to the console.
    *   This loop continues until the user types "exit".

### Technologies Used:

*   **Python 3.x:** The primary programming language.
*   **`pymupdf4llm`:** For efficient PDF content extraction and conversion to Markdown.
*   **`google-generativeai`:** Python client library for interacting with Google's Gemini LLMs.
*   **Google Gemini API:** Utilized by both the `RiskAgent`  and `QAAgent` for advanced natural language understanding and generation. Specifically, `gemini-2.5-flash` is used for Q&A.

## 3. How to Setup

Follow these steps to get the contract analysis system up and running.

### Prerequisites

*   **Python 3.x:** Ensure you have Python 3 installed on your system.
*   **Google Gemini API Key:** You will need an API key to access Google's Gemini models. Obtain one from [Google AI Studio](https://aistudio.google.com/).

### Installation

1.  **Clone the Repository:**
    (Assuming the codebase resides in a Git repository)
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Python Dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install pymupdf4llm google-generativeai
    ```

### Configuration

1.  **Set your Google Gemini API Key:**
    The system expects the `GEMINI_API_KEY` to be configured. While `main.py` contains a placeholder `GEMINI_API_KEY = "f4ke_4pi_k3y"`, it also includes a check for an environment variable.
    **It is highly recommended to set this as an environment variable** rather than modifying the source code.

    *   **On Linux/macOS:**
        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
        (Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent for persistent setting).
    *   **On Windows (Command Prompt):**
        ```bash
        set GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **On Windows (PowerShell):**
        ```bash
        $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    **Important:** Replace `"YOUR_GEMINI_API_KEY"` with the actual API key you obtained from Google AI Studio.

2.  **Prepare Sample Contracts:**
    The `main.py` script is configured to process a PDF located at `sample_contracts/vendor_contract.pdf`.
    *   Create a directory named `sample_contracts` in the root of your project.
    *   Place your target PDF contract file inside this directory and ensure its name matches `vendor_contract.pdf` or update the `pdf_path` variable in `main.py` to point to your desired contract.

### Running the Application

1.  **Execute the main script:**
    Ensure your virtual environment is activated and your API key is set.
    ```bash
    python main.py
    ```

2.  **Expected Output:**
    *   The console will print messages indicating the progress of PDF extraction and section parsing.
    *   It will then display each identified section's number, title, and start page.
    *   The system will proceed with "Running risk analysis...", printing the analysis status for each section.
    *   Upon completion of risk analysis, a file named `risk_report.md` will be created in the parent directory (`../risk_report.md` as per `pdf_parser.py` default path), containing a detailed markdown report of all identified risks.
    *   Finally, the application will enter an interactive Q&A mode:
        ```
        Enter your query or exit:
        ```
        You can type questions related to the contract. The agent will respond, grounding its answer in the contract context with page/section numbers.
    *   To exit the Q&A session, type `exit` and press Enter.
