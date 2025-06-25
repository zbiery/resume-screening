# structure
```
infra
├── main.bicep                   # Orchestrator module, calls all resource modules
├── parameters
│   ├── dev.parameters.json      # Parameter values for dev environment
│   ├── test.parameters.json     # Parameter values for test environment
│   └── prod.parameters.json     # Parameter values for prod environment
├── modules
│   ├── resourceGroup.bicep      # Creates the resource group
│   ├── network.bicep            # Creates VNet and subnets
│   ├── storage.bicep            # Creates Storage Account for blobs, logs, etc.
│   ├── cosmosdb.bicep           # Creates Cosmos DB (or SQL DB) for data storage
│   ├── openai.bicep             # Deploys Azure OpenAI service
│   ├── keyvault.bicep           # Creates Key Vault and access policies
│   ├── containerRegistry.bicep  # Creates Azure Container Registry for Docker images
│   ├── containerAppsEnv.bicep   # Creates Container Apps Environment (infrastructure for container apps)
│   ├── containerApps.bicep      # Deploys Container Apps (API and UI containers)
│   └── apiManagement.bicep      # Creates API Management service for API gateway
└── README.md                    # Documentation and instructions for infra deployment
```

before doing anything you must have an active azure account

VSCode
AzureCLI

project is set up for 3 different environments -- these are managed at the subscription level
make your subscriptions for dev, test, and prod within the [azure portal](https://www.portal.azure.com)

once subs are created, login to the azure portal and choose the subscription you wish to work with
```bash
az login
```

save your sub id as an environment secret in your github repo

before deploying any resources, we must do 2 things:
1. create our resource groups at the subscription level
2. create our service principal for our deployer (github actions)

Run this to create the resource groups within your active subscription. Do not forget to alter the parameters file to point at the correct biccepparam file for your environment depending on your subscription. Additionally, you may optionally change the location.

```bash
az deployment sub create \
  --location <location> \
  --template-file infra/modules/resourceGroups/main.bicep \
  --parameters infra/modules/resourceGroups/resourceGroups.<env>.bicepparam
```

Create a service principal (deployer) for each environment
```bash
az ad sp create-for-rbac --name "github-deployer-<env>" \
  --role "Contributor" \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth
```

to deploy resources run the appropriate workflow for your environment

it should be in order of 
1. core
2. networking
3. openai
4. containerApp
5. 


