import requests
from bs4 import BeautifulSoup
import time
import random
from config import TERMS_SP, LOCATION_BR, BLACKLIST

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def clean_text(text):
    if not text: return ""
    return " ".join(text.split())

def fetch_job_description(job_id):
    """Busca a descrição completa e tenta identificar se é Estágio"""
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Tenta pegar os critérios (Nível de experiência, Tipo de emprego)
        criteria_list = soup.find_all("li", class_="description__job-criteria-item")
        employment_type = "Não informado"
        for criteria in criteria_list:
            if "Nível de experiência" in criteria.text or "Employment type" in criteria.text:
                employment_type = criteria.text.replace("Nível de experiência", "").strip()

        # Pega o texto
        desc_div = soup.find("div", class_="show-more-less-html__markup") or soup.find("div", class_="description__text")
        text = desc_div.get_text(separator="\n\n").strip() if desc_div else "Ver no link."
        
        return text[:1500], employment_type # Aumentei para 1500 caracteres
    except:
        return "Detalhes no link.", "Desconhecido"

def fetch_linkedin_sp():
    """Busca focada em SP para Finanças/Bio"""
    print(f"🏙️ Buscando vagas em {LOCATION_BR}...")
    all_jobs = []
    
    # Seleciona 4 termos aleatórios da lista de Estágios para variar
    selected_terms = random.sample(TERMS_SP, 4)
    
    for term in selected_terms:
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={term}&location={LOCATION_BR}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")
            
            for card in job_cards:
                try:
                    title = clean_text(card.find("h3").text)
                    company = clean_text(card.find("h4").text)
                    link = card.find("a", class_="base-card__full-link")['href'].split("?")[0]
                    
                    # Filtra Lixo
                    if any(bad in title.lower() for bad in map(str.lower, BLACKLIST)): continue

                    # Define Categoria
                    cat = "FINANÇAS (SP)"
                    if any(x in title.lower() for x in ["bio", "lab", "genét"]): cat = "BIO/AGRO (SP)"
                    elif "quant" in title.lower(): cat = "QUANT (SP)"

                    job_id = link.split("view/")[1].split("/")[0] if "view/" in link else None

                    all_jobs.append({
                        "title": title,
                        "company": company,
                        "link": link,
                        "job_id": job_id,
                        "date": "Recente",
                        "category": cat,
                        "type": "Analise...", # Vamos preencher depois
                        "summary": "Carregando..."
                    })
                except: continue
            time.sleep(1)
        except Exception as e:
            print(f"Erro em '{term}': {e}")
            
    return all_jobs

def fetch_aisafety_global():
    """Busca Global de AI Safety (Mantida)"""
    url = "https://www.aisafety.com/jobs"
    print(f"🌍 Buscando AI Safety Global...")
    jobs = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # (Lógica simplificada para pegar os cards do site)
        cards = soup.find_all("div", role="listitem")
        if not cards: cards = soup.find_all("div", class_="collection-item")

        for card in cards:
            try:
                title = clean_text(card.find("h3").text)
                link = card.find("a")['href']
                if "http" not in link: link = "https://www.aisafety.com" + link
                
                jobs.append({
                    "title": title,
                    "company": "AI Safety Global",
                    "link": link,
                    "date": "Global",
                    "category": "AI SAFETY (INTL)",
                    "type": "Various",
                    "summary": "Vaga internacional de Alinhamento/Governança."
                })
            except: continue
    except: pass
    return jobs
