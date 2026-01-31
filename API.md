# API Reference - MCP Dataverse

Referência completa da API do MCP Dataverse Server.

## Base URL

```
https://<your-function-app>.azurewebsites.net/api/mcp
```

Para desenvolvimento local:
```
http://localhost:7071/api/mcp
```

## Protocolo

O servidor implementa o protocolo JSON-RPC 2.0 sobre HTTP POST.

### Formato de Requisição

```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": { },
  "id": 1
}
```

### Formato de Resposta

#### Sucesso
```json
{
  "jsonrpc": "2.0",
  "result": { },
  "id": 1
}
```

#### Erro
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Error message"
  },
  "id": 1
}
```

## Métodos Disponíveis

### 1. tools/list

Lista todas as ferramentas disponíveis no servidor MCP.

**Requisição:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

**Resposta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "search_companies_by_name",
        "description": "Search companies (accounts) by name",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "The company name to search for"
            }
          },
          "required": ["name"]
        }
      }
    ]
  },
  "id": 1
}
```

### 2. tools/call

Executa uma ferramenta específica com os argumentos fornecidos.

**Requisição:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "arg1": "value1"
    }
  },
  "id": 1
}
```

**Resposta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "JSON formatted result"
      }
    ]
  },
  "id": 1
}
```

## Ferramentas de Empresas (Accounts)

### search_companies_by_id

Busca uma empresa pelo ID único.

**Argumentos:**
- `account_id` (string, obrigatório): ID da empresa

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_id",
    "arguments": {
      "account_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

### search_companies_by_name

Busca empresas por nome (suporta busca parcial).

**Argumentos:**
- `name` (string, obrigatório): Nome da empresa para buscar

**Exemplo:**
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

### search_companies_by_cnpj

Busca empresas pelo CNPJ (Cadastro Nacional da Pessoa Jurídica).

**Argumentos:**
- `cnpj` (string, obrigatório): Número do CNPJ

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_cnpj",
    "arguments": {
      "cnpj": "12.345.678/0001-90"
    }
  },
  "id": 1
}
```

### search_companies_by_proximity

Busca empresas próximas a um CEP.

**Argumentos:**
- `cep` (string, obrigatório): Código postal (CEP)
- `radius_km` (number, opcional): Raio de busca em quilômetros (padrão: 50)

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_proximity",
    "arguments": {
      "cep": "01310-100",
      "radius_km": 25
    }
  },
  "id": 1
}
```

### search_companies_by_employees_revenue

Busca empresas por número de funcionários e/ou faturamento.

**Argumentos:**
- `min_employees` (integer, opcional): Número mínimo de funcionários
- `max_employees` (integer, opcional): Número máximo de funcionários
- `min_revenue` (number, opcional): Faturamento mínimo
- `max_revenue` (number, opcional): Faturamento máximo

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_employees_revenue",
    "arguments": {
      "min_employees": 50,
      "max_employees": 500,
      "min_revenue": 1000000,
      "max_revenue": 10000000
    }
  },
  "id": 1
}
```

### search_companies_by_days_without_visit

Busca empresas sem visita há X dias.

**Argumentos:**
- `days` (integer, obrigatório): Número de dias sem visita

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_days_without_visit",
    "arguments": {
      "days": 30
    }
  },
  "id": 1
}
```

### search_companies_by_days_without_contact

Busca empresas sem contato há X dias.

**Argumentos:**
- `days` (integer, obrigatório): Número de dias sem contato

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_companies_by_days_without_contact",
    "arguments": {
      "days": 60
    }
  },
  "id": 1
}
```

### list_accounts

Lista todas as contas.

**Argumentos:**
- `top` (integer, opcional): Número máximo de resultados (padrão: 100)

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_accounts",
    "arguments": {
      "top": 50
    }
  },
  "id": 1
}
```

## Ferramentas de Contatos

### search_contacts_by_id

Busca um contato pelo ID único.

**Argumentos:**
- `contact_id` (string, obrigatório): ID do contato

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_contacts_by_id",
    "arguments": {
      "contact_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

### search_contacts_by_name

Busca contatos por nome (suporta busca parcial).

**Argumentos:**
- `name` (string, obrigatório): Nome do contato

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_contacts_by_name",
    "arguments": {
      "name": "João Silva"
    }
  },
  "id": 1
}
```

### search_contacts_by_email

Busca contatos por email (suporta busca parcial).

**Argumentos:**
- `email` (string, obrigatório): Email do contato

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_contacts_by_email",
    "arguments": {
      "email": "joao@example.com"
    }
  },
  "id": 1
}
```

