import random
from account.models import UserAccountActivationKey


def get_random_key(size):
    alphabets = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    key = ''
    for _ in range(size):
        key += random.choice(alphabets)
    return key


def get_base_url(request):
    return "".join([f'{request.scheme}://', f'{request.get_host()}/'])  # http://127.0.0.1:8000/


def send_account_activation_mail(request, user):
    key = get_random_key(50)
    base_url = get_base_url(request)
    full_url = "".join([base_url, "account/activate/", f'{user.username.hex}/', f'{key}/']) # http://127.0.0.1:8000/account/activate/40b6baae27ee42df898693d1582f3be2/hfdshfhdsfjdsdhsfgdshfdsjds/
    subject = "User Account Activation"
    message = f"""
    Hello {user.get_full_name()}. Please click on this link to activate your account 
    {full_url}
    """
    from_email = "nexusadmin@noreply.com"
    user.email_user(subject=subject, message=message, from_email=from_email)
    UserAccountActivationKey.objects.create(user=user, key=key)
