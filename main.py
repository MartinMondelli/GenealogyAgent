# main.py

import typer
from agent.scraper import GenealogyScraper
from agent.parser import GenealogyParser
from agent.gedcom_gen import GedcomGenerator

app = typer.Typer()

@app.command()
def search(
    url: str = typer.Option(..., "--url", help="URL a raspar"),
    query: str = typer.Option("Antepasado", "--query", help="Nombre o término de búsqueda")
):
    print(f"[*] Buscando: {query} en {url}")
    
    # 1. Scraper
    scraper = GenealogyScraper(headless=True)
    raw_html = scraper.search_records(query=query, target_url=url)
    clean_text = scraper.clean_html_to_text(raw_html)

    # 2. IA Parser
    parser = GenealogyParser()
    resultado = parser.parse_raw_text(clean_text)

    # 3. GEDCOM
    gedcom_gen = GedcomGenerator()
    gedcom_gen.generate(resultado)

if __name__ == "__main__":
    app()