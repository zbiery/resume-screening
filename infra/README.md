# AI Resume Screening App - Azure Infrastructure

This folder contains the Azure Bicep templates for deploying the **AI Resume Screening application** on Azure across multiple environments (dev, test, prod).

---

## Prerequisites

Before doing anything, ensure the following:

- An **active Azure account**
- **Visual Studio Code** with the Bicep extension
- **Azure CLI** installed: [Install Link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Contributor or Owner role in each subscription
- Admin permission to create Azure AD service principals (for GitHub deployer)

---

## Project Structure

```bash
infra/
├── main.bicep                   # Main orchestration template
├── main.dev.bicepparam          # Parameters for development
├── main.test.bicepparam         # Parameters for test
├── main.prod.bicepparam         # Parameters for production
├── modules/
│   ├── identity.bicep           # User-assigned identity
│   ├── networking.bicep         # VNet, subnets, NSGs, private DNS
│   ├── monitoring.bicep         # Log Analytics and App Insights
│   ├── keyvault.bicep           # Key Vault and private endpoint
│   ├── storage.bicep            # Blob storage and private endpoint
│   ├── acr.bicep                # Azure Container Registry
│   ├── openai.bicep             # Azure OpenAI service
│   └── containerapp.bicep       # Container App with private networking
└── README.md                    # Documentation and instructions
```

## Environments
The infrastructure supports three separate environments:
1. dev
2. test
3. prod

#### Development
- Uses Standard SKUs where possible
- Single instance deployments
- Basic monitoring retention

#### Production
- Consider Premium SKUs for better performance
- Enable zone redundancy
- Increase retention periods for compliance

Each environment is managed at the subscription level. You must create separate subscriptions in the Azure Portal and link your deployments to the appropriate one. Deployments are handled through GitHub Actions using environment specific deployers (service principals). You must set up a service principal for each subscription (dev, test, prod).

### Service Principal Setup (One-Time)
1. Login to Azure:
```bash
az login
```
2. Set active subscription:
```bash
az account set --subscription "<subscription-id>"
```
3. Create a Service Principal for GitHub Actions per environment:
```bash
az ad sp create-for-rbac --name "github-deployer-<env>" \
  --role "Contributor" \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth
```
4. Save the generated JSON as a GitHub Actions secret along with the subscription ID
```
Name: AZURE_CREDENTIALS
Value: {
  "clientId": "XXX",
  "clientSecret": "XXX",
  "subscriptionId": "XXX",
  "tenantId": "XXX",
  "activeDirectoryEndpointUrl": "XXX",
  "resourceManagerEndpointUrl": "XXX",
  "activeDirectoryGraphResourceId": "XXX",
  "sqlManagementEndpointUrl": "XXX",
  "galleryEndpointUrl": "XXX",
  "managementEndpointUrl": "XXX"
}
Scope: Environment-level secret (dev, test, prod)

Name: AZURE_SUBSCRIPTION_ID
Value: xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx
Scope: Environment-level secret (dev, test, prod)
```
**Optional**
If you are utilizing a free trial or Azure student subscription, you may wish to refrain from using AzureOpenAI resources due to the strict quota provided. As a fallback option, this project has been configured to allow for the use of free open-source LLMs provided via [Groq](https://groq.com/). If you wish to utilize **Groq** as opposed to **AzureOpenAI**, register for a free account, retrieve your API key, and store it as a *Repository* secret in GitHub
```
Name: GROQ_API_KEY
Value: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Scope: Repository-level secret
```
To turn off OpenAI deployments, set the **useAzureOpenAi** parameter to *false* in the bicepparam files.

## Deployment Steps
1. Register required resource providers in your subscription. This may take a few moments.
```bash
az provider register --namespace Microsoft.Resources
az provider register --namespace Microsoft.Network
az provider register --namespace Microsoft.ManagedIdentity
az provider register --namespace Microsoft.Authorization
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.Insights
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.ContainerRegistry
az provider register --namespace Microsoft.CognitiveServices
az provider register --namespace Microsoft.ContainerService
```

2. Create a resource group for your environment:
```bash
az group create --name "<resource-group-name>" --location "<azure-region>"
```
3. Edit the parameter files for your desired configuration. 
4. Run the GitHub Actions Workflow for your target environment.
```
In your GitHub Repository:
Actions -> All Workflows -> Deploy Full Infrastructure -> Select Target Environment
```

**Optional**
To deploy Bicep manually (using the Azure CLI), run the following with the matching parameter file:
```bash
az deployment group create \
  --resource-group <resource-group-name> \
  --template-file main.bicep \
  --parameters @main.dev.bicepparam
```
⚠️ Replace main.dev.bicepparam with main.test.bicepparam or main.prod.bicepparam depending on the environment.

### What Gets Deployed

| Module       | Description                                              |
|--------------|----------------------------------------------------------|
| `identity`   | User-assigned managed identity                           |
| `networking` | VNet, subnets, NSGs, and private DNS zones               |
| `monitoring` | Log Analytics workspace and Application Insights         |
| `keyvault`   | Key Vault with private endpoint and RBAC                 |
| `storage`    | Blob storage account with private endpoint               |
| `acr`        | Azure Container Registry (private, optional)             |
| `openai`     | Azure OpenAI instance and model deployments              |
| `containerapp` | Hosts the application in a secure, scalable app       |

## Networking and Security
- No public exposure: All services are accessed via private endpoints
- User-assigned identity: Used to access all key services (OpenAI, ACR, KV, Storage)
- Private DNS Zones: For internal name resolution (e.g., privatelink.openai.azure.com)
- NSGs: Lock down subnets by function

### Subnets
| Subnet Name            | CIDR        | Purpose                        |
| ---------------------- | ----------- | ------------------------------ |
| `container-app-subnet` | 10.0.1.0/24 | Azure Container Apps           |
| `storage-subnet`       | 10.0.2.0/24 | Azure Storage private endpoint |
| `keyvault-subnet`      | 10.0.3.0/24 | Key Vault private endpoint     |
| `openai-subnet`        | 10.0.4.0/24 | Azure OpenAI private endpoint  |
| `acr-subnet`           | 10.0.5.0/24 | ACR (Azure Container Registry) |


### Private DNS Zones
| DNS Zone                                    | Associated Service                                                           |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| `privatelink.vaultcore.azure.net`           | Azure Key Vault                                                              |
| `privatelink.openai.azure.com`              | Azure OpenAI                                                                 |
| `privatelink.azurecr.io`                    | Azure Container Registry                                                     |
| `privatelink.blob.core.windows.net`         | Azure Blob Storage                                                           |
| `privatelink.monitor.azure.com`             | Azure Monitor / App Insights (optional, only needed for full private access) |

## Tips
- Subnet CIDR ranges must not overlap across environments
- Use `main.<env>.bicepparam` to manage environment differences
- Keep secrets and credentials in GitHub **environment-level** secrets

## Contributing
1. Clone the repo
2. Create a feature branch
3. Make changes and test with the appropriate .bicepparam
4. Submit a pull request with a clear description

### Useful Commands

```bash
# Check deployment status
az deployment group show -g myapp-rg -n main

# View container app logs
az containerapp logs show -g myapp-rg -n myapp-dev-ca

# Test private endpoint connectivity
az network private-endpoint-connection list -g myapp-rg

# Get Key Vault secrets (requires permissions)
az keyvault secret list --vault-name myapp-dev-kv-xxxxx
```

## Cleanup
To remove resources from your subscription:

```bash
az group delete --name <resource-group-name> --yes --no-wait
```