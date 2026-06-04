from google import genai
from google.genai import types
import json

class RiskAgent:

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def analyze_section(self, section):

        prompt = f"""
        You are an expert contract risk analyst.
        
        Analyze the following contract section.
        
        Section Number: {section['section_number']}
        Section Title: {section['title']}
        
        Section Content:
        {section['content']}
        
        Return ONLY valid JSON.
        
        {{
            "risk_level": "Low|Medium|High",
            "risks": [
                {{
                    "risk_type": "",
                    "severity": "",
                    "explanation": ""
                }}
            ]
        }}
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return json.loads(response.text)