#!/usr/bin/env python3
"""
Recipe collection for frozen meal prep (marmitas congeladas)
Recipes use ingredients commonly available in Porto Alegre supermarkets
"""

# Recipe data structure:
# Each recipe includes:
# - name: recipe name
# - description: brief description
# - ingredients: list of (quantity, unit, ingredient, calories_per_unit, glycemic_index)
# - instructions: step-by-step instructions
# - servings: number of servings

RECIPES = [
    {
        "name": "Frango com Batata Doce e Brócolis",
        "description": "Proteína magra com carboidrato de baixo índice glicêmico e vegetais",
        "servings": 4,
        "ingredients": [
            {"qty": 500, "unit": "g", "name": "Peito de frango", "cal_per_100g": 165, "gi": 0},
            {"qty": 400, "unit": "g", "name": "Batata doce", "cal_per_100g": 86, "gi": 63},
            {"qty": 300, "unit": "g", "name": "Brócolis", "cal_per_100g": 34, "gi": 15},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Azeite de oliva", "cal_per_unit": 120, "gi": 0},
            {"qty": 1, "unit": "unidade(s)", "name": "Cebola média", "cal_per_unit": 44, "gi": 10},
            {"qty": 3, "unit": "dente(s)", "name": "Alho", "cal_per_unit": 4, "gi": 0},
        ],
        "instructions": [
            "Corte o frango em cubos e tempere com sal, alho amassado e pimenta",
            "Descasque e corte a batata doce em cubos médios",
            "Lave e corte o brócolis em floretes",
            "Aqueça o azeite em uma panela e refogue a cebola picada",
            "Adicione o frango e deixe dourar",
            "Adicione a batata doce, 1 xícara de água e cozinhe por 15 minutos",
            "Adicione o brócolis e cozinhe por mais 5 minutos",
            "Ajuste o sal e sirva. Para congelar, deixe esfriar completamente antes"
        ]
    },
    {
        "name": "Carne Moída com Abóbora e Feijão",
        "description": "Refeição completa com proteína, fibras e carboidratos complexos",
        "servings": 4,
        "ingredients": [
            {"qty": 500, "unit": "g", "name": "Carne moída magra", "cal_per_100g": 250, "gi": 0},
            {"qty": 400, "unit": "g", "name": "Abóbora cabotiá", "cal_per_100g": 40, "gi": 75},
            {"qty": 300, "unit": "g", "name": "Feijão preto cozido", "cal_per_100g": 130, "gi": 30},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Óleo de soja", "cal_per_unit": 120, "gi": 0},
            {"qty": 1, "unit": "unidade(s)", "name": "Cebola média", "cal_per_unit": 44, "gi": 10},
            {"qty": 2, "unit": "unidade(s)", "name": "Tomate médio", "cal_per_unit": 22, "gi": 15},
            {"qty": 1, "unit": "unidade(s)", "name": "Pimentão verde", "cal_per_unit": 24, "gi": 15},
        ],
        "instructions": [
            "Refogue a cebola picada no óleo até dourar",
            "Adicione a carne moída e deixe cozinhar, mexendo ocasionalmente",
            "Adicione o tomate e pimentão picados",
            "Corte a abóbora em cubos e adicione à panela",
            "Adicione o feijão cozido e 1 xícara de água",
            "Cozinhe por 20 minutos até a abóbora ficar macia",
            "Tempere com sal, pimenta e salsinha. Deixe esfriar antes de congelar"
        ]
    },
    {
        "name": "Tilápia ao Molho com Arroz Integral e Cenoura",
        "description": "Peixe leve com carboidrato integral e vegetais coloridos",
        "servings": 4,
        "ingredients": [
            {"qty": 600, "unit": "g", "name": "Filé de tilápia", "cal_per_100g": 128, "gi": 0},
            {"qty": 300, "unit": "g", "name": "Arroz integral cozido", "cal_per_100g": 123, "gi": 50},
            {"qty": 300, "unit": "g", "name": "Cenoura", "cal_per_100g": 41, "gi": 35},
            {"qty": 200, "unit": "ml", "name": "Molho de tomate", "cal_per_100ml": 40, "gi": 35},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Azeite de oliva", "cal_per_unit": 120, "gi": 0},
            {"qty": 1, "unit": "unidade(s)", "name": "Cebola média", "cal_per_unit": 44, "gi": 10},
        ],
        "instructions": [
            "Tempere os filés de tilápia com sal, limão e alho",
            "Descasque e corte a cenoura em rodelas",
            "Refogue a cebola no azeite",
            "Adicione o molho de tomate e a cenoura, cozinhe por 10 minutos",
            "Coloque os filés de peixe sobre o molho",
            "Tampe e cozinhe por 15 minutos em fogo baixo",
            "Sirva com arroz integral. Congele em porções individuais após esfriar"
        ]
    },
    {
        "name": "Almôndegas de Carne com Purê de Mandioca",
        "description": "Proteína em formato prático com acompanhamento tradicional brasileiro",
        "servings": 4,
        "ingredients": [
            {"qty": 500, "unit": "g", "name": "Carne moída", "cal_per_100g": 250, "gi": 0},
            {"qty": 1, "unit": "unidade(s)", "name": "Ovo", "cal_per_unit": 78, "gi": 0},
            {"qty": 50, "unit": "g", "name": "Farinha de rosca", "cal_per_100g": 395, "gi": 70},
            {"qty": 500, "unit": "g", "name": "Mandioca", "cal_per_100g": 160, "gi": 46},
            {"qty": 200, "unit": "ml", "name": "Molho de tomate", "cal_per_100ml": 40, "gi": 35},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Óleo", "cal_per_unit": 120, "gi": 0},
        ],
        "instructions": [
            "Misture a carne moída com ovo, farinha de rosca, sal e alho",
            "Faça bolinhas pequenas (almôndegas)",
            "Doure as almôndegas no óleo e reserve",
            "Cozinhe a mandioca em água com sal até ficar macia",
            "Escorra e amasse a mandioca fazendo um purê",
            "Aqueça o molho de tomate e adicione as almôndegas",
            "Cozinhe por 10 minutos. Sirva com o purê de mandioca",
            "Congele as almôndegas com molho separadamente do purê"
        ]
    },
    {
        "name": "Strogonoff de Frango com Arroz e Vagem",
        "description": "Versão caseira do clássico com acompanhamentos balanceados",
        "servings": 4,
        "ingredients": [
            {"qty": 600, "unit": "g", "name": "Peito de frango", "cal_per_100g": 165, "gi": 0},
            {"qty": 200, "unit": "ml", "name": "Creme de leite light", "cal_per_100ml": 130, "gi": 0},
            {"qty": 100, "unit": "g", "name": "Champignon", "cal_per_100g": 22, "gi": 15},
            {"qty": 300, "unit": "g", "name": "Arroz branco cozido", "cal_per_100g": 130, "gi": 70},
            {"qty": 300, "unit": "g", "name": "Vagem", "cal_per_100g": 31, "gi": 15},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Óleo", "cal_per_unit": 120, "gi": 0},
            {"qty": 1, "unit": "unidade(s)", "name": "Cebola média", "cal_per_unit": 44, "gi": 10},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Molho de tomate", "cal_per_unit": 15, "gi": 35},
        ],
        "instructions": [
            "Corte o frango em tiras e tempere com sal",
            "Refogue a cebola picada no óleo",
            "Adicione o frango e deixe dourar",
            "Acrescente o champignon fatiado e o molho de tomate",
            "Adicione o creme de leite e cozinhe por 5 minutos",
            "Cozinhe a vagem no vapor até ficar al dente",
            "Sirva o strogonoff com arroz e vagem",
            "Para congelar, embale em porções e descongele na geladeira"
        ]
    },
    {
        "name": "Carne de Panela com Batata Inglesa e Couve",
        "description": "Receita tradicional brasileira adequada para congelamento",
        "servings": 4,
        "ingredients": [
            {"qty": 600, "unit": "g", "name": "Músculo bovino", "cal_per_100g": 210, "gi": 0},
            {"qty": 400, "unit": "g", "name": "Batata inglesa", "cal_per_100g": 77, "gi": 82},
            {"qty": 200, "unit": "g", "name": "Couve manteiga", "cal_per_100g": 27, "gi": 15},
            {"qty": 2, "unit": "unidade(s)", "name": "Tomate médio", "cal_per_unit": 22, "gi": 15},
            {"qty": 1, "unit": "unidade(s)", "name": "Cebola média", "cal_per_unit": 44, "gi": 10},
            {"qty": 2, "unit": "colher(es) de sopa", "name": "Óleo", "cal_per_unit": 120, "gi": 0},
        ],
        "instructions": [
            "Corte a carne em cubos grandes e tempere com sal e alho",
            "Doure a carne no óleo em uma panela de pressão",
            "Adicione cebola e tomate picados",
            "Adicione 2 xícaras de água e cozinhe na pressão por 30 minutos",
            "Descasque e corte as batatas em pedaços médios",
            "Após despressurizar, adicione as batatas e cozinhe por mais 10 minutos",
            "Pique a couve e refogue rapidamente em outro recipiente",
            "Sirva a carne com batata e couve. Congele sem a couve (adicione ao reaquecer)"
        ]
    },
]


