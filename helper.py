def get_category_color(category:str):
    COLORS = {'Sports': 'green', 'Tutorial': 'blue', 'Youtube': 'red', 'Learning': 'yellow', 'Study': 'cyan'}

    if category in COLORS:
        return COLORS[category]
    else:
        return 'white'