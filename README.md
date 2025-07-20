# Cloud Hosted AI Resume Screening Application

Capstone Project for University of Cincinnati M.S. Business Analytics Summer 2025

**Contributors**: Zachary Biery

**Demo**: 

## About the Project

This project is a cloud-native AI application designed to automate and enhance the resume review process for recruiters. Traditional systems rely on keyword matching, often overlooking qualified candidates due to a lack of contextual understanding. This project leverages large language models (LLMs) and semantic embeddings to provide a smarter, faster, and more accurate screening process.

### Key features

- Semantic matching of resumes to job descriptions using pretrained AI models.
- Automated extraction and summarization of key candidate information (skills, education, experience).
- Interactive frontend built with Streamlit and a FastAPI backend.
- Scalable and secure Azure container apps deployment using GitHub Actions.

This project showcases practical applications of AI system design, cloud engineering, and unstructured data processing.

## About the System
This system simulates a production-grade, enterprise-ready AI application for resume screening and candidate-job matching. It is built to be modular, secure, scalable, and easily maintainable using best practices in cloud infrastructure and modern ML system design.

### Infrastructure
The infrastructure is architected to closely reflect real-world enterprise production environments:

#### Security-First Design
Enforces strong network isolation using private endpoints, private DNS zones, network security groups (NSGs), and Azure Managed Identities. No public ingress is permitted into core services.

#### Modular & Reproducible
Built using Infrastructure-as-Code (IaC) with Bicep. Each module (networking, identity, compute, AI services, etc.) is independently deployable and parameterized to support environment-specific (dev, test, prod) configurations via CI/CD pipelines.

#### Scalable by Design
Loosely coupled services and a centralized identity model allow the system to grow organically. Additional AI providers, data sources, or processing flows can be added without disrupting existing functionality.

See the full [Infrastructure README.md](/infra/README.md) for deployment and module-specific details.

### Backend
The backend is powered by FastAPI and integrates with large language models from OpenAI or Groq. It provides a RESTful interface for the frontend and orchestrates AI-driven flows for extraction and matching.

#### Extraction Flows
Analyzes uploaded resumes and job descriptions to extract structured information (e.g. skills, education, experience, responsibilities). This output forms the foundation for downstream matching.

![extraction](/assets/extractionFlows.jpg)

#### Matching Flow
Compares candidates against selected jobs using structured semantic scoring across multiple dimensions (education, technical skills, experience, etc.), and produces an interpretable ranking with detailed reasoning.

![matching](/assets/matchFlow.jpg)

#### API Architecture
The API design separates core logic (analysis, matching) from routing and service abstraction layers for maintainability.

