# Azure Support Ticket - DKIM Verification Issue
**Data do Relatório:** 30 de Janeiro de 2026  
**Reportado por:** Julio Vicente

---

## 📋 RESUMO DO PROBLEMA

O domínio **bestsoft.com.br** está configurado no Azure Communication Services há **mais de 7 dias**, mas o status de verificação permanece incorreto:

| Registro | Status Reportado pelo Azure | Status Real no DNS |
|----------|----------------------------|-------------------|
| DKIM selector1 | ⏳ **VerificationInProgress** | ✅ **CONFIGURADO E FUNCIONANDO** |
| DMARC | ⚠️ **NotStarted** | ✅ **CONFIGURADO E FUNCIONANDO** |
| Domain Verification | ✅ Verified | ✅ Verified |
| SPF | ✅ Verified | ✅ Verified |
| DKIM selector2 | ✅ Verified | ✅ Verified |

**Problema:** O validador do Azure Communication Services não está reconhecendo que os registros DNS estão corretamente configurados, mesmo após mais de 7 dias de configuração.

---

## 🔧 DETALHES DOS RECURSOS AZURE

### Resource Information
- **Subscription ID:** `6f2e29ef-b429-43e7-8229-4e5c1f2532c1`
- **Resource Group:** `ACS`
- **Resource Name:** `bestsoft.com.br`
- **Resource Type:** `microsoft.communication/emailservices/domains`
- **Resource ID:** `/subscriptions/6f2e29ef-b429-43e7-8229-4e5c1f2532c1/resourceGroups/ACS/providers/Microsoft.Communication/EmailServices/bestsoft-email-service/Domains/bestsoft.com.br`
- **Location:** `global`
- **Data Location:** `United States`
- **Domain Management:** `CustomerManaged`
- **Provisioning State:** `Succeeded`

### Azure DNS Zone
- **DNS Zone Name:** `bestsoft.com.br`
- **Name Servers:**
  - `ns1-08.azure-dns.com.`
  - `ns2-08.azure-dns.net.`
  - `ns3-08.azure-dns.org.`
  - `ns4-08.azure-dns.info.`

---

## ✅ EVIDÊNCIAS TÉCNICAS - DNS CONFIGURADO CORRETAMENTE

### Verificação Realizada em: 30/01/2026 às 15:51 -03

### 1. DKIM Selector1 (Problema Reportado)
```bash
$ dig selector1-azurecomm-prod-net._domainkey.bestsoft.com.br CNAME +short
selector1-azurecomm-prod-net._domainkey.azurecomm.net.
```
**Status:** ✅ **CNAME configurado corretamente**  
**Valor Esperado pelo Azure:** `selector1-azurecomm-prod-net._domainkey.azurecomm.net`  
**Valor Atual no DNS:** `selector1-azurecomm-prod-net._domainkey.azurecomm.net.`  
**TTL:** 3600 segundos

### 2. DKIM Selector2 (Verificado com Sucesso)
```bash
$ dig selector2-azurecomm-prod-net._domainkey.bestsoft.com.br CNAME +short
selector2-azurecomm-prod-net._domainkey.azurecomm.net.
```
**Status:** ✅ **CNAME configurado corretamente**  
**Valor Esperado pelo Azure:** `selector2-azurecomm-prod-net._domainkey.azurecomm.net`  
**Valor Atual no DNS:** `selector2-azurecomm-prod-net._domainkey.azurecomm.net.`  
**TTL:** 36000 segundos

**Observação:** Ambos os seletores DKIM têm configuração idêntica, mas apenas o selector2 foi verificado com sucesso.

### 3. DMARC (NotStarted)
```bash
$ dig _dmarc.bestsoft.com.br TXT +short
"v=DMARC1; p=quarantine; pct=100; sp=reject; rua=mailto:admin@bestsoft.com.br;ruf=mailto:admin@bestsoft.com.br;"
```
**Status:** ✅ **TXT configurado corretamente**  
**Política:** Quarantine (rejeitar subdomínios)  
**Relatórios:** Configurados para admin@bestsoft.com.br

### 4. SPF (Verificado com Sucesso)
```bash
$ dig bestsoft.com.br TXT +short | grep spf
"v=spf1 include:spf.mailjet.com include:spf.protection.outlook.com include:beslink.bestsoft.com.br include:sendgrid.net ip4:20.72.188.1 ip4:20.93.203.168 -all"
```
**Status:** ✅ Verificado pelo Azure

