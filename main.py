import flet as ft
import json
import os
import time
import yt_dlp


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

def download_video(self, format):
        link = self.new_task.value
        if not link:
            self.video_info_view.controls.append(ft.Text("Por favor, insira um link válido.", color="red"))
            self.update()
            return

        
        info_dict = self.extract_video_info(link)
        if not info_dict:
            return

        
        self.loading_animation.visible = True
        self.update()

        ydl_opts = {
            'format': 'bestaudio/best' if format == 'mp3' else 'best',
            "username": CONFIG_FILE["usuario"],
            "password": CONFIG_FILE["senha"],
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if format == 'mp3' else [],
            'ffmpeg_location': 'C:\\FFMPEG\\ffmpeg.exe',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([link])
                completion_text = ft.Text(f"DOWNLOAD CONCLUÍDO EM FORMATO {format.upper()}!", color="yellow", weight="bold")

                
                self.tasks_view.controls.insert(0, ft.Column(controls=[
                    ft.Text(f"Título: {info_dict['title']}"),
                    ft.Image(src=info_dict['thumbnail'], width=250, height=300),
                    ft.Text(f"Formato: {format.upper()}"),
                    ft.Text(f"Link: {link}"),
                    completion_text
                ]))
                self.update()

            except Exception as ex:
                self.video_info_view.controls.append(ft.Text(f"Erro durante o download: {ex}", color="red"))

        
        self.loading_animation.visible = False
        self.update()

def salvar_configuracoes(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def main(page: ft.Page):
    page.title = "Downloader Moderno"
    page.window_width = 800
    page.window_height = 600
    page.padding = 20
    page.scroll = "adaptive"
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_900)

    page.fonts = {
        "Poppins": "fonts/Poppins-Bold.ttf",
        "Poppins2": "fonts/Poppins-Light.ttf",
        "Poppins3": "fonts/Poppins-Regular.ttf",
        }
    
    config = carregar_configuracoes()

    
    def atualizar_configuracoes(e):
        config["idade"] = int(idade_input.value)
        config["caminho_cookies"] = caminho_cookies_input.value
        config["usuario"] = usuario_input.value
        config["senha"] = senha_input.value
        salvar_configuracoes(config)
        status_text.visible = True
        status_text.value = "Configurações salvas com sucesso!"
        status_text.color = "green"
        configuracoes_modal.open = False
        page.update()

        time.sleep(5)
        status_text.visible = False
        page.update()

    
    def abrir_configuracoes(e):
        idade_input.value = str(config.get("idade", 18))
        caminho_cookies_input.value = config.get("caminho_cookies", "")
        usuario_input.value = config.get("usuario", "")
        senha_input.value = config.get("senha", "")
        page.overlay.append(configuracoes_modal) == configuracoes_modal
        configuracoes_modal.open = True
        page.update()

    
    def fechar_modal(e):
        configuracoes_modal.open = False
        page.update()

    
    url_input = ft.TextField(
        label="Insira a URL do vídeo",
        hint_text="Exemplo: https://www.youtube.com/watch?v=abc123",
        width=600,
    )

    
    btn_baixar = ft.ElevatedButton("Baixar Vídeo", icon=ft.icons.DOWNLOAD)
    btn_config = ft.ElevatedButton("Configurações", on_click=abrir_configuracoes, icon=ft.icons.SETTINGS)

   
    status_text = ft.Text(value="", size=16, color="black")

    
    idade_input = ft.TextField(label="Idade", value=str(config.get("idade", 18)))
    caminho_cookies_input = ft.TextField(
        label="Caminho dos cookies",
        value=config.get("caminho_cookies", ""),
        hint_text="Exemplo: C:/meus_cookies.txt"
    )
    usuario_input = ft.TextField(
        label="E-mail (Usuário)",
        value=config.get("usuario", ""),
        hint_text="Exemplo: usuario@gmail.com"
    )
    senha_input = ft.TextField(
        label="Senha",
        value=config.get("senha", ""),
        password=True,
        can_reveal_password=True
    )
    
    configuracoes_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Configurações"),
        content=ft.Column(
            [idade_input, caminho_cookies_input, usuario_input, senha_input],
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
                ft.Row([ft.Text("Baixe videos e audios tranquilamente xxD", size=24, weight="bold",font_family='Poppins2')], alignment="center"),
                ft.Divider(),
                ft.Row([url_input], alignment="center"),
                ft.Row([btn_baixar, btn_config], alignment="center", spacing=10),
                ft.Divider(),
                ft.Row([status_text], alignment="center"),
            ],
            spacing=20,
        )
    )


ft.app(target=main)
