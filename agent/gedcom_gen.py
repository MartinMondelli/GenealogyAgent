"""
=============================================================================
MÓDULO: agent/gedcom_gen.py
DESCRIPCIÓN: Convierte las entidades de Pydantic en un archivo formato GEDCOM.
=============================================================================
"""

import os
from models.schemas import ResultadoBusquedaGenealogica

class GedcomGenerator:
    def __init__(self, filename: str = "output/mi_arbol.ged"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def generate(self, resultado: ResultadoBusquedaGenealogica):
        """
        Genera un archivo .ged básico compatible con estándares genealógicos.
        """
        gedcom_lines = [
            "0 HEAD",
            "1 SOUR AGENTE_GENEALOGICO_IA",
            "2 VERS 1.0",
            "1 GEDC",
            "2 VERS 5.5.1",
            "2 FORM LINEAGE-LINKED",
            "1 CHAR UTF-8"
        ]

        indi_id = 1
        for persona in resultado.personas_encontradas:
            gedcom_lines.append(f"0 @I{indi_id}@ INDI")
            gedcom_lines.append(f"1 NAME {persona.nombre_completo}")
            
            if persona.genero:
                sex = "M" if persona.genero.lower().startswith("m") else "F"
                gedcom_lines.append(f"1 SEX {sex}")

            if persona.nacimiento:
                gedcom_lines.append("1 BIRT")
                if persona.nacimiento.fecha:
                    gedcom_lines.append(f"2 DATE {persona.nacimiento.fecha}")
                if persona.nacimiento.lugar:
                    gedcom_lines.append(f"2 PLAC {persona.nacimiento.lugar}")

            if persona.defuncion:
                gedcom_lines.append("1 DEAT")
                if persona.defuncion.fecha:
                    gedcom_lines.append(f"2 DATE {persona.defuncion.fecha}")
                if persona.defuncion.lugar:
                    gedcom_lines.append(f"2 PLAC {persona.defuncion.lugar}")

            if persona.notas:
                gedcom_lines.append(f"1 NOTE {persona.notas}")

            indi_id += 1

        gedcom_lines.append("0 TRLR")

        # Escribir el archivo
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("\n".join(gedcom_lines))
        
        print(f"[+] Archivo GEDCOM generado con éxito en: {self.filename}")