using 'main.bicep'

@description('Name of the Virtual Network')
param vnetName = 'vnet-networking-test-01'

@description('Location for all resources')
param location = 'eastus'

@description('Address space for the Virtual Network')
param vnetAddressPrefix = '10.20.0.0/16'

@description('Address prefix for the app subnet')
param appSubnetPrefix = '10.20.1.0/24'

@description('Address prefix for the private endpoints subnet')
param privateEndpointSubnetPrefix = '10.20.2.0/24'

@description('Name of the NSG')
param nsgName = 'nsg-networking-test-01'
