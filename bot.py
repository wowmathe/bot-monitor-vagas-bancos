print("BOT INICIADO")

import requests
import os
from datetime import datetime

# ================= CONFIG =================

CIDADES = [
    "São Paulo",
    "São Bernardo do Campo",
    "Santo André",
    "São Caetano do Sul"
]

PALAVRAS_CHAVE = [
    "agente de negócios"
]

VAGAS_ARQUIVO = "vagas_enviadas.txt"
RESUMO_ARQUIVO = "resumo.txt"

# ================= TELEGRAM =================

def carregar_env():
    env = {}
    with open(".env", "r") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                env[chave] = valor
    return env

env = carregar_env()

BOT_TOKEN = env.get("BOT_TOKEN")
CHAT_ID = env.get("CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def enviar_mensagem(texto):
    requests.post(
        TELEGRAM_URL,
        data={
            "chat_id": CHAT_ID,
            "text": texto,
            "parse_mode": "HTML"
        },
        timeout=15
    )

# ================= CONTROLE DE VAGAS =================

def carregar_vagas_enviadas():
    if not os.path.exists(VAGAS_ARQUIVO):
        return set()
    with open(VAGAS_ARQUIVO, "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

def salvar_vaga(vaga_id):
    with open(VAGAS_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(vaga_id + "\n")

# ================= RESUMO DIÁRIO =================

def adicionar_ao_resumo(texto):
    with open(RESUMO_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(texto + "\n\n")

def enviar_resumo_diario():
    if not os.path.exists(RESUMO_ARQUIVO):
        enviar_mensagem("📊 <b>Resumo diário</b>\nNenhuma vaga encontrada hoje.")
        return

    with open(RESUMO_ARQUIVO, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    if conteudo:
        enviar_mensagem(f"📊 <b>Resumo diário de vagas</b>\n\n{conteudo}")
    else:
        enviar_mensagem("📊 <b>Resumo diário</b>\nNenhuma vaga encontrada hoje.")

    os.remove(RESUMO_ARQUIVO)

# ================= BUSCA DE VAGAS =================

def buscar_vagas():
    vagas_enviadas = carregar_vagas_enviadas()
    encontrou_vaga = False

    for cidade in CIDADES:
        for palavra in PALAVRAS_CHAVE:
            url = (
                "https://bradesco.csod.com/ux/ats/careersite/1/search?"
                f"q={palavra.replace(' ', '%20')}&location={cidade.replace(' ', '%20')}"
            )

            vaga_id = f"{palavra}-{cidade}"

            try:
                response = requests.get(url, timeout=15)
                conteudo = response.text.lower()

                if palavra in conteudo and cidade.lower() in conteudo:
                    if vaga_id not in vagas_enviadas:
                        texto = (
                            f"🏦 <b>Nova vaga encontrada</b>\n"
                            f"📌 Cargo: {palavra.title()}\n"
                            f"📍 Local: {cidade}\n"
                            f"🔗 {url}"
                        )
                        adicionar_ao_resumo(texto)
                        salvar_vaga(vaga_id)
                        encontrou_vaga = True

            except Exception as e:
                adicionar_ao_resumo(
                    f"⚠️ Erro ao buscar vagas em {cidade}: {e}"
                )

    if not encontrou_vaga:
        adicionar_ao_resumo(
            f"🔍 Busca realizada em {datetime.now().strftime('%d/%m %H:%M')}\n"
            f"Nenhuma nova vaga encontrada."
        )

# ================= EXECUÇÃO =================

if __name__ == "__main__":
    buscar_vagas()
