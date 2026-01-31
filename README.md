# MCP Dataverse - Model Context Protocol Server for Microsoft Dataverse

Um servidor MCP (Model Context Protocol) implementado como Azure Function em Python para acesso completo ao Microsoft Dataverse.

## 📋 Funcionalidades

Este projeto implementa um servidor MCP que fornece acesso aos seguintes recursos do Microsoft Dataverse:

### 🏢 Empresas (Accounts)
- Buscar empresas por ID, nome ou CNPJ
- Buscar empresas por proximidade de um CEP
- Buscar empresas por número de funcionários e faturamento
- Buscar empresas por dias sem visita
- Buscar empresas por dias sem contato
- Listar todas as contas

### 👥 Contatos
- Buscar contatos por ID
- Buscar contatos por nome
- Buscar contatos por email

### 💼 Oportunidades
- Buscar oportunidades por ID
- Buscar oportunidades por nome
- Buscar oportunidades por empresa

### 📋 Cotações
- Buscar cotações por oportunidade
- Buscar cotações por código de cotação

### 📦 Produtos
- Buscar produtos de uma oportunidade

### 🔧 Gerenciamento
- Limpar cache de queries
- Obter estatísticas do cache

## ⚡ Cache em Memória

O servidor inclui um sistema de cache em memória simples para melhorar a performance:

- **TTL (Time To Live)**: Cache expira automaticamente após 5 minutos (configurável)
- **Habilitação**: Pode ser habilitado/desabilitado via variável de ambiente
- **Sem dependências externas**: Usa apenas memória da Azure Function
- **Limpeza automática**: Entradas expiradas são removidas automaticamente

**Configuração:**
```bash
DATAVERSE_CACHE_ENABLED=true  # Habilita/desabilita o cache
DATAVERSE_CACHE_TTL=300       # Tempo de vida em segundos (padrão: 5 minutos)
```

**Ferramentas de gerenciamento:**
- `clear_cache`: Limpa todas as entradas do cache
- `get_cache_stats`: Retorna estatísticas (total de entradas e tamanho)

**Nota:** O cache é limpo automaticamente quando a Azure Function é reciclada (warm-up).

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Cliente MCP   │
└────────┬────────┘
         │ HTTP/JSON-RPC
         ▼
┌─────────────────────────┐
│   Azure Function        │
│   (HTTP Trigger)        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   MCP Server            │
│   (mcp_server.py)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Dataverse Client      │
│   (dataverse_client.py) │
└────────┬────────────────┘
         │ REST API
         ▼
┌─────────────────────────┐
│   Microsoft Dataverse   │
│   API (v9.2)            │
└─────────────────────────┘
```

## 📦 Estrutura do Projeto

```
mcp-dataverse/
├── __init__.py                 # Azure Function handler
├── mcp_server.py              # MCP server implementation
├── dataverse_client.py        # Dataverse API client
├── dataverse_models.py        # Pydantic models for entities
├── function.json              # Azure Function configuration
├── host.json                  # Azure Functions host config
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── COST_ANALYSIS.md          # Azure cost impact analysis
├── ARCHITECTURE.md           # Architecture documentation
├── SETUP.md                  # Setup guide
├── DEPLOY.md                 # Deployment guide
└── API.md                    # API reference
```

## 💰 Custos Azure

Esta implementação é altamente custo-efetiva:

- **Até 1M requisições/mês:** GRÁTIS (Consumption Plan)
- **5M requisições/mês:** ~$66/mês
- **10M requisições/mês:** ~$150/mês

O cache em memória reduz custos em **80-90%** comparado a uma implementação sem cache, além de eliminar problemas de throttling do Dataverse.

📊 **[Ver análise completa de custos](COST_ANALYSIS.md)**

## 🚀 Configuração

### Pré-requisitos

- Python 3.9 ou superior
- Azure Functions Core Tools
- Conta Microsoft Dataverse
- Azure App Registration com acesso ao Dataverse

### Configuração do Azure App Registration

1. No portal Azure, crie um novo App Registration
2. Configure as permissões da API:
   - Dynamics CRM → user_impersonation
3. Crie um client secret
4. Anote:
   - Application (client) ID
   - Directory (tenant) ID
   - Client secret value

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/JulioVicente/site.git
cd site
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. Execute localmente:
```bash
func start
```

### Deploy para Azure

1. Crie uma Function App no Azure:
```bash
az functionapp create --resource-group <resource-group> \
  --consumption-plan-location <location> \
  --runtime python --runtime-version 3.9 \
  --functions-version 4 \
  --name <function-app-name> \
  --storage-account <storage-account>
