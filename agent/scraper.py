"""
=============================================================================
MÓDULO: scraper.py
DESCRIPCIÓN: Plantilla base para el scraper del agente genealógico.
=============================================================================
"""

from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup
import time
import random

class GenealogyScraper:
    def __init__(self, headless: bool = True):
        """
        INSTRUCCIÓN: Inicializa el navegador.
        - 'headless=True' abre el navegador de forma oculta (más rápido).
        - Si alguna página web te bloquea o pide resolver un CAPTCHA, 
          cambia temporalmente a 'headless=False' para ver el navegador 
          y resolverlo o debuguear.
        """
        self.headless = headless

    def _simulate_human_behavior(self, page: Page):
        """
        INSTRUCCIÓN OPCIONAL: Anti-bloqueo básico.
        Muchos archivos históricos o webs públicas bloquean bots agresivos.
        Aquí puedes añadir retardos aleatorios o movimientos de scroll simulados.
        """
        time.sleep(random.uniform(1.5, 3.5))

    def search_records(self, query: str, target_url: str = "https://www.familysearch.org/search/") -> str:
        """
        INSTRUCCIÓN PRINCIPAL:
        Esta función debe:
        1. Abrir una sesión de navegador.
        2. Navegar a la URL de búsqueda (o construir la URL usando Google Dorks).
        3. Rellenar los campos de búsqueda o inyectar la query si la web lo permite.
        4. Esperar a que carguen los resultados (¡Cuidado con las esperas implícitas/explícitas!).
        5. Extraer el HTML o el texto plano de los resultados y retornarlo.
        """
        raw_html_content = ""

        with sync_playwright() as p:
            # LIBRERÍA: playwright.sync_api.chromium
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                print(f"[*] Navegando a: {target_url}")
                # INSTRUCCIÓN: Navega a la página objetivo
                page.goto(target_url, timeout=60000)
                
                self._simulate_human_behavior(page)
                page.fill("input[name='q']", query)
                page.press("input[name='q']", "Enter")
                page.wait_for_selector(".search-results-container", timeout=10000)


                # Obtiene el HTML completo de la página de resultados actual
                raw_html_content = page.content()
                self._simulate_human_behavior(page)

            except Exception as e:
                print(f"[!] Error durante el scraping: {e}")
            
            finally:
                browser.close()

        return raw_html_content

    def clean_html_to_text(self, html_content: str) -> str:
        """
        INSTRUCCIÓN: Limpieza preliminar con BeautifulSoup.
        No le pases todo el HTML lleno de scripts, anuncios y menús a la IA 
        porque gastarás tokens a lo tonto. Usa BeautifulSoup para extraer 
        exclusivamente el texto de las tablas o bloques de resultados.
        """
        # LIBRERÍA: bs4 (BeautifulSoup)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Eliminar elementos basura (scripts, estilos, navegación)
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Extraer el texto limpio o enfocarse en selectores específicos de resultados
        # TODO PARA TI: Ajusta esto según el DOM de la página que raspes
        text_data = soup.get_text(separator="\n", strip=True)
        
        return text_data

# Bloque de prueba local para que pruebes tu scraper de forma aislada
if __name__ == "__main__":
    scraper = GenealogyScraper(headless=False) # Visible para que veas qué hace
    # Prueba con una URL estática o de prueba
    html = scraper.search_records(query="Juan Perez", target_url="https://example.com")
    clean_text = scraper.clean_html_to_text(html)
    print("\n--- TEXTO EXTRAÍDO ---")
    print(clean_text[:500]) # Muestra los primeros 500 caracteres