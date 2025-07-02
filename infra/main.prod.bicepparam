using 'main.bicep'

param environmentName = 'prod'
param location = 'eastus'
param useAzureOpenAI = false

param containerImage = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

param storageAccountSku = 'Standard_RAGZRS'
param storageAccountTier = 'Hot'

param logAnalyticsRetentionDays = 60
param logAnalyticsSku = 'PerGB2018'

param vnetAddressSpace = '10.2.0.0/16'

param containerAppSubnetPrefix = '10.2.1.0/24'
param storageSubnetPrefix = '10.2.2.0/24'
param keyVaultSubnetPrefix = '10.2.3.0/24'
param openAiSubnetPrefix = '10.2.4.0/24'
param acrSubnetPrefix = '10.2.5.0/24'

param openAiServiceSku = 'S0'
param modelDeploymentCapacity = 100

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
  Environment: 'prod'
  Project: 'ResumeScreener'
  CreatedBy: 'bieryzt@mail.uc.edu'
}
