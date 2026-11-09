# test.py
from agent.scraper import GenealogyScraper
from agent.parser import GenealogyParser
from agent.gedcom_gen import GedcomGenerator

url = "https://www.familysearch.org/ark:/61903/1:1:QPZ5-L2WV?lang=en"

print("[1/3] Raspando web...")
scraper = GenealogyScraper(headless=False) # Visual para ver qué hace
raw_html = scraper.search_records(query="Antepasado", target_url=url)
clean_text = scraper.clean_html_to_text(raw_html)

print("[2/3] Procesando con Groq...")
parser = GenealogyParser()
resultado = parser.parse_raw_text(clean_text)

print("[3/3] Exportando a GEDCOM...")
gedcom = GedcomGenerator()
gedcom.generate(resultado)

print("¡Hecho!")