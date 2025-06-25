@description('Name of the Virtual Network')
param vnetName string

@description('Location for all resources')
param location string = resourceGroup().location

@description('Address space for the Virtual Network')
param vnetAddressPrefix string

@description('Address prefix for the app subnet')
param appSubnetPrefix string

@description('Address prefix for the private endpoints subnet')
param privateEndpointSubnetPrefix string 

resource vnet 'Microsoft.Network/virtualNetworks@2021-05-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressPrefix
      ]
    }
    subnets: [
      {
        name: 'appSubnet'
        properties: {
          addressPrefix: appSubnetPrefix
        }
      }
      {
        name: 'privateEndpointSubnet'
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'  // Required for private endpoints
        }
      }
    ]
  }
}

output vnetId string = vnet.id
output appSubnetId string = '${vnet.id}/subnets/appSubnet'
output privateEndpointSubnetId string = '${vnet.id}/subnets/privateEndpointSubnet'