![API](/assets//apiDiagram.jpg)

### Frontend
The frontend is a lightweight Streamlit application that interacts with the backend API and offers a user-friendly interface for managing and evaluating both candidates and job postings.

#### Candidates Page
Upload resumes, view extracted candidate profiles, summaries, and metadata.

#### Jobs Page
Upload job descriptions and review structured breakdowns, summaries, and analysis results.

#### Matching Page
Select one or more candidates and a job to view detailed match scores, explanations, strengths, and gaps.

All pages are backed by real-time API calls and use consistent session state and layout utilities for seamless interaction.

## Usage

To use this project or replicate results, follow the information presented below.

### Prerequisites

You must have the following software installed before proceeding.

1. [Python](https://www.python.org/downloads/) 3.10+
2. [Docker](https://docs.docker.com/engine/install/)
3. [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
4. [VSCode](https://code.visualstudio.com/) or any other IDE
   - (Optional) Bicep extension for visual studio
   - (Optional) Docker extension for visual studio
5. An active Azure subscription

### Setup Instructions

To replicate this project, follow these steps.

1. Clone the Repository
```bash
# Navigate to your preferred directory
cd your/preferred/location

# Clone the repository
git clone https://github.com/zbiery/resume-screener.git

# (Optional) Open the project in VSCode
code .
```

2. **(Recommended)** Create and activate a virtual environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate.bat

# Activate (Mac/Linux)
source .venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Create .env

Copy the `template.env` in the [config directory](/config/) and place in the same directory. Name the file `.env` and replace the value with your target environment. 

5. Deploy Infrastructure

Follow the directions in the [infra directory](/infra/README.md) to complete this step

6. **(Optional)** Update Configurations

Update the configuration values in the [config](/config/) directory.

### App Startup

#### Local Use
To start the application & begin using it locally, run:

```bash
python app\main.py
```

This will:
- Start the FastAPI app on port 8000
- Start the Streamlit UI on port 8501

You can then navigate to your web browser to begin using the Streamlit app.

#### Cloud Use

To access the deployed cloud app, do the following:

1. Navigate to the [Azure portal](portal.azure.com)
2. Select your subscription > resource group > container app
3. Click the application URL in the overview page

## Project Structure
```
resume-screening/                      # Root directory of the resume screening project
│
├── .github/                           # GitHub configuration (e.g., CI/CD workflows)
│   └── workflows/                     # GitHub Actions workflows
│       └── deploy-iac.yml             # Workflow to deploy infrastructure-as-code (Bicep templates)
│
├── app/                               # Application source code
│   ├── backend/                       # FastAPI backend
│   │   ├── api/                       # API routes and data models
│   │   │   ├── main.py                # FastAPI app entry point
│   │   │   ├── routes.py              # Route definitions for REST endpoints
│   │   │   └── schemas.py             # Pydantic schemas for request/response validation
│   │   │
│   │   ├── common/                    # Shared utilities and configuration
│   │   │   ├── config.py              # App-wide configuration loader
│   │   │   ├── logger.py              # Logger configuration
│   │   │   └── utils.py               # General helper functions
│   │   │
│   │   ├── core/                      # Core processing logic
│   │   │   ├── analyzer.py            # High-level orchestration for analyzing resumes
│   │   │   ├── file_processor.py      # Handles file conversion, parsing, and validation
│   │   │   └── resume_parser.py       # Extracts structured data from resume files
│   │   │
│   │   ├── llm/                       # LLM interaction layer
│   │   │   ├── functions.py           # Function definitions for structured LLM outputs
│   │   │   └── prompts.py             # Prompt templates for LLM calls
│   │   │
│   │   ├── services/                  # LLM service clients and abstractions
│   │   │   ├── factory.py             # Factory to switch between OpenAI/Groq backends
│   │   │   ├── groq.py                # Wrapper for Groq API interactions
│   │   │   ├── openai.py              # Wrapper for Azure OpenAI API interactions
│   │   │   └── schema.py              # Service-specific request/response schemas
│   │   │
│   │   └── __init__.py                # Marks backend as a Python package
│
│   ├── frontend/                      # Streamlit frontend
│   │   ├── pages/                     # Streamlit multi-page app
│   │   │   ├── candidates.py          # UI page for candidate upload and display
│   │   │   ├── jobs.py                # UI page for job creation and listing
│   │   │   └── matching.py            # UI page for matching candidates to jobs
│   │   │
│   │   ├── __init__.py                # Marks frontend as a Python package
│   │   └── main.py                    # Streamlit app entry point
│
│   ├── logs/                          # Runtime application logs
│   │   └── app.log                    # Log output file
│
│   └── main.py                        # Unified entry point if needed for combined back/frontend
│   └── __init__.py                    # Marks `app` as a Python package
│
├── config/                            # Configuration files
│   ├── .env                           # Environment variables (not checked into Git)
│   ├── config.json                    # Runtime configuration used by the backend
│   └── template.env                   # Template for .env setup
│
├── data/                              # Sample resumes and test files
│   ├── ZacharyBiery_CV_2024.docx      # Example resume in Word format
│   └── ZacharyBiery_CV_2024.pdf       # Example resume in PDF format
│
├── infra/                             # Infrastructure-as-code (Bicep)
│   ├── modules/                       # Modular Bicep templates for individual resources
│   │   ├── acr.bicep                  # Azure Container Registry definition
│   │   ├── containerapp.bicep         # Azure Container App definition
│   │   ├── groq.bicep                 # Groq-specific infrastructure
│   │   ├── identity.bicep             # Managed identities
│   │   ├── keyvault.bicep             # Azure Key Vault configuration
│   │   ├── monitoring.bicep           # Log Analytics / monitoring setup
│   │   ├── networking.bicep           # Virtual network and subnets
│   │   ├── openai.bicep               # Azure OpenAI setup
│   │   └── storage.bicep              # Storage account with private endpoint
│   ├── main.bicep                     # Root Bicep file to deploy the full stack
│   ├── main.dev.bicepparam            # Parameters for dev environment deployment
│   ├── main.test.bicepparam           # Parameters for test environment deployment
│   ├── main.prod.bicepparam           # Parameters for prod environment deployment
│   └── README.md                      # Instructions and documentation for IaC
│
├── tests/                             # Test suite for backend/frontend
│
├── .dockerignore                      # Files/folders to exclude from Docker build context
├── .gitignore                         # Specifies intentionally untracked files to ignore
├── Dockerfile                         # Container build instructions for the application
├── LICENSE                            # Open source license
├── README.md                          # Project overview and setup instructions
├── requirements.txt                   # Python package dependencies
└── supervisord.conf                   # Supervisor configuration (used for managing processes in container)

```