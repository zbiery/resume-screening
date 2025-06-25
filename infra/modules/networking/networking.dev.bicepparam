using 'networking.bicep'

@description('Deployment environment (e.g., dev, test, prod)')
param env = 'dev'

@description('Azure region to deploy resources into')
param location = 'eastus'

@description('Address prefix for the VNet')
param vnetAddressPrefix = '10.0.0.0/16'

@description('Address prefix for the App Service subnet')
param appSubnetPrefix = '10.0.1.0/24'

@description('Address prefix for the Private Endpoint subnet')
param privateEndpointSubnetPrefix = '10.0.2.0/24'
