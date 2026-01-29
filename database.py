# Memória do bot para não repetir vagas

import sqlite3

DB_FILE = "jobs_history.db"

def init_db():
    """Cria o banco de dados se não existir."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_jobs (
            link TEXT PRIMARY KEY,
            date_sent TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_job_new(link):
    """Verifica se a vaga já foi enviada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_jobs WHERE link = ?", (link,))
    exists = cursor.fetchone()
    conn.close()
    return exists is None

def save_job(link):
    """Salva a vaga como enviada."""
    import datetime
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT OR IGNORE INTO sent_jobs (link, date_sent) VALUES (?, ?)", (link, now))
    conn.commit()
    conn.close()
