# Análise de Objetos Dataverse para Business Intelligence

Este documento identifica e analisa os objetos do Microsoft Dataverse necessários para implementar casos de uso avançados de business intelligence e gestão de relacionamento com clientes.

## 📊 Visão Geral dos Casos de Uso

### Casos de Uso Identificados:
1. **Otimização de Rotas de Visita** - Planejamento geográfico de visitas comerciais
2. **Análise de Compras por Período** - Identificar padrões de compra
3. **Segmentação por CNAE/Indústria** - Classificação de empresas por setor
4. **Scoring de Potencial** - Avaliar valor potencial de cada cliente
5. **Gestão de Contatos** - Visão consolidada de stakeholders
6. **Gestão de Compras e Renovações** - Ciclo de vida de produtos/contratos

---

## 🎯 Objetos Dataverse Necessários

### 1. Account (Empresa) ⭐⭐⭐⭐⭐
**Relevância:** CRÍTICA para todos os casos de uso

**Campos Atuais Relevantes:**
- ✅ `accountid` - Identificador único
- ✅ `name` - Nome da empresa
- ✅ `cnpj` - CNPJ (Brasil)
- ✅ `address1_latitude`, `address1_longitude` - Coordenadas GPS
- ✅ `address1_postalcode`, `address1_city`, `address1_stateorprovince` - Endereço
- ✅ `revenue` - Faturamento
- ✅ `numberofemployees` - Número de funcionários
- ✅ `lastvisitdate` - Última visita
- ✅ `lastcontactdate` - Último contato

**Campos Necessários Adicionais:**
```python
# Segmentação
industrycode: Optional[str]  # Código CNAE
cnae_description: Optional[str]  # Descrição do CNAE
segment: Optional[str]  # Segmento de mercado
subsegment: Optional[str]  # Sub-segmento

# Scoring e Potencial
creditrating: Optional[str]  # Rating de crédito
accountrating: Optional[str]  # Classificação da conta (A, B, C)
customerscore: Optional[int]  # Score de 0-100
potentialscore: Optional[int]  # Potencial de negócio (0-100)
lifecycle_stage: Optional[str]  # Estágio do ciclo de vida

# Planejamento de Visitas
territory: Optional[str]  # Território/região de vendas
assigned_salesperson: Optional[str]  # Vendedor responsável
visit_frequency: Optional[int]  # Frequência de visitas (dias)
next_scheduled_visit: Optional[datetime]  # Próxima visita agendada
preferred_visit_day: Optional[str]  # Dia preferido para visitas
preferred_visit_time: Optional[str]  # Horário preferido

# Análise de Compras
first_purchase_date: Optional[datetime]  # Data da primeira compra
last_purchase_date: Optional[datetime]  # Data da última compra
total_purchases: Optional[float]  # Total de compras (lifetime value)
average_purchase_value: Optional[float]  # Ticket médio
purchase_frequency: Optional[int]  # Frequência de compras (dias)
```

**Uso por Caso:**
- 🗺️ **Rotas de Visita**: latitude, longitude, address, territory, visit_frequency
- 🛒 **Compras**: last_purchase_date, total_purchases, average_purchase_value
- 🏢 **Segmentação**: industrycode, cnae_description, segment
- 📊 **Scoring**: revenue, numberofemployees, customerscore, potentialscore
- 👥 **Contatos**: Relacionamento via Contact.parentcustomerid
- 🔄 **Renovações**: last_purchase_date, purchase_frequency

---

### 2. Contact (Contato) ⭐⭐⭐⭐⭐
**Relevância:** CRÍTICA para gestão de relacionamentos

**Campos Atuais Relevantes:**
- ✅ `contactid` - Identificador único
- ✅ `fullname`, `firstname`, `lastname` - Nome
- ✅ `emailaddress1`, `emailaddress2` - Emails
- ✅ `telephone1`, `mobilephone` - Telefones
- ✅ `jobtitle` - Cargo
- ✅ `parentcustomerid` - Empresa (Account)

**Campos Necessários Adicionais:**
```python
# Hierarquia e Influência
reports_to: Optional[str]  # Superior direto
decision_maker: Optional[bool]  # É tomador de decisão
influencer: Optional[bool]  # É influenciador
department: Optional[str]  # Departamento
seniority_level: Optional[str]  # Nível hierárquico

# Relacionamento
contact_score: Optional[int]  # Score de relacionamento
preferred_contact_method: Optional[str]  # Email, telefone, WhatsApp
last_interaction_date: Optional[datetime]  # Última interação
interaction_frequency: Optional[int]  # Frequência de contato

# Área de Interesse
area_of_responsibility: Optional[str]  # Área de responsabilidade
budget_authority: Optional[bool]  # Tem autoridade de orçamento
technical_decision_maker: Optional[bool]  # Decisor técnico
```

