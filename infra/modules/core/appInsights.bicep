@description('Location for Application Insights')
param location string = resourceGroup().location

@description('Name of the Application Insights resource')
param appInsightsName string = ''

@description('Tags to apply to the resource')
param tags object = {}

@description('Log Analytics workspace resource ID to link App Insights')
param logAnalyticsWorkspaceId string

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspaceId
  }
}

output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output appInsightsConnectionString string = appInsights.properties.ConnectionString
