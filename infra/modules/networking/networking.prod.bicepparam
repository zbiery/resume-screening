using 'main.bicep'

@description('Name of the Virtual Network')
param vnetName = 'vnet-networking-prod-01'

@description('Location for all resources')
param location = 'eastus'

@description('Address space for the Virtual Network')
param vnetAddressPrefix = '10.30.0.0/16'

@description('Address prefix for the app subnet')
param appSubnetPrefix = '10.30.1.0/24'

@description('Address prefix for the private endpoints subnet')
param privateEndpointSubnetPrefix = '10.30.2.0/24'

@description('Name of the NSG')
param nsgName = 'nsg-networking-prod-01'
