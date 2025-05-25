import flet as ft
from pages.home import home_view

def about_view(page):
    # Reuse header & footer from home
    header = home_view(page).controls[0]
    footer = home_view(page).controls[-1]

    # Enhanced About Text Section
    about_text = ft.Column(
        spacing=25,
        controls=[
            ft.Text("About RunWay Cleanup", 
                   size=36, 
                   weight="w900", 
                   color=ft.Colors.BLUE_900),
            ft.Divider(height=10, color=ft.Colors.BLUE_200),
            ft.Text("We are a local business that provides powerful cleaning services in and around Hisar, Haryana. Our main job is to help homes, farms, and businesses with daily cleaning problems as well as big issues like blocked or full septic tanks.",
                   size=20,
                   weight="w600"),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCAL_SHIPPING, color=ft.Colors.BLUE_400),
                title=ft.Text("Septic Tank Experts", weight="w600"),
                subtitle=ft.Text("Fast, skilled team ready to handle blockages and plumbing issues"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CLEANING_SERVICES, color=ft.Colors.BLUE_400),
                title=ft.Text("Modern Equipment", weight="w600"),
                subtitle=ft.Text("Two large tractor-tankers and trained workers for efficient service"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.BLUE_400),
                title=ft.Text("Service Coverage", weight="w600"),
                subtitle=ft.Text("70km radius from Hisar including towns, villages, and farms. If you live in or around Hisar or Rohnat, we can reach you easily."),
            ),
            ft.Container(
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50,
                content=ft.Column([
                    ft.Text("Contact Information", size=18, weight="w600"),
                    ft.Row([
                        ft.Icon(ft.Icons.EMAIL, size=18),
                        ft.Text("runwaycleanup@gmail.com", size=16)
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=18),
                        ft.Text("Hisar and Rohnat, Haryana", size=16)
                    ], spacing=10)
                ], spacing=10)
            )
        ]
    )

    # Enhanced Team Section
    team = [
        {
            "name": "Ravi Kataria",
            "role": "Operations Manager",
            "bio": "Leads customer service and daily operations with a focus on customer satisfaction. He is hardworking and always ready to solve problems. He manages the team like a leader and ensures every customer is happy with our work.",
            "img": "rahul.jpg"
        },
        {
            "name": "Satpal Kataria",
            "role": "Equipment Manager", 
            "bio": "Maintains and operates our fleet of cleaning equipment and vehicles. His deep knowledge of farm equipment helps us complete our jobs on time. He also supports in transport and field work.",
            "img": "rahul.jpg"
        },
        {
            "name": "Rahul Kataria",
            "role": "Technology Lead",
            "bio": "Develops and maintains digital systems for seamless service management. He built our website and manages the software we use. Rahul also plans for future technology upgrades to make the service faster and better.",
            "img": "rahul.jpg"
        }
    ]

    team_cards = ft.ResponsiveRow(
        spacing=30,
        run_spacing=30,
        controls=[
            ft.Container(
                col={"sm": 12, "md": 6, "xl": 4},
                content=ft.Card(
                    elevation=8,
                    content=ft.Container(
                        width=350,
                        padding=20,
                        content=ft.Column([
                            ft.Container(
                                height=300,
                                border_radius=10,
                                content=ft.Image(
                                    src=member["img"],
                                    fit=ft.ImageFit.COVER,
                                    width=300,
                                    height=300
                                )
                            ),
                            ft.Container(height=15),
                            ft.Text(member["name"], 
                                  size=22, 
                                  weight="w700",
                                  color=ft.Colors.BLUE_900),
                            ft.Text(member["role"], 
                                  size=16, 
                                  color=ft.Colors.BLUE_600),
                            ft.Divider(height=15),
                            ft.Text(member["bio"], 
                                  size=15,
                                  color=ft.Colors.GREY_700)
                        ], spacing=5)
                    )
                )
            ) for member in team
        ]
    )

    # Main Content Container
    main_content = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=1200,
                    padding=40,
                    content=ft.Column([
                        about_text,
                        ft.Divider(height=40),
                        ft.Text("Our Team", 
                              size=36, 
                              weight="w900",
                              color=ft.Colors.BLUE_900,
                              text_align="center"),
                        team_cards
                    ], spacing=40)
                )
            ]
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.WHITE, ft.Colors.BLUE_50]
        )
    )

    # Hidden Admin Button (unchanged)
    hidden_admin_btn = ft.TextButton(
        "Admin Dashboard",
        on_click=lambda e: page.go("/admin"),
        style=ft.ButtonStyle(
            color=ft.Colors.TRANSPARENT,
            overlay_color=ft.Colors.TRANSPARENT,
            padding=0,
            shape=None
        ),
        height=20, 
        width=20
    )
    page.overlay.append(hidden_admin_btn)

    return ft.View(
        "/about",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            main_content,
            footer
        ]
    )
