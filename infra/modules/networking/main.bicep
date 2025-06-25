param vnetName string
param location string
param vnetAddressPrefix string
param appSubnetPrefix string
param privateEndpointSubnetPrefix string
param nsgName string

module vnet 'vnet.bicep' = {
  name: 'deployVnet'
  params: {
    vnetName: vnetName
    location: location
    vnetAddressPrefix: vnetAddressPrefix
    appSubnetPrefix: appSubnetPrefix
    privateEndpointSubnetPrefix: privateEndpointSubnetPrefix
  }
}

module nsg 'nsg.bicep' = {
  name: 'deployAppNsg'
  params: {
    nsgName: nsgName
    location: location
  }
}

resource subnetUpdate 'Microsoft.Network/virtualNetworks/subnets@2021-05-01' = {
  name: '${vnetName}/appSubnet'
  properties: {
    addressPrefix: appSubnetPrefix
    networkSecurityGroup: {
      id: nsg.outputs.nsgId
    }
  }
  dependsOn: [
    vnet
    nsg
  ]
}

// Outputs
output vnetId string = vnet.outputs.vnetId
output appSubnetId string = vnet.outputs.appSubnetId
output privateEndpointSubnetId string = vnet.outputs.privateEndpointSubnetId
output nsgId string = nsg.outputs.nsgId
