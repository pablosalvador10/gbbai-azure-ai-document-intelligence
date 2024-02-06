## Getting Started

### Setting Up Azure AI Services

+ **Azure OpenAI Service**: This service provides access to powerful AI models for various tasks such as text generation, translation, and summarization. To use this service, you need to create an Azure OpenAI service instance and obtain the API key. You can get started [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/).

- **Azure Document Intelligence AI Service**: This service uses AI to extract insights and data from unstructured documents. It can help automate data extraction and make sense of large volumes of documents. Learn more and get started [here](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).

+ **Azure Vision**: This service uses AI to analyze images and videos for various scenarios, including feature recognition, image classification, and object detection. Get started with Azure Vision [here](https://azure.microsoft.com/en-us/products/ai-services/ai-vision).

- **Azure Storage (Blob)**: Azure Blob Storage is a service for storing large amounts of unstructured object data, such as text or binary data. It can be used for serving images or documents directly to a browser, storing files for distributed access, and more. Learn more and get started [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction).


### Configure Environment Variables 

Before running this notebook, you must configure certain environment variables. We will now use environment variables to store our configuration. This is a more secure practice as it prevents sensitive data from being accidentally committed and pushed to version control systems.

Create a `.env` file in your project root (use the provided `.env.sample` as a template) and add the following variables:

```env
# Azure Open AI Completion Configuration
AZURE_OPENAI_KEY="[Your Azure OpenAI Key]"
AZURE_AOAI_CHAT_MODEL_NAME_DEPLOYMENT_ID="[Your Azure AOAI Chat Model Name Deployment ID]"
AZURE_AOAI_COMPLETION_MODEL_DEPLOYMENT_ID="[Your Azure AOAI Completion Model Deployment ID]"
AZURE_AOAI_EMBEDDING_MODEL_DEPLOYMENT_ID="[Your Azure AOAI Embedding Model Deployment ID]"
AZURE_OPENAI_API_ENDPOINT="[Your Azure OpenAI API Endpoint]"
AZURE_OPENAI_API_VERSION="[Your Azure OpenAI API Version]"

# OPTIONAL: Azure AI Search Service Configuration
AZURE_AI_SEARCH_SERVICE_ENDPOINT="[Your Azure AI Search Service Endpoint]"
AZURE_SEARCH_ADMIN_KEY="[Your Azure Search Admin Key]"
AZURE_AI_SEARCH_INDEX_NAME="[Your Azure AI Search Index Name]"

# Azure Open Vision API Configuration
AZURE_OPENAI_API_KEY_VISION='[Your OpenAI API Key for Vision]'
AZURE_OPENAI_ENDPOINT_VISION='[Your OpenAI Endpoint for Vision]'
AZURE_OPENAI_API_VERSION_VISION='[Your Azure OpenAI API Version for Vision]'
AZURE_OPENAI_API_DEPLOYMENT_NAME_VISION= '[Your Azure OpenAI Deployment Name for Vision]'

# Azure Document Intelligence API Configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="[Your Azure Document Intelligence Endpoint]"
AZURE_DOCUMENT_INTELLIGENCE_KEY="[Your Azure Document Intelligence Key]"

# Azure Vision API Configuration
AZURE_KEY_VISION='[Your Azure Key for Vision]'
AZURE_ENDPOINT_VISION='[Your Azure Endpoint for Vision]'

# Azure Open API Configuration
AZURE_STORAGE_CONNECTION_STRING='[Your Azure Storage Connection String]'
```

Replace the placeholders (e.g., [Your Azure Search Service Endpoint]) with your actual values.

- `AZURE_OPENAI_KEY`, `AZURE_AOAI_CHAT_MODEL_NAME_DEPLOYMENT_ID`, `AZURE_AOAI_COMPLETION_MODEL_DEPLOYMENT_ID`, `AZURE_AOAI_EMBEDDING_MODEL_DEPLOYMENT_ID`, `AZURE_OPENAI_API_ENDPOINT`, and `AZURE_OPENAI_API_VERSION` are used to configure the Azure OpenAI API.
- OPTIONAL: `AZURE_AI_SEARCH_SERVICE_ENDPOINT`, `AZURE_SEARCH_ADMIN_KEY`, and `AZURE_AI_SEARCH_INDEX_NAME` are used to configure the Azure AI Search Service.
- `AZURE_OPENAI_API_KEY_VISION`, `AZURE_OPENAI_ENDPOINT_VISION`, `AZURE_OPENAI_API_VERSION_VISION`, and `AZURE_OPENAI_API_DEPLOYMENT_NAME_VISION` are used to configure the Azure Open Vision API.
- `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` and `AZURE_DOCUMENT_INTELLIGENCE_KEY` are used to configure the Azure Document Intelligence API.
- `AZURE_KEY_VISION` and `AZURE_ENDPOINT_VISION` are used to configure the Azure Vision API.
- `AZURE_STORAGE_CONNECTION_STRING` is used to configure the Azure Storage service.

> 📌 **Note**
> Remember not to commit the .env file to your version control system. Add it to your .gitignore file to prevent it from being tracked.

### Setting Up Conda Environment and Configuring VSCode for Jupyter Notebooks (Optional)

Follow these steps to create a Conda environment and set up your VSCode for running Jupyter Notebooks:

#### Create Conda Environment from the Repository

> Instructions for Windows users: 

1. **Create the Conda Environment**:
   - In your terminal or command line, navigate to the repository directory.
   - Execute the following command to create the Conda environment using the `environment.yaml` file:
     ```bash
     conda env create -f environment.yaml
     ```
   - This command creates a Conda environment as defined in `environment.yaml`.

2. **Activating the Environment**:
   - After creation, activate the new Conda environment by using:
     ```bash
     conda activate document-intelligence
     ```

> Instructions for Linux users (or Windows users with WSL or other linux setup): 

1. **Use `make` to Create the Conda Environment**:
   - In your terminal or command line, navigate to the repository directory and look at the Makefile.
   - Execute the `make` command specified below to create the Conda environment using the `environment.yaml` file:
     ```bash
     make create_conda_env
     ```

2. **Activating the Environment**:
   - After creation, activate the new Conda environment by using:
     ```bash
     conda activate document-intelligence
     ```

#### Configure VSCode for Jupyter Notebooks

1. **Install Required Extensions**:
   - Download and install the `Python` and `Jupyter` extensions for VSCode. These extensions provide support for running and editing Jupyter Notebooks within VSCode.

2. **Open the Notebook**:
   - Open the Jupyter Notebook file (`01-ocr-gpt4v.ipynb`) in VSCode.

3. **Attach Kernel to VSCode**:
   - After creating the Conda environment, it should be available in the kernel selection dropdown. This dropdown is located in the top-right corner of the VSCode interface.
   - Select your newly created environment (`document-intelligence`) from the dropdown. This sets it as the kernel for running your Jupyter Notebooks.

4. **Run the Notebook**:
   - Once the kernel is attached, you can run the notebook by clicking on the "Run All" button in the top menu, or by running each cell individually.


By following these steps, you'll establish a dedicated Conda environment for your project and configure VSCode to run Jupyter Notebooks efficiently. This environment will include all the necessary dependencies specified in your `environment.yaml` file. If you wish to add more packages or change versions, please use `pip install` in a notebook cell or in the terminal after activating the environment, and then restart the kernel. The changes should be automatically applied after the session restarts.