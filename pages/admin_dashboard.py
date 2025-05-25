import datetime
import threading
import flet as ft
from utils.firebase import db
from pages.home import home_view    

def admin_dashboard_view(page: ft.Page):
    user = page.session.get("user")

    # Redirect if not logged in
    if not user:
        def delayed_redirect():
            import time
            time.sleep(1.5)
            page.go("/login")
        threading.Thread(target=delayed_redirect).start()
        return ft.View(
            "/admin",
            controls=[ft.Text("Redirecting to login...")],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    uid = user.get("uid")
    user_data = db.child("users").child(uid).get().val()

    # Redirect if not an admin
    if not user_data or user_data.get("role") != "admin":
        def delayed_redirect():
            import time
            time.sleep(1)
            page.go("/")
        threading.Thread(target=delayed_redirect).start()
        return ft.View(
            "/admin",
            controls=[ft.Text("Access denied. You are not an admin.")],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    header = home_view(page).controls[0]

    def get_booking_summary():
        data = db.child("bookings").get().val()
        total = 0
        pending = 0
        completed = 0
        cancelled = 0

        if data:
            for booking in data.values():
                total += 1
                status = booking.get("status")
                if status == "Pending":
                    pending += 1
                elif status == "Completed":
                    completed += 1
                elif status == "Cancelled":
                    cancelled += 1

        return total, pending, completed, cancelled

    def mark_booking_as_seen(booking_id):
        db.child("bookings").child(booking_id).update({"admin_seen": True})

    def build_booking_card(booking_id, data, status="N/A", index=None):
        timestamp = data.get("timestamp")
        time_str = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M') if timestamp else "N/A"
        admin_seen = data.get("admin_seen", True)
        admin_note = data.get("admin_note", "")

        status_color_map = {
            "Upcoming": {"text": ft.Colors.BLUE_900, "text_bg": ft.Colors.BLUE_100, "bg": ft.Colors.BLUE_50},
            "Pending": {"text": ft.Colors.AMBER_900, "text_bg": ft.Colors.AMBER_100, "bg": ft.Colors.AMBER_50},
            "Completed": {"text": ft.Colors.GREEN_900, "text_bg": ft.Colors.GREEN_100, "bg": ft.Colors.GREEN_50},
            "Cancelled": {"text": ft.Colors.RED_900, "text_bg": ft.Colors.RED_100, "bg": ft.Colors.RED_50},
            "N/A": {"text": ft.Colors.GREY_900, "text_bg": ft.Colors.GREY_100, "bg": ft.Colors.GREY_200}
        }
        colors = status_color_map.get(status, status_color_map["N/A"])
        border_color = ft.Colors.BLUE_400 if not admin_seen else colors["text"]

        note_input = ft.TextField(
            label="Internal Note",
            value=admin_note,
            multiline=True,
            max_lines=3,
            border_color=ft.Colors.GREY_400,
            content_padding=10,
            dense=True
        )

        def save_note(e):
            db.child("bookings").child(booking_id).update({"admin_note": note_input.value})
            page.update()

        action_buttons = []

        if status == "Upcoming":
            action_buttons = [
                ft.ElevatedButton("Accept", 
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600),
                    on_click=lambda e, bid=booking_id: update_status_directly(bid, "Pending")),
                ft.ElevatedButton("Reject", 
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
                    on_click=lambda e, bid=booking_id: update_status_directly(bid, "Cancelled"))
            ]
        elif status == "Pending":
            action_buttons = [
                ft.ElevatedButton("Mark Completed", 
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_600),
                    on_click=lambda e, bid=booking_id: update_status_directly(bid, "Completed")),
                ft.ElevatedButton("Cancel", 
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_600),
                    on_click=lambda e, bid=booking_id: update_status_directly(bid, "Cancelled"))
            ]

        return ft.Card(
            elevation=2,
            content=ft.Container(
                width=300,
                # height=200,
                padding=10,
                bgcolor=colors["bg"],
                border=ft.border.all(1, border_color),
                border_radius=10,
                content=ft.Column([

                    ft.Row([
                        ft.Text(f"#{index + 1}", weight="bold", color=colors["text"]),
                        ft.Text(f"Booking ID: {booking_id}", size=12, color=ft.Colors.GREY_600),
                    ], spacing=5),

                    ft.Container(
                        padding=ft.padding.symmetric(5, 10),
                        border_radius=5,
                        bgcolor=colors["text_bg"],
                        content=ft.Row([
                            ft.Icon(ft.Icons.CIRCLE, size=10, color=colors["text"]),
                            ft.Text(status, size=12, weight="bold", color=colors["text"])
                        ], spacing=5)
                    ),

                    ft.Divider(color=ft.Colors.GREY_300),
                    
                    ft.Column([
                        ft.Text(f"👤 {data.get('name')}", color=ft.Colors.BLACK87),
                        ft.Text(f"📞 {data.get('phone')}", color=ft.Colors.BLACK87),
                        ft.Text(f"📧 {data.get('email')}", color=ft.Colors.BLACK87),
                        ft.Text(f"🏠 {data.get('address')}", color=ft.Colors.BLACK87),
                        ft.Text(f"🔧 {data.get('service')}", color=ft.Colors.BLACK87),
                        ft.Text(f"🗓️ {time_str}", color=ft.Colors.BLACK87),
                    ], spacing=5),

                    ft.Divider(color=ft.Colors.GREY_300),
                    
                    ft.Text("Admin Notes:", size=12, color=ft.Colors.GREY_600),
                    note_input,
                    
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.ElevatedButton(
                                "Save Note",
                                icon=ft.Icons.SAVE,
                                # border_radius = 10,
                                style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_600),
                                on_click=save_note
                        ),

                    ),

                    ft.Row(
                        action_buttons, 
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ) if action_buttons else ft.Container()
                ], spacing=10)
            )
        )

    def update_status_directly(booking_id, new_status):
        db.child("bookings").child(booking_id).update({"status": new_status})
        page.update()
        page.views[-1] = admin_dashboard_view(page)
        page.update()

    # Search Components
    search_results_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.85,
        spacing=15,
        run_spacing=15,
        height=800,
        auto_scroll=True
    )

    def update_bookings():
        query = search_query.value.lower()
        all_data = db.child("bookings").get().val()
        filtered = []

        if all_data:
            for key, data in all_data.items():
                if any(query in str(data.get(field, "")).lower() for field in ["name", "phone", "email", "service"]):
                    filtered.append((key, data))

        search_results_grid.controls.clear()
        for i, (booking_id, data) in enumerate(filtered):
            search_results_grid.controls.append(
                build_booking_card(booking_id, data, data.get("status", "N/A"), index=i)
            )
        page.update()

    search_query = ft.TextField(
        label="Search bookings...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=20,
        border_color=ft.Colors.GREY_400,
        filled=True,
        bgcolor=ft.Colors.GREY_50,
        on_change=lambda e: update_bookings(),
        expand=True
    )

    # Date Filter Components
    date_filtered_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=350,
        child_aspect_ratio=0.85,
        spacing=15,
        run_spacing=15,
        height=800,
        auto_scroll=True
    )

    def update_bookings_by_date(e):
        selected_date = date_picker.value
        if selected_date is None:
            return

        selected_day = selected_date.day
        selected_month = selected_date.month
        selected_year = selected_date.year

        all_data = db.child("bookings").get().val()
        filtered = []

        if all_data:
            for key, data in all_data.items():
                timestamp = data.get("timestamp")
                if timestamp:
                    dt = datetime.datetime.fromtimestamp(timestamp)
                    if dt.day == selected_day and dt.month == selected_month and dt.year == selected_year:
                        filtered.append((key, data))

        date_filtered_grid.controls.clear()
        for i, (booking_id, data) in enumerate(filtered):
            date_filtered_grid.controls.append(
                build_booking_card(booking_id, data, data.get("status", "N/A"), index=i)  # Fixed closing parenthesis
            )
        page.update()

    date_picker = ft.DatePicker(
        on_change=update_bookings_by_date,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime(2100, 12, 31),
    )

    page.overlay.append(date_picker)

    pick_date_button = ft.ElevatedButton(
        text="Filter by Date",
        icon=ft.Icons.CALENDAR_MONTH,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_50,
            color=ft.Colors.BLUE_800
        ),
        on_click=lambda e: page.open(date_picker)
    )

    # Status Tabs
    tabs = ["Upcoming", "Pending", "Completed", "Cancelled"]

    def fetch_bookings_by_status(status):
        bookings_data = db.child("bookings").get().val()
        filtered = []
        if bookings_data:
            for key, data in bookings_data.items():
                if data.get("status") == status:
                    filtered.append((key, data))
                    if not data.get("admin_seen", False):
                        mark_booking_as_seen(key)
        filtered.sort(key=lambda item: item[1].get("timestamp", 0), reverse=True)
        return filtered

    tab_views = {}
    for tab in tabs:
        bookings = fetch_bookings_by_status(tab)
        cards = [build_booking_card(bid, data, tab, index=i) for i, (bid, data) in enumerate(bookings)]
        tab_views[tab] = ft.GridView(
            controls=cards,
            expand=True,
            runs_count=3,
            max_extent=350,
            child_aspect_ratio=0.65,
            spacing=15,
            run_spacing=15,
            # height=600  # Added fixed height
        )

    tabs_control = ft.Tabs(
        selected_index=0,
        tabs=[ft.Tab(
            text=tab,
            content=ft.Container(padding=10, content=tab_views[tab], height=600)  # Added fixed height
        ) for tab in tabs],
        expand=1,
        indicator_color=ft.Colors.BLUE_600,
        label_color=ft.Colors.BLUE_600,
        unselected_label_color=ft.Colors.GREY_600,
        scrollable=True  # Enable tab scrolling
    )

    total, pending, completed, cancelled = get_booking_summary()

    summary_cards = [
        ft.Container(
            ft.Column([
                ft.Text("Total Bookings", size=14, color=ft.Colors.BLUE_800),
                ft.Text(str(total), size=24, weight="bold", color=ft.Colors.BLUE_800)
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            expand=True
        ),
        ft.Container(
            ft.Column([
                ft.Text("Pending", size=14, color=ft.Colors.AMBER_800),
                ft.Text(str(pending), size=24, weight="bold", color=ft.Colors.AMBER_800)
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.AMBER_50,
            border_radius=10,
            expand=True
        ),
        ft.Container(
            ft.Column([
                ft.Text("Completed", size=14, color=ft.Colors.GREEN_800),
                ft.Text(str(completed), size=24, weight="bold", color=ft.Colors.GREEN_800)
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=10,
            expand=True
        ),
        ft.Container(
            ft.Column([
                ft.Text("Cancelled", size=14, color=ft.Colors.RED_800),
                ft.Text(str(cancelled), size=24, weight="bold", color=ft.Colors.RED_800)
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.RED_50,
            border_radius=10,
            expand=True
        )
    ]

        # Add logout functionality
    def logout(e):
        page.session.remove("user")
        page.go("/login")



    header_content = ft.Container(
        ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(f"Welcome, {user_data.get('name', 'Admin')}", 
                           size=24, weight="bold"),
                    ft.Text("Booking Management Dashboard", 
                           color=ft.Colors.GREY_600)
                ], expand=True),
                ft.Row([
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=40, color=ft.Colors.BLUE_600),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        icon_color=ft.Colors.RED_600,
                        tooltip="Logout",
                        on_click=logout,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, ft.Colors.RED_300),
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                ], spacing=20)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Text("📊 Quick Stats", size=16, weight="bold"),
            ft.Row(summary_cards, spacing=15),
            
            ft.Divider(height=20),
            
            ft.Text("📑 Bookings by Status", size=16, weight="bold"),
            ft.Container(
                tabs_control,
                height=600
            ),
            
            ft.Divider(height=20),
            
            ft.Row([
                search_query,
                pick_date_button
            ], spacing=15),
            
            ft.Container(
                ft.Tabs([
                    ft.Tab(
                        text="Search Results",
                        content=ft.Container(
                            content=search_results_grid,
                            height=400
                        )
                    ),
                    ft.Tab(
                        text="Date Filter Results",
                        content=ft.Container(
                            content=date_filtered_grid,
                            height=400
                        )
                    )
                ]),
                height=450
            ),
        ], spacing=20, expand=True),
        padding=ft.padding.symmetric(horizontal=30, vertical=20),
        expand=True
    )



    return ft.View(
        route="/admin",
        controls=[
            header,
            header_content,
            # footer
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0
    )
