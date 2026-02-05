# Análise de Impacto de Custos Azure - MCP Dataverse

Este documento analisa o impacto de custos da implementação do MCP Dataverse Server como Azure Function.

## 📊 Visão Geral de Custos

A solução utiliza os seguintes serviços Azure:
1. **Azure Functions** (Consumption Plan ou Premium)
2. **Azure Storage** (necessário para Functions)
3. **Microsoft Dataverse API** (chamadas via Dynamics 365/Power Platform)
4. **Application Insights** (opcional, monitoramento)

---

## 💰 Modelo de Custos Detalhado

### 1. Azure Functions - Consumption Plan (Recomendado)

O Consumption Plan cobra por:
- **Execuções**: Número de vezes que a função é executada
- **Tempo de execução**: GB-segundos (memória × duração)

**Preços (região East US - Janeiro 2024):**
- Primeiras 1 milhão de execuções: **GRÁTIS**
- Execuções adicionais: **$0,20 por milhão**
- Primeiros 400.000 GB-s: **GRÁTIS**
- GB-s adicionais: **$0,000016 por GB-s**

**Memória padrão por execução:** 1536 MB (1.5 GB)

#### Exemplo de Cálculo - Consumption Plan

**Cenário 1: Uso Baixo (Desenvolvimento/Teste)**
- 10.000 requisições/mês
- Tempo médio: 500ms por requisição
- Memória: 1.5 GB

```
Execuções: 10.000 (dentro do limite gratuito)
GB-s: 10.000 × 0.5s × 1.5 GB = 7.500 GB-s (dentro do limite gratuito)
Custo: $0/mês ✅ GRÁTIS
```

**Cenário 2: Uso Médio (Produção Pequena)**
- 100.000 requisições/mês
- Tempo médio: 500ms por requisição
- Memória: 1.5 GB

```
Execuções: 100.000 (dentro do limite gratuito)
GB-s: 100.000 × 0.5s × 1.5 GB = 75.000 GB-s (dentro do limite gratuito)
Custo: $0/mês ✅ GRÁTIS
```

**Cenário 3: Uso Alto (Produção Média)**
- 1.000.000 requisições/mês
- Tempo médio: 500ms por requisição
- Memória: 1.5 GB

```
Execuções: 1.000.000 (dentro do limite gratuito)
GB-s: 1.000.000 × 0.5s × 1.5 GB = 750.000 GB-s
  - 400.000 GB-s gratuitos
  - 350.000 GB-s pagos × $0,000016 = $5,60
Custo: $5,60/mês 💰
```

**Cenário 4: Uso Muito Alto (Produção Grande)**
- 5.000.000 requisições/mês
- Tempo médio: 500ms por requisição
- Memória: 1.5 GB

```
Execuções: 
  - 1.000.000 gratuitos
  - 4.000.000 pagos × $0,20/milhão = $0,80
GB-s: 5.000.000 × 0.5s × 1.5 GB = 3.750.000 GB-s
  - 400.000 GB-s gratuitos
  - 3.350.000 GB-s pagos × $0,000016 = $53,60
Custo total: $0,80 + $53,60 = $54,40/mês 💰
```

### 2. Azure Functions - Premium Plan

**Quando considerar Premium Plan:**
- Necessidade de VNet integration
- Warm instances sempre ativas (sem cold start)
- Instâncias maiores (até 14 GB RAM)
- Execuções de longa duração (>10 minutos)

**Preços (região East US):**
- EP1 (1 vCore, 3.5 GB): **~$146/mês**
- EP2 (2 vCores, 7 GB): **~$292/mês**
- EP3 (4 vCores, 14 GB): **~$584/mês**

**Recomendação:** Para este projeto, **Consumption Plan é suficiente** para a maioria dos casos.

---

### 3. Azure Storage Account

**Necessário para:** Armazenar configuração da Azure Function

**Custo:** Mínimo (< $1/mês)
- LRS (Locally Redundant Storage)
- Poucos KB de dados
- Transações mínimas

---

### 4. Microsoft Dataverse API - Custos e Limites

#### Limites de Rate (Service Protection)

O Dataverse impõe limites para proteção do serviço:

**Limites por usuário (application user):**
- **6.000 requisições por 5 minutos** (1.200 req/min)
- **52 requisições simultâneas**

**Se exceder:**
- HTTP 429 (Too Many Requests)
- Retry-After header com tempo de espera
- Possível bloqueio temporário

