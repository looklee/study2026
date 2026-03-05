# 邮件通知服务

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
from jinja2 import Template
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """邮件服务"""
    
    def __init__(
        self,
        smtp_server: str = None,
        smtp_port: int = None,
        username: str = None,
        password: str = None,
        use_tls: bool = True
    ):
        self.smtp_server = smtp_server or settings.SMTP_SERVER
        self.smtp_port = smtp_port or settings.SMTP_PORT
        self.username = username or settings.SMTP_USERNAME
        self.password = password or settings.SMTP_PASSWORD
        self.use_tls = use_tls
        self.from_email = settings.SMTP_FROM_EMAIL or self.username
        self.from_name = settings.SMTP_FROM_NAME or "Study2026"
    
    def create_message(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str = None,
        text_content: str = None,
        attachments: List[str] = None
    ) -> MIMEMultipart:
        """创建邮件消息"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = ", ".join(to_emails)
        
        # 添加文本内容
        if text_content:
            part = MIMEText(text_content, "plain", "utf-8")
            msg.attach(part)
        
        # 添加 HTML 内容
        if html_content:
            part = MIMEText(html_content, "html", "utf-8")
            msg.attach(part)
        
        # 添加附件
        if attachments:
            for file_path in attachments:
                try:
                    with open(file_path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        
                        filename = Path(file_path).name
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={filename}"
                        )
                        msg.attach(part)
                except Exception as e:
                    logger.error(f"添加附件失败：{file_path}, 错误：{e}")
        
        return msg
    
    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str = None,
        text_content: str = None,
        attachments: List[str] = None
    ) -> bool:
        """发送邮件"""
        try:
            msg = self.create_message(
                to_emails, subject, html_content, text_content, attachments
            )
            
            # 连接 SMTP 服务器
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            
            server.login(self.username, self.password)
            server.sendmail(self.from_email, to_emails, msg.as_string())
            server.quit()
            
            logger.info(f"邮件发送成功：{subject} -> {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"邮件发送失败：{subject}, 错误：{e}")
            return False
    
    def send_template_email(
        self,
        to_emails: List[str],
        subject: str,
        template_path: str,
        context: Dict[str, Any] = None
    ) -> bool:
        """使用模板发送邮件"""
        try:
            template = Template(Path(template_path).read_text(encoding="utf-8"))
            html_content = template.render(context or {})
            
            return self.send_email(to_emails, subject, html_content=html_content)
        except Exception as e:
            logger.error(f"模板邮件发送失败：{e}")
            return False


# 预定义邮件模板
WELCOME_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 30px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 欢迎加入 Study2026!</h1>
        </div>
        <div class="content">
            <p>亲爱的 {{ username }}，</p>
            <p>欢迎加入 Study2026 AI 学习平台！从现在开始，你将拥有一个智能学习伴侣，帮助你更高效地学习。</p>
            <p>你的账户已经创建成功，现在可以开始：</p>
            <ul>
                <li>📚 创建个性化学习路径</li>
                <li>🤖 与 AI 助手对话学习</li>
                <li>🎮 培养你的学习宠物</li>
                <li>📊 追踪学习进度</li>
            </ul>
            <a href="{{ login_url }}" class="button">立即开始学习</a>
            <p style="margin-top: 30px;">如果你有任何问题，随时联系我们的支持团队。</p>
            <p>祝你学习愉快！<br>Study2026 团队</p>
        </div>
        <div class="footer">
            <p>© 2026 Study2026. All rights reserved.</p>
            <p>这封邮件发送至 {{ email }}</p>
        </div>
    </div>
</body>
</html>
"""

CHECKIN_REMINDER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .streak { font-size: 48px; text-align: center; margin: 20px 0; }
        .button { display: inline-block; padding: 12px 30px; background: #f5576c; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔔 每日签到提醒</h1>
        </div>
        <div class="content">
            <p>亲爱的 {{ username }}，</p>
            <p>新的一天开始了，别忘了来签到哦！</p>
            <div class="streak">🔥 {{ streak }}天</div>
            <p style="text-align: center;">当前连续签到天数</p>
            {% if streak >= 7 %}
            <p style="text-align: center; color: #f5576c;">💪 太棒了！继续保持，你已经养成学习习惯了！</p>
            {% else %}
            <p style="text-align: center;">坚持{{ 7 - streak }}天就能获得「周勤学者」徽章！加油！</p>
            {% endif %}
            <div style="text-align: center;">
                <a href="{{ checkin_url }}" class="button">立即签到</a>
            </div>
        </div>
    </div>
</body>
</html>
"""


# 全局实例
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """获取邮件服务实例"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


# 便捷函数
async def send_welcome_email(user_email: str, username: str, login_url: str = "#"):
    """发送欢迎邮件"""
    service = get_email_service()
    
    html_content = WELCOME_EMAIL_TEMPLATE
    from jinja2 import Template
    template = Template(html_content)
    html = template.render({
        "username": username,
        "email": user_email,
        "login_url": login_url
    })
    
    return service.send_email(
        to_emails=[user_email],
        subject="🎉 欢迎加入 Study2026!",
        html_content=html
    )


async def send_checkin_reminder(user_email: str, username: str, streak: int, checkin_url: str = "#"):
    """发送签到提醒邮件"""
    service = get_email_service()
    
    template = Template(CHECKIN_REMINDER_TEMPLATE)
    html = template.render({
        "username": username,
        "streak": streak,
        "checkin_url": checkin_url
    })
    
    return service.send_email(
        to_emails=[user_email],
        subject="🔔 每日签到提醒 - 别让你的连续记录中断!",
        html_content=html
    )