**Uso por Caso:**
- 🗺️ **Rotas de Visita**: Contatos principais para agendar
- 📊 **Scoring**: decision_maker, influencer, seniority_level
- 👥 **Contatos**: Todos os campos para visão completa
- 🔄 **Renovações**: Responsáveis por renovações contratuais

---

### 3. Opportunity (Oportunidade) ⭐⭐⭐⭐
**Relevância:** ALTA para análise de pipeline e potencial

**Campos Atuais Relevantes:**
- ✅ `opportunityid` - Identificador único
- ✅ `customerid` - Empresa relacionada
- ✅ `estimatedvalue`, `actualvalue` - Valores
- ✅ `estimatedclosedate`, `actualclosedate` - Datas
- ✅ `closeprobability` - Probabilidade de fechamento
- ✅ `statecode`, `statuscode` - Status

**Campos Necessários Adicionais:**
```python
# Origem e Tipo
opportunity_source: Optional[str]  # Origem (inbound, outbound, referral)
opportunity_type: Optional[str]  # Tipo (nova venda, upsell, cross-sell, renovação)
sales_stage: Optional[str]  # Estágio de vendas detalhado
competitor: Optional[str]  # Concorrente principal

# Análise de Ciclo
days_in_stage: Optional[int]  # Dias no estágio atual
total_days_open: Optional[int]  # Dias totais em aberto
expected_revenue: Optional[float]  # Receita esperada (value × probability)

# Relacionamento
primary_contact: Optional[str]  # Contato principal
sales_owner: Optional[str]  # Responsável pela venda
```

**Uso por Caso:**
- 🛒 **Compras**: Histórico de oportunidades fechadas
- 📊 **Scoring**: Pipeline ativo, valores, probabilidades
- 🔄 **Renovações**: Oportunidades tipo "renovação"

---

### 4. Quote (Cotação) ⭐⭐⭐⭐
**Relevância:** ALTA para análise de propostas e conversão

**Campos Atuais Relevantes:**
- ✅ `quoteid` - Identificador único
- ✅ `quotenumber` - Número da cotação
- ✅ `opportunityid` - Oportunidade relacionada
- ✅ `customerid` - Empresa
- ✅ `totalamount`, `totaltax` - Valores
- ✅ `effectivefrom`, `effectiveto` - Período de validade
- ✅ `discountamount`, `discountpercentage` - Descontos

**Campos Necessários Adicionais:**
```python
# Status e Aprovação
approval_status: Optional[str]  # Status de aprovação
approved_by: Optional[str]  # Aprovado por
approval_date: Optional[datetime]  # Data de aprovação
rejection_reason: Optional[str]  # Motivo de rejeição

# Análise de Conversão
presentation_date: Optional[datetime]  # Data de apresentação
response_date: Optional[datetime]  # Data de resposta do cliente
days_to_close: Optional[int]  # Dias até fechamento
conversion_probability: Optional[int]  # Probabilidade de conversão

# Competição
competitor_quote: Optional[bool]  # Cliente tem cotação de concorrente
competitive_price_difference: Optional[float]  # Diferença de preço
```

**Uso por Caso:**
- 🛒 **Compras**: Histórico de cotações e conversão
- 📊 **Scoring**: Taxa de conversão, valores médios
- 🔄 **Renovações**: Cotações de renovação de contratos

---

### 5. Product (Produto) ⭐⭐⭐⭐
**Relevância:** ALTA para análise de mix de produtos

**Campos Atuais Relevantes:**
- ✅ `productid` - Identificador único
- ✅ `name` - Nome do produto
- ✅ `productnumber` - Código do produto
- ✅ `price` - Preço
- ✅ `description` - Descrição

