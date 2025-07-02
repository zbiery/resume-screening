@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region for the deployment')
param location string

@description('Tags to apply to all resources')
param tags object

@description('User-assigned managed identity that needs Key Vault access')
param userAssignedIdentityName string

@description('Subnet ID for private endpoint')
param privateEndpointSubnetId string

@description('Virtual Network ID for private DNS zone link')
param virtualNetworkId string

// Key Vault name must be globally unique, let's generate
var keyVaultName = toLower('${environmentName}kv${uniqueString(resourceGroup().id)}')

var dnsZoneName = 'privatelink.vaultcore.azure.net'

// Reference existing UMI
resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: userAssignedIdentityName
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: [] // empty; we'll use RBAC instead of access policies
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    enablePurgeProtection: true
    enableSoftDelete: true
    // networkAcls: {
    //   bypass: 'AzureServices'
    //   defaultAction: 'Deny'
    //   virtualNetworkRules: [
    //     {
    //       id: privateEndpointSubnetId
    //     }
    //   ]
    //   ipRules: []
    // }
  }
  dependsOn: []
}

// Private Endpoint for Key Vault
resource keyVaultPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-09-01' = {
  name: '${environmentName}-kv-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${environmentName}-kv-pls'
        properties: {
          privateLinkServiceId: keyVault.id
          groupIds: [
            'vault'
          ]
        }
      }
    ]
  }
}

// Private DNS Zone for Key Vault
resource keyVaultPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: dnsZoneName
  location: 'global'
  tags: tags
}

// Link Private DNS Zone to VNet
resource keyVaultPrivateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: keyVaultPrivateDnsZone
  name: '${environmentName}-kv-dns-link'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: virtualNetworkId
    }
    registrationEnabled: false
  }
}

// Attach Private DNS Zone to Private Endpoint
resource keyVaultPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-09-01' = {
  parent: keyVaultPrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'vault-dns'
        properties: {
          privateDnsZoneId: keyVaultPrivateDnsZone.id
        }
      }
    ]
  }
}

// RBAC role assignments for the UMI on the Key Vault
resource keyVaultContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, userAssignedIdentity.id, 'keyvault-contributor-role')
  scope: keyVault
  properties: {
    roleDefinitionId: 'b86a8fe4-44ce-4948-aee5-eccb2c155cd7' // Key Vault Contributor
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [
    keyVault
    userAssignedIdentity
  ]
}

resource keyVaultSecretsUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, userAssignedIdentity.id, 'keyvault-secrets-user-role')
  scope: keyVault
  properties: {
    roleDefinitionId: '4633458b-17de-408a-b874-0445c86b69e6' // Key Vault Secrets User
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [
    keyVault
    userAssignedIdentity
  ]
}

output keyVaultId string = keyVault.id
output keyVaultName string = keyVault.name
output keyVaultPrivateEndpointId string = keyVaultPrivateEndpoint.id
output keyVaultPrivateDnsZoneId string = keyVaultPrivateDnsZone.id
