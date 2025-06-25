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