**Campos Necessários Adicionais:**
```python
# Categorização
product_category: Optional[str]  # Categoria do produto
product_family: Optional[str]  # Família de produtos
product_line: Optional[str]  # Linha de produtos
is_recurring: Optional[bool]  # Produto recorrente (assinatura)

# Comercial
cost: Optional[float]  # Custo do produto
margin: Optional[float]  # Margem de lucro
standard_discount: Optional[float]  # Desconto padrão
minimum_quantity: Optional[int]  # Quantidade mínima

# Renovação
renewal_frequency: Optional[int]  # Frequência de renovação (meses)
renewal_notice_period: Optional[int]  # Período de aviso (dias)
default_contract_term: Optional[int]  # Prazo contratual padrão (meses)

# Performance
total_units_sold: Optional[int]  # Total de unidades vendidas
total_revenue: Optional[float]  # Receita total gerada
avg_selling_price: Optional[float]  # Preço médio de venda
```

**Uso por Caso:**
- 🛒 **Compras**: Produtos mais vendidos por período
- 📊 **Scoring**: Mix de produtos, margem
- 🔄 **Renovações**: Produtos recorrentes, períodos de renovação

---

### 6. OpportunityProduct (Produto da Oportunidade) ⭐⭐⭐⭐
**Relevância:** ALTA para análise de itens vendidos

**Campos Atuais Relevantes:**
- ✅ `opportunityproductid` - Identificador único
- ✅ `opportunityid` - Oportunidade
- ✅ `productid` - Produto
- ✅ `quantity` - Quantidade
- ✅ `priceperunit` - Preço unitário
- ✅ `baseamount`, `tax`, `extendedamount` - Valores

**Uso por Caso:**
- 🛒 **Compras**: Detalhamento de itens por período
- 📊 **Scoring**: Mix de produtos comprados
- 🔄 **Renovações**: Produtos para renovação

---

### 7. Order (Pedido) ⭐⭐⭐⭐⭐ 🆕
**Relevância:** CRÍTICA para análise de compras reais
**Status:** NÃO IMPLEMENTADO - NECESSÁRIO

**Modelo Sugerido:**
```python
class Order(BaseModel):
    """
    Order (Pedido) entity in Dataverse
    Representa uma compra efetivada
    """
    orderid: Optional[str] = Field(None, description="Order ID")
    ordernumber: Optional[str] = Field(None, description="Order number")
    name: Optional[str] = Field(None, description="Order name")
    
    # Relacionamentos
    customerid: Optional[str] = Field(None, alias="_customerid_value", 
                                      description="Customer account ID")
    opportunityid: Optional[str] = Field(None, alias="_opportunityid_value", 
                                         description="Related opportunity ID")
    quoteid: Optional[str] = Field(None, alias="_quoteid_value", 
                                   description="Related quote ID")
    
    # Valores
    totalamount: Optional[float] = Field(None, description="Total amount")
    totaltax: Optional[float] = Field(None, description="Total tax")
    totallineitemamount: Optional[float] = Field(None, description="Total line items")
    discountamount: Optional[float] = Field(None, description="Discount amount")
    freightamount: Optional[float] = Field(None, description="Freight amount")
    
    # Datas
    order_date: Optional[datetime] = Field(None, alias="new_orderdate", 
                                           description="Order date")
    requested_delivery_date: Optional[datetime] = Field(None, 
                                                        description="Requested delivery")
    actual_delivery_date: Optional[datetime] = Field(None, 
                                                     description="Actual delivery")
    
    # Status
    statecode: Optional[int] = Field(None, description="State (0=Active, 1=Submitted, etc)")
    statuscode: Optional[int] = Field(None, description="Status reason")
    order_status: Optional[str] = Field(None, description="Order status")
    
    # Tipo
    order_type: Optional[str] = Field(None, description="Order type (new, renewal, upsell)")
    
    # Pagamento
    payment_terms: Optional[str] = Field(None, description="Payment terms")
    payment_status: Optional[str] = Field(None, description="Payment status")
    
    # Audit
    createdon: Optional[datetime] = Field(None, description="Created date")
    modifiedon: Optional[datetime] = Field(None, description="Modified date")
```

**Uso por Caso:**
- 🛒 **Compras**: ESSENCIAL - histórico completo de pedidos
- 📊 **Scoring**: Total de pedidos, frequência, valores
- 🔄 **Renovações**: Identificar pedidos para renovação

---

### 8. OrderProduct (Item do Pedido) ⭐⭐⭐⭐ 🆕
**Relevância:** ALTA para análise detalhada de compras
**Status:** NÃO IMPLEMENTADO - NECESSÁRIO

