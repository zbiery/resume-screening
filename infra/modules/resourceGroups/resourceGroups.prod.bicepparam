using 'main.bicep'

@description('Deployment environment name')
param environment = 'prod'

@description('Location for all core resources')
param location = 'eastus'

@description('Tags to apply to all core resources')
param tags  = {
  environment: environment
  owner: 'zach'
  project: 'resume-screener'
}
