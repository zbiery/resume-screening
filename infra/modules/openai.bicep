@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region for the deployment')
param location string

@description('Tags to apply to all resources')
param tags object

@description('User-assigned managed identity that needs OpenAI access')
param userAssignedIdentityName string

@description('Subnet ID for the private endpoint')
param subnetId string

@description('VNet ID for private DNS zone link')
param virtualNetworkId string

@description('Capacity per deployment (default: 30)')
@minValue(1)
param modelDeploymentCapacity int = 30

@description('Sku for the OpenAI Service Account')
param openAiServiceSku string = 'S0'

@description('Array of model deployments')
param modelDeployments array = [
  {
    name: 'gpt-4o-mini'
    modelName: 'gpt-4o-mini'
  }
  {
    name: 'text-embedding-ada-002'
    modelName: 'text-embedding-ada-002'
  }
]

var dnsZoneName = 'privatelink.openai.azure.com'

// Azure OpenAI resource
resource openAiService 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: '${environmentName}-openai-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: openAiServiceSku
  }
  properties: {
    customSubDomainName: '${environmentName}-openai-${uniqueString(resourceGroup().id)}'
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
      virtualNetworkRules: []
      ipRules: []
    }
  }
}

// Deploy models
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = [for model in modelDeployments: {
  name: model.name
  parent: openAiService
  sku: {
    name: 'Standard'
    capacity: modelDeploymentCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: model.modelName
    }
    raiPolicyName: 'Microsoft.Default'
    versionUpgradeOption: 'OnceCurrentVersionExpired'
  }
}]

// Get UMI
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: userAssignedIdentityName
}

// Assign Cognitive Services AI User role to UMI
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid(userAssignedIdentity.id, openAiService.id, 'openai-user-role')
  scope: openAiService
  properties: {
    roleDefinitionId: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Private DNS zone
resource openAiDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: dnsZoneName
  location: 'global'
  tags: tags
}

// Private DNS zone link to VNet
resource openAiDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: '${environmentName}-openai-dns-link'
  parent: openAiDnsZone
  location: 'global'
  properties: {
    virtualNetwork: {
      id: virtualNetworkId
    }
    registrationEnabled: false
  }
}

// Private endpoint for OpenAI
resource openAiPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-09-01' = {
  name: '${environmentName}-openai-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${environmentName}-openai-pls'
        properties: {
          privateLinkServiceId: openAiService.id
          groupIds: [ 'account' ]
        }
      }
    ]
  }
}

// Attach DNS zone to the private endpoint
resource openAiPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-09-01' = {
  parent: openAiPrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'openai-config'
        properties: {
          privateDnsZoneId: openAiDnsZone.id
        }
      }
    ]
  }
}

// Outputs
output openAiServiceId string = openAiService.id
output openAiResourceName string = openAiService.name
output openAiEndpoint string = openAiService.properties.endpoint
output privateDnsZoneId string = openAiDnsZone.id
