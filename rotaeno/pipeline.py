def save_discord_username(backend, user, response, *args, **kwargs):
    if backend.name == 'discord':
        user.username = response.get('username', user.username)
        user.save()