### 5. Domain Verification (Verificado com Sucesso)
```bash
$ dig bestsoft.com.br TXT +short | grep ms-domain
"ms-domain-verification=ac7e793b-ea48-45c4-84b9-77cec7fbed4b"
```
**Status:** ✅ Verificado pelo Azure

---

## 🔍 ANÁLISE DO PROBLEMA

### Fatos Confirmados:
1. ✅ Todos os registros DNS necessários estão configurados corretamente
2. ✅ Os registros respondem corretamente quando consultados nos nameservers do Azure
3. ✅ Já passou mais de 7 dias desde a configuração (tempo suficiente para propagação)
4. ✅ Outros registros (SPF, Domain Verification, DKIM selector2) foram verificados com sucesso
5. ⚠️ DKIM selector1 permanece em "VerificationInProgress" sem errorCode
6. ⚠️ DMARC permanece em "NotStarted"

### Comportamento Inconsistente:
- **DKIM selector2** foi verificado com sucesso
- **DKIM selector1** permanece "VerificationInProgress" com registro DNS idêntico
- Ambos apontam para o mesmo destino (*.azurecomm.net)
- Ambos respondem corretamente nas consultas DNS

### Hipóteses:
1. **Cache ou bug no validador do Azure Communication Services**
2. **Problema específico com a validação do selector1**
3. **DMARC não é verificado automaticamente pelo ACS** (comportamento esperado?)

---

## 📊 STATUS ATUAL NO AZURE

```json
{
  "verificationStates": {
    "Domain": {
      "status": "Verified",
      "errorCode": "None"
    },
    "DKIM2": {
      "status": "Verified",
      "errorCode": "None"
    },
    "DKIM": {
      "status": "VerificationInProgress",
      "errorCode": ""
    },
    "DMARC": {
      "status": "NotStarted"
    },
    "SPF": {
      "status": "Verified",
      "errorCode": "None"
    }
  }
}
```

---

## 🎯 SOLICITAÇÃO AO SUPORTE AZURE

Solicitamos investigação e resolução dos seguintes pontos:

### 1. DKIM Selector1 - VerificationInProgress há mais de 7 dias
**Pergunta:** Por que o DKIM selector1 permanece em "VerificationInProgress" quando:
- O registro DNS está configurado corretamente
- Responde às consultas DNS corretamente
- O selector2 (idêntico) foi verificado com sucesso
- Não há errorCode específico reportado

**Ação Solicitada:** 
- Forçar re-verificação do DKIM selector1
- OU esclarecer se há algum problema conhecido
- OU confirmar se o registro precisa de algum ajuste específico

### 2. DMARC - NotStarted
**Pergunta:** O Azure Communication Services verifica registros DMARC automaticamente?

**Ação Solicitada:**
- Se SIM: Forçar verificação do registro DMARC que está configurado
- Se NÃO: Esclarecer a documentação sobre a necessidade do DMARC

---

## 📝 IMPACTO

**Impacto Operacional:** BAIXO
- O serviço de email está funcionando
- O DKIM selector2 verificado é suficiente para envio

**Impacto de Compliance/Segurança:** MÉDIO
- Status de verificação incorreto pode indicar problemas de configuração que não existem
- Dificulta auditorias e verificações de segurança
- Pode afetar deliverability se o Azure decidir usar selector1

---

## 🔗 REFERÊNCIAS

- [Azure Communication Services - Email Domains](https://learn.microsoft.com/azure/communication-services/concepts/email/email-domain-and-sender-authentication)
- [DKIM Configuration Best Practices](https://learn.microsoft.com/azure/communication-services/quickstarts/email/add-custom-verified-domains)

---

## 📞 INFORMAÇÕES DE CONTATO

**Nome:** Julio Vicente  
**Email:** julio@bestsoft.com.br  
**Telefone:** +55 51 99342-3901  
**País:** Brasil  
**Idioma Preferido:** Português  
**Tenant ID:** `ac2edcbd-0bbe-4ae8-b2cf-c819f03140b6`  
**Subscription:** `6f2e29ef-b429-43e7-8229-4e5c1f2532c1`

---

**Observação Final:** Este relatório contém todas as evidências técnicas necessárias para troubleshooting. Estamos à disposição para fornecer logs adicionais ou realizar testes conforme solicitado pelo time de suporte.
