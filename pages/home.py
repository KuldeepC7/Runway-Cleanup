import flet as ft

def home_view(page):
    def go_to_booking(e):
        page.go("/book")

    def go_to_about(e):
        page.go("/about")

    def go_home(e):
        page.go("/")

    def header():
        return ft.AppBar(
            leading=ft.Icon(ft.Icons.CLEANING_SERVICES, color=ft.Colors.WHITE, size=32),
            leading_width=40,
            title=ft.Row([
                ft.Text("RUNWAY", style=ft.TextThemeStyle.TITLE_LARGE, 
                       color=ft.Colors.WHITE, font_family='Roboto Slab', size=28),
                ft.Text("CLEANUP", style=ft.TextThemeStyle.TITLE_LARGE,
                       color=ft.Colors.AMBER_400, font_family='Roboto Slab', size=28)
            ], spacing=0),
            bgcolor=ft.Colors.BLUE_900,
            center_title=False,
            toolbar_height=70,
            actions=[
                ft.Container(
                    content=ft.Row([
                        ft.TextButton("Home", on_click=go_home, 
                                    style=ft.ButtonStyle(color=ft.Colors.WHITE, padding=10)),
                        ft.TextButton("About", on_click=go_to_about, 
                                    style=ft.ButtonStyle(color=ft.Colors.WHITE, padding=10)),
                        ft.FilledButton("Book Now", on_click=go_to_booking, 
                                      style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_400, 
                                                         color=ft.Colors.BLUE_900,
                                                         padding=15))
                    ], spacing=20),
                    padding=ft.padding.only(right=30)
                )
            ],
        )

    def greeting_section():
        return ft.Container(
            expand=True,
            height=600,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_700]
            ),
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="back.jpg",
                            opacity=0.2,
                            fit=ft.ImageFit.COVER,
                            expand = True,
                            # width = 650,
                            # height = 650
                        ),

                        # image_src="back.jpg",
                        # image_opacity=0.2,
                        # image_fit=ft.ImageFit.COVER,
                        # expand=True
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=30, vertical=120),
                        content=ft.Column([
                            ft.Text(
                                "Professional Cleaning Services",
                                size=48,
                                weight="w900",
                                text_align="center",
                                color=ft.Colors.WHITE,
                                font_family='Roboto Slab'
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                "Your Trusted Partner in Sanitation & Maintenance Solutions",
                                size=24,
                                text_align="center",
                                color=ft.Colors.AMBER_100
                            ),
                            ft.Container(height=30),
                            ft.FilledButton(
                                "Get Started →",
                                on_click=go_to_booking,
                                style=ft.ButtonStyle(
                                    padding=20,
                                    bgcolor=ft.Colors.AMBER_400,
                                    color=ft.Colors.BLUE_900
                                ),
                                height=50,
                                width=200
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ]
            )
        )

    def services_section():
        services = [
            {
                "title": "Septic Tank Cleanup",
                "desc": "Professional septic system maintenance with eco-friendly solutions.\n\nEnsure a clean and efficient septic system with professional septic  tank cleanup services in Hisar, Haryana. Our expert team provides thorough cleaning, maintenance, and waste disposal, ensuring hygiene and environmental safety. Using advanced techniques, we remove sludge and blockages, preventing system failures and unpleasant odors. Trust us for reliable and affordable solutions to keep your septic tank functioning smoothly. Contact us today for hassle-free service!\n\n₹800",
                "img": "tank.jpg",
                "icon": ft.Icons.WATER_DAMAGE,
                "color": ft.Colors.BLUE_400
            },
            {
                "title": "Pest Control",
                "desc": "Effective pest elimination using safe, modern techniques.\n\nProtect your home and business from pests with expert pest control services in Hisar, Haryana. Our skilled team uses safe and effective techniques to eliminate insects, rodents, and other nuisances, ensuring a hygienic and pest-free environment. With eco-friendly solutions and advanced methods, we prevent infestations and safeguard your health. Trust us for reliable and affordable pest management tailored to your needs. Contact us today for a hassle-free experience!\n\n₹500",
                "img": "pest.jpg",
                "icon": ft.Icons.BUG_REPORT,
                "color": ft.Colors.AMBER_400
            },
            {
                "title": "Tractor Rentals",
                "desc": "Reliable agricultural equipment for all your needs.\n\nLooking for reliable tractor rentals in Hisar, Haryana? We offer high-quality, well-maintained tractors for agricultural and commercial use, ensuring efficiency and performance. Our fleet is available at competitive rates, with flexible rental options to suit your needs. Whether for farming, construction, or transport, trust us for dependable equipment and hassle-free service. Contact us today to book your rental!\n\n₹1000",
                "img": "tractor.jpg",
                "icon": ft.Icons.AGRICULTURE,
                "color": ft.Colors.GREEN_400
            },
        ]


        cards = []
        for service in services:
            card = ft.Container(
                width=600,
                height=340,
                bgcolor=ft.Colors.WHITE,
                padding=ft.Padding(left=25, top=25, right=25, bottom=25),
                margin=20,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400, offset=ft.Offset(2, 2)),
                content=ft.Row(
                    controls=[
                        # Image on the left
                        ft.Image(
                            src=service["img"],
                            width=250,
                            height=250,
                            fit=ft.ImageFit.COVER,
                            border_radius=8
                        ),
                        # Text and button on the right
                        ft.Container(
                            expand=True,
                            padding=15,
                            content=ft.Column(
                                controls=[
                                    ft.Text(service["title"], size=23, weight="bold", color=ft.Colors.BLUE_900),
                                    ft.Text(service["desc"], size=16),
                                    ft.FilledButton(
                                        "Book Service",
                                        on_click=go_to_booking,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.BLUE_900,
                                            color=ft.Colors.WHITE,
                                            padding=15
                                        )
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
            cards.append(card)




        return ft.Container(
            bgcolor=ft.Colors.GREY_50,
            padding=ft.padding.symmetric(vertical=80, horizontal=30),
            content=ft.Column([
                ft.Text("Our Services", 
                      size=36, 
                      weight="w900", 
                      color=ft.Colors.BLUE_900,
                      text_align="center"),
                ft.Container(height=30),
                ft.ResponsiveRow(
                    controls=cards,
                    alignment=ft.MainAxisAlignment.CENTER,
                    run_spacing=40,
                    spacing=40
                )
            ])
        )

    def map_section():
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(vertical=80, horizontal=30),
            content=ft.Column([
                ft.Text("Service Areas", 
                      size=36, 
                      weight="w900", 
                      color=ft.Colors.BLUE_900,
                      text_align="center"),
                ft.Container(height=30),
                ft.Card(
                    elevation=15,
                    content=ft.Container(
                        height=500,
                        border_radius=15,
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    expand=2,
                                    padding=30,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=[ft.Colors.BLUE_50, ft.Colors.BLUE_100]
                                    ),
                                    content=ft.Column([
                                        ft.Text("Coverage Area", 
                                              size=28, 
                                              weight="w700",
                                              color=ft.Colors.BLUE_900),
                                        ft.Container(height=20),
                                        ft.Text(
                                            "Serving Hisar and surrounding areas within a 70km radius:\n\n"
                                            "• Residential Communities\n"
                                            "• Commercial Establishments\n"
                                            "• Agricultural Fields\n"
                                            "• Rural Area\n\n"
                                            "7 Days Service Available",
                                            size=18,
                                            color=ft.Colors.BLUE_900
                                        )
                                    ])
                                ),
                                ft.Container(
                                    expand=3,
                                    content=ft.Image(
                                        src="https://maps.geoapify.com/v1/staticmap?style=osm-bright-smooth&width=600&height=400&center=lonlat%3A75.7217%2C29.1492&zoom=10&marker=lonlat%3A75.7217%2C29.1492%3Btype%3Aawesome%3Bcolor%3A%23bb3f73%3Bsize%3Ax-large%3Bicon%3Astar&apiKey=52be50548b3f4d11a74c07c4820dd588",
                                        fit=ft.ImageFit.COVER,
                                        border_radius=ft.BorderRadius(bottom_right=15, top_right=15, top_left=15, bottom_left=15)
                                    )
                                )
                            ]
                        )
                    )
                )
            ])
        )

    def footer():
        return ft.Container(
            bgcolor=ft.Colors.BLUE_900,
            padding=ft.padding.symmetric(vertical=40, horizontal=80),  # Combined padding
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Contact Us", color=ft.Colors.WHITE, size=20, weight="w700"),
                        ft.Text("Hisar, Haryana 125001", color=ft.Colors.WHITE),
                        ft.Text("Email: runwaycleanup@gmail.com", color=ft.Colors.WHITE),
                        ft.Text("Phone: +91 99999 55555", color=ft.Colors.WHITE)
                    ], expand=True),
                    ft.VerticalDivider(color=ft.Colors.WHITE24),
                    ft.Column([
                        ft.Text("Quick Links", color=ft.Colors.WHITE, size=20, weight="w700"),
                        ft.TextButton("Home", on_click=go_home),
                        ft.TextButton("About Us", on_click=go_to_about),
                        ft.TextButton("Book Service", on_click=go_to_booking)
                    ], expand=True),
                    # ft.VerticalDivider(color=ft.Colors.WHITE24),
                ], spacing=40),
                ft.Divider(color=ft.Colors.WHITE24, height=40),
                ft.Row([
                    ft.Text("© 2024 RunWay Cleanup. All rights reserved.", 
                        color=ft.Colors.WHITE, 
                        size=14),
                    ft.Text("Privacy Policy | Terms of Service", 
                        color=ft.Colors.WHITE, 
                        size=14)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return ft.View(
        "/",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header(),
            greeting_section(),
            services_section(),
            map_section(),
            footer()
        ]
    )