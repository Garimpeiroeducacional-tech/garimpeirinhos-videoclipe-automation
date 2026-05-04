# Garimpeirinhos Videoclipe Automation

Automacao completa para geracao de videoclipes das musicas dos **Garimpeirinhos** usando a API **Seedance 2.0**.

## Arquitetura

```
inputs/
  nome_da_musica.json   # roteiro com cenas
  nome_da_musica.mp3    # audio da musica
  personagem_ref.png    # imagem de referencia (opcional)

outputs/
  clips/                # cenas individuais geradas
  final/                # videoclipe final montado
```

## Fluxo da Automacao

```
[Roteiro JSON] --> [Gerar prompts por cena]
                       |
                       v
              [API Seedance 2.0]
                       |
                       v
              [Polling de status]
                       |
                       v
              [Download dos clipes]
                       |
                       v
        [Montagem com audio original] (moviepy)
                       |
                       v
              [Videoclipe final .mp4]
```

## Instalacao

```bash
# Clone o repositorio
git clone https://github.com/Garimpeiroeducacional-tech/garimpeirinhos-videoclipe-automation.git
cd garimpeirinhos-videoclipe-automation

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependencias
pip install -r requirements.txt
```

## Configuracao

Crie um arquivo `.env` na raiz do projeto:

```env
SEEDANCE_API_KEY=sua_chave_aqui
SEEDANCE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
SEEDANCE_MODEL=seedance-1-0-lite-t2v-250428
```

## Formato do Roteiro (JSON)

Crie um arquivo `inputs/nome_da_musica.json`:

```json
{
  "titulo": "O Tesouro do Garimpo",
  "cenas": [
    {
      "descricao": "criancas exploradores encontram um mapa antigo",
      "personagens": "tres criancas com chapeu de aventureiro",
      "ambiente": "floresta tropical com luz dourada",
      "plano": "plano medio",
      "imagem_referencia": "inputs/personagens_ref.png"
    },
    {
      "descricao": "grupo corre animado pela trilha da floresta",
      "personagens": "tres criancas sorrindo",
      "ambiente": "trilha com arvores altas e raios de sol",
      "plano": "plano americano"
    }
  ]
}
```

## Uso

### Processar uma musica especifica

```bash
python main.py --roteiro inputs/tesouro.json --audio inputs/tesouro.mp3
```

### Processar todas as musicas da pasta inputs/

```bash
python main.py
```

### Manter clipes temporarios apos a montagem

```bash
python main.py --manter-temp
```

## Modulos

| Arquivo | Funcao |
|---|---|
| `main.py` | Orquestrador principal |
| `seedance_api.py` | Integracao com API Seedance 2.0 |
| `video_builder.py` | Montagem do videoclipe final |
| `config.py` | Configuracoes e variaveis |

## Personalizacao do Estilo Visual

Edite `STYLE_PROMPT` em `config.py` para ajustar o estilo de animacao:

```python
STYLE_PROMPT = (
    "estilo animacao infantil colorida e alegre, personagens criancas exploradores "
    "com roupas de aventureiro, cenario tropical brasileiro, cores vibrantes"
)
```

## Licenca

MIT License - veja [LICENSE](LICENSE) para detalhes.

---
Projeto desenvolvido por **Garimpeiroeducacional-tech** para o CTPM Ipatinga.