def calculate_recipe_nutrition(recipe):
    """Calculate total calories and glycemic load for a recipe"""
    total_calories = 0
    total_gl = 0  # Glycemic Load
    total_carbs = 0
    
    for ing in recipe["ingredients"]:
        qty = ing["qty"]
        
        # Calculate calories
        if "cal_per_100g" in ing:
            calories = (ing["cal_per_100g"] * qty) / 100
        elif "cal_per_100ml" in ing:
            calories = (ing["cal_per_100ml"] * qty) / 100
        else:
            calories = ing["cal_per_unit"] * qty
        
        total_calories += calories
        
        # Calculate glycemic load (GL = GI * carbs / 100)
        # Rough estimation: assume carbs are 30% of calories for carb sources
        gi = ing["gi"]
        if gi > 0:
            # Rough carb estimation (varies by food type)
            if "cal_per_100g" in ing or "cal_per_100ml" in ing:
                estimated_carbs = (qty / 100) * (ing.get("cal_per_100g", ing.get("cal_per_100ml", 0)) * 0.25 / 4)  # carbs = 4 cal/g
            else:
                estimated_carbs = (calories * 0.25 / 4)
            
            gl = (gi * estimated_carbs) / 100
            total_gl += gl
            total_carbs += estimated_carbs
    
    return {
        "total_calories": round(total_calories),
        "calories_per_serving": round(total_calories / recipe["servings"]),
        "total_glycemic_load": round(total_gl, 1),
        "glycemic_load_per_serving": round(total_gl / recipe["servings"], 1),
        "glycemic_load_category": categorize_gl(total_gl / recipe["servings"])
    }


def categorize_gl(gl_per_serving):
    """Categorize glycemic load per serving"""
    if gl_per_serving < 10:
        return "Baixo"
    elif gl_per_serving < 20:
        return "Médio"
    else:
        return "Alto"


if __name__ == "__main__":
    # Test the calculation
    for recipe in RECIPES:
        print(f"\n{recipe['name']}:")
        nutrition = calculate_recipe_nutrition(recipe)
        print(f"  Calorias por porção: {nutrition['calories_per_serving']} kcal")
        print(f"  Carga glicêmica por porção: {nutrition['glycemic_load_per_serving']} ({nutrition['glycemic_load_category']})")
