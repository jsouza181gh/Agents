# Agents — agent loop em Python

Prática do curso **AI Agents and Agentic AI with Python & Generative AI** (Vanderbilt University / Coursera, nota 100% — [certificado](https://coursera.org/verify/XXZRDYYGJD8B)).

Implementação do zero, sem framework de agentes, para entender cada peça de um agente: loop de decisão, tool calling, memória e critério de parada. As chamadas ao modelo passam pelo [LiteLLM](https://github.com/BerriAI/litellm), então trocar de provedor (Gemini, OpenAI, Anthropic) é trocar a string do modelo.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `loop.py` | Agente com **agent loop**: a cada iteração o LLM escolhe uma tool (`list_files`, `read_file`, `terminate`) num bloco `action` em JSON; o resultado da tool volta para a memória como feedback. Para no `terminate` ou após 10 iterações. |
| `agent.py` | Agente que **gera código Python** a partir de um pedido. Mostra o código e só executa com confirmação, com timeout de 30 s. |
| `informations/` | Dados de exemplo consultados pelo `loop.py`: saldo, cotações do bitcoin em reais e explicação da conversão. |

## Como o loop funciona (`loop.py`)

```
pedido do usuário
   └─► LLM decide a próxima ação ──► ```action {"tool_name": "...", "args": "..."}```
          ▲                                   │
          └──── resultado da tool volta ◄─────┘   (até "terminate" ou 10 iterações)
```

Exemplo de pedido: *"Quantos bitcoins consigo comprar com meu saldo pela cotação mais recente?"* — o agente lista os arquivos, lê o saldo e as cotações, aplica a fórmula da explicação e encerra com a resposta.

## Rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.exemple .env             # preencha GEMINI_API_KEY (ou exporte a variável no terminal)

python loop.py
python agent.py
```

Modelo usado: `gemini/gemini-3.1-flash-lite`.

## Segurança

`agent.py` executa código escrito por um LLM. Por isso ele mostra o código antes, pede confirmação explícita e encerra a execução após 30 s. Mesmo assim o código roda no seu Python local: para pedidos arbitrários, use um ambiente isolado (container ou VM).

## Próximos passos

- Registro de tools com decorators, mantendo definição e documentação da tool sincronizadas.
- Modelar o agente com o framework GAME (Goals, Actions, Memory, Environment).
- Tratar respostas do LLM fora do formato `action` e erros de leitura de arquivo dentro do loop.
