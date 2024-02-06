# <img src="./utils/images/azure_logo.png" alt="Azure Logo" style="width:30px;height:30px;"/> Advanced OCR and Document Intelligence with Azure AI (Preview Version)

This project aims to demonstrate the implementation of advanced Optical Character Recognition (OCR) and document intelligence services using Azure AI and GPT-4 Vision. The guide is divided into three main sections, each covered in a separate Jupyter notebook.

- **[OCR with Azure AI Document Intelligence](./01-ocr-document-intelligence.ipynb)**
    - Overview of Azure's Document Analysis Client
    - Custom logic for processing extracted information
    - Retrieval-Augmented Generation (RAG) with a pretrained Large Language Model (LLM)

- **[OCR with GPT-4 Vision](./02-ocr-gpt4v.ipynb)**
    - Conversion of PDF documents into images
    - Text recognition and extraction from images using GPT-4 Vision
    - Context-aware text generation with `AzureOpenAIAssistant`

- **[Azure AI Indexer Orchestration](./03-azure-ai-search-orchestration.ipynb)**
    - Operation of indexers, skillsets, and skills for data ingestion, enrichment, and searchability

## 🔧 Prerequisites

Please make sure you have met all the prerequisites for this project. A detailed guide on how to set up your environment and get ready to run all the notebooks and code in this repository can be found in the [REQUIREMENTS.md](REQUIREMENTS.md) file. Please follow the instructions there to ensure a smooth exprience.


## 🔄 Continuous Integration/Continuous Deployment (CI/CD) (preview)

This project leverages GitHub Actions for automating our DevOps lifecycle. More #TODO

You can view the configuration and status of our GitHub Actions workflows in the `.github/workflows` directory and the "Actions" tab of our GitHub repository, respectively.

## 💼 Contributing:

Eager to make significant contributions? Our **[CONTRIBUTING](./CONTRIBUTING.md)** guide is your essential resource! It lays out a clear path.


