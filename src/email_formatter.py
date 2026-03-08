from datetime import datetime

def format_as_html(briefing_data: list) -> str:
    """
    Formats the list of interest-based briefing data into a professional NYT-style HTML email.
    Refactored for mobile responsiveness and client compatibility.
    """
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    
    # Outer table wrapper for alignment and background
    html = f"""
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; width: 100% !important;">
        <tr>
            <td align="center">
                <!-- Main Container -->
                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 650px; width: 100%; font-family: 'Georgia', serif; color: #333333; line-height: 1.6; border: 1px solid #eeeeee; box-sizing: border-box;">
                    <tr>
                        <td style="padding: 20px;">
                            
                            <!-- Header -->
                            <div style="text-align: center; border-bottom: 3px double #333333; padding-bottom: 15px; margin-bottom: 30px;">
                                <h1 style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: clamp(32px, 8vw, 48px); font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: -1px; line-height: 1.1;">
                                    The Morning Brief
                                </h1>
                                <p style="font-style: italic; color: #666666; margin: 10px 0 0 0; font-size: 16px;">{date_str}</p>
                            </div>
    """
    
    for entry in briefing_data:
        interest = entry.get('interest')
        data = entry.get('content')
        
        # Interest Header with Split Line
        html += f"""
                            <div style="margin-top: 40px; margin-bottom: 40px;">
                                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 20px;">
                                    <tr>
                                        <td width="1%" style="white-space: nowrap;">
                                            <h2 style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #000000; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
                                                {interest}
                                            </h2>
                                        </td>
                                        <td style="padding-left: 15px;">
                                            <div style="height: 2px; background-color: #333333; width: 100%;"></div>
                                        </td>
                                    </tr>
                                </table>
        """
        
        for section in data.get("sections", []):
            # Sub-section title
            html += f"<h3 style='font-size: 18px; color: #444444; text-transform: uppercase; margin-bottom: 15px;'>{section.get('section_title')}</h3>"
            
            for story in section.get("stories", []):
                html += f"""
                            <div style="margin-bottom: 25px; border-left: 4px solid #eeeeee; padding-left: 15px;">
                                <h4 style="font-size: 18px; margin: 0 0 8px 0; color: #111111;">{story.get('title')}</h4>
                                <p style="margin: 0; color: #444444;">
                                    {story.get('summary')}
                                    <a href="{story.get('link')}" style="color: #0645ad; text-decoration: none; font-weight: bold; font-size: 14px; margin-left: 5px;">
                                        [{story.get('source')}]
                                    </a>
                                </p>
                            </div>
                """
        
        html += "                            </div>"
    
    # Footer
    html += """
                            <div style="text-align: center; border-top: 1px solid #eeeeee; padding-top: 30px; margin-top: 50px; font-size: 12px; color: #999999; font-family: Arial, sans-serif;">
                                <p style="margin: 5px 0;">You are receiving this because you subscribed to the Daily News Briefing AI Agent.</p>
                                <p style="margin: 5px 0; font-weight: bold;">&copy; 2026 Daily News Briefing AI</p>
                            </div>

                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    """
    return html
