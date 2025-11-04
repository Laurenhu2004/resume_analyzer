import json
from typing import Optional
from openai import OpenAI
from app.core.config import settings


def get_openai_client():
    """Get OpenAI client instance."""
    return OpenAI(api_key=settings.OPENAI_API_KEY)


async def analyze_resume(resume_text: str, target_role: Optional[str] = None) -> dict:
    """
    Analyze resume using OpenAI GPT-4.
    Returns structured analysis with score, feedback, and improvements.
    """
    system_prompt = """You are an expert resume reviewer with years of experience in HR and recruitment. 
    Analyze resumes objectively and provide actionable, constructive feedback. Focus on:
    1. Structure and formatting clarity
    2. Keyword optimization for ATS systems
    3. Content quality and impact
    4. Tailoring for specific roles
    Be specific, professional, and encouraging."""
    
    user_prompt = f"""Please analyze the following resume and provide detailed feedback. 
    
    Resume content:
    {resume_text}
    """
    
    if target_role:
        user_prompt += f"\n\nTarget role: {target_role}"
    
    user_prompt += """
    
    Provide your analysis in the following JSON format:
    {
        "score": <integer 0-100>,
        "structure_feedback": "<detailed feedback on resume structure, formatting, sections, and length>",
        "keyword_analysis": "<analysis of keywords, industry terms, and ATS optimization suggestions>",
        "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
        "improved_content": "<complete improved version of the resume as plain text, maintaining professional format with sections, headings, and bullet points>"
    }
    
    CRITICAL: Ensure consistency between your "improvements" list and "improved_content":
    - If you mention adding a professional summary in "improvements", you MUST actually include it in "improved_content" with proper formatting
    - If you mention any other additions or changes in "improvements", they MUST be reflected in "improved_content"
    - The "improved_content" should be a complete, ready-to-use resume that incorporates all suggested improvements
    
    CRITICAL: Format the improved_content as follows for proper PDF generation:
    1. First line: Full name only (no contact info)
    2. Second line: Contact information separated by " | " (e.g., "email@example.com | (555) 123-4567 | City, State | linkedin.com/in/name")
    3. Section headers: ALL CAPS on separate lines (e.g., "PROFESSIONAL SUMMARY", "EXPERIENCE", "EDUCATION", "SKILLS", "PROJECTS", "ACTIVITIES", "ADDITIONAL")
    
    IMPORTANT: If you add a professional summary, objective, or profile, it MUST be formatted as a proper section:
    - Include a section header: "SUMMARY", "PROFESSIONAL SUMMARY", "OBJECTIVE", or "PROFILE" (in ALL CAPS on its own line)
    - Place the summary content on lines following the header
    - Do NOT place summary text on line 3 (after contact info) without a section header - it will not be rendered correctly
    
    5. Work Experience entries: Format as follows:
       - First line: "Company Name | Location | Start Date - End Date" (all on one line with | separators)
       - Second line: Job Title (regular text, not bold)
       - Following lines: Bullet points starting with "• "
    
    6. Education entries: Format as follows:
       - First line: "Institution Name | Location | Dates" (all on one line with | separators)
       - Second line: Degree/Program name (regular text)
       - Following lines: Additional details (GPA, coursework, etc.)
    
    7. Projects entries: Format as follows:
       - First line: "Project Name | Date" (all on one line with | separator)
       - Following lines: Bullet points starting with "• "
    
    8. Activities entries: Format as follows:
       - First line: "Organization Name | Location | Dates" (all on one line with | separators)
       - Second line: Role name (regular text)
       - Following lines: Bullet points starting with "• " (if applicable)
    
    9. Additional section entries: Format as "Category: content" on same line (e.g., "Technical Skills: Python, R, SQL" or "Languages: English (Native), Spanish (Fluent)")
    
    10. Bullet points: Always start each line with "• " (bullet symbol and space)
    
    Use consistent formatting throughout and ensure proper spacing between sections.
    """
    
    try:
        client = get_openai_client()
        content = None
        # Use gpt-4o or gpt-4-turbo which support JSON mode
        # Fallback to gpt-4 if those aren't available, but parse JSON manually
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
        except Exception:
            # Fallback to gpt-4-turbo
            try:
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            except Exception:
                # Fallback to regular gpt-4 without JSON mode
                user_prompt_with_json = user_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON, no other text before or after."
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt + " You must respond with valid JSON only."},
                        {"role": "user", "content": user_prompt_with_json}
                    ],
                    temperature=0.7
                )
                content = response.choices[0].message.content
        
        # Clean the content in case there's markdown formatting
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        analysis = json.loads(content)
        
        return analysis
    
    except json.JSONDecodeError as e:
        error_msg = f"Failed to parse OpenAI response as JSON: {str(e)}"
        if content:
            error_msg += f". Response: {content[:200]}"
        raise Exception(error_msg)
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")
