#!/usr/bin/env python3
# main.py - Orquestrador da automacao de videoclipes dos Garimpeirinhos
"""
Fluxo completo:
  1. Le musicas da pasta inputs/
  2. Carrega o roteiro (JSON) com cenas e prompts
  3. Envia cada cena para a API Seedance 2.0
  4. Aguarda geracao de cada clipe (polling)
  5. Faz download dos clipes gerados
  6. Monta o videoclipe final com o audio original
  7. Salva em outputs/final/
"""
import os
import json
import glob
import argparse
from pathlib import Path
from tqdm import tqdm

from config import INPUT_DIR, CLIPS_DIR, STYLE_PROMPT, CENE_DURATION
from seedance_api import submit_text_to_video, submit_image_to_video, poll_task, download_video
from video_builder import montar_videoclipe, limpar_clipes_temporarios


def carregar_roteiro(roteiro_path: str) -> dict:
    """Carrega o arquivo JSON de roteiro da musica."""
    with open(roteiro_path, "r", encoding="utf-8") as f:
        return json.load(f)


def gerar_prompt_cena(cena: dict) -> str:
    """Combina descricao da cena com o estilo visual padrao dos Garimpeirinhos."""
    descricao = cena.get("descricao", "")
    personagens = cena.get("personagens", "")
    ambiente = cena.get("ambiente", "")
    plano = cena.get("plano", "plano medio")
    return (
        f"{plano}, {descricao}, {personagens}, {ambiente}. "
        f"{STYLE_PROMPT}"
    )


def processar_musica(roteiro_path: str, audio_path: str, limpar_temp: bool = True):
    """Processa uma musica completa: gera cenas, monta e exporta."""
    roteiro = carregar_roteiro(roteiro_path)
    titulo = roteiro.get("titulo", "Garimpeirinhos")
    cenas = roteiro.get("cenas", [])
    output_name = Path(roteiro_path).stem

    print(f"\n{'='*60}")
    print(f"Musica: {titulo}")
    print(f"Total de cenas: {len(cenas)}")
    print(f"{'='*60}\n")

    os.makedirs(CLIPS_DIR, exist_ok=True)
    clips_gerados = []

    for i, cena in enumerate(tqdm(cenas, desc="Gerando cenas"), start=1):
        prompt = gerar_prompt_cena(cena)
        imagem_ref = cena.get("imagem_referencia")  # opcional

        print(f"\n[Cena {i}/{len(cenas)}] {cena.get('descricao', '')}")
        print(f"  Prompt: {prompt[:80]}...")

        # Envia para a API
        if imagem_ref and os.path.exists(imagem_ref):
            task_id = submit_image_to_video(prompt, imagem_ref, duration=CENE_DURATION)
        else:
            task_id = submit_text_to_video(prompt, duration=CENE_DURATION)

        # Aguarda conclusao
        task_data = poll_task(task_id)

        # Faz download
        dest = os.path.join(CLIPS_DIR, f"{output_name}_cena{i:02d}.mp4")
        download_video(task_data, dest)
        clips_gerados.append(dest)

    # Monta videoclipe final
    print(f"\n[Montagem] Unindo {len(clips_gerados)} cenas...")
    video_final = montar_videoclipe(clips_gerados, audio_path, titulo, output_name)

    if limpar_temp:
        limpar_clipes_temporarios(clips_gerados)

    print(f"\n[CONCLUIDO] Videoclipe disponivel em: {video_final}\n")
    return video_final


def main():
    parser = argparse.ArgumentParser(
        description="Gerador automatico de videoclipes dos Garimpeirinhos"
    )
    parser.add_argument(
        "--roteiro", "-r",
        help="Caminho do arquivo JSON de roteiro. Se omitido, processa todos em inputs/"
    )
    parser.add_argument(
        "--audio", "-a",
        help="Caminho do arquivo de audio .mp3"
    )
    parser.add_argument(
        "--manter-temp", action="store_true",
        help="Nao remove clipes temporarios apos a montagem"
    )
    args = parser.parse_args()

    if args.roteiro and args.audio:
        # Processa musica especifica
        processar_musica(args.roteiro, args.audio, limpar_temp=not args.manter_temp)
    else:
        # Processa todos os roteiros encontrados em inputs/
        roteiros = glob.glob(os.path.join(INPUT_DIR, "*.json"))
        if not roteiros:
            print(f"Nenhum arquivo .json encontrado em '{INPUT_DIR}'.")
            print("Crie um roteiro no formato: inputs/nome_da_musica.json")
            return
        for roteiro_path in roteiros:
            nome = Path(roteiro_path).stem
            audio_path = os.path.join(INPUT_DIR, f"{nome}.mp3")
            if not os.path.exists(audio_path):
                print(f"[AVISO] Audio nao encontrado para '{nome}', pulando...")
                continue
            processar_musica(roteiro_path, audio_path, limpar_temp=not args.manter_temp)


if __name__ == "__main__":
    main()
