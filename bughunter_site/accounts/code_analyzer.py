import json
from .gemini_client import initialize_gemini


def analyze_code_directly(code_content, language):
    """Analyze code directly with detailed suggestions and fixes."""
    model = initialize_gemini()
    
    prompt = f"""
You are a senior software engineer and code reviewer. Analyze the following {language} code and provide comprehensive feedback.

Code to analyze:
```{language}
{code_content}
```

Return ONLY valid JSON in this exact format:
{{
  "overall_assessment": {{
    "quality_score": 85,
    "readability": "good|fair|poor",
    "maintainability": "high|medium|low",
    "performance": "excellent|good|fair|poor"
  }},
  "bugs": [
    {{
      "title": "Bug title",
      "severity": "low|medium|high|critical",
      "description": "Detailed description",
      "line_range": [start_line, end_line],
      "suggested_fix": "How to fix it",
      "fixed_code_example": "Example of fixed code"
    }}
  ],
  "vulnerabilities": [
    {{
      "title": "Security issue title",
      "severity": "low|medium|high|critical", 
      "description": "Security issue description",
      "line_range": [start_line, end_line],
      "suggested_fix": "Security fix recommendation",
      "fixed_code_example": "Secure code example"
    }}
  ],
  "improvements": [
    {{
      "title": "Improvement suggestion",
      "category": "performance|readability|maintainability|best_practices",
      "description": "What can be improved",
      "line_range": [start_line, end_line],
      "suggested_fix": "How to improve",
      "improved_code_example": "Better code example"
    }}
  ],
  "best_practices": [
    {{
      "title": "Best practice recommendation",
      "description": "Recommendation description",
      "example": "Code example following best practices"
    }}
  ]
}}

Focus on:
1. Actual bugs and logic errors
2. Security vulnerabilities
3. Performance improvements
4. Code readability and maintainability
5. Language-specific best practices
6. Error handling improvements

If no issues are found in a category, return empty arrays.
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean up the response to extract JSON
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        
        return json.loads(result_text)
    except Exception as e:
        print(f"Error analyzing code: {e}")
        return {
            "overall_assessment": {
                "quality_score": 0,
                "readability": "unknown",
                "maintainability": "unknown", 
                "performance": "unknown"
            },
            "bugs": [],
            "vulnerabilities": [],
            "improvements": [],
            "best_practices": []
        }