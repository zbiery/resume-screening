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