import os
import flet as ft
from main import main

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, port=port, view=ft.WEB_BROWSER, assets_dir='assets')