targetScope = 'subscription'

@description('Environment name (e.g., dev, test, prod)')
param environment string

@description('Azure location for resource groups')
param location string = 'eastus'

@description('Tags to apply to all resource groups')
param tags object = {}

resource coreRg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-core-${environment}'
  location: location
  tags: tags
}

resource networkingRg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-networking-${environment}'
  location: location
  tags: tags
}

resource appRg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-app-${environment}'
  location: location
  tags: tags
}

resource openaiRg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-openai-${environment}'
  location: location
  tags: tags
}

output coreResourceGroupName string = coreRg.name
output networkingResourceGroupName string = networkingRg.name
output appResourceGroupName string = appRg.name
output openaiResourceGroupName string = openaiRg.name
