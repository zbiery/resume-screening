using 'main.bicep'

// @description('Deployment environment name')
// param environment = 'prod'

@description('Location for all core resources')
param location = 'eastus'

@description('Name of the Log Analytics workspace')
param logAnalyticsName  = 'log-core-prod-01'

@description('Name of the Application Insights resource')
param appInsightsName = 'appi-core-prod-01'

@description('Name of the Storage Account')
param storageAccountName = 'stor-${uniqueString('dev-core')}-01'

@description('Name of the Blob container for uploaded files')
param containerName = 'container-uploads-core-test-01'

@description('Tags to apply to all core resources')
param tags  = {
  environment: 'prod'
  owner: 'zach'
  project: 'resume-screener'
}
