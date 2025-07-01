@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region')
param location string

@description('Tags to apply to all resources')
param tags object

@description('Storage account SKU (e.g., Standard_LRS)')
param storageAccountSku string

@description('Storage account access tier (Hot or Cool)')
param storageAccountTier string

@description('VNet resource ID')
param vnetId string

@description('Subnet ID for private endpoint')
param subnetId string

@description('The name of the user-assigned managed identity to grant Blob Data Contributor role')
param userAssignedIdentityName string

var dnsZoneName string = 'privatelink.blob.core.windows.net'

// Storage account (no system assigned identity)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${replace(environmentName, '-', '')}sa${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: storageAccountSku
  }
  kind: 'StorageV2'
  properties: {
    defaultToOAuthAuthentication: true
    allowCrossTenantReplication: false
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false // Force token-only auth
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
      virtualNetworkRules: []
      ipRules: []
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: storageAccountTier
    publicNetworkAccess: 'Disabled'
  }
}

// Blob container
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/resumes'
  properties: {
    publicAccess: 'None'
  }
  dependsOn: [
    storageAccount
  ]
}

// Private DNS zones
resource blobDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: dnsZoneName
  location: 'global'
  tags: tags
}

// DNS links to VNet
resource blobDnsVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: blobDnsZone
  name: '${environmentName}-blob-dns-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnetId
    }
  }
}

// Private Endpoints for blob and file
resource blobPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${storageAccount.name}-blob-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'blob-link'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: [ 'blob' ]
        }
      }
    ]
  }
}

// Private DNS zone groups for private endpoints
resource blobZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  name: 'blob-dns-zone-group'
  parent: blobPrivateEndpoint
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'blob'
        properties: {
          privateDnsZoneId: blobDnsZone.id
        }
      }
    ]
  }
}

// Get UMI
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: userAssignedIdentityName
}

// RBAC assignment: grant Blob Data Contributor to user-assigned managed identity
resource blobDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, userAssignedIdentity.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [
    storageAccount
    userAssignedIdentity
  ]
}

// Outputs
output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name
output blobContainerName string = blobContainer.name
