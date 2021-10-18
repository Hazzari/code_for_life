"""Простой скрипт отправки письма на заданную почту"""
import smtplib
from email.mime.text import MIMEText

from environs import Env

env = Env()
env.read_env()

from utils import Message


def send_email(*, to, subject, message):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = env.str('FROM')
    msg['To'] = to

    server = smtplib.SMTP_SSL(env.str('SERVER'))
    # server.set_debuglevel(1)
    server.login(env.str('LOGIN'), env.str('PASSWORD'))
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    send_email(
        to=Message.email,
        subject=Message.subject,
        message=Message.message)
