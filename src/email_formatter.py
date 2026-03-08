from datetime import datetime

def format_as_html(briefing_data: list) -> str:
    """
    Formats the list of interest-based briefing data into a professional NYT-style HTML email.
    Each item in briefing_data is a dict with 'interest' and 'content' (the JSON from Gemini).
    """
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    
    html = f"""
    <div style="font-family: 'Georgia', serif; color: #333; max-width: 650px; margin: 0 auto; line-height: 1.6; background-color: #fff; padding: 20px; border: 1px solid #eee;">
        <!-- Header -->
        <div style="text-align: center; border-bottom: 3px double #333; padding-bottom: 15px; margin-bottom: 30px;">
            <h1 style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: -1px; line-height: 1;">The Morning Brief</h1>
            <p style="font-style: italic; color: #666; margin: 10px 0 0 0; font-size: 16px;">{date_str}</p>
        </div>
    """
    
    for entry in briefing_data:
        interest = entry.get('interest')
        data = entry.get('content')
        
        # Interest Header with Split Line
        html += f"""
        <div style="margin-top: 40px; margin-bottom: 40px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <h2 style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 28px; font-weight: bold; color: #000; margin: 0; white-space: nowrap; text-transform: uppercase; letter-spacing: 1px;">
                    {interest}
                </h2>
                <div style="flex-grow: 1; height: 2px; background-color: #333; margin-left: 15px;"></div>
            </div>
        """
        
        for section in data.get("sections", []):
            # Sub-section title
            html += f"<h3 style='font-size: 20px; color: #444; text-transform: uppercase; margin-bottom: 15px;'>{section.get('section_title')}</h3>"
            
            for story in section.get("stories", []):
                html += f"""
                <div style="margin-bottom: 25px; border-left: 4px solid #eee; padding-left: 15px;">
                    <h4 style="font-size: 19px; margin: 0 0 8px 0; color: #111;">{story.get('title')}</h4>
                    <p style="margin: 0; color: #444;">
                        {story.get('summary')}
                        <a href="{story.get('link')}" style="color: #0645ad; text-decoration: none; font-weight: bold; font-size: 14px; margin-left: 5px;">
                            [{story.get('source')}]
                        </a>
                    </p>
                </div>
                """
        
        html += "</div>"
    
    # Footer
    html += """
        <div style="text-align: center; border-top: 1px solid #eee; padding-top: 30px; margin-top: 50px; font-size: 12px; color: #999; font-family: Arial, sans-serif;">
            <p style="margin: 5px 0;">You are receiving this because you subscribed to the Daily News Briefing AI Agent.</p>
            <p style="margin: 5px 0; font-weight: bold;">&copy; 2026 Daily News Briefing AI</p>
        </div>
    </div>
    """
    return html
