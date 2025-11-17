#!/usr/bin/env python3
"""
Generate a fancy PDF report for EIDL Loans Analysis
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import pandas as pd
from datetime import datetime
import os

def create_fancy_pdf_report():
    """Create a professional PDF report"""
    
    # Create the PDF document
    doc = SimpleDocTemplate("EIDL_Analysis_Executive_Report.pdf", pagesize=A4,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2563eb'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748b'),
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("EIDL LOANS ANALYSIS", title_style))
    story.append(Paragraph("Executive Dashboard & Comprehensive Report", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary Box
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    exec_summary = """
    This comprehensive analysis examines <b>995,409 EIDL loans</b> totaling <b>$72.85 billion</b> 
    distributed during the critical early months of the COVID-19 pandemic (April 1 - June 9, 2020). 
    The program delivered unprecedented economic relief to businesses across all 50 states and territories, 
    supporting the backbone of American commerce during an extraordinary crisis.
    """
    story.append(Paragraph(exec_summary, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Key Statistics Table
    story.append(Paragraph("KEY STATISTICS", heading_style))
    
    stats_data = [
        ['Metric', 'Value', 'Significance'],
        ['Total Loans Approved', '995,409', 'Nearly 1 million businesses supported'],
        ['Total Funding Deployed', '$72.85 Billion', 'Massive economic relief injection'],
        ['Average Loan Size', '$73,186', 'Substantial support per business'],
        ['Median Loan Amount', '$49,000', 'Focus on small enterprises'],
        ['Total Subsidy Cost', '$9.92 Billion', '13.6% average subsidy rate'],
        ['Geographic Coverage', '56 Jurisdictions', 'All states + territories'],
        ['Time Period', '70 Days', 'Rapid deployment during crisis']
    ]
    
    stats_table = Table(stats_data, colWidths=[2.2*inch, 1.5*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    story.append(stats_table)
    story.append(PageBreak())
    
    # Geographic Analysis
    story.append(Paragraph("GEOGRAPHIC DISTRIBUTION ANALYSIS", heading_style))
    
    geo_text = """
    The geographic distribution of EIDL loans reveals significant patterns that align with state economic 
    activity and business density. California emerged as the dominant recipient, securing 17.3% of all loans, 
    followed by Florida and Texas. This distribution reflects both the economic impact of COVID-19 and the 
    relative size of state economies.
    """
    story.append(Paragraph(geo_text, body_style))
    
    # Top States Table
    geo_data = [
        ['Rank', 'State', 'Loan Count', 'Total Amount', 'Avg Amount', '% of Total'],
        ['1', 'California', '172,307', '$13.64B', '$79,136', '17.3%'],
        ['2', 'Florida', '95,167', '$6.22B', '$65,321', '9.6%'],
        ['3', 'Texas', '84,165', '$6.15B', '$73,086', '8.5%'],
        ['4', 'New York', '70,513', '$5.43B', '$76,942', '7.1%'],
        ['5', 'Georgia', '37,746', '$2.56B', '$67,861', '3.8%']
    ]
    
    geo_table = Table(geo_data, colWidths=[0.6*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch])
    geo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(geo_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Business Type Analysis
    story.append(Paragraph("BUSINESS TYPE ANALYSIS", heading_style))
    
    business_text = """
    The program successfully served diverse business structures, with regular businesses (Type R) comprising 
    74.2% of all loans. Notably, minority-owned businesses (Type MR) secured substantial average loan amounts 
    of $81,165, demonstrating the program's effectiveness in supporting underrepresented entrepreneurs.
    """
    story.append(Paragraph(business_text, body_style))
    
    # Business Types Table
    business_data = [
        ['Business Type', 'Description', 'Count', '% of Total', 'Avg Amount'],
        ['Type R', 'Regular Businesses', '738,407', '74.2%', '$85,053'],
        ['Type PR', 'Proprietorships', '231,197', '23.2%', '$35,844'],
        ['Type MR', 'Minority-owned', '19,181', '1.9%', '$81,165'],
        ['Type P', 'Partnerships', '6,624', '0.7%', '$30,542']
    ]
    
    business_table = Table(business_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    business_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fffbeb')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(business_table)
    story.append(PageBreak())
    
    # Key Findings
    story.append(Paragraph("KEY FINDINGS & STRATEGIC IMPLICATIONS", heading_style))
    
    findings = [
        ("Unprecedented Scale", "Nearly 1 million loans totaling $72.85 billion demonstrates the extraordinary scope of COVID-19 economic relief, representing one of the largest disaster relief programs in U.S. history."),
        ("Geographic Equity", "While larger states received more loans in absolute terms, the program achieved nationwide coverage, ensuring economic support reached businesses in all 50 states and territories."),
        ("Small Business Focus", "With a median loan of $49K and 50.5% of loans under $50K, the program successfully targeted small and micro-enterprises most vulnerable to pandemic disruption."),
        ("Diverse Business Support", "The wide loan distribution ($7K-$900K) demonstrates the program's flexibility in addressing varied business needs across different industries and sizes."),
        ("Economic Investment", "$9.9B in subsidy costs represents a significant government investment in economic recovery, with an average subsidy rate of 13.6% of loan value."),
        ("Business Type Equity", "While regular businesses received higher average amounts, the program successfully served diverse business structures including proprietorships, partnerships, and minority-owned enterprises.")
    ]
    
    for i, (title, description) in enumerate(findings, 1):
        finding_text = f"<b>{i:02d}. {title}</b><br/>{description}"
        story.append(Paragraph(finding_text, body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # Data Quality & Methodology
    story.append(Paragraph("DATA QUALITY & METHODOLOGY", heading_style))
    
    methodology_text = """
    <b>Dataset:</b> DATAACT_EIDL_LOANS_20200401-20200609.csv (313.8 MB, 995,409 records)<br/>
    <b>Analysis Tools:</b> Python 3.12, Pandas, NumPy, Matplotlib, Seaborn<br/>
    <b>Data Processing:</b> 24 records skipped due to CSV parsing errors (malformed address fields)<br/>
    <b>Date Issues:</b> Temporal analysis limited due to date formatting inconsistencies<br/>
    <b>Quality Assurance:</b> Statistical validation, outlier detection, and cross-validation performed
    """
    story.append(Paragraph(methodology_text, body_style))
    
    limitations_text = """
    <b>Key Limitations:</b><br/>
    • Date formatting issues prevent detailed temporal analysis<br/>
    • Some negative loan values present (likely corrections/adjustments)<br/>
    • Congressional district analysis not performed due to data complexity<br/>
    • Industry-specific analysis not available in current dataset
    """
    story.append(Paragraph(limitations_text, body_style))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_text = f"""
    Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    Analysis Period: April 1 - June 9, 2020 | COVID-19 Economic Relief Program<br/>
    Technology: Python Data Science Stack | Visualization: Matplotlib & Seaborn
    """
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748b')
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(story)
    print("✅ Fancy PDF report generated: EIDL_Analysis_Executive_Report.pdf")

if __name__ == "__main__":
    try:
        create_fancy_pdf_report()
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("Installing reportlab...")
        import subprocess
        subprocess.run(["pip", "install", "reportlab"], check=True)
        create_fancy_pdf_report()