using 'main.bicep'

param environmentName = 'dev'
param location = 'eastus'

param containerImage = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

param storageAccountSku = 'Standard_LRS'
param storageAccountTier = 'Hot'

param logAnalyticsRetentionDays = 30
param logAnalyticsSku = 'PerGB2018'

param vnetAddressSpace = '10.0.0.0/16'

param containerAppSubnetPrefix = '10.0.1.0/24'
param storageSubnetPrefix = '10.0.2.0/24'
param keyVaultSubnetPrefix = '10.0.3.0/24'
param openAiSubnetPrefix = '10.0.4.0/24'
param acrSubnetPrefix = '10.0.5.0/24'

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
  Environment: 'dev'
  Project: 'ResumeScreener'
  CreatedBy: 'bieryzt@mail.uc.edu'
}
