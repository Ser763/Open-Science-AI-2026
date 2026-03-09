import os
import time
import requests
from grobid_client.grobid_client import GrobidClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import lxml.etree as ET

# --- CONFIGURACIÓN PARA DOCKER ---
import matplotlib
matplotlib.use('Agg')

def run_analysis():
    # 1. Configuración de conexión
    grobid_host = os.getenv("GROBID_SERVER", "http://localhost:8070")
    
    print(f"--- Paso 1: Conectando a Grobid en {grobid_host} ---")
    
    # Espera activa para que Grobid cargue
    while True:
        try:
            response = requests.get(f"{grobid_host}/api/isalive", timeout=5)
            if response.status_code == 200:
                print("[+] ¡Grobid está listo!")
                break
        except:
            print("[...] Grobid cargando, esperando 5 segundos...")
            time.sleep(5)

    os.makedirs("./output", exist_ok=True)
    os.makedirs("./Articles", exist_ok=True)

    client = GrobidClient(grobid_server=grobid_host, batch_size=1)

    # 2. Procesar los PDFs
    print("[*] Procesando PDFs...")
    client.process("processFulltextDocument", "./Articles", output="./output", force=True)

    # 3. Análisis de datos
    print("--- Paso 2: Extrayendo información y enlaces ---")
    all_abstracts = ""
    stats = {}
    enlaces_por_archivo = {} # Nueva lista para los links
    
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    for file in os.listdir("./output"):
        if file.endswith(".xml"):
            try:
                tree = ET.parse(os.path.join("./output", file))
                root = tree.getroot()

                # A. Extraer Abstract para Nube de Palabras
                abstract = root.find(".//tei:abstract", ns)
                if abstract is not None:
                    all_abstracts += " ".join(abstract.itertext())

                # B. Contar figuras
                num_figures = len(tree.xpath("//tei:figure", namespaces=ns))
                stats[file[:15]] = num_figures

                # C. EXTRAER ENLACES (Nuevo requisito)
                # Buscamos en todo el documento etiquetas que tengan un atributo 'target' (URLs)
                links = tree.xpath("//@target")
                valid_links = [l for l in links if l.startswith("http")]
                enlaces_por_archivo[file] = list(set(valid_links)) # set() evita duplicados

            except Exception as e:
                print(f"Error procesando {file}: {e}")

    # --- GENERACIÓN DE RESULTADOS ---

    # 1. Guardar Lista de Enlaces en TXT
    with open("lista_enlaces.txt", "w", encoding="utf-8") as f:
        f.write("LISTA DE ENLACES ENCONTRADOS EN LOS ARTÍCULOS\n")
        f.write("============================================\n\n")
        for archivo, links in enlaces_por_archivo.items():
            f.write(f"Archivo: {archivo}\n")
            if links:
                for link in links:
                    f.write(f"  - {link}\n")
            else:
                f.write("  - No se encontraron enlaces externos.\n")
            f.write("-" * 30 + "\n")
    print("[+] Lista de enlaces guardada en 'lista_enlaces.txt'")

    # 2. Nube de Palabras
    if all_abstracts:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_abstracts)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig("nube_abstracts.png")
        print("[+] Nube de palabras guardada.")

    # 3. Gráfico de Barras
    if stats:
        plt.figure(figsize=(12, 6))
        plt.bar(stats.keys(), stats.values(), color='skyblue')
        plt.title('Análisis de Contenido Visual')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("figuras_por_articulo.png")
        print("[+] Gráfico de barras guardado.")

    print("\n--- ¡Proceso finalizado con éxito! ---")

if __name__ == "__main__":
    run_analysis()