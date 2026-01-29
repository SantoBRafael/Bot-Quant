import requests
import os

def send_job_alert(job):
    webhook_url = os.getenv("MATTERMOST_WEBHOOK")
    if not webhook_url: return False

    cat = job.get('category', 'Geral')
    
    # Cores e Ícones
    icon = "💼"
    color = "#777777"
    if "AI SAFETY" in cat: 
        icon = "🤖"
        color = "#FF8800"
    elif "QUANT" in cat: 
        icon = "🧮"
        color = "#0000FF"
    elif "BIO" in cat: 
        icon = "🧬"
        color = "#00AA00"

    # Monta a mensagem
    payload = {
        "username": "Bot de Carreiras",
        "icon_emoji": icon,
        "attachments": [
            {
                "color": color,
                "title": f"{icon} {job['title']}",
                "title_link": job['link'],
                "fields": [
                    {"short": True, "title": "Empresa", "value": job['company']},
                    {"short": True, "title": "Local/Tag", "value": f"`{cat}`"},
                    {"short": True, "title": "Tipo", "value": job.get('type', 'Ver Descrição')}, # Novo campo!
                ],
                "text": f"📝 **Descrição / Requisitos:**\n> {job['summary'][:600]}...", # Limita tamanho
                "actions": [
                    {"type": "button", "name": "Aplicar Agora", "url": job['link'], "style": "primary"}
                ]
            }
        ]
    }

    try:
        requests.post(webhook_url, json=payload)
        return True
    except: return False
