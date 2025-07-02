using 'main.bicep'

param environmentName = 'test'
param location = 'eastus'
param useAzureOpenAI = false

param containerImage = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

param storageAccountSku = 'Standard_GRS'
param storageAccountTier = 'Hot'

param logAnalyticsRetentionDays = 30
param logAnalyticsSku = 'PerGB2018'
param logAnalyticsWorkspaceName = 'test-law'

param vnetAddressSpace = '10.1.0.0/16'

param containerAppSubnetPrefix = '10.1.1.0/24'
param storageSubnetPrefix = '10.1.2.0/24'
param keyVaultSubnetPrefix = '10.1.3.0/24'
param openAiSubnetPrefix = '10.1.4.0/24'
param acrSubnetPrefix = '10.1.5.0/24'

param openAiServiceSku = 'S0'
param modelDeploymentCapacity = 30

param modelDeployments = [
  {
    name: 'gpt-4o-mini'
    modelName: 'gpt-4o-mini'
  }
  {
    name: 'text-embedding-ada-002'
    modelName: 'text-embedding-ada-002'
  }
]

param tags = {
  Environment: 'test'
  Project: 'ResumeScreener'
  CreatedBy: 'bieryzt@mail.uc.edu'
}