**Modelo Sugerido:**
```python
class OrderProduct(BaseModel):
    """
    OrderProduct (Item do Pedido) entity in Dataverse
    Representa um item/linha em um pedido
    """
    orderproductid: Optional[str] = Field(None, description="Order product ID")
    orderid: Optional[str] = Field(None, alias="_orderid_value", description="Order ID")
    productid: Optional[str] = Field(None, alias="_productid_value", description="Product ID")
    
    # Quantidades
    quantity: Optional[float] = Field(None, description="Quantity")
    shipped_quantity: Optional[float] = Field(None, description="Shipped quantity")
    
    # Valores
    priceperunit: Optional[float] = Field(None, description="Price per unit")
    baseamount: Optional[float] = Field(None, description="Base amount")
    tax: Optional[float] = Field(None, description="Tax")
    extendedamount: Optional[float] = Field(None, description="Extended amount")
    manual_discount: Optional[float] = Field(None, description="Manual discount")
    
    # Detalhes
    description: Optional[str] = Field(None, description="Description")
    lineitemnumber: Optional[int] = Field(None, description="Line item number")
    
    # Audit
    createdon: Optional[datetime] = Field(None, description="Created date")
    modifiedon: Optional[datetime] = Field(None, description="Modified date")
```

**Uso por Caso:**
- 🛒 **Compras**: Produtos comprados por período
- 📊 **Scoring**: Produtos mais relevantes por cliente
- 🔄 **Renovações**: Itens elegíveis para renovação

---

### 9. Contract (Contrato) ⭐⭐⭐⭐⭐ 🆕
**Relevância:** CRÍTICA para gestão de renovações
**Status:** NÃO IMPLEMENTADO - NECESSÁRIO

**Modelo Sugerido:**
```python
class Contract(BaseModel):
    """
    Contract (Contrato) entity in Dataverse
    Representa contratos com clientes
    """
    contractid: Optional[str] = Field(None, description="Contract ID")
    contractnumber: Optional[str] = Field(None, description="Contract number")
    title: Optional[str] = Field(None, description="Contract title")
    
    # Relacionamentos
    customerid: Optional[str] = Field(None, alias="_customerid_value", 
                                      description="Customer account ID")
    billingaccountid: Optional[str] = Field(None, description="Billing account")
    
    # Datas
    contract_start_date: Optional[datetime] = Field(None, description="Start date")
    contract_end_date: Optional[datetime] = Field(None, description="End date")
    renewal_date: Optional[datetime] = Field(None, description="Renewal date")
    cancellation_date: Optional[datetime] = Field(None, description="Cancellation date")
    
    # Valores
    total_contract_value: Optional[float] = Field(None, description="Total value")
    monthly_recurring_revenue: Optional[float] = Field(None, description="MRR")
    annual_recurring_revenue: Optional[float] = Field(None, description="ARR")
    
    # Renovação
    contract_term: Optional[int] = Field(None, description="Term in months")
    renewal_notice_required: Optional[int] = Field(None, 
                                                   description="Notice days")
    auto_renewal: Optional[bool] = Field(None, description="Auto-renewal enabled")
    renewal_status: Optional[str] = Field(None, 
                                          description="Status (pending, renewed, not renewed)")
    
    # Status
    statecode: Optional[int] = Field(None, description="State")
    statuscode: Optional[int] = Field(None, description="Status reason")
    contract_status: Optional[str] = Field(None, description="Contract status")
    
    # Tipo
    contract_type: Optional[str] = Field(None, 
                                         description="Type (standard, custom, framework)")
    payment_terms: Optional[str] = Field(None, description="Payment terms")
    billing_frequency: Optional[str] = Field(None, 
                                             description="Frequency (monthly, quarterly, annual)")
    
    # Audit
    createdon: Optional[datetime] = Field(None, description="Created date")
    modifiedon: Optional[datetime] = Field(None, description="Modified date")
```

**Uso por Caso:**
- 🔄 **Renovações**: ESSENCIAL - gestão completa de renovações
- 📊 **Scoring**: MRR, ARR, duração de contratos
- 🛒 **Compras**: Contratos ativos e histórico

---

### 10. Industry (Indústria/CNAE) ⭐⭐⭐ 🆕
**Relevância:** ALTA para segmentação
**Status:** NÃO IMPLEMENTADO - RECOMENDADO

