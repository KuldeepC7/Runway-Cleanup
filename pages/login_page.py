# pages/login.py
import flet as ft
from utils.firebase import auth, db
from pages.home import home_view

def login_view(page: ft.Page):
    # Reuse header & footer
    header = home_view(page).controls[0]
    footer = home_view(page).controls[-1]

    # Custom Colors
    PRIMARY_COLOR = ft.Colors.BLUE_900
    SECONDARY_COLOR = ft.Colors.BLUE_50

    # Form Fields
    email = ft.TextField(
        label="Email",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=12,
        border_color=ft.Colors.GREY_400,
        focused_border_color=PRIMARY_COLOR,
        filled=True,
        bgcolor=SECONDARY_COLOR,
        width=320
    )

    password = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        border_radius=12,
        border_color=ft.Colors.GREY_400,
        focused_border_color=PRIMARY_COLOR,
        filled=True,
        bgcolor=SECONDARY_COLOR,
        password=True,
        can_reveal_password=True,
        width=320
    )

    info = ft.Container(visible=False, padding=10)

    # Login Logic
    def login_user(e):
        try:
            user = auth.sign_in_with_email_and_password(
                email.value.strip(),
                password.value.strip()
            )
            uid = user["localId"]
            user_data = db.child("users").child(uid).get().val()

            if not user_data:
                show_message("User data not found.", ft.Colors.RED_500)
            else:
                page.session.set("user", {"uid": uid, "email": email.value.strip()})
                show_message(f"Welcome, {user_data.get('name', 'Admin')}!", ft.Colors.GREEN_500)
                page.go("/admin" if user_data.get("role") == "admin" else "/")
                
        except Exception as e:
            show_message("Login failed - please check credentials.", ft.Colors.RED_500)
        page.update()

    def show_message(text, color):
        info.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.INFO_OUTLINED if color == ft.Colors.RED_500 else ft.Icons.CHECK_CIRCLE_OUTLINED,
                        color=color,
                        size=20),
                ft.Text(text, color=color, size=14)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        info.visible = True
        info.bgcolor = color + "20"  # Add opacity to color
        info.border_radius = 8
        info.update()

    # Login Card
    login_card = ft.Container(
        width=400,
        padding=30,
        margin=50,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        # shadow=ft.BoxShadow(
        #     blur_radius=20,
        #     spread_radius=2,
        #     color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900),
        #     offset=ft.Offset(0, 4)
        # ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("Welcome Back", 
                              size=28, 
                              weight="w900",
                              color=PRIMARY_COLOR),
                        ft.Text("Admin Portal Access", 
                              size=16, 
                              color=ft.Colors.GREY_600)
                    ], spacing=5),
                    padding=ft.padding.only(bottom=30)
                ),
                email,
                password,
                ft.Container(height=10),
                ft.FilledButton(
                    "Sign In",
                    icon=ft.Icons.LOGIN_OUTLINED,
                    on_click=login_user,
                    style=ft.ButtonStyle(
                        bgcolor=PRIMARY_COLOR,
                        color=ft.Colors.WHITE,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        overlay_color=PRIMARY_COLOR.with_opacity(0.8, ft.Colors.PRIMARY)
                    ),
                    width=320,
                    height=50
                ),
                info,
                ft.Container(
                    padding=10,
                    content=ft.TextButton(
                        "Forgot Password?",
                        style=ft.ButtonStyle(color=ft.Colors.GREY_600),
                        on_click=lambda e: page.go("/reset-password")
                    )
                )
            ],
            spacing=20
        )
    )

    # Main Container
    main_container = ft.Container(
        expand=True,
        height=600,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_50, ft.Colors.WHITE]
        ),
        content=ft.Stack(
            controls=[
                ft.Image(
                    src="admin.jpg",
                    opacity=0.15,
                    expand=True,
                    fit=ft.ImageFit.COVER,
                    height=700,
                    width=1000
                    
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=login_card
                )
            ]
        )
    )

    return ft.View(
        "/login",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            main_container,
            footer
        ]
    )