#### Custos de Licenciamento

O acesso ao Dataverse geralmente está incluído em:
- **Dynamics 365** (CRM, Sales, Customer Service, etc.)
- **Power Apps** (Por usuário ou Por app)
- **Power Platform**

**Não há custo adicional por chamada API**, mas você precisa ter:
- Licenças válidas do Dynamics 365 ou Power Apps
- Application User configurado corretamente

**Nota:** Exceder rate limits não gera custos adicionais, mas pode degradar performance.

---

## 🎯 Impacto do Cache na Redução de Custos

### Sem Cache

**Cenário:** Dashboard que mostra lista de 20 empresas, atualizado a cada 5 segundos por 100 usuários simultâneos.

```
Requisições por hora: 100 usuários × (3600s / 5s) × 1 req = 72.000 req/h
Requisições por mês: 72.000 × 24h × 30 dias = 51.840.000 req/mês

Azure Function:
- Execuções: 51.840.000 - 1.000.000 (grátis) = 50.840.000 pagos
- Custo execuções: 50.840.000 × ($0,20/1.000.000) = $10,17
- GB-s: 51.840.000 × 0.5s × 1.5 GB = 38.880.000 GB-s
  - 400.000 gratuitos = 38.480.000 pagos
  - Custo GB-s: 38.480.000 × $0,000016 = $615,68
- TOTAL: $625,85/mês ❌

Dataverse:
- 51.840.000 req/mês = 864.000 req/hora
- EXCEDE o limite de 6.000 req/5min (72.000/5min)
- Causará throttling severo ❌
```

### Com Cache (TTL 5 minutos)

```
Cache hit rate: ~80% (assumindo queries repetidas)
Requisições reais ao Dataverse: 51.840.000 × 20% = 10.368.000 req/mês

Azure Function (todas as requisições ainda passam pela function):
- Execuções: 51.840.000 (mesmo número)
- Custo execuções: $10,17
- Tempo médio com cache: 50ms (10x mais rápido)
- GB-s: 51.840.000 × 0.05s × 1.5 GB = 3.888.000 GB-s
  - 400.000 gratuitos = 3.488.000 pagos
  - Custo GB-s: 3.488.000 × $0,000016 = $55,81
- TOTAL: $65,98/mês ✅ (90% de economia!)

Dataverse:
- 10.368.000 req/mês = 172.800 req/hora
- 2.880 req/5min
- DENTRO do limite de 6.000 req/5min ✅
- Sem throttling ✅
```

### Resumo de Economia com Cache

| Métrica | Sem Cache | Com Cache | Economia |
|---------|-----------|-----------|----------|
| **Custo Azure Function** | $625,85/mês | $65,98/mês | **89% 💰** |
| **Requisições Dataverse** | 51.8M/mês | 10.4M/mês | **80% 📉** |
| **Throttling** | ❌ Sim | ✅ Não | **100% ✅** |
| **Tempo resposta** | 500ms | 50ms | **90% ⚡** |

---

## 📈 Estimativas por Volume de Uso

### Tabela de Custos Mensais (Consumption Plan + Cache)

| Requisições/Mês | Cache Hit Rate | Custo Azure Function | Status Dataverse |
|-----------------|----------------|----------------------|------------------|
| 10K | 0% | $0 (grátis) | ✅ OK |
| 100K | 0% | $0 (grátis) | ✅ OK |
| 500K | 50% | $2,80 | ✅ OK |
| 1M | 70% | $8,50 | ✅ OK |
| 5M | 80% | $65,98 | ✅ OK |
| 10M | 85% | $145,20 | ✅ OK |
| 50M | 90% | $850,00 | ⚠️ Considerar Premium |

**Notas:**
- Cache hit rate aumenta com volume (mais queries repetidas)
- Sem cache, volumes acima de 1M/mês causariam throttling
- Custos assumem tempo médio de 50ms com cache, 500ms sem cache

---

## 🔧 Otimizações para Reduzir Custos

### 1. Ajustar TTL do Cache

**Impacto:** Aumentar o cache TTL aumenta hit rate

```python
# .env
DATAVERSE_CACHE_TTL=600  # 10 minutos (padrão: 300)
```

**Trade-off:**
- ✅ Mais economia (hit rate maior)
- ⚠️ Dados podem ficar desatualizados por mais tempo