**Modelo Sugerido:**
```python
class Industry(BaseModel):
    """
    Industry (Indústria/CNAE) entity in Dataverse
    Tabela de referência para classificação de empresas
    """
    industryid: Optional[str] = Field(None, description="Industry ID")
    name: Optional[str] = Field(None, description="Industry name")
    
    # Códigos
    cnae_code: Optional[str] = Field(None, description="CNAE code")
    cnae_division: Optional[str] = Field(None, description="CNAE division")
    cnae_group: Optional[str] = Field(None, description="CNAE group")
    cnae_class: Optional[str] = Field(None, description="CNAE class")
    cnae_subclass: Optional[str] = Field(None, description="CNAE subclass")
    
    # Segmentação
    sector: Optional[str] = Field(None, description="Sector")
    segment: Optional[str] = Field(None, description="Market segment")
    subsegment: Optional[str] = Field(None, description="Market subsegment")
    
    # Características
    description: Optional[str] = Field(None, description="Description")
    typical_products: Optional[str] = Field(None, description="Typical products")
    target_company_size: Optional[str] = Field(None, description="Target size")
    
    # Métricas
    average_deal_size: Optional[float] = Field(None, description="Avg deal size")
    typical_sales_cycle: Optional[int] = Field(None, description="Sales cycle (days)")
```

**Uso por Caso:**
- 🏢 **Segmentação**: ESSENCIAL - classificação completa
- 📊 **Scoring**: Benchmarks por indústria
- 🗺️ **Rotas**: Agrupar visitas por setor

---

### 11. Visit (Visita) ⭐⭐⭐⭐ 🆕
**Relevância:** ALTA para gestão de visitas
**Status:** NÃO IMPLEMENTADO - RECOMENDADO

**Modelo Sugerido:**
```python
class Visit(BaseModel):
    """
    Visit (Visita) entity in Dataverse
    Representa visitas realizadas ou agendadas a clientes
    """
    visitid: Optional[str] = Field(None, description="Visit ID")
    name: Optional[str] = Field(None, description="Visit name")
    
    # Relacionamentos
    accountid: Optional[str] = Field(None, alias="_accountid_value", 
                                     description="Account visited")
    contactid: Optional[str] = Field(None, alias="_contactid_value", 
                                     description="Contact met")
    ownerid: Optional[str] = Field(None, description="Sales rep")
    
    # Datas e Localização
    scheduled_date: Optional[datetime] = Field(None, description="Scheduled date")
    actual_date: Optional[datetime] = Field(None, description="Actual date")
    duration: Optional[int] = Field(None, description="Duration in minutes")
    checkin_time: Optional[datetime] = Field(None, description="Check-in time")
    checkout_time: Optional[datetime] = Field(None, description="Check-out time")
    
    # Localização
    checkin_latitude: Optional[float] = Field(None, description="Check-in latitude")
    checkin_longitude: Optional[float] = Field(None, description="Check-in longitude")
    distance_to_account: Optional[float] = Field(None, 
                                                  description="Distance in km")
    
    # Conteúdo
    visit_type: Optional[str] = Field(None, 
                                      description="Type (sales, support, follow-up)")
    visit_purpose: Optional[str] = Field(None, description="Purpose")
    visit_notes: Optional[str] = Field(None, description="Notes")
    visit_outcome: Optional[str] = Field(None, description="Outcome")
    
    # Próximas ações
    follow_up_required: Optional[bool] = Field(None, description="Follow-up needed")
    next_action: Optional[str] = Field(None, description="Next action")
    next_visit_date: Optional[datetime] = Field(None, description="Next visit")
    
    # Status
    statecode: Optional[int] = Field(None, description="State")
    statuscode: Optional[int] = Field(None, description="Status")
    visit_status: Optional[str] = Field(None, 
                                        description="Status (scheduled, completed, cancelled)")
    
    # Audit
    createdon: Optional[datetime] = Field(None, description="Created date")
    modifiedon: Optional[datetime] = Field(None, description="Modified date")
```

**Uso por Caso:**
- 🗺️ **Rotas de Visita**: ESSENCIAL - planejamento e histórico
- 📊 **Scoring**: Frequência e qualidade de visitas
- 👥 **Contatos**: Relacionamento presencial

---

## 🔗 Relacionamentos Entre Entidades

```
Account (Empresa)
├── Contact (1:N) - Contatos da empresa
├── Opportunity (1:N) - Oportunidades de venda
│   └── OpportunityProduct (1:N) - Produtos da oportunidade
├── Quote (1:N) - Cotações para a empresa
├── Order (1:N) - Pedidos efetivados
│   └── OrderProduct (1:N) - Itens dos pedidos
├── Contract (1:N) - Contratos ativos/histórico
├── Visit (1:N) - Visitas realizadas/agendadas
└── Industry (N:1) - Classificação por CNAE

Product (Produto)
├── OpportunityProduct (1:N) - Produtos em oportunidades
├── OrderProduct (1:N) - Produtos em pedidos
└── Contract (N:N) - Produtos em contratos
```

