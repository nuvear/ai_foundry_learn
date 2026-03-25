# Phase 1: Foundation & Setup (Developer Guide)

Welcome to the start of the **AI DevTeam** project. In this phase, we set up the Azure infrastructure and your local Python development environment. By the end of this phase, your local code will be able to communicate securely with a Large Language Model hosted in Microsoft AI Foundry.

> **Developer Note:** This guide has been battle-tested on macOS and Windows. It specifically accounts for the Microsoft AI Foundry SDK v2.0+ updates, which introduced a new endpoint URL format and deprecated the old connection string format.

---

## Step 1: Create an Azure AI Foundry Project

Microsoft AI Foundry organizes resources into **Projects**. A project contains your models, data, and agent definitions.

1. Navigate to the [Microsoft AI Foundry Portal](https://ai.azure.com/).
2. Sign in with your Azure account.
3. In the left navigation pane, click **Projects** and then click **+ New project**.
4. Name your project (e.g., `ai-devteam-project`).
5. Choose or create a new **Azure Resource Group** (e.g., `rg-ai-devteam`).
6. Click **Create** and wait for the provisioning to finish (this may take a few minutes).

---

## Step 2: Deploy a Foundation Model

Our agents need a "brain." We will deploy a model from the Foundry Model Catalog.

1. Inside your newly created project in the Foundry portal, navigate to **Models + endpoints** under the **My assets** section on the left.
2. Click **+ Deploy model** and select **Deploy base model**.
3. Search for and select **gpt-4o** (or your preferred model like DeepSeek-R1).
4. Click **Confirm** and give your deployment a name.
   * *Best Practice: Keep the deployment name simple, e.g., `gpt-4o`. You will need this name later.*
5. Click **Deploy**.

---

## Step 3: Gather Connection Details

To connect our Python code to the Foundry project using the **SDK v2.0+**, we need the Project Endpoint URL.

1. In the Foundry portal, go to your project's **Overview** page.
2. Look for the **Project details** panel on the right side.
3. Find the **Endpoint** field and copy it.
   * *Format looks like: `https://<project-name>-resource.services.ai.azure.com/api/projects/<project-name>`*
4. Also note your **Subscription ID** and **Resource Group** from the same panel.

---

## Step 4: Local Environment Setup

Now, let's set up your local machine. You need Python 3.10 or higher installed.

### 1. Clone the Repository
Open your terminal and clone this repository:
```bash
git clone https://github.com/nuvear/ai_foundry_learn.git
cd ai_foundry_learn/ai_devteam
```

### 2. Verify Your Python Version
Confirm you have Python 3.10 or higher. 
*Note for macOS users: The command is `python3`.*
```bash
python3 --version
# Expected: Python 3.10.x or higher
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### 3. Create a Virtual Environment
It is best practice to isolate project dependencies.
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
Once activated, your terminal prompt will show `(.venv)` at the start.

### 4. Install Dependencies
Install the Microsoft AI Foundry SDKs and other required packages. We explicitly pin `azure-ai-projects>=2.0.0` to ensure API compatibility.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 5: Configure Environment Variables

We use environment variables to store configuration securely without committing it to version control.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file in your code editor (e.g., VS Code: `code .env`).
3. Fill in your values. Your file should look exactly like this:

```text
# Found in: Foundry Portal → Project Overview → Endpoint
AIPROJECT_CONNECTION_STRING=https://ai-devteam-project-resource.services.ai.azure.com/api/projects/ai-devteam-project

# The name you gave your GPT-4o deployment
MODEL_DEPLOYMENT_NAME=gpt-4o

# Found in: Azure Portal or Foundry Project Overview
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_GROUP=rg-ai-devteam
```

---

## Step 6: Authenticate with Azure CLI

We use `DefaultAzureCredential` in our code, which allows secure, keyless authentication by leveraging your local Azure CLI login.

1. **Install Azure CLI** (if not already installed):
   * macOS: `brew install azure-cli`
   * Windows: Download the MSI from the [Microsoft docs](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. **Log in to Azure** from the terminal:
   ```bash
   az login
   ```
   *This will open a browser window. Sign in with your Azure account.*
3. **Set your active subscription** (if you have multiple):
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

---

## Step 7: Verify the Connection

You are now ready to test the setup. The verification script will load your config, connect to Foundry using the new SDK v2.0 endpoint format, and ask the model to introduce itself.

Run the following command from the `ai_devteam` directory:
```bash
python phase1_verify_connection.py
```

**Expected Output:**
If everything is configured correctly, you will see a green success panel with a response from the model:

> *"I am the Project Manager of AI DevTeam, responsible for leading our AI-powered software development team to deliver innovative, efficient, and impactful technological solutions."*

---

## Troubleshooting Common Issues

| Issue | Solution |
| :--- | :--- |
| `zsh: command not found: python` | On macOS, use `python3` instead of `python`. |
| `AttributeError: type object 'AIProjectClient' has no attribute 'from_connection_string'` | You have an older SDK version. Run `pip install --upgrade azure-ai-projects openai` and ensure your `.env` uses the `https://...` endpoint format. |
| `azure.core.exceptions.ClientAuthenticationError` | You are not logged in. Run `az login` in the terminal. |

---

## Next Steps

Once you have successfully run the verification script, you are ready to move on to **Phase 2: Core Intelligence**, where we will start building the brains of our virtual agents.
