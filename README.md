# Azure AI OCR services (preview version) <img src="./utils/images/azure_logo.png" alt="Azure Logo" style="width:30px;height:30px;"/>

This project is a comprehensive guide to leveraging advanced OCR AI services from Azure. It provides a hands-on approach to understanding and implementing the following services:

1. **PDF to Image Conversion with `OCRHelper`**: This section explains how to use `OCRHelper` to manage Azure Blob Storage connections and convert PDF files into images for further processing by the OCR GPT-4 Vision model.

2. **Advanced Text Extraction with GPT-4 Vision**: This part demonstrates how to use the `GPT4VisionManager` to perform OCR on images, leveraging the GPT-4 Vision model's ability to recognize and extract text from images for applications like document analysis and data extraction.

3. [**Contextual Text Generation with AzureOpenAIAssistant**]: After text extraction, this section shows how to use the `AzureOpenAIAssistant` to process the output. It interacts with the Azure OpenAI API to generate context-aware responses based on the extracted text, enhancing the system's interactivity and intelligence.

4. **Document Analysis with Azure AI Document Intelligence**: This section provides an overview of Azure's Document Analysis Client and its pre-trained models for document analysis.

5.**Data Processing from the Layout Model**: This part delves into the insights from the data extracted from the layout model, discussing the need for custom logic for processing and the benefits of leveraging LangChain Integration for dynamic interaction with documents and content generation.

For a detailed explanation and walkthrough, please refer to the notebooks `01-ocr-gpt4v.ipynb` and `02-ocr-document-intelligence.ipynb`.

## 🔧 Prerequisites 

### Setting Up Azure AI Services

 **Azure OpenAI Service**: This service provides access to powerful AI models for various tasks such as text generation, translation, and summarization. To use this service, you need to create an Azure OpenAI service instance and obtain the API key. You can get started [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/).

- **Azure Document Intelligence AI Service**: This service uses AI to extract insights and data from unstructured documents. It can help automate data extraction and make sense of large volumes of documents. Learn more and get started [here](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).

- **Azure Vision**: This service uses AI to analyze images and videos for various scenarios, including feature recognition, image classification, and object detection. Get started with Azure Vision [here](https://azure.microsoft.com/en-us/products/ai-services/ai-vision).

- **Azure Storage (Blob)**: Azure Blob Storage is a service for storing large amounts of unstructured object data, such as text or binary data. It can be used for serving images or documents directly to a browser, storing files for distributed access, and more. Learn more and get started [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction).


## 🌲 Project Tree Structure

```
📂 gbbai-azure-ai-document-intelligence
┣ 📂 notebooks <- For development, EDA, and quick testing (Jupyter notebooks for analysis and development).
┣ 📦 src <- Houses main source code.
┣ 📂 test <- Runs unit and integration tests for code validation and QA. 
┣ 📂 utils <- Contains utility functions and shared code used throughout the project. 
┣ 📜 .pre-commit-config.yaml <- Config for pre-commit hooks ensuring code quality and consistency.
┣ 📜 01-ocr-gpt4v.ipynb
┣ 📜 02-ocr-document-intelligence.ipynb
┣ 📜 CONTRIBUTING.md <- Guidelines for contributing to the project.
┣ 📜 CHANGELOG.md <- Logs project changes, updates, and version history.
┣ 📜 CONTRIBUTING.md <- Guidelines for contributing to the project.
┣ 📜 environment.yaml <- Conda environment configuration.
┣ 📜 Makefile <- Simplifies common development tasks and commands.
┣ 📜 pyproject.toml <- Configuration file for build system requirements and packaging-related metadata.
┣ 📜 README.md <- Overview, setup instructions, and usage details of the project.
┣ 📜 requirements-codequality.txt <- Requirements for code quality tools and libraries.
┣ 📜 requirements.txt <- General project dependencies.
```

