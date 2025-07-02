@description('Key Vault name for storing Groq API key')
param keyVaultName string

@description('Groq API key')
@secure()
param groqApiKey string

resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' existing = {
  name: keyVaultName
}

resource secret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'GroqApiKey'
  properties: {
    value: groqApiKey
  }
}

output groqSecretUri string = secret.properties.secretUri