```

2. Configure as variáveis de ambiente no Azure:
```bash
az functionapp config appsettings set --name <function-app-name> \
  --resource-group <resource-group> \
  --settings \
    DATAVERSE_URL="https://your-org.crm.dynamics.com" \
    DATAVERSE_CLIENT_ID="your-client-id" \
    DATAVERSE_CLIENT_SECRET="your-client-secret" \
    DATAVERSE_TENANT_ID="your-tenant-id"
```

3. Deploy:
```bash
func azure functionapp publish <function-app-name>
```

## 📚 Uso

### Estrutura de Requisição MCP

O servidor implementa o protocolo MCP (Model Context Protocol). Todas as requisições seguem o formato JSON-RPC:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_name",
    "arguments": {
      "name": "Contoso"
    }
  },
  "id": 1
}
```

### Exemplos de Uso

#### Listar Ferramentas Disponíveis

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

#### Buscar Empresa por Nome

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_companies_by_name",
      "arguments": {
        "name": "Contoso"
      }
    },
    "id": 1
  }'
```

#### Buscar Empresa por CNPJ

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_companies_by_cnpj",
      "arguments": {
        "cnpj": "12.345.678/0001-90"
      }
    },
    "id": 1
  }'
```

#### Buscar Contatos por Email

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_contacts_by_email",
      "arguments": {
        "email": "john@contoso.com"
      }
    },
    "id": 1
  }'
```

#### Buscar Oportunidades por Empresa

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_opportunities_by_account",
      "arguments": {
        "account_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
    },
    "id": 1
  }'
```

## 🔧 Ferramentas MCP Disponíveis

| Ferramenta | Descrição | Parâmetros |
|-----------|-----------|------------|
| `search_companies_by_id` | Buscar empresa por ID | `account_id` |
| `search_companies_by_name` | Buscar empresa por nome | `name` |
| `search_companies_by_cnpj` | Buscar empresa por CNPJ | `cnpj` |
| `search_companies_by_proximity` | Buscar empresas próximas a um CEP | `cep`, `radius_km` (opcional) |
| `search_companies_by_employees_revenue` | Buscar por funcionários/faturamento | `min_employees`, `max_employees`, `min_revenue`, `max_revenue` |
| `search_companies_by_days_without_visit` | Buscar por dias sem visita | `days` |
| `search_companies_by_days_without_contact` | Buscar por dias sem contato | `days` |
| `list_accounts` | Listar todas as contas | `top` (opcional) |
| `search_contacts_by_id` | Buscar contato por ID | `contact_id` |
| `search_contacts_by_name` | Buscar contato por nome | `name` |
| `search_contacts_by_email` | Buscar contato por email | `email` |
| `search_opportunities_by_id` | Buscar oportunidade por ID | `opportunity_id` |
| `search_opportunities_by_name` | Buscar oportunidade por nome | `name` |
| `search_opportunities_by_account` | Buscar oportunidades por empresa | `account_id` |
| `search_quotes_by_opportunity` | Buscar cotações por oportunidade | `opportunity_id` |
| `search_quotes_by_code` | Buscar cotação por código | `quote_number` |
| `search_products_by_opportunity` | Buscar produtos de oportunidade | `opportunity_id` |

## 🔒 Segurança

- Todas as requisições ao Dataverse são autenticadas via OAuth 2.0
- Os tokens de acesso são armazenados em cache e renovados automaticamente
- As credenciais devem ser armazenadas como variáveis de ambiente
- Recomenda-se usar Azure Key Vault para armazenar secrets em produção

## 📝 Modelo de Dados

### Account (Empresa)
```python
{
    "accountid": "uuid",
    "name": "string",
    "accountnumber": "string",
    "cnpj": "string",
    "numberofemployees": "integer",
    "revenue": "float",
    "address1_postalcode": "string",
    "lastvisitdate": "datetime",
    "lastcontactdate": "datetime"
}
```

### Contact (Contato)
```python
{
    "contactid": "uuid",
    "firstname": "string",
    "lastname": "string",
    "fullname": "string",
    "emailaddress1": "string",
    "telephone1": "string",
    "mobilephone": "string",
    "jobtitle": "string"
}
```

### Opportunity (Oportunidade)
```python
{
    "opportunityid": "uuid",
    "name": "string",
    "customerid": "uuid",
    "estimatedvalue": "float",
    "estimatedclosedate": "datetime",
    "statuscode": "integer"
}
```

### Quote (Cotação)
```python
{
    "quoteid": "uuid",
    "name": "string",
    "quotenumber": "string",
    "opportunityid": "uuid",
    "totalamount": "float",
    "statuscode": "integer"
}
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 📧 Contato

Julio Vicente - [@JulioVicente](https://github.com/JulioVicente)

Link do Projeto: [https://github.com/JulioVicente/site](https://github.com/JulioVicente/site)

## 🙏 Agradecimentos

- [Microsoft Dataverse](https://docs.microsoft.com/en-us/power-apps/developer/data-platform/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/)