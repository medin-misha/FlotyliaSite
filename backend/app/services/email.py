import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings

logger = logging.getLogger(__name__)


def _send_email_sync(to_email: str, subject: str, html_content: str) -> None:
    """Синхронная отправка почты через SMTP сервер."""
    smtp_config = settings.smtp
    if not smtp_config.host or not smtp_config.user:
        logger.warning("SMTP-сервер не настроен в конфигурации. Отправка письма отменена.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_config.sender or smtp_config.user
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        if smtp_config.use_ssl:
            with smtplib.SMTP_SSL(smtp_config.host, smtp_config.port, timeout=10) as server:
                server.login(smtp_config.user, smtp_config.password)
                server.sendmail(smtp_config.sender or smtp_config.user, to_email, msg.as_string())
        else:
            with smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=10) as server:
                if smtp_config.port == 587:
                    server.starttls()
                server.login(smtp_config.user, smtp_config.password)
                server.sendmail(smtp_config.sender or smtp_config.user, to_email, msg.as_string())
        logger.info(f"Письмо успешно отправлено на {to_email}")
    except Exception as exc:
        logger.error(f"Ошибка при отправке письма на {to_email}: {exc}", exc_info=True)


async def send_activation_email(to_email: str, name: str) -> None:
    """Асинхронная отправка письма с уведомлением об одобрении заявки."""
    subject = "Команда MFS приняла вашу заявку"
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eef2f5;">
          <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: #d32f2f; margin: 0; font-size: 24px; font-weight: 700;">Статус заявки: Принята</h2>
          </div>
          
          <p style="font-size: 16px; margin-top: 0;">Здравствуйте, <strong>{name}</strong>!</p>
          
          <p style="font-size: 15px;">Команда MFS приняла вашу заявку.</p>
          
          <div style="text-align: center; margin: 30px 0;">
            <a href="https://t.me/MFS_support" target="_blank" style="background-color: #e53935; color: #ffffff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 15px; display: inline-block; transition: background-color 0.2s;">
              Связаться с поддержкой @MFS_support
            </a>
          </div>
          
          <hr style="border: none; border-top: 1px solid #eef2f5; margin: 25px 0;">
          
          <p style="font-size: 12px; color: #888888; text-align: center; margin: 0;">
            Это автоматическое сообщение. Пожалуйста, не отвечайте на него.<br>
            © MFS 2026. Все права защищены.
          </p>
        </div>
      </body>
    </html>
    """

    await asyncio.to_thread(_send_email_sync, to_email, subject, html_content)
