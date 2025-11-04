from io import BytesIO
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, HexColor


def generate_pdf_from_text(content: str, filename: str = "improved_resume.pdf") -> BytesIO:
    """
    Generate a professional, ATS-friendly PDF from resume text content.
    Intelligently parses resume structure and applies professional formatting.
    """
    buffer = BytesIO()
    
    # Set margins for professional appearance
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Define professional styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=20,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=24
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=12
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeaderStyle',
        parent=styles['Normal'],
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        leading=15
    )
    
    job_title_style = ParagraphStyle(
        'JobTitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=2,
        leading=13
    )
    
    company_date_style = ParagraphStyle(
        'CompanyDateStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=HexColor('#4a5568'),
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=12
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_LEFT,
        leftIndent=18,
        spaceAfter=3,
        leading=12,
        bulletIndent=9
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=12
    )
    
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=12
    )
    
    # Regex patterns for detection
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)
    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    date_pattern = re.compile(r'\b\d{4}\s*[-–]\s*\d{4}\b|\b\d{4}\s*[-–]\s*(Present|Current)\b', re.IGNORECASE)
    
    # Common section headers
    section_keywords = {
        'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT', 'PROFESSIONAL EXPERIENCE',
        'EDUCATION', 'ACADEMIC BACKGROUND',
        'SKILLS', 'TECHNICAL SKILLS', 'COMPETENCIES',
        'PROJECTS', 'PROJECT EXPERIENCE',
        'SUMMARY', 'PROFESSIONAL SUMMARY', 'OBJECTIVE', 'PROFILE',
        'CERTIFICATIONS', 'CERTIFICATES', 'LICENSES',
        'AWARDS', 'ACHIEVEMENTS', 'HONORS',
        'PUBLICATIONS', 'PUBLICATIONS & RESEARCH',
        'LANGUAGES', 'LANGUAGE SKILLS'
    }
    
    # Parse content
    lines = content.split('\n')
    
    # Track state
    line_index = 0
    is_first_line = True
    is_contact_line = False
    current_section = None
    
    while line_index < len(lines):
        line = lines[line_index].strip()
        
        # Skip empty lines (but add minimal spacing)
        if not line:
            if story:  # Only add spacer if we have content
                story.append(Spacer(1, 0.05 * inch))
            line_index += 1
            continue
        
        # Detect name (first non-empty line, typically no special characters except hyphens/apostrophes)
        if is_first_line and not re.search(r'[|•\-\*@]', line):
            # Check if it's likely a name (2-4 words, proper case, no numbers typically)
            words = line.split()
            if 2 <= len(words) <= 4 and not re.search(r'\d', line):
                story.append(Paragraph(line, name_style))
                story.append(Spacer(1, 0.1 * inch))
                is_first_line = False
                line_index += 1
                continue
        
        # Detect contact information (contains email, phone, or common contact patterns)
        if (email_pattern.search(line) or phone_pattern.search(line) or 
            'linkedin.com' in line.lower() or 'github.com' in line.lower() or
            '|' in line and (email_pattern.search(line) or phone_pattern.search(line))):
            # Format contact line
            story.append(Paragraph(line.replace('|', ' | '), contact_style))
            story.append(Spacer(1, 0.15 * inch))
            is_first_line = False
            line_index += 1
            continue
        
        # Detect bullet points FIRST (before section headers to avoid false positives)
        if line.startswith('•') or line.startswith('-') or line.startswith('*') or line.startswith('·'):
            bullet_text = re.sub(r'^[•\-\*\·]\s*', '', line)
            # Escape HTML special characters for ReportLab
            bullet_text = bullet_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
            line_index += 1
            continue
        
        # Detect section headers (ALL CAPS, or common section keywords)
        # Exclude lines that start with bullet characters (already handled above)
        line_upper = line.upper().strip()
        is_section_header = (
            (line_upper in section_keywords or 
             any(keyword in line_upper for keyword in section_keywords) or
             (line.isupper() and len(line) < 50 and not '|' in line and not line.strip().startswith(('•', '-', '*', '·'))))
        )
        
        if is_section_header:
            current_section = line_upper
            # Add horizontal line before section header
            if story and not isinstance(story[-1], Spacer):
                story.append(Spacer(1, 0.1 * inch))
            story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=black))
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph(line.upper(), section_header_style))
            story.append(Spacer(1, 0.05 * inch))
            line_index += 1
            continue
        
        # Detect job entries (contains "|" separator and possibly dates)
        if '|' in line and (date_pattern.search(line) or current_section and 'EXPERIENCE' in current_section):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                # First part is usually job title
                job_title = parts[0]
                company_and_date = ' | '.join(parts[1:])
                story.append(Paragraph(job_title, job_title_style))
                story.append(Paragraph(company_and_date, company_date_style))
                line_index += 1
                continue
        
        # Detect education entries (format: Degree | University | Year)
        if '|' in line and current_section and 'EDUCATION' in current_section:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                degree = parts[0]
                rest = ' | '.join(parts[1:])
                story.append(Paragraph(degree, job_title_style))
                story.append(Paragraph(rest, company_date_style))
                line_index += 1
                continue
        
        # Summary/Objective section (typically appears early, before experience)
        if current_section and ('SUMMARY' in current_section or 'OBJECTIVE' in current_section or 'PROFILE' in current_section):
            # Escape HTML special characters
            safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(safe_line, summary_style))
            line_index += 1
            continue
        
        # Skills section (often comma-separated or bullet points)
        if current_section and 'SKILLS' in current_section:
            # If comma-separated, keep as single line
            safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(safe_line, body_style))
            line_index += 1
            continue
        
        # Default: regular body text
        is_first_line = False
        # Escape HTML special characters
        safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        story.append(Paragraph(safe_line, body_style))
        line_index += 1
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
