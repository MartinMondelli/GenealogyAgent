"""
=============================================================================
SCRIPT: procesar_persona.py
DESCRIPCIÓN: Extracción de datos genealógicos con salida simultánea a
             GEDCOM (.ged) y JSON (.json).
=============================================================================
"""

import os
import json
from agent.parser import GenealogyParser
from agent.gedcom_gen import GedcomGenerator

# Reemplaza este texto por los datos verdaderos que tengas de FamilySearch o actas
texto_registro = """
Registro parroquial: Argentina, Buenos Aires, registros parroquiales, 1635-2017.
Persona mencionada: Romeo Mondelli.
Sexo: Masculino (M).

Cónyuge / Esposa:
- Nombre: Nena Aura Marina
- Sexo: Femenino (F)

Hijo:
- Nombre: Alexis Romeo Angel Mondelli Marina
- Sexo: Masculino
- Fecha de nacimiento: 8 de noviembre de 1916
- Fecha de bautismo: 12 de marzo de 1917
- Lugar del evento: Santa María del Carmen, Necochea, Buenos Aires, Argentina.
"""

def main():
    print("[*] Enviando texto a Groq para extracción genealógica...")
    
    # Instanciación con selección automática de modelos activos
    parser = GenealogyParser()
    resultado = parser.parse_raw_text(texto_registro)
    
    # 1. Imprimir resumen en consola
    print(f"\n[✔] Personas encontradas: {len(resultado.personas_encontradas)}")
    for persona in resultado.personas_encontradas:
        print(f" - Nombre: {persona.nombre_completo}")
        if persona.nacimiento:
            print(f"   Nacimiento: {persona.nacimiento.fecha} | Lugar: {persona.nacimiento.lugar}")
        if persona.defuncion:
            print(f"   Defunción: {persona.defuncion.fecha} | Lugar: {persona.defuncion.lugar}")
        if persona.padres:
            print(f"   Padres: {', '.join(persona.padres)}")
        if persona.conyuge:
            print(f"   Cónyuge: {persona.conyuge}")

    # Asegurar que existe la carpeta de salida
    os.makedirs("output", exist_ok=True)

    # 2. Exportar a GEDCOM (.ged)
    print("\n[*] Generando archivo GEDCOM...")
    gedcom_gen = GedcomGenerator(filename="output/romeo_mondelli.ged")
    gedcom_gen.generate(resultado)

    # 3. Exportar a JSON (.json)
    json_path = "output/romeo_mondelli.json"
    print(f"[*] Generando archivo JSON en {json_path}...")
    
    # Convertimos el modelo Pydantic a diccionario / JSON estructurado
    datos_dict = resultado.model_dump()
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(datos_dict, f, ensure_ascii=False, indent=4)

    print("[✔] ¡Proceso completado con éxito! Archivos generados en output/")

if __name__ == "__main__":
    main()