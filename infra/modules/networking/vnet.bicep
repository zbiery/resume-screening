param env string
param location string
param vnetAddressPrefix string 
param appSubnetPrefix string 
param privateEndpointSubnetPrefix string 

var vnetName = 'vnet-${env}-01'
var subnetAppName = 'snet-app-${env}-01'
var subnetPeName = 'snet-pe-${env}-01'
var nsgAppName = 'nsg-app-${env}-01'
var nsgPeName = 'nsg-pe-${env}-01'

resource nsgApp 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
  name: nsgAppName
  location: location
  properties: {}
}

resource nsgPe 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
  name: nsgPeName
  location: location
  properties: {}
}

resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [ vnetAddressPrefix ]
    }
    subnets: [
      {
        name: subnetAppName
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
          networkSecurityGroup: {
            id: nsgApp.id
          }
        }
      }
      {
        name: subnetPeName
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          networkSecurityGroup: {
            id: nsgPe.id
          }
        }
      }
    ]
  }
}
