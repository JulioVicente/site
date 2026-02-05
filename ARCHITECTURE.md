# Arquitetura do MCP Dataverse

## Visão Geral

O MCP Dataverse é um servidor de Model Context Protocol (MCP) que fornece uma interface padronizada para acessar dados do Microsoft Dataverse. Ele é implementado como uma Azure Function em Python.

## Componentes Principais

### 1. Azure Function Handler (`__init__.py`)

- **Responsabilidade**: Ponto de entrada HTTP para requisições
- **Funcionalidades**:
  - Recebe requisições HTTP POST
  - Valida JSON da requisição
  - Delega processamento para o MCP Server
  - Retorna respostas formatadas

### 2. MCP Server (`mcp_server.py`)

- **Responsabilidade**: Implementação do protocolo MCP
- **Funcionalidades**:
  - Registra ferramentas disponíveis
  - Processa requisições MCP (tools/list, tools/call)
  - Mapeia chamadas de ferramenta para operações do Dataverse
  - Formata respostas no padrão MCP

### 3. Dataverse Client (`dataverse_client.py`)

- **Responsabilidade**: Comunicação com a API do Dataverse
- **Funcionalidades**:
  - Autenticação OAuth 2.0
  - Cache de tokens de acesso
  - Execução de queries OData
  - Métodos específicos para cada tipo de busca

### 4. Modelos de Dados (`dataverse_models.py`)

- **Responsabilidade**: Definição de estruturas de dados
- **Funcionalidades**:
  - Modelos Pydantic para validação
  - Mapeamento de campos do Dataverse
  - Suporte a campos customizados

## Fluxo de Dados

```
1. Cliente HTTP → POST /api/mcp
   Requisição JSON-RPC

2. Azure Function Handler → Valida requisição
   Extrai body JSON

3. MCP Server → Processa comando MCP
   - tools/list: retorna lista de ferramentas
   - tools/call: executa ferramenta

4. Dataverse Client → Executa query
   - Autentica via OAuth
   - Monta query OData
   - Executa requisição HTTP

5. Microsoft Dataverse API → Retorna dados
   JSON com entidades

6. MCP Server → Formata resposta
   Estrutura MCP com conteúdo

7. Azure Function → Retorna HTTP Response
   JSON-RPC response
```

## Autenticação e Autorização

### Fluxo OAuth 2.0 Client Credentials

```
1. Dataverse Client → Solicita token
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
   
   Body:
   - client_id
   - client_secret
   - scope: {dataverse_url}/.default
   - grant_type: client_credentials

2. Azure AD → Valida credenciais
   Verifica app registration e permissões

3. Azure AD → Retorna token
   access_token com validade de 1 hora

4. Dataverse Client → Armazena token
   Cache em memória até expiração

5. Requisições subsequentes → Usa token
   Header: Authorization: Bearer {token}
```

### Permissões Necessárias

- **Dynamics CRM**: user_impersonation
- **Scope**: {dataverse_url}/.default

## Estrutura de Queries OData

O Dataverse usa OData v4.0 para queries. Exemplos:

### Busca Simples
```
GET /api/data/v9.2/accounts?$filter=name eq 'Contoso'
```

### Busca com Contains
```
GET /api/data/v9.2/accounts?$filter=contains(name, 'Contoso')
```

### Busca com Operadores
```
GET /api/data/v9.2/accounts?$filter=numberofemployees ge 100 and revenue le 1000000
```

### Busca com Relacionamentos
```
GET /api/data/v9.2/opportunities?$filter=_customerid_value eq '...'
```

## Padrões de Design

### 1. Singleton Pattern
- DataverseClient mantém instância única de conexão
- Cache de tokens de acesso

### 2. Factory Pattern
- MCPServer cria e registra ferramentas dinamicamente
- Mapeamento tool_name → método

### 3. Strategy Pattern
- Diferentes estratégias de busca (por ID, nome, etc.)
- Implementadas como métodos do DataverseClient

### 4. DTO Pattern
- Modelos Pydantic para transferência de dados
- Validação automática de tipos

## Escalabilidade

### Considerações

1. **Cache de Tokens**: Reduz chamadas ao Azure AD
2. **Stateless**: Function é stateless, escalável horizontalmente
3. **Connection Pooling**: Requests usa pool de conexões HTTP
4. **Paginação**: Suporte a $top para limitar resultados

### Limites

- Azure Functions Consumption Plan: 230 segundos de timeout
- Dataverse API: Rate limits por tenant
- OData: Limite de 5000 registros por query

## Monitoramento

### Logs

- Application Insights integrado via Azure Functions
- Logs de erro e info no logger Python
- Rastreamento de requisições HTTP

### Métricas Recomendadas

- Tempo de resposta por ferramenta
- Taxa de erro por tipo
- Número de chamadas por ferramenta
- Cache hit rate de tokens

## Segurança

### Camadas de Segurança

1. **Transport**: HTTPS obrigatório
2. **Autenticação**: OAuth 2.0 client credentials
3. **Autorização**: Permissões do app registration
4. **Validação**: Input validation via Pydantic
5. **Secrets**: Armazenados em variáveis de ambiente

### Melhores Práticas

- Nunca commitar secrets no código
- Usar Azure Key Vault em produção
- Rotacionar client secrets regularmente
- Limitar permissões ao mínimo necessário
- Habilitar logging de auditoria no Dataverse

## Extensibilidade

### Adicionar Nova Ferramenta

1. Criar método no DataverseClient
2. Registrar ferramenta no MCPServer._register_tools()
3. Adicionar case no MCPServer._execute_tool()
4. Documentar na README

### Adicionar Nova Entidade

1. Criar modelo Pydantic em dataverse_models.py
2. Adicionar métodos de query no DataverseClient
3. Criar ferramentas correspondentes no MCPServer

## Troubleshooting

### Erros Comuns

1. **401 Unauthorized**
   - Verificar credenciais OAuth
   - Verificar permissões do app registration
   - Verificar expiração de client secret

2. **404 Not Found**
   - Verificar URL do Dataverse
   - Verificar nome da entidade
   - Verificar se entidade existe no ambiente

3. **500 Internal Server Error**
   - Verificar logs no Application Insights
   - Verificar formato da query OData
   - Verificar conexão com Dataverse

## Referências

- [Microsoft Dataverse Web API](https://docs.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
- [OData v4.0 Specification](https://www.odata.org/documentation/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