---

## 📋 Resumo por Caso de Uso

### 1. 🗺️ Otimização de Rotas de Visita

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Account | ⭐⭐⭐⭐⭐ | latitude, longitude, address, territory |
| Visit | ⭐⭐⭐⭐⭐ | scheduled_date, checkin_time, location |
| Contact | ⭐⭐⭐ | Contatos para agendar |

**Query Exemplo:**
```python
# Buscar contas em uma região específica, ordenadas por última visita
accounts = search_accounts(
    filter_query="address1_stateorprovince eq 'SP' and address1_city eq 'São Paulo'",
    orderby="new_lastvisitdate asc"
)

# Calcular rotas otimizadas usando latitude/longitude
# Considerar: last_visit_date, priority, territory
```

**Algoritmo de Otimização:**
1. Filtrar contas por território/região
2. Priorizar por: dias desde última visita, score, urgência
3. Agrupar geograficamente (clustering)
4. Calcular rota usando algoritmo de TSP (Traveling Salesman Problem)
5. Considerar: horário de preferência, disponibilidade de contatos

---

### 2. 🛒 Localizar Compras Típicas em um Período

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Order | ⭐⭐⭐⭐⭐ | order_date, totalamount, order_type |
| OrderProduct | ⭐⭐⭐⭐⭐ | productid, quantity, priceperunit |
| Product | ⭐⭐⭐⭐ | name, category, product_family |
| Account | ⭐⭐⭐ | industrycode, segment |

**Query Exemplo:**
```python
# Compras no último trimestre
orders = search_orders(
    filter_query="order_date ge '2024-01-01' and order_date le '2024-03-31'",
    expand="orderproducts,account"
)

# Produtos mais vendidos
top_products = aggregate_order_products(
    period="Q1-2024",
    group_by="productid",
    metrics=["sum(quantity)", "sum(extendedamount)", "count(distinct orderid)"]
)
```

**Análises Possíveis:**
- Produtos mais vendidos por período
- Sazonalidade de vendas
- Ticket médio por período
- Produtos frequentemente comprados juntos (cross-sell)
- Clientes que pararam de comprar (churn)

---

### 3. 🏢 Localizar por Segmento ou CNAE

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Account | ⭐⭐⭐⭐⭐ | industrycode, cnae_description, segment |
| Industry | ⭐⭐⭐⭐ | cnae_code, sector, segment |
| Order | ⭐⭐⭐ | Para análise de performance por segmento |

**Query Exemplo:**
```python
# Empresas do setor financeiro (CNAE 64xx)
accounts = search_accounts(
    filter_query="startswith(new_industrycode, '64')",
    select="accountid,name,new_cnpj,new_industrycode,revenue"
)

# Análise por segmento
segment_analysis = {
    "Varejo": search_accounts(filter_query="new_segment eq 'Varejo'"),
    "Indústria": search_accounts(filter_query="new_segment eq 'Indústria'"),
    "Serviços": search_accounts(filter_query="new_segment eq 'Serviços'")
}
```

**Análises Possíveis:**
- Performance de vendas por CNAE
- Penetração de mercado por segmento
- Tamanho médio de deal por indústria
- Ciclo de vendas por setor

---

### 4. 📊 Pontuar Empresa Quanto ao Potencial

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Account | ⭐⭐⭐⭐⭐ | revenue, numberofemployees, customerscore |
| Order | ⭐⭐⭐⭐⭐ | Total histórico, frequência, recência |
| Opportunity | ⭐⭐⭐⭐ | Pipeline ativo, valores |
| Contract | ⭐⭐⭐⭐ | MRR, ARR, duração |
| Contact | ⭐⭐⭐ | Decisores, influenciadores |

