targetScope = 'resourceGroup'

@allowed([
  'dev'
  'test'
  'prod'
])
@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region for the deployment')
param location string = resourceGroup().location

@description('Whether or not to deploy an Azure Open AI resource.')
param useAzureOpenAI bool = false

@description('Container image to deploy')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

@allowed([
  'Standard_LRS'	
  'Standard_GRS'	
  'Standard_RAGRS'	
  'Standard_ZRS'	
  'Premium_LRS'	
  'Premium_ZRS'	
  'Standard_GZRS'
  'Standard_RAGZRS'	
])
@description('Storage account SKU')
param storageAccountSku string = 'Standard_LRS'

@allowed([
  'Hot'
  'Cool'
  'Cold'
])
@description('Storage account access tier')
param storageAccountTier string = 'Hot'

@minValue(7)
@maxValue(90)
@description('Log Analytics retention days')
param logAnalyticsRetentionDays int = 30

@description('Log Analytics SKU')
param logAnalyticsSku string = 'PerGB2018'

@description('Virtual network address space')
param vnetAddressSpace string = '10.0.0.0/16'

@description('Container Apps subnet prefix')
param containerAppSubnetPrefix string = '10.0.1.0/24'

@description('Storage subnet prefix')
param storageSubnetPrefix string = '10.0.2.0/24'

@description('Key Vault subnet prefix')
param keyVaultSubnetPrefix string = '10.0.3.0/24'

@description('OpenAI subnet prefix')
param openAiSubnetPrefix string = '10.0.4.0/24'

@description('ACR subnet prefix')
param acrSubnetPrefix string = '10.0.5.0/24'

@allowed([
  'S0'
])
@description('Sku for the OpenAI Service Account')
param openAiServiceSku string = 'S0'

@minValue(1)
@maxValue(300)
@description('OpenAI model deployment capacity')
param modelDeploymentCapacity int = 30

@description('Array of OpenAI model deployments')
param modelDeployments array = [
  {
    name: 'gpt-4o-mini'
    modelName: 'gpt-4o-mini'
  }
  {
    name: 'text-embedding-ada-002'
    modelName: 'text-embedding-ada-002'
  }
]

@description('Tags to apply to all resources')
param tags object = {
  Environment: environmentName
  Project: 'ResumeScreener'
  CreatedBy: 'bieryzt@mail.uc.edu'
}

@description('Optional. Groq API key. Used as a fallback if useAzureOpenAI is set to false.')
@secure()
param groqApiKey string = ''

// Deploy User-Assigned Managed Identity first
module identity 'modules/identity.bicep' = {
  name: 'identity-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
  }
}

// Deploy networking infrastructure
module networking 'modules/networking.bicep' = {
  name: 'networking-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    vnetAddressSpace: vnetAddressSpace
    containerAppSubnetPrefix: containerAppSubnetPrefix
    storageSubnetPrefix: storageSubnetPrefix
    keyVaultSubnetPrefix: keyVaultSubnetPrefix
    openAiSubnetPrefix: openAiSubnetPrefix
    acrSubnetPrefix: acrSubnetPrefix
  }
}

// Deploy monitoring infrastructure
module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    logAnalyticsRetentionDays: logAnalyticsRetentionDays
    logAnalyticsSku: logAnalyticsSku
  }
}

// Deploy Key Vault
module keyVault 'modules/keyvault.bicep' = {
  name: 'keyvault-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    userAssignedIdentityName: identity.outputs.userAssignedIdentityName
    privateEndpointSubnetId: networking.outputs.keyVaultSubnetId
    virtualNetworkId: networking.outputs.vnetId
  }
  dependsOn: [
    identity
    networking
  ]
}

// Deploy Storage Account
module storage 'modules/storage.bicep' = {
  name: 'storage-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    storageAccountSku: storageAccountSku
    storageAccountTier: storageAccountTier
    vnetId: networking.outputs.vnetId
    subnetId: networking.outputs.storageSubnetId
    userAssignedIdentityName: identity.outputs.userAssignedIdentityName
  }
  dependsOn: [
    identity
    networking
  ]
}

