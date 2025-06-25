@description('Name of the Storage Account in which to create the blob container')
param storageAccountName string

@description('Name of the Blob container')
param containerName string

@description('Public access level for the container (None, Blob, or Container)')
@allowed([
  'None'
  'Blob'
  'Container'
])
param publicAccess string = 'None'

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccountName}/default/${containerName}'
  properties: {
    publicAccess: publicAccess
  }
}

output blobContainerName string = blobContainer.name
