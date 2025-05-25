import requests
import re
import time
import flet as ft
from utils.firebase import db
from pages.home import home_view

def book_form_view(page):
    # Define a reusable dialog object
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[],
    )
    page.dialog = dialog

    page.overlay.append(dialog)
    page.update()



    def show_dialog(title_text, message_text):
        dialog.title = ft.Text(title_text)
        dialog.content = ft.Text(message_text)
        dialog.actions = [
            ft.TextButton("OK", on_click=lambda e: close_dialog())
        ]
        dialog.open = True
        page.update()

    def close_dialog():
        dialog.open = False
        page.update()



    # Form Fields with Modern Styling
    def create_field(label, icon, **kwargs):
        return ft.Container(
            width=400,
            height=65,
            content=ft.TextField(
                label=label,
                prefix_icon=icon,
                border_color=ft.Colors.GREY_400,
                focused_border_color=ft.Colors.BLUE_600,
                border_radius=8,
                label_style=ft.TextStyle(color=ft.Colors.GREY_700),
                **kwargs
            )
        )

    name = create_field("Name", ft.Icons.PERSON_OUTLINE)
    phone = create_field("Mobile Number", ft.Icons.PHONE_ANDROID)
    email = create_field("Email (optional)", ft.Icons.EMAIL_OUTLINED)
    address = create_field("Address", ft.Icons.LOCATION_ON_OUTLINED)
    
    service = ft.Container(
        width=400,
        content=ft.Dropdown(
            label="Service",
            options=[
                ft.dropdown.Option("Septic Tank Cleanup"),
                ft.dropdown.Option("Pest Control"),
                ft.dropdown.Option("Rent Tractors"),
            ],
            prefix_icon=ft.Icons.BUILD_CIRCLE_OUTLINED,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE_600,
            border_radius=8,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700)
        )
    )

    remarks = ft.Container(
        width=400,
        content=ft.TextField(
            label="Remarks",
            prefix_icon=ft.Icons.COMMENT_BANK_OUTLINED,
            multiline=True,
            min_lines=3,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE_600,
            border_radius=8,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700)
        )
    )

    # Submit Logic (unchanged except for visual updates)
    def submit_booking(e):
        # --- Validation ---
        if not name.content.value.strip():
            show_dialog("Validation Error", "Please enter your name.")
            return

        if not phone.content.value.strip():
            show_dialog("Validation Error", "Please enter your mobile number.")
            return
        elif not phone.content.value.isdigit() or len(phone.content.value) != 10:
            show_dialog("Validation Error", "Mobile number must be exactly 10 digits.")
            return

        if email.content.value.strip():
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, email.content.value.strip()):
                show_dialog("Validation Error", "Please enter a valid email address.")
                return

        if not address.content.value.strip():
            show_dialog("Validation Error", "Please enter your address.")
            return

        if not service.content.value:
            show_dialog("Validation Error", "Please select a service.")
            return

        # ------------------ Proceed if validated ------------------

        GEOAPIFY_API_KEY = "52be50548b3f4d11a74c07c4820dd588"
        hisar_lat, hisar_lon = 29.1492, 75.7217

        user_address = address.content.value
        print("User address:", user_address)

        geocode_url = f"https://api.geoapify.com/v1/geocode/search?text={user_address}&apiKey={GEOAPIFY_API_KEY}"
        geocode_resp = requests.get(geocode_url)
        print("Geocode status:", geocode_resp.status_code, geocode_resp.text)

        if geocode_resp.status_code != 200:
            snack_bar.content.value = "Error geocoding the address."
            snack_bar.open = True
            page.update()
            return

        geocode_data = geocode_resp.json()
        if not geocode_data['features']:
            snack_bar.content.value = "Invalid address. Please enter a valid one."
            snack_bar.open = True
            page.update()
            return

        user_coords = geocode_data['features'][0]['geometry']['coordinates']
        user_lon, user_lat = user_coords[0], user_coords[1]

        routing_url = f"https://api.geoapify.com/v1/routing?waypoints={hisar_lat},{hisar_lon}|{user_lat},{user_lon}&mode=drive&apiKey={GEOAPIFY_API_KEY}"

        routing_resp = requests.get(routing_url)
        print("Routing status:", routing_resp.status_code, routing_resp.text)

        if routing_resp.status_code != 200:
            snack_bar.content.value = "Error calculating distance."
            snack_bar.open = True
            page.update()
            return

        routing_data = routing_resp.json()

        if 'features' not in routing_data or not routing_data['features']:
            snack_bar.content.value = "Couldn't calculate distance between addresses."
            snack_bar.open = True
            page.update()
            return

        distance_meters = routing_data['features'][0]['properties']['distance']
        distance_km = distance_meters / 1000

        print("Distance in km:", distance_km)

        if distance_km > 70:
            show_dialog("Service Area Limit", "Service available only within 70 km of Hisar.")
            return

        data = {
            "name": name.content.value,
            "phone": phone.content.value,
            "email": email.content.value,
            "address": address.content.value,
            "service": service.content.value,
            "remarks": remarks.content.value,
            "status": "Upcoming",
            "timestamp": time.time(),
            "admin_seen": False,
            "distance_km": round(distance_km, 2)
        }

        db.child("bookings").push(data)
        show_dialog("Success", "Booking submitted successfully!")


    # Header & Footer from Home
    header = home_view(page).controls[0]
    footer = home_view(page).controls[-1]

    snack_bar = ft.SnackBar(content=ft.Text(""), duration=3000)
    page.overlay.append(snack_bar)
    page.update()  # Ensure the overlay gets rendered

    # Main View with Modern UI
    return ft.View(
        "/book",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.BLUE_50, ft.Colors.WHITE]
                ),
                content=ft.Stack(
                    controls=[
                        ft.Container(
                        # Background image
                            expand=True,
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                src="admin.jpg",
                                opacity=0.08,
                                fit=ft.ImageFit.COVER,
                                expand = True,
                                width= 800,
                                height=650
                        ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=40,
                            content=ft.Card(
                                elevation=20,
                                color=ft.Colors.WHITE,
                                surface_tint_color=ft.Colors.WHITE,
                                content=ft.Container(
                                    width=600,
                                    padding=40,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("Book Service", 
                                                   size=32, 
                                                   weight="w900",
                                                   color=ft.Colors.BLUE_900),
                                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                            ft.Text("Complete the form below and our team will contact you",
                                                   size=18,
                                                   color=ft.Colors.GREY_700),
                                            ft.Container(height=30),
                                            ft.Column(
                                                controls=[
                                                    name,
                                                    phone,
                                                    email,
                                                    address,
                                                    service,
                                                    remarks,
                                                    ft.Container(height=20),
                                                    ft.FilledButton(
                                                        "Submit Booking",
                                                        icon=ft.Icons.SEND_OUTLINED,
                                                        on_click=submit_booking,
                                                        style=ft.ButtonStyle(
                                                            bgcolor=ft.Colors.BLUE_900,
                                                            color=ft.Colors.WHITE,
                                                            padding=20,
                                                            shape=ft.RoundedRectangleBorder(radius=8),
                                                        ),
                                                        height=50,
                                                        width=200
                                                    )
                                                ],
                                                spacing=15
                                            )
                                        ]
                                    )
                                )
                            )
                        )
                    ]
                )
            ),
            footer
        ]
    )