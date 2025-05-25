import os
from dotenv import load_dotenv

load_dotenv()

import flet as ft
from pages.home import home_view
from pages.book_form import book_form_view
from pages.admin_dashboard import admin_dashboard_view
from pages.login_page import login_view  #   ✅ import login view
from pages.about import about_view

def main(page: ft.Page):
    page.title = "RunWay Cleanup"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.session.set("user", page.session.get("user") or None)  # Init session if not set
    page.assets_dir = "assets"

    def route_change(route):
        page.views.clear()      
        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/book":
            page.views.append(book_form_view(page))
        elif page.route == "/about":
            page.views.append(about_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/admin":
            page.views.append(admin_dashboard_view(page))
        elif page.route == "/logout":
            page.session.set("user", None)
            page.go("/login")
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, view=ft.WEB_BROWSER, assets_dir = 'assets')
