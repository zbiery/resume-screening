@description('Environment name (e.g., dev, test, prod)')
param environmentName string

@description('Azure region for the deployment')
param location string

@description('Tags to apply to the identity')
param tags object

var userAssignedIdentityName = '${environmentName}-umi'

resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: userAssignedIdentityName
  location: location
  tags: tags
}

output userAssignedIdentityName string = userAssignedIdentityName
output identityId string = userAssignedIdentity.id
output clientId string = userAssignedIdentity.properties.clientId
output principalId string = userAssignedIdentity.properties.principalId
