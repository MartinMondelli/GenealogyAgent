"""
=============================================================================
MÓDULO: agent/parser.py
DESCRIPCIÓN: Parser configurado para los modelos activos de la cuenta (GPT-OSS / Qwen).
=============================================================================
"""

import os
import instructor
from groq import Groq
from models.schemas import ResultadoBusquedaGenealogica

class GenealogyParser:
    def __init__(self, model_name: str = None):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("[!] La variable GROQ_API_KEY no está configurada.")

        self.raw_client = Groq(api_key=api_key)
        self.client = instructor.from_groq(
            self.raw_client,
            mode=instructor.Mode.JSON
        )
        
        # Lista de modelos de texto activos en tu catálogo por orden de preferencia
        self.target_models = [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "qwen/qwen3.8-27b"
        ]
        
        self.model_name = model_name if model_name else self.target_models[0]

    def parse_raw_text(self, raw_text: str) -> ResultadoBusquedaGenealogica:
        prompt = f"""
        Eres un historiador experto en genealogía. Analiza el siguiente texto e identifica todas las personas,
        fechas de nacimiento, defunción, lugares, padres y cónyuges.
        
        TEXTO A ANALIZAR:
        {raw_text}
        """

        # Intenta con los modelos de texto válidos de tu lista
        models_to_try = [self.model_name] + [m for m in self.target_models if m != self.model_name]

        last_exception = None
        for model in models_to_try:
            try:
                print(f"[*] Procesando con el modelo: {model}")
                response = self.client.chat.completions.create(
                    model=model,
                    response_model=ResultadoBusquedaGenealogica,
                    messages=[
                        {"role": "system", "content": "Eres un asistente especializado en extracción de datos genealógicos."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0
                )
                self.model_name = model
                return response
            except Exception as e:
                print(f"[!] Falló el modelo {model}: {e}")
                last_exception = e

        raise last_exception