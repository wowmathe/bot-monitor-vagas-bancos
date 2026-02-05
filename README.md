🤖 Bot Monitor de Vagas Bancárias

Projeto pessoal desenvolvido para automatizar a busca por vagas no setor bancário, com foco em otimização de tempo, aprendizado prático em automação e aplicação de programação no dia a dia.

O bot realiza buscas periódicas em páginas de instituições financeiras, filtra vagas por cargo e localidade e envia um resumo automático, inclusive quando nenhuma vaga é encontrada — garantindo visibilidade total da execução.


---

🚀 Funcionalidades

🔎 Monitoramento automatizado de vagas

🎯 Filtro por cargo e localidade

📩 Envio de resumo diário (com ou sem vagas encontradas)

⏱️ Execução agendada via cron (Termux)

🧪 Testes manuais para validação de funcionamento



---

🛠️ Tecnologias Utilizadas

Python

Automação de tarefas

Estrutura modular de código

Termux (ambiente Linux no Android)

Cron (agendamento de tarefas)



---

📂 Estrutura do Projeto

bot-monitor-vagas-bancos/
├── bot.py               # Script principal do bot
├── enviar_resumo.py     # Responsável pelo envio das mensagens
├── README.md            # Documentação do projeto
├── .gitignore           # Arquivos ignorados pelo Git


---

▶️ Como Executar o Projeto

Pré-requisitos

Python 3 instalado

Termux (ou qualquer ambiente Linux)


Execução manual

python bot.py

Execução automática (cron)

Exemplo de agendamento diário às 08h:

0 8 * * * python /caminho/para/bot.py >> cron.log 2>&1


---

🎯 Objetivo do Projeto

Este projeto foi criado com o objetivo de:

Automatizar e otimizar a busca por oportunidades no setor bancário

Aplicar conceitos de programação e automação na prática

Desenvolver autonomia técnica, adaptabilidade e resiliência

Criar um projeto real para portfólio profissional



---

📈 Próximas Melhorias (Roadmap)

[ ] Suporte a múltiplas fontes de vagas

[ ] Logs mais detalhados

[ ] Tratamento avançado de erros

[ ] Containerização (Docker)

[ ] Interface simples para configuração



---

⚠️ Aviso

Este é um projeto pessoal com fins educacionais e de portfólio.
Nenhuma credencial, token ou dado sensível é versionado neste repositório.


---

👤 Autor

Matheus Lucizano
Projeto desenvolvido como iniciativa pessoal para aprendizado contínuo, automação de processos e evolução profissional.
📌 Fique à vontade para clonar, testar ou deixar sugestões!
