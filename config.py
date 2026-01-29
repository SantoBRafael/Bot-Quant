import os
from dotenv import load_dotenv

load_dotenv()

MM_WEBHOOK = os.getenv("MATTERMOST_WEBHOOK")

# --- CONFIGURAÇÃO DE MIRA ---

# 1. Para Finanças/Quant/Bio: Foco total em SP e Estágio
LOCATION_BR = "São Paulo, Brazil"

# Termos otimizados para buscar ESTÁGIO em SP
# O LinkedIn funciona melhor se formos específicos
TERMS_SP = [
    # Finanças / Quant
    "Estágio Quant",
    "Estágio Quantitative Finance",
    "Estágio Mercado Financeiro",
    "Estágio Equity Research",
    "Estágio Investment Banking",
    "Estágio M&A",
    "Estágio Risco de Mercado",
    "Estágio Economia",
    
    # Biologia / Biorisco
    "Estágio Biologia",
    "Estágio Laboratório",
    "Estágio Pesquisa Clínica",
    "Estágio Biotecnologia"

        # --- AI SAFETY (Mantendo seu nicho) ---
    "AI Safety",
    "AI Governance"
]

# Blacklist: Remove vagas operacionais ou que não são o foco
BLACKLIST = [
    "Vendedor", "Atendente", "Recepcionista", "Técnico de Manutenção", 
    "Professor", "RH", "Recursos Humanos", "Departamento Pessoal"
]
