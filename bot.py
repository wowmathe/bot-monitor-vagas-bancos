import requests
import os
from datetime import datetime

# ================= CONFIGURAÇÃO =================
VAGAS_ARQUIVO = "vagas_enviadas.txt"
RESUMO_ARQUIVO = "resumo.txt"

CIDADES = ["São Paulo", "São Bernardo do Campo", "Santo André", "São Caetano do Sul"]
PALAVRAS_CHAVE = ["agente de negócios", "gerente de negócios"]

# ================= TELEGRAM =================
BOT_TOKEN = "7647732498:AAGPq-FOJ-1VinDgZ2R9-DoKH504qNS5eWc"
CHAT_ID = "6679053851"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def enviar_mensagem(texto):
    try:
        response = requests.post(
            TELEGRAM_URL,
            data={
                "chat_id": CHAT_ID,
                "text": texto,
                "parse_mode": "HTML"
            },
            timeout=15
        )
        if response.status_code != 200:
            print("Falha ao enviar mensagem. Status:", response.status_code)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

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
        enviar_mensagem("📊 <b>Resumo diário de vagas</b>\nNenhuma nova vaga encontrada hoje.")
        return

    with open(RESUMO_ARQUIVO, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    if conteudo:
        enviar_mensagem(f"📊 <b>Resumo diário de vagas</b>\n\n{conteudo}")
    else:
        enviar_mensagem("📊 <b>Resumo diário de vagas</b>\nNenhuma nova vaga encontrada hoje.")

    os.remove(RESUMO_ARQUIVO)

# ================= BUSCA DE VAGAS =================
def buscar_vagas():
    vagas_enviadas = carregar_vagas_enviadas()
    encontrou_vaga = False

    for cidade in CIDADES:
        for palavra in PALAVRAS_CHAVE:
            # URL de busca do Bradesco (exemplo simplificado)
            url = (
                "https://bradesco.csod.com/ux/ats/careersite/search?"
                f"q={palavra.replace(' ', '%20')}&location={cidade.replace(' ', '%20')}"
            )

            vaga_id = f"{palavra}-{cidade}"

            try:
                response = requests.get(url, timeout=15)
                conteudo = response.text.lower()

                # Se encontrar palavra-chave no HTML da página
                if palavra.lower() in conteudo and vaga_id not in vagas_enviadas:
                    # Formatação HTML para Telegram
                    texto = (
                        f"🏦 <b>Nova vaga - Bradesco</b>\n"
                        f"📌 Cargo: <b>{palavra.title()}</b>\n"
                        f"📍 Local: {cidade}\n"
                        f"🔗 <a href='{url}'>Clique aqui para acessar a vaga</a>"
                    )
                    adicionar_ao_resumo(texto)
                    salvar_vaga(vaga_id)
                    encontrou_vaga = True

            except Exception as e:
                adicionar_ao_resumo(
                    f"⚠️ Erro ao buscar vagas em {cidade} (Bradesco): {e}"
                )

    if not encontrou_vaga:
        adicionar_ao_resumo(
            f"🔍 Busca realizada em {datetime.now().strftime('%d/%m/%Y %H:%M')}: nenhuma nova vaga encontrada."
        )

# ================= EXECUÇÃO =================
if __name__ == "__main__":
    print("BOT INICIADO")
    buscar_vagas()
    enviar_resumo_diario()
    print("Busca finalizada!")
