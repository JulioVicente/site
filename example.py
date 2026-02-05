#!/usr/bin/env python3
"""
Example of how to use the recipe system
"""

from recipes import RECIPES, calculate_recipe_nutrition

def show_recipe_summary():
    """Display a summary of all available recipes"""
    print("\n" + "="*70)
    print("RECEITAS PARA MARMITAS CONGELADAS")
    print("="*70 + "\n")
    
    for i, recipe in enumerate(RECIPES, 1):
        nutrition = calculate_recipe_nutrition(recipe)
        
        print(f"{i}. {recipe['name']}")
        print(f"   {recipe['description']}")
        print(f"   📊 {nutrition['calories_per_serving']} kcal/porção | "
              f"CG: {nutrition['glycemic_load_per_serving']} ({nutrition['glycemic_load_category']})")
        print(f"   👥 {recipe['servings']} porções\n")

def show_shopping_list():
    """Generate a shopping list with all unique ingredients"""
    print("\n" + "="*70)
    print("LISTA DE COMPRAS (TODOS OS INGREDIENTES)")
    print("="*70 + "\n")
    
    # Collect all unique ingredients
    ingredients_set = set()
    for recipe in RECIPES:
        for ing in recipe["ingredients"]:
            ingredients_set.add(ing["name"])
    
    # Sort and display
    for ing in sorted(ingredients_set):
        print(f"  • {ing}")
    
    print(f"\nTotal de ingredientes diferentes: {len(ingredients_set)}")

def show_recipe_details(recipe_index):
    """Show detailed information for a specific recipe"""
    if recipe_index < 0 or recipe_index >= len(RECIPES):
        print("Índice de receita inválido!")
        return
    
    recipe = RECIPES[recipe_index]
    nutrition = calculate_recipe_nutrition(recipe)
    
    print("\n" + "="*70)
    print(recipe['name'].upper())
    print("="*70)
    print(f"\n{recipe['description']}\n")
    
    print(f"Porções: {recipe['servings']}")
    print(f"Calorias por porção: {nutrition['calories_per_serving']} kcal")
    print(f"Carga glicêmica por porção: {nutrition['glycemic_load_per_serving']} "
          f"({nutrition['glycemic_load_category']})\n")
    
    print("INGREDIENTES:")
    for ing in recipe["ingredients"]:
        qty_str = f"{ing['qty']:.0f}" if ing['qty'] >= 1 else f"{ing['qty']:.1f}"
        print(f"  • {qty_str} {ing['unit']} de {ing['name']}")
    
    print("\nMODO DE PREPARO:")
    for i, instruction in enumerate(recipe["instructions"], 1):
        print(f"  {i}. {instruction}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Show summary of all recipes
    show_recipe_summary()
    
    # Show shopping list
    show_shopping_list()
    
    # Show details of first recipe as example
    print("\n\nDETALHES DA PRIMEIRA RECEITA:")
    show_recipe_details(0)