## Ferramentas de Oportunidades

### search_opportunities_by_id

Busca uma oportunidade pelo ID único.

**Argumentos:**
- `opportunity_id` (string, obrigatório): ID da oportunidade

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_opportunities_by_id",
    "arguments": {
      "opportunity_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

### search_opportunities_by_name

Busca oportunidades por nome (suporta busca parcial).

**Argumentos:**
- `name` (string, obrigatório): Nome da oportunidade

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_opportunities_by_name",
    "arguments": {
      "name": "Venda Software"
    }
  },
  "id": 1
}
```

### search_opportunities_by_account

Busca oportunidades relacionadas a uma empresa específica.

**Argumentos:**
- `account_id` (string, obrigatório): ID da empresa

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_opportunities_by_account",
    "arguments": {
      "account_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

## Ferramentas de Cotações

### search_quotes_by_opportunity

Busca cotações relacionadas a uma oportunidade.

**Argumentos:**
- `opportunity_id` (string, obrigatório): ID da oportunidade

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_quotes_by_opportunity",
    "arguments": {
      "opportunity_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

### search_quotes_by_code

Busca cotações pelo código/número da cotação.

**Argumentos:**
- `quote_number` (string, obrigatório): Número da cotação

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_quotes_by_code",
    "arguments": {
      "quote_number": "QUO-2024-001"
    }
  },
  "id": 1
}
```

## Ferramentas de Produtos

### search_products_by_opportunity

Busca produtos relacionados a uma oportunidade.

**Argumentos:**
- `opportunity_id` (string, obrigatório): ID da oportunidade

**Exemplo:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_products_by_opportunity",
    "arguments": {
      "opportunity_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  },
  "id": 1
}
```

## Códigos de Erro

### Códigos JSON-RPC Padrão

- `-32700`: Parse error - JSON inválido
- `-32600`: Invalid Request - Requisição malformada
- `-32601`: Method not found - Método não existe
- `-32602`: Invalid params - Parâmetros inválidos
- `-32603`: Internal error - Erro interno do servidor

### Códigos de Erro do Dataverse

- `401`: Autenticação falhou
- `403`: Acesso negado
- `404`: Entidade não encontrada
- `429`: Rate limit excedido
- `500`: Erro interno do Dataverse

## Limites e Restrições

### Rate Limits

O Dataverse possui limites de taxa baseados em:
- Número de requisições por usuário
- Número de requisições por tenant
- Recursos computacionais consumidos

Limites típicos:
- **Service Protection API Limits**: 6.000 requisições por 5 minutos por usuário
- **Concurrent Requests**: 52 requisições simultâneas por organização

### Limites de Paginação

- Máximo de 5.000 registros por query
- Use `$top` para limitar resultados
- Para mais de 5.000 registros, use paginação com `$skiptoken`

## Autenticação

A autenticação é gerenciada automaticamente pelo servidor usando OAuth 2.0 Client Credentials Flow.

As credenciais devem estar configuradas nas variáveis de ambiente:
- `DATAVERSE_CLIENT_ID`
- `DATAVERSE_CLIENT_SECRET`
- `DATAVERSE_TENANT_ID`
- `DATAVERSE_URL`

## Exemplos com cURL

### Listar ferramentas
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

### Buscar empresa por nome
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_companies_by_name",
      "arguments": {"name": "Contoso"}
    },
    "id": 1
  }'
```

### Buscar contatos por email
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_contacts_by_email",
      "arguments": {"email": "john@example.com"}
    },
    "id": 1
  }'
```

## Exemplos com Python

```python
import requests

def call_mcp_tool(base_url, tool_name, arguments):
    response = requests.post(
        base_url,
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 1
        }
    )
    return response.json()

# Exemplo de uso
result = call_mcp_tool(
    "https://your-function-app.azurewebsites.net/api/mcp",
    "search_companies_by_name",
    {"name": "Contoso"}
)
print(result)
```

## Webhooks e Eventos

Atualmente, o servidor não suporta webhooks. Para notificações em tempo real, considere:
1. Polling periódico
2. Integração com Power Automate
3. Usar Change Tracking do Dataverse

## Versionamento

A API segue versionamento semântico. A versão atual do Dataverse API usada é v9.2.

Para mudanças futuras:
- Mudanças menores serão backwards-compatible
- Mudanças maiores serão comunicadas com antecedência
- Versões antigas serão suportadas por pelo menos 6 meses

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs no Application Insights
2. Consulte a documentação do Dataverse
3. Abra uma issue no GitHub
