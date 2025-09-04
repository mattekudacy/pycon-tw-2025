import flet as ft


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(
                    self.get_initials(message.user_name),
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
                radius=20,
            ),
            ft.Column(
                [
                    ft.Text(
                        message.user_name, 
                        weight=ft.FontWeight.BOLD,
                        color="#FF6B35",  # Taiwan sunset orange
                        size=14,
                    ),
                    ft.Container(
                        content=ft.Text(
                            message.text, 
                            selectable=True,
                            color=ft.Colors.WHITE,
                            size=13,
                        ),
                        bgcolor="#1A2332",  # Taiwan night blue
                        padding=10,
                        border_radius=8,
                        border=ft.border.all(1, "#E74C3C"),  # Taiwan red border
                    ),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "U"

    def get_avatar_color(self, user_name: str):
        # Taiwan-inspired colors
        colors_lookup = [
            "#E74C3C",  # Taiwan red
            "#FF6B35",  # Taiwan sunset orange
            "#2ECC71",  # Taiwan mountain green
            "#3498DB",  # Taiwan ocean blue
            "#F39C12",  # Taiwan temple gold
            "#9B59B6",  # Taiwan orchid purple
            "#E67E22",  # Taiwan persimmon orange
            "#1ABC9C",  # Taiwan jade green
            "#34495E",  # Taiwan slate grey
            "#E91E63",  # Taiwan bougainvillea pink
            "#16A085",  # Taiwan emerald
            "#C0392B",  # Taiwan deep red
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    # Taiwan-themed page setup
    page.title = "🇹🇼 PyCon Taiwan 2025 Chat"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D1B2A"  # Taiwan night sky
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    
    # Taiwan-inspired theme colors
    page.theme = ft.Theme(
        color_scheme_seed="#E74C3C",  # Taiwan red
        color_scheme=ft.ColorScheme(
            primary="#E74C3C",
            secondary="#FF6B35",
            surface="#1A2332",
            background="#0D1B2A",
        )
    )

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            welcome_dlg.open = False
            new_message.prefix = ft.Text(
                f"{join_user_name.value}: ", 
                color="#FF6B35",
                weight=ft.FontWeight.BOLD,
            )
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"🎉 {join_user_name.value} 加入了聊天室！Welcome to PyCon Taiwan! 🇹🇼",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Container(
                content=ft.Text(
                    message.text, 
                    italic=True, 
                    color="#FF6B35",
                    size=12,
                    text_align=ft.TextAlign.CENTER,
                ),
                bgcolor="#1A2332",
                padding=8,
                border_radius=15,
                margin=ft.margin.symmetric(horizontal=50),
                border=ft.border.all(1, "#E74C3C"),
            )
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Taiwan-themed dialog
    join_user_name = ft.TextField(
        label="請輸入您的名字加入 PyCon Taiwan 聊天室",
        autofocus=True,
        on_submit=join_chat_click,
        bgcolor="#1A2332",
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color="#FF6B35"),
        border_color="#E74C3C",
        focused_border_color="#FF6B35",
    )
    
    welcome_dlg = ft.AlertDialog(
        open=True,
        modal=True,
        bgcolor="#0D1B2A",
        title=ft.Text(
            "🇹🇼 歡迎來到 PyCon Taiwan 2025! Welcome! 🐍", 
            color="#FF6B35",
            weight=ft.FontWeight.BOLD,
        ),
        content=ft.Column([join_user_name], width=400, height=70, tight=True),
        actions=[
            ft.ElevatedButton(
                text="加入聊天室 Join Chat 🚀",
                on_click=join_chat_click,
                bgcolor="#E74C3C",
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(welcome_dlg)

    # Chat messages container with Python theme
    chat = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True,
        padding=15,
    )

    # Taiwan-themed message input
    new_message = ft.TextField(
        hint_text="在這裡輸入您的訊息... Type your message here... 💬",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
        bgcolor="#1A2332",
        color=ft.Colors.WHITE,
        hint_style=ft.TextStyle(color="#888888"),
        border_color="#E74C3C",
        focused_border_color="#FF6B35",
        border_radius=12,
    )

    # Taiwan-themed chat header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CHAT, color="#FF6B35", size=24),
            ft.Text(
                "🇹🇼 PyCon Taiwan 2025 即時聊天室 Live Chat 🐍",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#FF6B35",
            ),
            ft.Container(expand=True),
            ft.Icon(ft.Icons.PEOPLE, color="#E74C3C", size=20),
        ]),
        bgcolor="#1A2332",
        padding=15,
        border_radius=ft.border_radius.only(top_left=12, top_right=12),
        border=ft.border.all(1, "#E74C3C"),
    )

    # Add everything to the page with Taiwan theme
    page.add(
        ft.Column([
            header,
            ft.Container(
                content=chat,
                border=ft.border.only(
                    left=ft.BorderSide(1, "#E74C3C"),
                    right=ft.BorderSide(1, "#E74C3C"),
                    bottom=ft.BorderSide(1, "#E74C3C"),
                ),
                border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12),
                bgcolor="#0F1419",
                expand=True,
            ),
            ft.Container(
                content=ft.Row([
                    new_message,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=send_message_click,
                        bgcolor="#E74C3C",
                        icon_color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.CircleBorder(),
                        ),
                    ),
                ], spacing=10),
                padding=15,
                bgcolor="#1A2332",
                border_radius=12,
                margin=ft.margin.only(top=10),
            ),
        ], expand=True)
    )


ft.app(target=main)