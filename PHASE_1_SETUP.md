# Phase 1: Foundation & Setup

Welcome to the start of the **AI DevTeam** project. In this phase, we will set up the Azure infrastructure and your local Python development environment. By the end of this phase, your local code will be able to communicate securely with a Large Language Model hosted in Microsoft AI Foundry.

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
   * *Note: Keep the deployment name simple, e.g., `gpt-4o`. You will need this name later.*
5. Click **Deploy**.

---

## Step 3: Gather Connection Details

To connect our Python code to the Foundry project, we need the Project Connection String.

1. In the Foundry portal, go to your project's **Overview** page.
2. Look for the **Project details** panel on the right side.
3. Find the **Project connection string** and copy it.
   * *Format looks like: `<region>.api.azureml.ms;<subscription-id>;<resource-group>;<project-name>`*

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
On macOS, the command is `python3` (not `python`). Confirm you have Python 3.10 or higher:
```bash
python3 --version
# Expected: Python 3.10.x or higher
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### 3. Create a Virtual Environment
It is best practice to isolate project dependencies.
```bash
# macOS / Linux — use python3
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
Once activated, your terminal prompt will show `(.venv)` at the start.

### 4. Install Dependencies
Install the Microsoft AI Foundry SDKs and other required packages:
```bash
pip install -r requirements.txt
```

---

## Step 5: Configure Environment Variables

We use environment variables to store configuration securely without committing it to version control.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file in your code editor.
3. Paste the **Project connection string** you copied in Step 3.
4. Enter the **Model deployment name** you chose in Step 2.
5. Fill in your **Azure Subscription ID** and **Resource Group** name.

---

## Step 6: Authenticate with Azure CLI

We use `DefaultAzureCredential` in our code, which allows secure, keyless authentication by leveraging your local Azure CLI login.

1. If you don't have the Azure CLI installed, [download and install it here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Log in to your Azure account from the terminal:
   ```bash
   az login
   ```
3. Set your active subscription (if you have multiple):
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

---

## Step 7: Verify the Connection

You are now ready to test the setup. I have provided a verification script that will load your config, connect to Foundry, and ask the model to introduce itself.

Run the following command from the `ai_devteam` directory:
```bash
python phase1_verify_connection.py
```

**Expected Output:**
If everything is configured correctly, you will see a success message and a response from the model introducing itself as the Project Manager of the AI DevTeam.

---

## Next Steps

Once you have successfully run the verification script, let me know! We will then move on to **Phase 2**, where we will start writing the actual inference and orchestration code for the agents.
