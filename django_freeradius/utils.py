from django.contrib.auth import get_user_model


def find_available_username(username, users_list):
    User = get_user_model()
    suffix = 1
    tmp = username
    names_list = map(lambda x: x.username, users_list)
    while User.objects.filter(username=tmp).exists() or tmp in names_list:
        tmp = '{}{}'.format(username, suffix)
        suffix += 1
    return tmp
