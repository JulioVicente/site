# 📋 BLOCOS PRONTOS PARA ABERTURA DE TICKET

---

## 🎫 BLOCO 1: TÍTULO DO TICKET
```
DKIM Selector1 stuck in VerificationInProgress after 7+ days - bestsoft.com.br
```

---

## 📝 BLOCO 2: DESCRIÇÃO COMPLETA
```
RESUMO
O domínio bestsoft.com.br está configurado no Azure Communication Services há mais de 7 dias, mas o DKIM selector1 permanece em VerificationInProgress e DMARC em NotStarted, mesmo com todos os registros DNS configurados corretamente.

RECURSO AFETADO
- Resource ID: /subscriptions/6f2e29ef-b429-43e7-8229-4e5c1f2532c1/resourceGroups/ACS/providers/Microsoft.Communication/EmailServices/bestsoft-email-service/Domains/bestsoft.com.br
- Domain: bestsoft.com.br
- Location: global
- Data Location: United States

PROBLEMA TÉCNICO
1. DKIM selector1: Status "VerificationInProgress" há mais de 7 dias sem errorCode
2. DMARC: Status "NotStarted" mesmo com registro TXT configurado
3. DKIM selector2: Verificado com sucesso (configuração idêntica ao selector1)

EVIDÊNCIAS DNS (Verificado em 30/01/2026 às 15:51 BRT)

✓ selector1 CNAME configurado:
  Nome: selector1-azurecomm-prod-net._domainkey.bestsoft.com.br
  Valor: selector1-azurecomm-prod-net._domainkey.azurecomm.net.
  Status DNS: Respondendo corretamente

✓ selector2 CNAME configurado:
  Nome: selector2-azurecomm-prod-net._domainkey.bestsoft.com.br
  Valor: selector2-azurecomm-prod-net._domainkey.azurecomm.net.
  Status Azure: Verified

✓ DMARC TXT configurado:
  Nome: _dmarc.bestsoft.com.br
  Valor: v=DMARC1; p=quarantine; pct=100; sp=reject; rua=mailto:admin@bestsoft.com.br
  Status DNS: Respondendo corretamente

✓ SPF TXT: Verificado pelo Azure
✓ Domain Verification TXT: Verificado pelo Azure

ANÁLISE DO PROBLEMA
- Todos os registros DNS estão corretos e respondendo
- Já passou mais de 7 dias desde a configuração (tempo suficiente para propagação)
- selector2 foi verificado com sucesso (mesma configuração do selector1)
- Não há errorCode específico reportado pelo Azure
- Comportamento inconsistente do validador do Azure Communication Services

SOLICITAÇÃO
1. Forçar re-verificação do DKIM selector1
2. Esclarecer por que o validador não reconhece o registro DNS que está correto
3. Confirmar se DMARC é verificado automaticamente ou se o status "NotStarted" é esperado

IMPACTO
- Operacional: BAIXO (serviço funcionando com selector2)
- Compliance: MÉDIO (status incorreto dificulta auditorias)
```

---

## 👤 BLOCO 3: INFORMAÇÕES DE CONTATO
```
Nome: Julio Vicente
Email: julio@bestsoft.com.br
Telefone: +55 51 99342-3901
País: Brasil
Idioma Preferido: Português (pt-BR)
Timezone: (UTC-03:00) Brasília
```

---

## 🏢 BLOCO 4: INFORMAÇÕES DE PARTNER (Se solicitado)
```
Microsoft Partner (MPN)
Tenant ID: ac2edcbd-0bbe-4ae8-b2cf-c819f03140b6
Subscription: Assinatura do Visual Studio Enterprise – MPN - ok
Subscription ID: 6f2e29ef-b429-43e7-8229-4e5c1f2532c1
```

---

## 🔍 BLOCO 5: DADOS TÉCNICOS DNS (Opcional - Detalhamento)
```
CONSULTAS DNS REALIZADAS:

$ dig selector1-azurecomm-prod-net._domainkey.bestsoft.com.br CNAME @ns1-08.azure-dns.com +short
selector1-azurecomm-prod-net._domainkey.azurecomm.net.

$ dig selector2-azurecomm-prod-net._domainkey.bestsoft.com.br CNAME @ns1-08.azure-dns.com +short
selector2-azurecomm-prod-net._domainkey.azurecomm.net.

$ dig _dmarc.bestsoft.com.br TXT @ns1-08.azure-dns.com +short
"v=DMARC1; p=quarantine; pct=100; sp=reject; rua=mailto:admin@bestsoft.com.br;ruf=mailto:admin@bestsoft.com.br;"

$ dig bestsoft.com.br TXT @ns1-08.azure-dns.com +short | grep spf
"v=spf1 include:spf.mailjet.com include:spf.protection.outlook.com include:beslink.bestsoft.com.br include:sendgrid.net ip4:20.72.188.1 ip4:20.93.203.168 -all"

Nameservers Azure DNS:
- ns1-08.azure-dns.com
- ns2-08.azure-dns.net
- ns3-08.azure-dns.org
- ns4-08.azure-dns.info
```

---

## 📊 BLOCO 6: STATUS AZURE (JSON do Resource)
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

## 🎯 INSTRUÇÕES DE USO:

### Para Partner Center:
1. Copie o **BLOCO 1** no campo "Title"
2. Copie o **BLOCO 2** no campo "Description"
3. Cole **BLOCO 3** no final da descrição ou nos campos de contato
4. Anexe o arquivo: Azure-Support-Ticket-DKIM-Verification.md

### Para Azure Portal:
1. Acesse: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest
2. Preencha os campos básicos
3. Cole os blocos conforme solicitado
4. Severidade: **C - Minimal Impact**

### Para Telefone (0800 762 1146):
- Tenha os **BLOCOS 1, 3 e 4** em mãos
- Mencione o Resource ID do **BLOCO 2**

---

✅ **Todos os blocos estão prontos para copiar e colar!**
