# Guia de Deploy para Azure

Este guia detalha como fazer o deploy do MCP Dataverse no Azure.

## Pré-requisitos

- Azure CLI instalado ([Instalar Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- Azure Functions Core Tools instalado ([Instalar Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local))
- Python 3.9 ou superior
- Conta Azure ativa

## Opção 1: Deploy via Azure Functions Core Tools

### Passo 1: Login no Azure

```bash
az login
```

### Passo 2: Criar Resource Group

```bash
az group create --name mcp-dataverse-rg --location eastus
```

### Passo 3: Criar Storage Account

```bash
az storage account create \
  --name mcpdataversestorage \
  --resource-group mcp-dataverse-rg \
  --location eastus \
  --sku Standard_LRS
```

### Passo 4: Criar Function App

```bash
az functionapp create \
  --resource-group mcp-dataverse-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name mcp-dataverse-func \
  --storage-account mcpdataversestorage \
  --os-type Linux
```

### Passo 5: Configurar Variáveis de Ambiente

```bash
az functionapp config appsettings set \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --settings \
    DATAVERSE_URL="https://your-org.crm.dynamics.com" \
    DATAVERSE_CLIENT_ID="your-client-id" \
    DATAVERSE_CLIENT_SECRET="your-client-secret" \
    DATAVERSE_TENANT_ID="your-tenant-id"
```

### Passo 6: Deploy da Function

```bash
func azure functionapp publish mcp-dataverse-func
```

### Passo 7: Testar o Deploy

```bash
# Obter a URL da função
FUNCTION_URL=$(az functionapp function show \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --function-name mcp_server \
  --query "invokeUrlTemplate" -o tsv)

# Testar lista de ferramentas
curl -X POST "${FUNCTION_URL}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Opção 2: Deploy via Portal Azure

### Passo 1: Criar Function App no Portal

1. Acesse o [Portal Azure](https://portal.azure.com)
2. Clique em "Create a resource"
3. Busque por "Function App"
4. Preencha os detalhes:
   - **Resource Group**: Crie novo ou selecione existente
   - **Function App name**: `mcp-dataverse-func`
   - **Runtime stack**: Python
   - **Version**: 3.9
   - **Region**: East US (ou sua preferência)
   - **Operating System**: Linux
   - **Plan type**: Consumption (Serverless)

5. Clique em "Review + create" e depois "Create"

### Passo 2: Configurar Variáveis de Ambiente

1. No Function App criado, vá para **Configuration**
2. Adicione as seguintes Application Settings:
   - `DATAVERSE_URL`
   - `DATAVERSE_CLIENT_ID`
   - `DATAVERSE_CLIENT_SECRET`
   - `DATAVERSE_TENANT_ID`

3. Clique em "Save"

### Passo 3: Deploy do Código

#### Opção 3A: Via VS Code

1. Instale a extensão "Azure Functions" no VS Code
2. Abra o projeto no VS Code
3. Pressione F1 e selecione "Azure Functions: Deploy to Function App"
4. Selecione sua subscription e Function App
5. Confirme o deploy

#### Opção 3B: Via GitHub Actions

Crie um arquivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure Functions

on:
  push:
    branches:
      - main

env:
  AZURE_FUNCTIONAPP_NAME: mcp-dataverse-func
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.'
  PYTHON_VERSION: '3.9'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: 'Checkout GitHub Action'
      uses: actions/checkout@v3

    - name: Setup Python ${{ env.PYTHON_VERSION }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: 'Resolve Project Dependencies'
      shell: bash
      run: |
        pushd './${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}'
        python -m pip install --upgrade pip
        pip install -r requirements.txt --target=".python_packages/lib/site-packages"
        popd

    - name: 'Run Azure Functions Action'
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
        package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
        scm-do-build-during-deployment: true
        enable-oryx-build: true
```

Para usar GitHub Actions, você precisa:
1. No Portal Azure, vá para o Function App
2. Vá para "Deployment Center"
3. Clique em "Download publish profile"
4. No GitHub, vá para Settings → Secrets → Actions
5. Crie um secret chamado `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` com o conteúdo do arquivo baixado

## Opção 3: Deploy via Azure DevOps

### Criar Pipeline YAML

```yaml
trigger:
  branches:
    include:
    - main

variables:
  azureSubscription: 'your-service-connection'
  functionAppName: 'mcp-dataverse-func'
  pythonVersion: '3.9'

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '$(pythonVersion)'
  displayName: 'Use Python $(pythonVersion)'

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt --target="./.python_packages/lib/site-packages"
  displayName: 'Install dependencies'

- task: AzureFunctionApp@1
  inputs:
    azureSubscription: '$(azureSubscription)'
    appType: 'functionAppLinux'
    appName: '$(functionAppName)'
    package: '$(System.DefaultWorkingDirectory)'
    runtimeStack: 'PYTHON|3.9'
  displayName: 'Deploy to Azure Functions'
```

## Configurações de Produção

### 1. Habilitar Application Insights

```bash
# Criar Application Insights
az monitor app-insights component create \
  --app mcp-dataverse-insights \
  --location eastus \
  --resource-group mcp-dataverse-rg

# Obter Instrumentation Key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app mcp-dataverse-insights \
  --resource-group mcp-dataverse-rg \
  --query "instrumentationKey" -o tsv)

# Configurar no Function App
az functionapp config appsettings set \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="${INSTRUMENTATION_KEY}"
```

### 2. Configurar Managed Identity

```bash
# Habilitar System-assigned Managed Identity
az functionapp identity assign \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg
```

### 3. Usar Azure Key Vault para Secrets

```bash
# Criar Key Vault
az keyvault create \
  --name mcp-dataverse-kv \
  --resource-group mcp-dataverse-rg \
  --location eastus

# Adicionar secrets
az keyvault secret set \
  --vault-name mcp-dataverse-kv \
  --name dataverse-client-secret \
  --value "your-client-secret"

# Dar permissão para o Function App acessar o Key Vault
PRINCIPAL_ID=$(az functionapp identity show \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --query principalId -o tsv)

az keyvault set-policy \
  --name mcp-dataverse-kv \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list

# Atualizar configuração para usar Key Vault
az functionapp config appsettings set \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --settings \
    DATAVERSE_CLIENT_SECRET="@Microsoft.KeyVault(SecretUri=https://mcp-dataverse-kv.vault.azure.net/secrets/dataverse-client-secret/)"
```

### 4. Configurar Custom Domain (Opcional)

```bash
# Adicionar custom domain
az functionapp config hostname add \
  --webapp-name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --hostname api.yourdomain.com

# Habilitar HTTPS
az functionapp update \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg \
  --set httpsOnly=true
```

## Monitoramento e Logs

### Ver Logs em Tempo Real

```bash
func azure functionapp logstream mcp-dataverse-func
```

### Consultar Application Insights

No Portal Azure:
1. Vá para o Application Insights
2. Clique em "Logs"
3. Execute queries KQL:

```kql
// Ver últimas requisições
requests
| where timestamp > ago(1h)
| order by timestamp desc
| take 100

// Ver erros
exceptions
| where timestamp > ago(1h)
| order by timestamp desc

// Ver performance
requests
| where timestamp > ago(1h)
| summarize avg(duration), percentiles(duration, 50, 95, 99) by name
```

## Troubleshooting

### Erro: "Function App not found"

Verifique se o nome está correto e se você está na subscription correta:
```bash
az account show
az functionapp list --query "[].name"
```

### Erro: "Deployment failed"

Verifique os logs de deployment:
```bash
func azure functionapp logstream mcp-dataverse-func
```

### Erro: "401 Unauthorized" do Dataverse

Verifique se as configurações estão corretas:
```bash
az functionapp config appsettings list \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg
```

## Rollback de Deploy

Se houver problemas, faça rollback para versão anterior:

```bash
# Listar deployments
az functionapp deployment list \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg

# Rollback para deployment anterior
az functionapp deployment source sync \
  --name mcp-dataverse-func \
  --resource-group mcp-dataverse-rg
```

## Limpeza de Recursos

Para deletar todos os recursos criados:

```bash
az group delete --name mcp-dataverse-rg --yes --no-wait
```

## Recursos Adicionais

- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Functions Best Practices](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices)
- [Monitoring Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-monitoring)
