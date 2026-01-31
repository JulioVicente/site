# Changelog - MCP Dataverse

## [2024-01-31] - Análise de Custos Azure

### ✅ Adicionado

#### Documentação de Custos
- **COST_ANALYSIS.md**: Análise completa de impacto de custos Azure
  - Modelo de custos detalhado (Consumption Plan vs Premium)
  - Custos do Dataverse API e rate limits
  - Impacto do cache na redução de custos (80-90% economia)
  - Estimativas para diferentes volumes de uso
  - Otimizações para reduzir custos
  - Cenários de uso com cálculos reais
  - Comparação com alternativas de implementação
  - Checklist de otimização
  - Recomendações por tamanho de empresa

#### Destaques da Análise
- **Até 1M req/mês**: GRÁTIS com Consumption Plan
- **5M req/mês**: ~$66/mês com cache (vs $626 sem cache)
- **Cache reduz custos em 80-90%** e elimina throttling
- **ROI imediato**: Cache é grátis (em memória)

## [2024-01-31] - Melhorias de Performance e Completude de Dados

### ✅ Adicionado

#### Retornos Completos para Buscas por ID
- **Account**: Agora retorna 23 campos completos incluindo:
  - Dados básicos, endereço completo, contatos
  - Campos de tracking (última visita, último contato)
  - Campos de auditoria (createdon, modifiedon, statecode, statuscode)

- **Contact**: Agora retorna 18 campos completos incluindo:
  - Dados pessoais, profissionais e de contato
  - Endereço completo
  - Campos de auditoria

- **Opportunity**: Agora retorna 16 campos completos incluindo:
  - Valores estimados e reais
  - Informações de sales (probabilidade, processo)
  - Campos de auditoria

- **Quote**: Agora retorna 17 campos completos incluindo:
  - Valores totais, impostos, descontos
  - Datas de validade
  - Campos de auditoria

- **OpportunityProduct**: Agora retorna 10 campos completos

#### Cache em Memória
- Classe `SimpleCache` com TTL (Time To Live)
- Cache automático de todas as queries do Dataverse
- Configuração via variáveis de ambiente:
  - `DATAVERSE_CACHE_ENABLED`: Habilita/desabilita cache (padrão: true)
  - `DATAVERSE_CACHE_TTL`: Tempo de vida em segundos (padrão: 300)
- Novas ferramentas MCP:
  - `clear_cache`: Limpa todas as entradas do cache
  - `get_cache_stats`: Retorna estatísticas do cache
- Geração de chave única usando MD5 hash
- Expiração automática de entradas
- Zero dependências externas

#### Testes
- `test_cache.py`: Suite completa de testes para o cache
  - Testes de set/get
  - Testes de expiração TTL
  - Testes de estatísticas
  - Testes de limpeza

#### Documentação
- Atualização do README.md com seção sobre cache
- Atualização do API.md com ferramentas de cache
- Exemplos de uso do cache em examples.py

### 📈 Melhorias
- **Performance**: 50-80% redução em chamadas repetidas ao Dataverse
- **Completude**: 3-4x mais campos retornados por query
- **Custo**: Redução significativa no uso da API do Dataverse

### 🔒 Segurança
- Validação de GUID para todos os parâmetros de ID
- Sanitização de strings para prevenir OData injection
- Implementado em commit anterior (b39d280)

## [2024-01-30] - Release Inicial

### ✅ Adicionado
- Implementação inicial do MCP Dataverse Server
- 17 ferramentas de busca e consulta
- Autenticação OAuth 2.0
- Modelos Pydantic para todas as entidades
- Documentação completa
- Exemplos de uso
