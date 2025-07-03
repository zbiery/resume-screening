param environmentName string
param location string
param tags object
param vnetAddressSpace string = '10.0.0.0/16'
param containerAppSubnetPrefix string = '10.0.0.0/23' // 10.0.0.0 – 10.0.1.255
param storageSubnetPrefix string = '10.0.2.0/24' // 10.0.2.0 – 10.0.2.255
param keyVaultSubnetPrefix string = '10.0.3.0/24' // 10.0.3.0 – 10.0.3.255
param openAiSubnetPrefix string = '10.0.4.0/24' // 10.0.4.0 – 10.0.4.255
param acrSubnetPrefix string = '10.0.5.0/24' // 10.0.5.0 – 10.0.5.255


// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: '${environmentName}-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressSpace
      ]
    }
    subnets: [
      {
        name: '${environmentName}-container-app-subnet'
        properties: {
          addressPrefix: containerAppSubnetPrefix
          delegations: [
            {
              name: 'Microsoft.App/environments'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: '${environmentName}-storage-subnet'
        properties: {
          addressPrefix: storageSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          serviceEndpoints: [
            {
              service: 'Microsoft.Storage'
              locations: [
                location
              ]
            }
          ]
        }
      }
      {
        name: '${environmentName}-keyvault-subnet'
        properties: {
          addressPrefix: keyVaultSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          serviceEndpoints: [
            {
              service: 'Microsoft.KeyVault'
              locations: [
                location
              ]
            }
          ]
        }
      }
      {
        name: '${environmentName}-openai-subnet'
        properties: {
          addressPrefix: openAiSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          serviceEndpoints: [
            {
              service: 'Microsoft.CognitiveServices'
              locations: [
                location
              ]
            }
          ]
        }
      }
      {
        name: '${environmentName}-acr-subnet'
        properties: {
          addressPrefix: acrSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          serviceEndpoints: [
            {
              service: 'Microsoft.ContainerRegistry'
              locations: [
                location
              ]
            }
          ]
        }
      }
    ]
  }
}

// Network Security Group for Container Apps
resource containerAppNsg 'Microsoft.Network/networkSecurityGroups@2023-09-01' = {
  name: '${environmentName}-container-app-nsg'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'AllowHTTPS'
        properties: {
          priority: 1000
          access: 'Allow'
          direction: 'Inbound'
          destinationPortRange: '443'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
        }
      }
      {
        name: 'AllowHTTP'
        properties: {
          priority: 1100
          access: 'Allow'
          direction: 'Inbound'
          destinationPortRange: '80'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}

// Associate NSGs with subnets
resource containerAppSubnetNsgAssociation 'Microsoft.Network/virtualNetworks/subnets@2023-09-01' = {
  parent: vnet
  name: '${environmentName}-container-app-subnet'
  properties: {
    addressPrefix: containerAppSubnetPrefix
    networkSecurityGroup: {
      id: containerAppNsg.id
    }
    delegations: [
      {
        name: 'Microsoft.App/environments'
        properties: {
          serviceName: 'Microsoft.App/environments'
        }
      }
    ]
  }
}

// Outputs
output vnetId string = vnet.id
output vnetName string = vnet.name
output containerAppSubnetId string = '${vnet.id}/subnets/${environmentName}-container-app-subnet'
output storageSubnetId string = '${vnet.id}/subnets/${environmentName}-storage-subnet'
output keyVaultSubnetId string = '${vnet.id}/subnets/${environmentName}-keyvault-subnet'
output openAiSubnetId string = '${vnet.id}/subnets/${environmentName}-openai-subnet'
output acrSubnetId string = '${vnet.id}/subnets/${environmentName}-acr-subnet'
