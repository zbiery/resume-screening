@description('Name of the VNet')
param vnetName string

@description('Location for the network')
param location string

@description('Address prefix for the VNet')
param vnetAddressPrefix string = '10.0.0.0/16'

@description('Address prefix for the App Service subnet')
param appSubnetPrefix string = '10.0.1.0/24'

@description('Address prefix for the Private Endpoint subnet')
param privateEndpointSubnetPrefix string = '10.0.2.0/24'

// VNet with two subnets
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
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
        name: 'snet-app'
        properties: {
          addressPrefix: appSubnetPrefix
          delegations: [
            {
              name: 'appsvc-delegation'
              properties: {
                serviceName: 'Microsoft.Web/serverFarms'
              }
            }
          ]
        }
      }
      {
        name: 'snet-pe'
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}
