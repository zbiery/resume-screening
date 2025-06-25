using 'main.bicep'

// @description('Deployment environment name')
// param environment = 'dev'

@description('Location for all core resources')
param location = 'eastus'

@description('Name of the Log Analytics workspace')
param logAnalyticsName  = 'log-core-dev-01'

@description('Name of the Application Insights resource')
param appInsightsName = 'appi-core-dev-01'

@description('Name of the Storage Account')
param storageAccountName = 'stor-${uniqueString('dev-core')}-01'

@description('Name of the Blob container for uploaded files')
param containerName = 'container-uploads-core-dev-01'

@description('Tags to apply to all core resources')
param tags  = {
  environment: 'dev'
  owner: 'zach'
  project: 'resume-screener'
}
