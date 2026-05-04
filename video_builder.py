# video_builder.py - Montagem final do videoclipe
import os
from moviepy.editor import (
    VideoFileClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip
)
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, FINAL_DIR


def montar_videoclipe(clips_paths: list, audio_path: str, titulo: str, output_name: str) -> str:
    """
    Concatena clips de video, sincroniza com o audio da musica
    e exporta o videoclipe final.

    Args:
        clips_paths: lista de caminhos dos clipes .mp4 gerados
        audio_path:  caminho do arquivo de audio .mp3 da musica
        titulo:      nome da musica (exibido como texto inicial)
        output_name: nome do arquivo de saida sem extensao

    Returns:
        Caminho do arquivo final exportado.
    """
    os.makedirs(FINAL_DIR, exist_ok=True)

    # Carrega e ajusta cada clipe ao tamanho padrao
    clipes = []
    for path in clips_paths:
        clip = VideoFileClip(path).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
        clipes.append(clip)

    # Concatena todos os clipes
    video_concat = concatenate_videoclips(clipes, method="compose")

    # Carrega audio e corta/estende para durar o mesmo que o video
    audio = AudioFileClip(audio_path)
    if audio.duration > video_concat.duration:
        audio = audio.subclip(0, video_concat.duration)
    else:
        video_concat = video_concat.subclip(0, audio.duration)

    video_com_audio = video_concat.set_audio(audio)

    # Adiciona titulo como legenda inicial (3 segundos)
    try:
        txt_clip = (
            TextClip(titulo, fontsize=48, color="white", font="Arial-Bold",
                     stroke_color="black", stroke_width=2)
            .set_position(("center", "bottom"))
            .set_duration(3)
        )
        video_final = CompositeVideoClip([video_com_audio, txt_clip])
    except Exception:
        # Caso nao tenha fontes disponiveis, exporta sem texto
        video_final = video_com_audio

    output_path = os.path.join(FINAL_DIR, f"{output_name}.mp4")
    video_final.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp_audio.m4a",
        remove_temp=True,
        verbose=False,
        logger=None
    )
    print(f"[VideoBuilder] Videoclipe exportado: {output_path}")
    return output_path


def limpar_clipes_temporarios(clips_paths: list):
    """Remove arquivos de clipes individuais apos a montagem."""
    for path in clips_paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
    print(f"[VideoBuilder] {len(clips_paths)} clipes temporarios removidos.")
