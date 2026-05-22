from app.modules.notifications.config import NotificationsSettings


def test_notify_chat_ids_accepts_single_numeric_env_value() -> None:
    settings = NotificationsSettings(NOTIFY_CHAT_IDS=5828326482)

    assert settings.notify_chat_ids == [5828326482]


def test_notify_chat_ids_accepts_comma_separated_env_value() -> None:
    settings = NotificationsSettings(NOTIFY_CHAT_IDS="5828326482,-1001234567890")

    assert settings.notify_chat_ids == [5828326482, -1001234567890]


def test_notify_chat_ids_accepts_list_value() -> None:
    settings = NotificationsSettings(NOTIFY_CHAT_IDS=["5828326482", -1001234567890])

    assert settings.notify_chat_ids == [5828326482, -1001234567890]
