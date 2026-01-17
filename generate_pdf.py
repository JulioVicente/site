#!/usr/bin/env python3
"""
Generate PDF with recipes for frozen meal prep
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

from recipes import RECIPES, calculate_recipe_nutrition


def create_recipe_pdf(filename="receitas_marmitas.pdf"):
    """Generate a PDF with all recipes"""
    
    # Create document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    recipe_title_style = ParagraphStyle(
        'RecipeTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#27AE60'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2980B9'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Title page
    elements.append(Paragraph("Receitas para Marmitas Congeladas", title_style))
    elements.append(Paragraph(
        "Receitas práticas com ingredientes disponíveis em Porto Alegre<br/>Com informações calóricas e glicêmicas",
        subtitle_style
    ))
    elements.append(Spacer(1, 1*cm))
    
    # Introduction
    intro_text = """
    Este guia contém receitas saudáveis e práticas, especialmente desenvolvidas para 
    preparar marmitas congeladas. Todas as receitas utilizam ingredientes facilmente 
    encontrados em supermercados de Porto Alegre e são adequadas para congelamento, 
    mantendo sabor e textura após o descongelamento.
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Tips section
    elements.append(Paragraph("Dicas para Congelamento:", section_title_style))
    tips = [
        "Deixe as preparações esfriarem completamente antes de congelar",
        "Use recipientes próprios para congelamento ou sacos zip-lock",
        "Retire o máximo de ar possível das embalagens",
        "Etiquete com o nome da receita e data de preparo",
        "Consuma em até 3 meses para melhor qualidade",
        "Descongele na geladeira na noite anterior ou use micro-ondas",
    ]
    
    for tip in tips:
        elements.append(Paragraph(f"• {tip}", normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # Glycemic load explanation
    elements.append(Paragraph("Sobre a Carga Glicêmica:", section_title_style))
    gl_text = """
    A carga glicêmica (CG) indica o impacto real do alimento nos níveis de açúcar no sangue.
    <b>Baixo (< 10)</b>: Impacto mínimo; <b>Médio (10-20)</b>: Impacto moderado; 
    <b>Alto (> 20)</b>: Impacto significativo. Refeições com CG baixa a média são ideais 
    para controle de peso e energia estável.
    """
    elements.append(Paragraph(gl_text, normal_style))
    
    elements.append(PageBreak())
    
    # Add each recipe
    for i, recipe in enumerate(RECIPES):
        # Calculate nutrition
        nutrition = calculate_recipe_nutrition(recipe)
        
        # Recipe title
        elements.append(Paragraph(recipe["name"], recipe_title_style))
        elements.append(Paragraph(recipe["description"], normal_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # Nutrition information table
        nutrition_data = [
            ["Porções", "Calorias/Porção", "Carga Glicêmica/Porção"],
            [
                str(recipe["servings"]),
                f"{nutrition['calories_per_serving']} kcal",
                f"{nutrition['glycemic_load_per_serving']} ({nutrition['glycemic_load_category']})"
            ]
        ]
        
        nutrition_table = Table(nutrition_data, colWidths=[3*cm, 4*cm, 5*cm])
        nutrition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(nutrition_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # Ingredients section
        elements.append(Paragraph("Ingredientes:", section_title_style))
        
        for ing in recipe["ingredients"]:
            qty_str = f"{ing['qty']:.0f}" if ing['qty'] >= 1 else f"{ing['qty']:.1f}"
            ing_text = f"• {qty_str} {ing['unit']} de {ing['name']}"
            elements.append(Paragraph(ing_text, normal_style))
        
        elements.append(Spacer(1, 0.3*cm))
        
        # Instructions section
        elements.append(Paragraph("Modo de Preparo:", section_title_style))
        
        for j, instruction in enumerate(recipe["instructions"], 1):
            elements.append(Paragraph(f"{j}. {instruction}", normal_style))
        
        # Add page break between recipes (except for the last one)
        if i < len(RECIPES) - 1:
            elements.append(PageBreak())
    
    # Footer section
    elements.append(PageBreak())
    elements.append(Spacer(1, 2*cm))
    footer_text = f"""
    <para align=center>
    <b>Receitas para Marmitas Congeladas</b><br/>
    Documento gerado em {datetime.now().strftime('%d/%m/%Y')}<br/>
    <i>Bom apetite e ótimas marmitas!</i>
    </para>
    """
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    print(f"PDF gerado com sucesso: {filename}")


if __name__ == "__main__":
    create_recipe_pdf()
