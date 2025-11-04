from io import BytesIO
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
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
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Define professional styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=22,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=26
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
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_LEFT,
        spaceBefore=14,
        spaceAfter=4,
        leading=14
    )
    
    company_institution_style = ParagraphStyle(
        'CompanyInstitutionStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=2,
        leading=13,
        leftIndent=6
    )
    
    job_title_style = ParagraphStyle(
        'JobTitleStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=12
    )
    
    date_location_style = ParagraphStyle(
        'DateLocationStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_RIGHT,
        spaceAfter=2,
        leading=12
    )
    
    company_date_style = ParagraphStyle(
        'CompanyDateStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=black,
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
        leftIndent=0,
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
        'LANGUAGES', 'LANGUAGE SKILLS', 'COMMUNITY INVOLVEMENT'
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
        
        # Skills section (often comma-separated or bullet points)
        # Check BEFORE section header detection to avoid misclassifying skills content as headers
        # But first check if this line is actually a new section header - if so, let it be processed below
        if current_section and 'SKILLS' in current_section:
            # Check if this line is a section header - be STRICT to avoid false positives
            # Only skip if it's EXACTLY a section keyword (not just contains one) and clearly a standalone header
            line_upper_check = line.upper().strip()
            # Exact match only - don't use "contains" to avoid matching skills content that mentions keywords
            # Skills content often has commas, bullets, or multiple words - section headers don't
            is_new_section_header = (
                line_upper_check in section_keywords and
                # Must be clearly a standalone header: short, no separators/bullets/commas
                len(line) < 30 and 
                not '|' in line and 
                not ',' in line and  # Skills often have commas
                not line.strip().startswith(('•', '-', '*', '·'))  # Skills might be bulleted
            )
            # If it's a new section header, skip processing here and let section header detection handle it
            if not is_new_section_header:
                # If comma-separated, keep as single line
                safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe_line, body_style))
                line_index += 1
                continue
        
        # Summary/Objective/Profile section
        # Check BEFORE section header detection to avoid misclassifying summary content as headers
        # But first check if this line is actually a new section header - if so, let it be processed below
        if current_section and ('SUMMARY' in current_section or 'OBJECTIVE' in current_section or 'PROFILE' in current_section):
            # Check if this line is a section header - be STRICT to avoid false positives
            # Only skip if it's EXACTLY a section keyword (not just contains one) and clearly a standalone header
            line_upper_check = line.upper().strip()
            # Exact match only - don't use "contains" to avoid matching summary content that mentions keywords
            # Summary content can be multi-line paragraphs - section headers are short and standalone
            is_new_section_header = (
                line_upper_check in section_keywords and
                # Must be clearly a standalone header: short, no separators/bullets/commas
                len(line) < 30 and 
                not '|' in line and 
                not ',' in line and  # Summary might have commas
                not line.strip().startswith(('•', '-', '*', '·'))  # Summary might be bulleted
            )
            # If it's a new section header, skip processing here and let section header detection handle it
            if not is_new_section_header:
                # Escape HTML special characters
                safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe_line, summary_style))
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
            story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=black))
            story.append(Spacer(1, 0.04 * inch))
            story.append(Paragraph(line.upper(), section_header_style))
            story.append(Spacer(1, 0.04 * inch))
            line_index += 1
            continue
        
        # Detect job entries (contains "|" separator and possibly dates)
        if '|' in line and (date_pattern.search(line) or current_section and 'EXPERIENCE' in current_section):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                # Parse: Company Name | Location | Dates
                # or: Job Title | Company | Location | Dates
                # Try to detect if first part is company or job title based on context
                if len(parts) >= 3:
                    # Likely format: Company | Location | Dates
                    company_name = parts[0]
                    location_date = ' | '.join(parts[1:])
                    # Create table for side-by-side layout
                    table_data = [
                        [Paragraph(company_name, company_institution_style), 
                         Paragraph(location_date, date_location_style)]
                    ]
                    table = Table(table_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (0, 0), 0),
                        ('RIGHTPADDING', (1, 0), (1, 0), 0),
                        ('RIGHTPADDING', (0, 0), (0, 0), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    story.append(table)
                    # Next line should be job title
                    if line_index + 1 < len(lines):
                        next_line = lines[line_index + 1].strip()
                        if next_line and not next_line.startswith(('•', '-', '*', '·')) and '|' not in next_line:
                            story.append(Paragraph(next_line, job_title_style))
                            line_index += 1
                else:
                    # Fallback: First part is job title, rest is company/date
                    job_title = parts[0]
                    company_and_date = ' | '.join(parts[1:])
                    story.append(Paragraph(job_title, job_title_style))
                    story.append(Paragraph(company_and_date, company_date_style))
                line_index += 1
                continue
        
        # Detect education entries (format: Institution | Location | Dates)
        if '|' in line and current_section and 'EDUCATION' in current_section:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                # Format: Institution Name | Location | Dates
                if len(parts) >= 3:
                    institution_name = parts[0]
                    location_date = ' | '.join(parts[1:])
                    # Create table for side-by-side layout
                    table_data = [
                        [Paragraph(institution_name, company_institution_style), 
                         Paragraph(location_date, date_location_style)]
                    ]
                    table = Table(table_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (0, 0), 0),
                        ('RIGHTPADDING', (1, 0), (1, 0), 0),
                        ('RIGHTPADDING', (0, 0), (0, 0), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    story.append(table)
                    # Next line should be degree/program
                    if line_index + 1 < len(lines):
                        next_line = lines[line_index + 1].strip()
                        if next_line and not next_line.startswith(('•', '-', '*', '·')) and '|' not in next_line:
                            story.append(Paragraph(next_line, job_title_style))
                            line_index += 1
                else:
                    # Fallback: First part is degree, rest is institution/date
                    degree = parts[0]
                    rest = ' | '.join(parts[1:])
                    story.append(Paragraph(degree, job_title_style))
                    story.append(Paragraph(rest, company_date_style))
                line_index += 1
                continue
        
        # Projects section - similar to work experience
        if current_section and ('PROJECT' in current_section or 'PROJECTS' in current_section):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    project_name = parts[0]
                    date = ' | '.join(parts[1:]) if len(parts) > 1 else parts[1]
                    # Create table for side-by-side layout
                    table_data = [
                        [Paragraph(project_name, company_institution_style), 
                         Paragraph(date, date_location_style)]
                    ]
                    table = Table(table_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (0, 0), 0),
                        ('RIGHTPADDING', (1, 0), (1, 0), 0),
                        ('RIGHTPADDING', (0, 0), (0, 0), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    story.append(table)
                    line_index += 1
                    continue
        
        # Activities section - similar to work experience
        if current_section and 'ACTIVIT' in current_section:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    organization_name = parts[0]
                    location_date = ' | '.join(parts[1:])
                    # Create table for side-by-side layout
                    table_data = [
                        [Paragraph(organization_name, company_institution_style), 
                         Paragraph(location_date, date_location_style)]
                    ]
                    table = Table(table_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (0, 0), 0),
                        ('RIGHTPADDING', (1, 0), (1, 0), 0),
                        ('RIGHTPADDING', (0, 0), (0, 0), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    story.append(table)
                    # Next line should be role
                    if line_index + 1 < len(lines):
                        next_line = lines[line_index + 1].strip()
                        if next_line and not next_line.startswith(('•', '-', '*', '·')) and '|' not in next_line:
                            story.append(Paragraph(next_line, job_title_style))
                            line_index += 1
                    line_index += 1
                    continue
        
        # Additional section - format with inline category headers
        if current_section and 'ADDITIONAL' in current_section:
            # Look for pattern like "Category: content"
            if ':' in line and not line.strip().startswith(('•', '-', '*', '·')):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    category = parts[0].strip().replace('&', '&amp;')
                    content = parts[1].strip().replace('&', '&amp;')
                    # Format as bold category followed by content on same line
                    formatted_line = f'<b>{category}:</b> {content}'
                    story.append(Paragraph(formatted_line, body_style))
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
