def get_url_profile(name):
    name_parts = name.split(' ')
    first_name = name_parts[0]
    last_name = None

    if len(name_parts) > 1:
        last_name = name_parts[1]

    if last_name:
        return f'https://ui-avatars.com/api/?name={first_name}+{last_name}&background=27272A&color=fff&format=png&font-size=0.5'
    return f'https://ui-avatars.com/api/?name={first_name}&background=27272A&color=fff&format=png&font-size=0.5'
