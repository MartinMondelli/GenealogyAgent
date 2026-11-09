"""
=============================================================================
MÓDULO: models/schemas.py
DESCRIPCIÓN: Modelos Pydantic para estructurar la información genealógica.
=============================================================================
Instalación: pip install pydantic
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class EventoGenealogico(BaseModel):
    tipo: str = Field(..., description="Tipo de evento: Nacimiento, Bautismo, Matrimonio, Defuncion, Censo")
    fecha: Optional[str] = Field(None, description="Fecha del evento (ej. '12 de Mayo de 1890' o '1890')")
    lugar: Optional[str] = Field(None, description="Lugar del evento (Ciudad, Provincia, País)")
    fuente_url: Optional[str] = Field(None, description="URL o referencia de donde se extrajo")

class Persona(BaseModel):
    nombre_completo: str = Field(..., description="Nombre y apellidos de la persona")
    genero: Optional[str] = Field(None, description="Masculino, Femenino o Desconocido")
    nacimiento: Optional[EventoGenealogico] = None
    defuncion: Optional[EventoGenealogico] = None
    padres: List[str] = Field(default=[], description="Nombres completos de los padres si se mencionan")
    conyuge: Optional[str] = Field(None, description="Nombre del cónyuge si se menciona")
    notas: Optional[str] = Field(None, description="Cualquier detalle histórico relevante extraído del registro")

class ResultadoBusquedaGenealogica(BaseModel):
    personas_encontradas: List[Persona] = Field(description="Lista de personas identificadas en el texto del documento")