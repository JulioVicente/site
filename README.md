# site

## Receitas para Marmitas Congeladas

Este projeto coleta receitas adequadas para marmitas congeladas, utilizando ingredientes facilmente disponíveis em supermercados de Porto Alegre. Cada receita inclui informações calóricas e glicêmicas detalhadas.

### Características

- **6 receitas completas** adequadas para congelamento
- **Ingredientes disponíveis** em supermercados de Porto Alegre
- **Informações nutricionais**: calorias e carga glicêmica por porção
- **Geração de PDF** formatado e profissional

### Receitas Incluídas

1. Frango com Batata Doce e Brócolis
2. Carne Moída com Abóbora e Feijão
3. Tilápia ao Molho com Arroz Integral e Cenoura
4. Almôndegas de Carne com Purê de Mandioca
5. Strogonoff de Frango com Arroz e Vagem
6. Carne de Panela com Batata Inglesa e Couve

### Como Usar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Gerar o PDF com as receitas:**
   ```bash
   python3 generate_pdf.py
   ```

   Isso criará o arquivo `receitas_marmitas.pdf` com todas as receitas formatadas.

3. **Testar cálculos nutricionais:**
   ```bash
   python3 recipes.py
   ```

### Estrutura do Projeto

- `recipes.py`: Dados das receitas e funções de cálculo nutricional
- `generate_pdf.py`: Script para gerar o PDF formatado
- `requirements.txt`: Dependências do projeto
- `receitas_marmitas.pdf`: PDF gerado com as receitas (criado após executar generate_pdf.py)

### Informações Nutricionais

Cada receita inclui:
- **Calorias por porção**: Energia total fornecida
- **Carga glicêmica por porção**: Impacto nos níveis de açúcar no sangue
  - Baixo (< 10): Ideal para controle de peso
  - Médio (10-20): Impacto moderado
  - Alto (> 20): Impacto significativo

### Dicas para Congelamento

- Deixe as preparações esfriarem completamente antes de congelar
- Use recipientes próprios para congelamento ou sacos zip-lock
- Retire o máximo de ar possível das embalagens
- Etiquete com o nome da receita e data de preparo
- Consuma em até 3 meses para melhor qualidade
- Descongele na geladeira na noite anterior ou use micro-ondas
