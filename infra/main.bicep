targetScope = 'subscription'

@description('Base name prefix for resources')
param baseName string = 'dev-01'

@description('Deployment region')
param location string = 'eastus'

var coreRgName = 'rg-core-${baseName}'
var vnetName = 'vnet-${baseName}'

resource coreRg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: coreRgName
  location: location
}

// Deploy VNet and subnets
module network './modules/network.bicep' = {
  name: 'deploy-network'
  scope: coreRg
  params: {
    vnetName: vnetName
    location: location
  }
}