**Modelo de Scoring:**
```python
def calculate_account_score(account, orders, opportunities, contracts, contacts):
    """
    Score de 0-100 baseado em múltiplos fatores
    """
    score = 0
    
    # Tamanho da Empresa (30 pontos)
    if account.revenue > 10_000_000:
        score += 15
    elif account.revenue > 1_000_000:
        score += 10
    elif account.revenue > 100_000:
        score += 5
    
    if account.numberofemployees > 500:
        score += 15
    elif account.numberofemployees > 100:
        score += 10
    elif account.numberofemployees > 20:
        score += 5
    
    # Histórico de Compras (25 pontos)
    total_purchases = sum(order.totalamount for order in orders)
    if total_purchases > 500_000:
        score += 15
    elif total_purchases > 100_000:
        score += 10
    elif total_purchases > 10_000:
        score += 5
    
    # Recência (RFM - Recency) (10 pontos)
    days_since_last_purchase = (datetime.now() - max(order.order_date)).days
    if days_since_last_purchase < 30:
        score += 10
    elif days_since_last_purchase < 90:
        score += 7
    elif days_since_last_purchase < 180:
        score += 4
    
    # Frequência (10 pontos)
    purchase_frequency = len(orders) / max(1, days_active / 365)
    if purchase_frequency > 4:  # Mais de 4 compras/ano
        score += 10
    elif purchase_frequency > 2:
        score += 7
    elif purchase_frequency > 1:
        score += 4
    
    # Contratos Ativos (15 pontos)
    active_contracts_value = sum(c.monthly_recurring_revenue * 12 
                                   for c in contracts if c.statecode == 0)
    if active_contracts_value > 100_000:
        score += 15
    elif active_contracts_value > 50_000:
        score += 10
    elif active_contracts_value > 10_000:
        score += 5
    
    # Pipeline (Oportunidades Ativas) (5 pontos)
    active_pipeline = sum(o.estimatedvalue * (o.closeprobability / 100) 
                          for o in opportunities if o.statecode == 0)
    if active_pipeline > 100_000:
        score += 5
    elif active_pipeline > 50_000:
        score += 3
    elif active_pipeline > 10_000:
        score += 1
    
    # Qualidade de Contatos (5 pontos)
    decision_makers = sum(1 for c in contacts if c.decision_maker)
    if decision_makers >= 3:
        score += 5
    elif decision_makers >= 1:
        score += 3
    
    return min(100, score)
```

**Fatores de Scoring:**
- Tamanho (revenue, employees)
- Histórico de compras (RFM: Recency, Frequency, Monetary)
- Contratos ativos (MRR/ARR)
- Pipeline de oportunidades
- Qualidade de relacionamento (contatos, visitas)
- Engajamento (interações, visitas)

---

### 5. 👥 Visão de Contatos

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Contact | ⭐⭐⭐⭐⭐ | Todos os campos |
| Account | ⭐⭐⭐⭐⭐ | Empresa do contato |
| Opportunity | ⭐⭐⭐ | Oportunidades relacionadas |
| Visit | ⭐⭐⭐ | Histórico de visitas |

**Query Exemplo:**
```python
# Visão completa de contatos de uma empresa
account_contacts = search_contacts(
    filter_query=f"_parentcustomerid_value eq '{account_id}'",
    orderby="new_decision_maker desc, new_seniority_level desc"
)

# Contatos tomadores de decisão
decision_makers = [c for c in account_contacts if c.decision_maker]

# Contatos influenciadores
influencers = [c for c in account_contacts if c.influencer]

# Estrutura hierárquica
org_chart = build_org_chart(account_contacts)  # Baseado em reports_to
```

**Visualização:**
```
Empresa XYZ
├── João Silva (CEO) - Tomador de Decisão ⭐
│   ├── Maria Santos (CFO) - Tomador de Decisão ⭐
│   └── Pedro Costa (CTO) - Tomador de Decisão ⭐
│       └── Ana Lima (Dev Manager) - Influenciador
└── Carlos Souza (COO)
    └── Lucia Oliveira (Procurement Manager) - Tomador de Decisão ⭐
```

---

### 6. 🔄 Visão de Compras e Renovações de Produto

**Objetos Necessários:**
| Objeto | Prioridade | Campos Críticos |
|--------|-----------|-----------------|
| Contract | ⭐⭐⭐⭐⭐ | renewal_date, contract_end_date, MRR/ARR |
| Order | ⭐⭐⭐⭐⭐ | order_date, order_type (renewal) |
| OrderProduct | ⭐⭐⭐⭐ | Produtos para renovação |
| Product | ⭐⭐⭐⭐ | is_recurring, renewal_frequency |
| Account | ⭐⭐⭐⭐ | Cliente |

