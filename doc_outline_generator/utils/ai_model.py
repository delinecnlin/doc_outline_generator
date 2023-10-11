## utils/ai_model.py

import openai
import os
from typing import Union

class AIModel:
    def __init__(self, template_text: str):
        self.template_text = template_text

    def generate_outline(self) -> str:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=self.template_text,
          temperature=0.5,
          max_tokens=100
        )
        return response.choices[0].text.strip()
