@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region for the deployment')
param location string

@description('Tags to apply to all resources')
param tags object

@description('Subnet ID for private endpoint')
param subnetId string

@description('User-assigned managed identity name to assign AcrPull role')
param userAssignedIdentityName string

var dnsZoneName = 'privatelink.azurecr.io'

// Private DNS Zone for ACR
resource acrPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: dnsZoneName
  location: 'global'
  tags: tags
}

// Azure Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: '${replace(environmentName, '-', '')}acr${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: 'Premium'
  }
  properties: {
    adminUserEnabled: false
    networkRuleSet: {
      defaultAction: 'Deny'
      ipRules: []
    }
    publicNetworkAccess: 'Disabled'
    zoneRedundancy: 'Disabled'
  }
}

// Private Endpoint for ACR
resource acrPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-09-01' = {
  name: '${environmentName}-acr-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${environmentName}-acr-pls'
        properties: {
          privateLinkServiceId: containerRegistry.id
          groupIds: [
            'registry'
          ]
        }
      }
    ]
  }
}

// Private DNS Zone Group for ACR Private Endpoint
resource acrPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-09-01' = {
  parent: acrPrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'acr-config'
        properties: {
          privateDnsZoneId: acrPrivateDnsZone.id
        }
      }
    ]
  }
}

// Reference existing UMI
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: userAssignedIdentityName
}

// RBAC role assignment: AcrPull for UMI
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(containerRegistry.id, userAssignedIdentity.id, 'acr-pull-role')
  properties: {
    roleDefinitionId: '7f951dda-4ed3-4680-a7ca-43fe172d538d'
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [
    containerRegistry
    userAssignedIdentity
  ]
}

// Outputs
output acrId string = containerRegistry.id
output acrName string = containerRegistry.name
output loginServer string = containerRegistry.properties.loginServer
output acrPrivateDnsZoneId string = acrPrivateDnsZone.id
