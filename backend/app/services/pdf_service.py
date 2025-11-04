from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT


def generate_pdf_from_text(content: str, filename: str = "improved_resume.pdf") -> BytesIO:
    """
    Generate a professional PDF from text content.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#1a202c',
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2d3748',
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor='#4a5568',
        leftIndent=0,
        rightIndent=0,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor='#4a5568',
        leftIndent=20,
        rightIndent=0,
        spaceAfter=4,
        fontName='Helvetica'
    )
    
    # Parse content and build PDF
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1 * inch))
            continue
        
        # Detect headings (lines that are all caps or short lines before content)
        if line.isupper() and len(line) < 50:
            story.append(Paragraph(line, heading_style))
        elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
            # Bullet point
            story.append(Paragraph(line.lstrip('•-*').strip(), bullet_style))
        else:
            # Regular paragraph
            story.append(Paragraph(line, body_style))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer
