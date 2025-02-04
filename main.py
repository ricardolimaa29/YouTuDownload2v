import flet as ft
import json
import os
import yt_dlp
import re
import time
CONFIG_FILE = "config.json"

def carregar_configuracoes():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    return {
        "idade": 18,
        "caminho_cookies": "",
        "usuario": "",
        "senha": ""
    }
config = carregar_configuracoes()

def salvar_configuracoes(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)



def main(page: ft.Page):
    page.title = "DW - YouT by Ricardo Rodrigues"
    page.window_width = 800
    page.window_height = 600
    page.padding = 20
    page.scroll = "adaptive"
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_900)

    config = carregar_configuracoes()
    progress_bar = ft.ProgressBar(width=600, value=0, visible=False)

    formato_download = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mp4", label="MP4"),
            ft.Radio(value="mp3", label="MP3")
        ]),
        value="mp4"  
    )
    def abrir_configuracoes(e):
        idade_input.value = str(config.get("idade", 18))
        caminho_cookies_input.value = config.get("caminho_cookies", "")
        page.overlay.append(configuracoes_modal) == configuracoes_modal
        configuracoes_modal.open = True
        page.update()

    def atualizar_progresso(d):
        
        if d['status'] == 'downloading':
            downloaded = d.get('_percent_str', '0%').strip()

            
            downloaded = re.sub(r'\x1b\[.*?m', '', downloaded)

            try:
                
                progress_bar.value = float(downloaded.strip('%')) / 100
                page.update()
            except ValueError:
                pass  
    def fechar_modal(e):
        configuracoes_modal.open = False
        page.update()

    def download_video(e):
        link = url_input.value
        if not link:
            status_text.value = "Por favor, insira um link válido."
            status_text.color = "red"
            status_text.visible = True
            page.update()
            return

        formato_escolhido = formato_download.value  

       
        if formato_escolhido == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'cookiefile': config["caminho_cookies"],
                'progress_hooks': [atualizar_progresso],
                'verbose': True,
                'ffmpeg_location': 'C:\\FFMPEG\\ffmpeg.exe',
            }
        else: 
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'cookiefile': config["caminho_cookies"],
                'progress_hooks': [atualizar_progresso],
                'verbose': True,
                'ffmpeg_location': 'C:\\FFMPEG\\ffmpeg.exe',
            }

        progress_bar.value = 0
        progress_bar.visible = True
        page.update()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                titulo = info_dict.get('title', 'Sem título')
                thumbnail = info_dict.get('thumbnail', '')

                video_info_view.controls.append(ft.Column(controls=[
                    ft.Text(f"Título: {titulo}", size=16, weight="bold"),
                    ft.Image(src=thumbnail, width=250, height=300),
                    ft.Text(f"DOWNLOAD CONCLUÍDO! - {formato_escolhido}", color="YELLOW", size=18, weight="bold")
                ]))
                status_text.value = ""
                page.update()

        except yt_dlp.utils.DownloadError as ex:
            status_text.value = f"Erro: {ex}"
            status_text.color = "red"
            status_text.visible = True

        progress_bar.visible = False
        page.update()

    url_input = ft.TextField(
        label="Insira a URL do vídeo",
        hint_text="Exemplo: https://www.youtube.com/watch?v=abc123",
        width=600,
    )

    btn_baixar = ft.ElevatedButton("Baixar", icon=ft.icons.DOWNLOAD, on_click=download_video)
    btn_config = ft.ElevatedButton("Configurações", on_click=abrir_configuracoes, icon=ft.icons.SETTINGS)
    status_text = ft.Text(value="", size=16, color="black", visible=False)

    video_info_view = ft.Column()

    idade_input = ft.TextField(label="Idade", value=str(config.get("idade", 18)))
    caminho_cookies_input = ft.TextField(
        label="Caminho dos cookies",
        value=config.get("caminho_cookies", ""),
        hint_text="Exemplo: C:/meus_cookies.txt"
    )
    def atualizar_configuracoes(e):
            config["idade"] = int(idade_input.value)
            config["caminho_cookies"] = caminho_cookies_input.value
            salvar_configuracoes(config)
            status_text.value = "Configurações salvas com sucesso!"
            status_text.color = "green"
            status_text.visible = True
            configuracoes_modal.open = False
            page.update()
            time.sleep(3)
            status_text.visible = False
            page.update()

    configuracoes_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Configurações"),
        content=ft.Column(
            [idade_input, caminho_cookies_input],
            tight=True,
        ),
        actions=[
            ft.TextButton("Salvar", on_click=atualizar_configuracoes),
            ft.TextButton("Fechar", on_click=fechar_modal),
        ],
    )

    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Utilize o melhor sistema de download de audios e videos", size=24, weight="bold")], alignment="center"),
                ft.Divider(),
                ft.Row([url_input], alignment="center"),
                ft.Row([formato_download], alignment="center"),
                ft.Row([btn_baixar,btn_config], alignment="center"),
                ft.Divider(),
                ft.Row([progress_bar], alignment="center"),
                ft.Row([status_text], alignment="center"),
                video_info_view,
            ],
            spacing=20,
        )
    )

ft.app(target=main)
