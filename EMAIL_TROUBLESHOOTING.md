# 📧 Email Troubleshooting Guide for BugHunter

## Common Email Issues and Solutions

### 1. Emails Not Sending on Live Website

#### Symptoms:
- Users not receiving verification emails
- No analysis notification emails
- Email functions return False

#### Possible Causes & Solutions:

**A. Missing Environment Variables**
```bash
# Check your production .env file has all required variables:
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**B. Gmail App Password Issues**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Use the 16-character app password (not your regular password)
4. Remove spaces from app password

**C. Production vs Development Settings**
- Ensure `DEBUG=False` in production
- Check `ALLOWED_HOSTS` includes your domain
- Verify email backend is set to SMTP in production

### 2. Testing Email Configuration

Run the email test script:
```bash
python test_email.py
```

### 3. Gmail SMTP Settings

**Correct Gmail SMTP Configuration:**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

**Alternative (SSL):**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

### 4. Firewall and Network Issues

**Check if your hosting provider blocks SMTP:**
- Some hosting providers block port 587/465
- Contact your hosting provider
- Consider using their SMTP service instead

### 5. Email Provider Alternatives

**If Gmail doesn't work, try:**

**SendGrid:**
```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-mailgun-username
EMAIL_HOST_PASSWORD=your-mailgun-password
```

### 6. Debugging Steps

**1. Check Logs:**
```bash
# Check application logs
tail -f logs/bughunter.log

# Check server logs (if applicable)
tail -f /var/log/nginx/error.log
```

**2. Test SMTP Connection:**
```python
import smtplib
from email.mime.text import MIMEText

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-app-password')
    print("✅ SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"❌ SMTP connection failed: {e}")
```

**3. Django Shell Test:**
```python
python manage.py shell

from django.core.mail import send_mail
from django.conf import settings

# Test basic email
send_mail(
    'Test Subject',
    'Test message',
    settings.DEFAULT_FROM_EMAIL,
    ['test@example.com'],
    fail_silently=False
)
```

### 7. Production Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set all email environment variables
- [ ] Use Gmail App Password (not regular password)
- [ ] Test email sending with `test_email.py`
- [ ] Check hosting provider SMTP restrictions
- [ ] Verify domain/DNS settings (if using custom domain)
- [ ] Test from production environment

### 8. Security Considerations

**Never commit sensitive data:**
```bash
# Add to .gitignore
.env
.env.production
*.log
```

**Use environment variables:**
```python
# ❌ Don't do this
EMAIL_HOST_PASSWORD = 'hardcoded-password'

# ✅ Do this
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### 9. Alternative Email Backends

**For development/testing:**
```python
# Console backend (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# File backend (saves to file)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'
```

### 10. Contact Support

If issues persist:
1. Run `python test_email.py` and share output
2. Check logs in `logs/bughunter.log`
3. Verify all environment variables are set
4. Test SMTP connection manually
5. Contact hosting provider about SMTP restrictions

---

## Quick Fix Commands

```bash
# Test email configuration
python test_email.py

# Check Django settings
python manage.py shell -c "from django.conf import settings; print(f'Email Host: {settings.EMAIL_HOST}'); print(f'Email User: {settings.EMAIL_HOST_USER}')"

# Test SMTP connection
python -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('SMTP OK')"
```