**Query Exemplo:**
```python
# Contratos para renovação nos próximos 90 dias
renewal_pipeline = search_contracts(
    filter_query=f"""
        new_renewal_date ge '{today}' and 
        new_renewal_date le '{today + 90}' and
        statecode eq 0
    """,
    orderby="new_renewal_date asc"
)

# Produtos recorrentes comprados pelo cliente
recurring_products = search_order_products(
    filter_query=f"""
        _orderid_value/customerid eq '{account_id}' and
        _productid_value/new_is_recurring eq true
    """,
    expand="product,order"
)

# Histórico de renovações
renewal_history = search_orders(
    filter_query=f"""
        customerid eq '{account_id}' and
        new_order_type eq 'Renewal'
    """,
    orderby="new_order_date desc"
)
```

**Dashboard de Renovações:**
```
Próximas Renovações (90 dias):
┌─────────────────────────────────────────────────────┐
│ Contrato #123 - Empresa ABC                        │
│ Renovação: 15/02/2024 (30 dias)                   │
│ MRR: R$ 5.000  |  ARR: R$ 60.000                   │
│ Status: ⚠️  Ação necessária                         │
├─────────────────────────────────────────────────────┤
│ Contrato #456 - Empresa XYZ                        │
│ Renovação: 01/03/2024 (45 dias)                   │
│ MRR: R$ 12.000  |  ARR: R$ 144.000                 │
│ Status: ✅ Em negociação                            │
└─────────────────────────────────────────────────────┘

Taxa de Renovação (últimos 12 meses): 85%
Receita em Risco (próximos 90 dias): R$ 500.000
```

---

## 🎯 Priorização de Implementação

### Fase 1: Essencial (Já Implementado)
- ✅ Account
- ✅ Contact
- ✅ Opportunity
- ✅ Quote
- ✅ Product
- ✅ OpportunityProduct

### Fase 2: Crítico para BI (Implementar Urgente)
- 🔴 **Order** - Essencial para análise de compras
- 🔴 **OrderProduct** - Detalhamento de compras
- 🔴 **Contract** - Essencial para renovações

### Fase 3: Importante (Implementar Médio Prazo)
- 🟡 **Visit** - Otimização de rotas
- 🟡 **Industry** - Segmentação por CNAE

### Fase 4: Campos Adicionais (Implementar Gradualmente)
- 🟢 Campos de scoring em Account
- 🟢 Campos de segmentação em Account
- 🟢 Campos de renovação em Product
- 🟢 Campos de hierarquia em Contact

---

## 📊 Métricas de Sucesso

Após implementação completa, será possível calcular:

### Métricas de Vendas
- Total de vendas por período
- Ticket médio
- Taxa de conversão (oportunidade → pedido)
- Ciclo de vendas médio
- Taxa de win/loss

### Métricas de Cliente
- Customer Lifetime Value (CLV)
- Customer Acquisition Cost (CAC)
- Churn rate
- Net Revenue Retention (NRR)
- Gross Revenue Retention (GRR)

### Métricas de Renovação
- Renewal rate
- Expansion rate
- Contraction rate
- Revenue churn

### Métricas de Eficiência
- Visitas por dia
- Km percorridos por visita
- Taxa de conversão de visitas
- Tempo médio de deslocamento

---

## 🚀 Próximos Passos

1. **Implementar Modelos Faltantes**
   - Adicionar Order, OrderProduct, Contract ao dataverse_models.py
   - Adicionar Industry e Visit (opcional)

2. **Estender Modelos Existentes**
   - Adicionar campos de segmentação ao Account
   - Adicionar campos de hierarquia ao Contact
   - Adicionar campos de renovação ao Product

3. **Criar Ferramentas MCP**
   - Adicionar tools para Order, Contract
   - Criar tools de análise (scoring, segmentação)
   - Criar tools de otimização de rotas

4. **Implementar Cliente Dataverse**
   - Métodos de busca para novos objetos
   - Métodos de análise e agregação
   - Métodos de scoring

5. **Documentação**
   - Atualizar API.md com novos endpoints
   - Criar guia de análise de BI
   - Criar exemplos de queries complexas

---

## 📚 Referências

- [Dataverse Web API](https://docs.microsoft.com/power-apps/developer/data-platform/webapi/overview)
- [Dataverse Entity Reference](https://docs.microsoft.com/power-apps/developer/data-platform/reference/entities/overview)
- [Sales Entities](https://docs.microsoft.com/dynamics365/sales/developer/entities/overview)
- [Contract Management](https://docs.microsoft.com/dynamics365/sales/create-edit-contracts)

---

**Última atualização:** Janeiro 2024  
**Autor:** MCP Dataverse Team
