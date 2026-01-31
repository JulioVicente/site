# Guia de Configuração do Microsoft Dataverse

Este guia detalha como configurar o Microsoft Dataverse e criar um App Registration no Azure para usar com o MCP Dataverse.

## Pré-requisitos

- Assinatura do Microsoft Azure
- Ambiente Dataverse (Power Apps/Dynamics 365)
- Permissões de administrador no Azure AD

## Passo 1: Criar App Registration no Azure

1. Acesse o [Portal Azure](https://portal.azure.com)

2. Navegue até **Azure Active Directory** → **App registrations** → **New registration**

3. Configure o registro:
   - **Name**: `MCP Dataverse Server`
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: (deixe em branco para aplicação server-to-server)

4. Clique em **Register**

5. Anote os seguintes valores da página de Overview:
   - **Application (client) ID**
   - **Directory (tenant) ID**

## Passo 2: Criar Client Secret

1. No App Registration criado, vá para **Certificates & secrets**

2. Clique em **New client secret**

3. Configure:
   - **Description**: `MCP Dataverse Secret`
   - **Expires**: Escolha o período (recomendado: 12 meses)

4. Clique em **Add**

5. **IMPORTANTE**: Copie o **Value** do secret imediatamente. Ele não será exibido novamente.

## Passo 3: Configurar Permissões da API

1. No App Registration, vá para **API permissions**

2. Clique em **Add a permission**

3. Selecione **Dynamics CRM**

4. Selecione **Delegated permissions**

5. Marque a permissão:
   - ☑ **user_impersonation**

6. Clique em **Add permissions**

7. Clique em **Grant admin consent** para conceder as permissões

## Passo 4: Criar Usuário Aplicação no Dataverse

1. Acesse o [Power Platform Admin Center](https://admin.powerplatform.microsoft.com)

2. Selecione o ambiente desejado

3. Vá para **Settings** → **Users + permissions** → **Application users**

4. Clique em **+ New app user**

5. Configure:
   - **App**: Selecione o App Registration criado
   - **Business unit**: Selecione a unidade de negócio
   - **Security roles**: Adicione as roles necessárias (ex: System Administrator)

6. Clique em **Create**

## Passo 5: Obter URL do Dataverse

1. No Power Platform Admin Center, selecione seu ambiente

2. Vá para **Details**

3. Copie a **Environment URL** (exemplo: `https://org123456.crm.dynamics.com`)

## Passo 6: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# Substitua pelos valores copiados nas etapas anteriores
DATAVERSE_URL=https://org123456.crm.dynamics.com
DATAVERSE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
DATAVERSE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATAVERSE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Configuração do Azure Functions
FUNCTIONS_WORKER_RUNTIME=python
```

## Passo 7: Configurar Campos Customizados (Opcional)

Se você está usando campos customizados no Dataverse para CNPJ, última visita, etc., configure-os:

1. Acesse o [Power Apps Portal](https://make.powerapps.com)

2. Selecione o ambiente

3. Vá para **Tables** → **Account**

4. Adicione os campos customizados:

### Campo CNPJ
- **Display name**: CNPJ
- **Name**: `new_cnpj`
- **Data type**: Text
- **Maximum length**: 18

### Campo Last Visit Date
- **Display name**: Last Visit Date
- **Name**: `new_lastvisitdate`
- **Data type**: Date and Time
- **Format**: Date Only

### Campo Last Contact Date
- **Display name**: Last Contact Date
- **Name**: `new_lastcontactdate`
- **Data type**: Date and Time
- **Format**: Date Only

5. Clique em **Save Table**

## Passo 8: Testar Conexão

Execute o seguinte script Python para testar a conexão:

```python
import os
from dotenv import load_dotenv
from dataverse_client import DataverseClient

# Carregar variáveis de ambiente
load_dotenv()

# Criar cliente
client = DataverseClient()

# Testar listagem de contas
try:
    accounts = client.list_accounts(top=5)
    print(f"✓ Conexão bem-sucedida! Encontradas {len(accounts)} contas.")
    for account in accounts:
        print(f"  - {account.get('name', 'N/A')}")
except Exception as e:
    print(f"✗ Erro na conexão: {str(e)}")
```

## Troubleshooting

### Erro: "AADSTS700016: Application not found"

**Causa**: O App Registration não foi encontrado no tenant.

**Solução**: Verifique se o `DATAVERSE_CLIENT_ID` está correto.

### Erro: "AADSTS7000215: Invalid client secret"

**Causa**: O client secret está incorreto ou expirado.

**Solução**: 
1. Crie um novo client secret no Azure Portal
2. Atualize a variável `DATAVERSE_CLIENT_SECRET`

### Erro: "401 Unauthorized" nas chamadas ao Dataverse

**Causa**: O usuário da aplicação não tem permissões suficientes.

**Solução**: 
1. Verifique se o Application User foi criado no Dataverse
2. Verifique se as Security Roles adequadas foram atribuídas
3. Garanta que o admin consent foi concedido para as permissões da API

### Erro: "Principal user is missing prvRead privilege"

**Causa**: O Application User não tem permissão de leitura na entidade.

**Solução**: 
1. Vá para o Application User no Power Platform Admin Center
2. Adicione ou ajuste as Security Roles para incluir permissões de leitura

## Segurança em Produção

### Usar Azure Key Vault

Para ambientes de produção, recomenda-se usar Azure Key Vault:

1. Crie um Azure Key Vault

2. Adicione os secrets:
   - `dataverse-client-id`
   - `dataverse-client-secret`
   - `dataverse-tenant-id`
   - `dataverse-url`

3. Configure o Function App para acessar o Key Vault:
   - Habilite Managed Identity no Function App
   - Conceda permissão "Get" e "List" secrets ao Managed Identity

4. Referencie os secrets no Function App:
```bash
DATAVERSE_CLIENT_SECRET=@Microsoft.KeyVault(SecretUri=https://your-vault.vault.azure.net/secrets/dataverse-client-secret/)
```

### Rotação de Secrets

1. Configure alertas para expiração de client secrets

2. Crie um novo client secret antes da expiração

3. Atualize o Key Vault ou variáveis de ambiente

4. Aguarde propagação (pode levar alguns minutos)

5. Delete o secret antigo após confirmar funcionamento

## Permissões Mínimas Recomendadas

Para seguir o princípio do menor privilégio, crie uma Security Role customizada com apenas as permissões necessárias:

### Leitura de Dados
- Account: Read
- Contact: Read
- Opportunity: Read
- Quote: Read
- Product: Read
- Opportunity Product: Read

### Sem Permissões de Escrita
- Não conceda permissões de Create, Write, Delete, Append, Assign ou Share

## Monitoramento

Configure alertas para:
- Falhas de autenticação OAuth
- Rate limiting do Dataverse
- Expiração de client secrets
- Alterações em Application Users

## Recursos Adicionais

- [Dataverse Web API Overview](https://docs.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
- [Authenticate with Microsoft Dataverse](https://docs.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth)
- [Azure AD Application Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Power Platform Security](https://docs.microsoft.com/en-us/power-platform/admin/security/)
