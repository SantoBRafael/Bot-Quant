import time
import random
from database import init_db, is_job_new, save_job
from scrapers import fetch_linkedin_sp, fetch_aisafety_global, fetch_job_description
from mattermost import send_job_alert

def run_job_search():
    init_db()
    
    # 1. Coleta os dois mundos
    jobs_sp = fetch_linkedin_sp()      # Foco: Estágio/SP
    jobs_ai = fetch_aisafety_global()  # Foco: Global/Pesquisa
    
    print(f"📊 Bruto: {len(jobs_sp)} vagas SP | {len(jobs_ai)} vagas AI Global")

    # 2. Filtra Repetidas
    new_sp = [j for j in jobs_sp if is_job_new(j['link'])]
    new_ai = [j for j in jobs_ai if is_job_new(j['link'])]
    
    # 3. Seleção Balanceada (Ex: 6 de SP, 4 de AI)
    # Prioriza SP pois é onde você quer o estágio agora
    random.shuffle(new_sp)
    final_list = new_sp[:7] + new_ai[:5]
    
    print(f"🎯 Enviando {len(final_list)} vagas selecionadas...")
    
    count = 0
    for job in final_list:
        # Se for vaga do LinkedIn (tem job_id), baixa os detalhes
        if job.get('job_id'):
            print(f"📥 Baixando detalhes: {job['title']}")
            desc_text, emp_type = fetch_job_description(job['job_id'])
            
            job['summary'] = desc_text
            job['type'] = emp_type
            
            # Se a descrição confirmar que é ESTÁGIO, adiciona um emoji especial
            if "Internship" in emp_type or "Estágio" in emp_type or "Estágio" in job['title']:
                job['title'] = "🎓 " + job['title'] # Destaque visual
        
        # Envia
        if send_job_alert(job):
            save_job(job['link'])
            count += 1
            time.sleep(2)

    print(f"✅ Fim. {count} vagas enviadas.")

if __name__ == "__main__":
    run_job_search()