**Recomendação por tipo de dado:**
- Produtos/Catálogos: 1800s (30 min) - mudam raramente
- Empresas: 600s (10 min) - mudam ocasionalmente
- Oportunidades: 300s (5 min) - mudam frequentemente
- Cotações ativas: 60s (1 min) - mudam muito

### 2. Implementar Cache Seletivo

Nem todas as queries precisam de cache:

```python
# Exemplo: Desabilitar cache para queries de escrita ou dados sensíveis
result = self._query(entity, filter_query, select, top, use_cache=False)
```

**Quando desabilitar cache:**
- Operações de escrita
- Dados em tempo real
- Dados sensíveis que mudam constantemente

### 3. Compressão de Respostas

Reduz tempo de transmissão e GB-s:

```python
# Adicionar ao _get_headers()
"Accept-Encoding": "gzip, deflate"
```

**Economia:** ~60-70% redução no payload

### 4. Batch Requests

Agrupar múltiplas queries em uma requisição:

```python
# OData $batch endpoint
# Reduz número de chamadas ao Dataverse
```

**Economia:** Até 90% menos execuções da function

### 5. Monitorar e Ajustar Memória

Azure Functions aloca mais memória que o necessário:

```json
// host.json
{
  "functionAppScaleLimit": 10,
  "functionTimeout": "00:05:00"
}
```

**Teste com diferentes tamanhos de memória no Premium Plan**

### 6. Cold Start Mitigation (Premium Plan)

Se cold starts são problema:
- Premium Plan EP1: $146/mês
- Always-on instances
- Elimina cold starts

**Quando vale a pena:**
- Requisições > 10M/mês
- SLA crítico
- Cold start > 2s inaceitável

---

## 📊 Application Insights - Custo de Monitoramento

**Preços:**
- Primeiros 5 GB/mês: **GRÁTIS**
- Adicional: **$2,30 por GB**

**Estimativa de telemetria:**
- 1M requisições ≈ 0.5-1 GB de logs
- 5M requisições ≈ 2.5-5 GB (dentro do grátis)
- 50M requisições ≈ 25-50 GB = $46-104/mês

**Otimização:**
- Usar sampling (só 10% das requests)
- Desabilitar logs verbosos em produção
- Retention: 30 dias (padrão 90 dias)

```json
// applicationinsights.config
{
  "sampling": {
    "isEnabled": true,
    "maxTelemetryItemsPerSecond": 5
  }
}
```

---

## 💡 Recomendações por Cenário

### Startup / MVP (< 100K req/mês)
```
✅ Consumption Plan
✅ Cache habilitado (TTL: 300s)
✅ Application Insights (sampling 100%)
✅ LRS Storage

Custo estimado: $0-5/mês
```

### Pequena Empresa (100K - 1M req/mês)
```
✅ Consumption Plan
✅ Cache habilitado (TTL: 600s)
✅ Application Insights (sampling 50%)
✅ LRS Storage

Custo estimado: $5-15/mês
```

### Média Empresa (1M - 10M req/mês)
```
✅ Consumption Plan
✅ Cache habilitado (TTL: 600s)
✅ Application Insights (sampling 20%)
✅ LRS Storage
✅ Considerar batch requests

Custo estimado: $15-150/mês
```

### Grande Empresa (> 10M req/mês)
```
⚠️ Avaliar Premium Plan EP1
✅ Cache habilitado (TTL: 900s)
✅ Application Insights (sampling 10%)
✅ LRS Storage
✅ Batch requests obrigatório
✅ CDN para dados estáticos

Custo estimado: $146-500/mês (Premium)
ou $150-1000/mês (Consumption otimizado)
```

---

## 📈 Monitoramento de Custos

### Azure Cost Management

Configure alertas de custo:

```bash
# Alerta de custo mensal
az consumption budget create \
  --budget-name "mcp-dataverse-monthly" \
  --amount 100 \
  --time-grain Monthly \
  --start-date 2024-01-01 \
  --end-date 2025-12-31
```

### Métricas Importantes

**Azure Portal > Cost Management:**
1. **Custo por serviço** (Function vs Storage vs Insights)
2. **Tendência mensal**
3. **Forecast** (projeção)

**Application Insights:**
1. **Requests/second**
2. **Execution time** (reduzir GB-s)
3. **Cache hit rate** (aumentar)
4. **Failed requests** (podem causar retries caros)

