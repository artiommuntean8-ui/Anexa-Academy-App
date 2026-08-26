from plyer import notification

def show_toast(title: str, message: str):
    """Afișează o notificare nativă pe Windows."""
    notification.notify(
        title=title,
        message=message,
        app_name="Academia ArkiTech",
        timeout=5,  # secunde
    )
