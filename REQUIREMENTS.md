## Getting Started

#### Configure Environment Variables 

Before running this notebook, you must configure certain environment variables. We will now use environment variables to store our configuration. This is a more secure practice as it prevents sensitive data from being accidentally committed and pushed to version control systems.

Create a `.env` file in your project root (use the provided `.env.sample` as a template) and add the following variables:

```env
# Azure Open API Configuration
AZURE_OPENAI_API_KEY='[Your OpenAI API Key]'
AZURE_OPENAI_ENDPOINT='[Your OpenAI Endpoint]'
AZURE_OPENAI_API_VERSION='[Your Azure OpenAI API Version]'

# Azure Vision API Configuration
AZURE_KEY_VISION='[Your Azure Vision API Key]'
AZURE_ENDPOINT_VISION='[Your Azure Vision API Endpoint]'

# Azure Document Intelligence API Configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT='[Your Document Intelligence Endpoint]'
AZURE_DOCUMENT_INTELLIGENCE_KEY='[Your Document Intelligence Key]'

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING='[Your Azure Storage Connection String]'
```

Replace the placeholders (e.g., [Your Azure Search Service Endpoint]) with your actual values.

- `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` and `AZURE_DOCUMENT_INTELLIGENCE_KEY` are used to configure the Azure Document Intelligence API.
- `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_API_VERSION` are used to configure the Azure OpenAI API.
- `AZURE_KEY_VISION` and `AZURE_ENDPOINT_VISION` are used to configure the Azure Vision API.
- `AZURE_STORAGE_CONNECTION_STRING` is used to configure the Azure Storage service.

> 📌 **Note**
> Remember not to commit the .env file to your version control system. Add it to your .gitignore file to prevent it from being tracked.

#### Setting Up Conda Environment and Configuring VSCode for Jupyter Notebooks (Optional)

Follow these steps to create a Conda environment and set up your VSCode for running Jupyter Notebooks:

##### Create Conda Environment from the Repository

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

##### Configure VSCode for Jupyter Notebooks

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