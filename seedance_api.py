# seedance_api.py - Integracao com a API Seedance 2.0
import time
import requests
from config import (
    SEEDANCE_API_KEY, SEEDANCE_BASE_URL, SEEDANCE_MODEL,
    POLLING_INTERVAL, MAX_RETRIES
)


def _headers():
    return {
        "Authorization": f"Bearer {SEEDANCE_API_KEY}",
        "Content-Type": "application/json",
    }


def submit_text_to_video(prompt: str, duration: int = 5) -> str:
    """Envia um prompt de texto e retorna o task_id."""
    payload = {
        "model": SEEDANCE_MODEL,
        "content": [
            {
                "type": "text",
                "text": prompt
            }
        ],
        "parameters": {
            "duration": duration,
            "resolution": "720p",
            "fps": 24
        }
    }
    url = f"{SEEDANCE_BASE_URL}/videos/generations"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["id"]


def submit_image_to_video(prompt: str, image_url: str, duration: int = 5) -> str:
    """Envia prompt + imagem de referencia e retorna o task_id."""
    payload = {
        "model": SEEDANCE_MODEL,
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": prompt}
        ],
        "parameters": {
            "duration": duration,
            "resolution": "720p",
            "fps": 24
        }
    }
    url = f"{SEEDANCE_BASE_URL}/videos/generations"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["id"]


def poll_task(task_id: str) -> dict:
    """Aguarda conclusao da tarefa e retorna os dados finais."""
    url = f"{SEEDANCE_BASE_URL}/videos/generations/{task_id}"
    for attempt in range(MAX_RETRIES):
        resp = requests.get(url, headers=_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")
        print(f"  [Seedance] Task {task_id} | Status: {status} | Tentativa {attempt + 1}/{MAX_RETRIES}")
        if status == "succeeded":
            return data
        elif status in ("failed", "cancelled"):
            raise RuntimeError(f"Task {task_id} falhou com status: {status}")
        time.sleep(POLLING_INTERVAL)
    raise TimeoutError(f"Task {task_id} nao concluiu em {MAX_RETRIES * POLLING_INTERVAL}s")


def download_video(task_data: dict, dest_path: str) -> str:
    """Faz download do video gerado e salva em dest_path."""
    video_url = task_data["video_result"][0]["url"]
    resp = requests.get(video_url, stream=True, timeout=120)
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  [Download] Salvo em: {dest_path}")
    return dest_path
