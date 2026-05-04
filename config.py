# config.py — Configuracoes centrais da automacao Garimpeirinhos
import os
from dotenv import load_dotenv

load_dotenv()

# === API Seedance 2.0 ===
SEEDANCE_API_KEY = os.getenv("SEEDANCE_API_KEY", "")
SEEDANCE_BASE_URL = os.getenv("SEEDANCE_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
SEEDANCE_MODEL = os.getenv("SEEDANCE_MODEL", "seedance-1-0-lite-t2v-250428")

# === Diretorios ===
INPUT_DIR = "inputs"       # pasta com musicas (.mp3) e imagens de personagens
OUTPUT_DIR = "outputs"     # pasta para clipes gerados
CLIPS_DIR = "outputs/clips"  # cenas individuais
FINAL_DIR = "outputs/final"  # videoclipes completos

# === Configuracoes de video ===
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 24
CENE_DURATION = 5  # segundos por cena

# === Estilo visual padrao dos Garimpeirinhos ===
STYLE_PROMPT = (
    "estilo animacao infantil colorida e alegre, personagens criancas exploradores "
    "com roupas de aventureiro, cenario tropical brasileiro, cores vibrantes, "
    "iluminacao quente, qualidade cinematografica"
)

# === Configuracoes de polling ===
POLLING_INTERVAL = 10  # segundos entre verificacoes de status
MAX_RETRIES = 60        # tentativas maximas antes de timeout
