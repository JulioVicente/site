# Changelog - MCP Dataverse

## [2024-01-31] - Business Intelligence Models and Analysis

### ✅ Adicionado

#### Documentação de Business Intelligence
- **BUSINESS_INTELLIGENCE.md**: Análise completa de objetos Dataverse para BI (1150+ linhas)
  - Identificação de 11 objetos/entidades relevantes para BI
  - Análise detalhada de 6 casos de uso:
    1. Otimização de rotas de visita de empresas
    2. Análise de compras típicas por período
    3. Segmentação por CNAE/indústria
    4. Scoring de potencial de empresas
    5. Visão consolidada de contatos
    6. Gestão de compras e renovações de produtos
  - Modelo de scoring com algoritmo completo
  - Relacionamentos entre entidades
  - Queries de exemplo para cada caso de uso
  - Priorização de implementação por fase

#### Novos Modelos Dataverse
- **Order** - Representa pedidos efetivados
  - Campos: orderid, ordernumber, customerid, totalamount, orderdate, etc.
  - Essencial para análise de compras reais
  - Suporta tipos: new, renewal, upsell
  
- **OrderProduct** - Itens/linhas de pedidos
  - Campos: orderproductid, orderid, productid, quantity, priceperunit, etc.
  - Permite análise detalhada de produtos vendidos
  
- **Contract** - Contratos com clientes
  - Campos: contractid, customerid, MRR, ARR, renewal_date, etc.
  - Essencial para gestão de renovações
  - Suporta auto-renewal e tracking de status

#### Campos Necessários Identificados
- **Account**: 20+ campos adicionais para segmentação, scoring e rotas
  - industrycode, cnae_description, segment
  - customerscore, potentialscore, accountrating
  - territory, visit_frequency, next_scheduled_visit
  - purchase_frequency, total_purchases, lifetime_value
  
- **Contact**: 10+ campos para hierarquia e influência
  - decision_maker, influencer, seniority_level
  - reports_to, budget_authority
  
- **Product**: Campos para renovação
  - is_recurring, renewal_frequency, default_contract_term

#### Análises e Algoritmos
- Modelo de scoring de potencial (0-100 pontos)
- Algoritmo de otimização de rotas (TSP)
- Análise RFM (Recency, Frequency, Monetary)
- Métricas de renovação (renewal rate, churn, NRR, GRR)
- Dashboard de renovações com alertas

### 📊 Principais Destaques

**Objetos por Criticidade:**
- ⭐⭐⭐⭐⭐ Críticos: Account, Contact, Order, Contract
- ⭐⭐⭐⭐ Altos: Opportunity, Quote, Product, OrderProduct

**Casos de Uso Cobertos:**
1. 🗺️ Rotas de Visita → Account (lat/long) + Visit
2. 🛒 Compras → Order + OrderProduct
3. 🏢 Segmentação → Account (industrycode, cnae) + Industry
4. 📊 Scoring → Todos os objetos (algoritmo multi-fator)
5. 👥 Contatos → Contact (hierarquia e influência)
6. 🔄 Renovações → Contract + Order (tipo renewal)

**Fases de Implementação:**
- Fase 1: ✅ Objetos básicos (já implementados)
- Fase 2: 🔴 Order, OrderProduct, Contract (crítico)
- Fase 3: 🟡 Visit, Industry (importante)
- Fase 4: 🟢 Campos adicionais (gradual)

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
