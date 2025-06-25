// param environment string
param location string 
param logAnalyticsName string
param appInsightsName string
param storageAccountName string
param containerName string
param tags object 

module logAnalyticsModule './logAnalytics.bicep' = {
  name: 'deployLogAnalytics'
  params: {
    location: location
    logAnalyticsName: logAnalyticsName
    tags: tags
  }
}

module appInsightsModule './appInsights.bicep' = {
  name: 'deployAppInsights'
  params: {
    location: location
    appInsightsName: appInsightsName
    tags: tags
    logAnalyticsWorkspaceId: logAnalyticsModule.outputs.logAnalyticsWorkspaceId
  }
}

module storageModule './storageAccount.bicep' = {
  name: 'deployStorage'
  params: {
    location: location
    storageAccountName: storageAccountName
    tags: tags
  }
}

module blobContainerModule './blobContainer.bicep' = {
  name: 'deployBlobContainer'
  params: {
    storageAccountName: storageAccountName
    containerName: containerName
  }
}

output logAnalyticsWorkspaceId string = logAnalyticsModule.outputs.logAnalyticsWorkspaceId
output logAnalyticsWorkspaceName string = logAnalyticsModule.outputs.logAnalyticsWorkspaceName
output appInsightsInstrumentationKey string = appInsightsModule.outputs.appInsightsInstrumentationKey
output appInsightsConnectionString string = appInsightsModule.outputs.appInsightsConnectionString
output storageAccountId string = storageModule.outputs.storageAccountId
output storageAccountName string = storageModule.outputs.storageAccountName
output blobContainerName string = blobContainerModule.outputs.blobContainerName
