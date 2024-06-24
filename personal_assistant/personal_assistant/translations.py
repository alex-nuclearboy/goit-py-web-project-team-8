# translations.py

translations = {
    'password_too_short': {
        'en': "This password is too short. It must contain at least 8 characters.",
        'uk': "Цей пароль занадто короткий. Він повинен містити принаймні 8 символів.",
    },
    'password_too_common': {
        'en': "This password is too common.",
        'uk': "Цей пароль занадто поширений.",
    },
    'password_entirely_numeric': {
        'en': "This password is entirely numeric.",
        'uk': "Цей пароль складається лише з цифр.",
    },
    'password_mismatch': {
        'en': "The two password fields didn’t match.",
        'uk': "Два поля паролю не співпадають.",
    },
    'username_or_password_didnt_match': {
        'en': "Username or password didn't match",
        'uk': "Ім'я користувача або пароль не співпадають",
    },
    'logout_success': {
        'en': "You have been logged out successfully",
        'uk': "Ви успішно вийшли з системи",
    },
    'profile_update_success': {
        'en': "Your profile is updated successfully",
        'uk': "Ваш профіль успішно оновлено",
    },
    'password_reset_no_account': {
        'en': "No account found with the specified email address.",
        'uk': "Не знайдено обліковий запис з вказаною адресою електронної пошти.",
    },
    'email_send_error': {
        'en': "An error occurred while sending the email. Please try again later.",
        'uk': "Сталася помилка при відправці електронної пошти. Спробуйте пізніше.",
    },
    'smtp_error': {
        'en': "SMTP error occurred. Please try again later.",
        'uk': "Сталася SMTP помилка. Спробуйте пізніше.",
    },
    'password_reset_complete': {
        'en': "Your password has been set. You may go ahead and log in now.",
        'uk': "Ваш пароль було встановлено. Тепер ви можете увійти.",
    },
    'password_reset_done': {
        'en': "Password reset email sent",
        'uk': "Лист для скидання паролю відправлено",
    },
    'password_reset_email_sent': {
        'en': "We've emailed you with instructions on how to reset your password.",
        'uk': "Ми надіслали вам інструкції щодо скидання пароля на електронну пошту.",
    }
}

def get_translation(key, language):
    return translations.get(key, {}).get(language, key)