// Deploy Azure Container Registry
module acr 'modules/acr.bicep' = {
  name: 'acr-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    subnetId: networking.outputs.acrSubnetId
    userAssignedIdentityName: identity.outputs.userAssignedIdentityName
  }
  dependsOn: [
    identity
    networking
  ]
}

// Deploy OpenAI Service (only if useAzureOpenAI is true)
module openai 'modules/openai.bicep' = if (useAzureOpenAI) {
  name: 'openai-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    userAssignedIdentityName: identity.outputs.userAssignedIdentityName
    subnetId: networking.outputs.openAiSubnetId
    virtualNetworkId: networking.outputs.vnetId
    modelDeploymentCapacity: modelDeploymentCapacity
    modelDeployments: modelDeployments
    openAiServiceSku: openAiServiceSku
  }
  dependsOn: [
    identity
    networking
  ]
}

// If OpenAI is not used, fallback to Groq and store as KV secret.
module groq 'modules/groq.bicep' = if (!useAzureOpenAI) {
  name: 'groq-deployment'
  params: {
    keyVaultName: keyVault.outputs.keyVaultName
    groqApiKey: groqApiKey
  }
  dependsOn: [
    identity
    keyVault
  ]
}

// Deploy Container App (depends on all other services)
module containerApp 'modules/containerapp.bicep' = {
  name: 'containerapp-deployment'
  params: {
    environmentName: environmentName
    location: location
    tags: tags
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsWorkspaceId
    applicationInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
    userAssignedIdentityName: identity.outputs.userAssignedIdentityName
    keyVaultUri: 'https://${keyVault.outputs.keyVaultName}.vault.azure.net/'
    openAiEndpoint: useAzureOpenAI ? (openai.outputs.openAiEndpoint ?? '') : 'https://api.groq.com/openai/v1'
    containerImage: containerImage
    subnetId: networking.outputs.containerAppSubnetId
    acrLoginServer: acr.outputs.loginServer
  }
  dependsOn: [
    identity
    networking
    monitoring
    keyVault
    acr
  ]
}

// Outputs
output resourceGroupName string = resourceGroup().name
output environmentName string = environmentName
output location string = location

// Identity outputs
output userAssignedIdentityId string = identity.outputs.identityId
output userAssignedIdentityClientId string = identity.outputs.clientId
output userAssignedIdentityPrincipalId string = identity.outputs.principalId

// Networking outputs
output vnetId string = networking.outputs.vnetId
output vnetName string = networking.outputs.vnetName

// Monitoring outputs
output logAnalyticsWorkspaceId string = monitoring.outputs.logAnalyticsWorkspaceId
output applicationInsightsId string = monitoring.outputs.applicationInsightsId

// Key Vault outputs
output keyVaultId string = keyVault.outputs.keyVaultId
output keyVaultName string = keyVault.outputs.keyVaultName
output keyVaultUri string = 'https://${keyVault.outputs.keyVaultName}.vault.azure.net/'

// Storage outputs
output storageAccountId string = storage.outputs.storageAccountId
output storageAccountName string = storage.outputs.storageAccountName

// ACR outputs
output acrId string = acr.outputs.acrId
output acrName string = acr.outputs.acrName
output acrLoginServer string = acr.outputs.loginServer

// Conditional OpenAI outputs (only when useAzureOpenAI is true)
output openAiServiceId string = useAzureOpenAI ? openai.outputs.openAiServiceId : ''
output openAiResourceName string = useAzureOpenAI ? openai.outputs.openAiResourceName : ''
output openAiEndpoint string = useAzureOpenAI ? openai.outputs.openAiEndpoint : ''

// Container App outputs
output containerAppId string = containerApp.outputs.containerAppId
output containerAppName string = containerApp.outputs.containerAppName
output containerAppUrl string = containerApp.outputs.containerAppUrl
output containerAppFqdn string = containerApp.outputs.containerAppFqdn