### KPIs de Custo

| KPI | Meta | Crítico |
|-----|------|---------|
| Custo/1000 requisições | < $0,05 | > $0,20 |
| Cache hit rate | > 70% | < 50% |
| Tempo médio execução | < 200ms | > 1000ms |
| Throttling errors | 0% | > 1% |

---

## 🎯 Comparação: Alternativas de Implementação

### Opção 1: Azure Function + Cache (Atual)
```
Custo: $5-150/mês (até 10M req)
Pros: Serverless, auto-scaling, pay-per-use
Contras: Cold starts, limites do consumption plan
```

### Opção 2: Azure Function Premium + Redis Cache
```
Custo: $146 (EP1) + $15 (Redis Basic) = $161/mês
Pros: Cache compartilhado, sem cold start, maior performance
Contras: Custo fixo mesmo com baixo uso
```

### Opção 3: Azure App Service + Redis
```
Custo: $55 (B1) + $15 (Redis) = $70/mês
Pros: Custo previsível, always-on
Contras: Não escala automaticamente, requer gerenciamento
```

### Opção 4: Azure Container Apps
```
Custo: $20-100/mês (pay-per-use)
Pros: Kubernetes-like, escala bem
Contras: Mais complexo, overhead operacional
```

**Conclusão:** Para a maioria dos cenários, **Opção 1 (atual)** é a mais custo-efetiva até ~10M requisições/mês.

---

## ✅ Checklist de Otimização de Custos

- [ ] Cache habilitado com TTL apropriado
- [ ] Application Insights com sampling configurado
- [ ] Alertas de custo configurados
- [ ] Monitoramento de cache hit rate
- [ ] Logs apenas em nível INFO/WARNING em produção
- [ ] Compressão gzip habilitada
- [ ] Timeout de function configurado (evitar execuções longas)
- [ ] Retry policy otimizado (evitar retries excessivos)
- [ ] Storage account em LRS (não precisa GRS)
- [ ] Limpeza de logs antigos automatizada

---

## 📞 Quando Escalar?

### Sinais para Considerar Premium Plan

1. **Custo Consumption > $150/mês**
2. **Cold starts > 2 segundos** impactando UX
3. **Necessidade de VNet** para segurança
4. **Execuções > 10M/mês** consistentemente
5. **Picos de tráfego** requerem warm instances

### Sinais para Otimizar Mais

1. **Cache hit rate < 50%**
2. **Tempo execução > 500ms** consistentemente
3. **Throttling errors do Dataverse**
4. **Custo crescendo mais rápido que uso**

---

## 💰 Resumo Executivo

### Custo Total Estimado (Cache Habilitado)

| Volume Mensal | Azure Function | Storage | App Insights | **TOTAL** |
|---------------|----------------|---------|--------------|-----------|
| 10K req | $0 | $0.50 | $0 | **$0.50** |
| 100K req | $0 | $0.50 | $0 | **$0.50** |
| 1M req | $8.50 | $0.50 | $0 | **$9.00** |
| 5M req | $65.98 | $0.50 | $0 | **$66.48** |
| 10M req | $145.20 | $0.50 | $5.00 | **$150.70** |

### ROI do Cache

- **Sem cache:** Custos 10x maiores + throttling garantido
- **Com cache:** 80-90% de economia + sem throttling
- **Payback:** Imediato (cache é grátis)

### Recomendação Final

✅ **A implementação atual é altamente custo-efetiva**

- Cache em memória é **grátis** (sem Redis/banco adicional)
- Consumption Plan é **grátis** até 1M execuções
- Redução de **80-90% nos custos** comparado a sem cache
- **Elimina throttling** do Dataverse

**Para 99% dos casos de uso, o custo mensal será < $100 com excelente performance.**

---

## 📚 Referências

- [Azure Functions Pricing](https://azure.microsoft.com/pricing/details/functions/)
- [Azure Storage Pricing](https://azure.microsoft.com/pricing/details/storage/)
- [Application Insights Pricing](https://azure.microsoft.com/pricing/details/monitor/)
- [Dataverse API Limits](https://docs.microsoft.com/power-platform/admin/api-request-limits-allocations)
- [Azure Cost Management](https://docs.microsoft.com/azure/cost-management-billing/)

---

**Última atualização:** Janeiro 2024  
**Moeda:** USD (dólar americano)  
**Região base:** East US (preços podem variar por região)
