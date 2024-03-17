from consts import *


def load_sources():
    ball_img = {}
    for color in COLORS:
        source_burst_img = ["src", f"{color}.png"]
        source = os.path.join(*source_burst_img)
        image = pygame.image.load(source).convert_alpha()
        ball_img[color] = image

    burst_img = []
    for i in range(8):
        source_burst_img = ["src", "burst", f"burst{i}.png"]
        source = os.path.join(*source_burst_img)
        image = pygame.image.load(source).convert_alpha()
        burst_img.append(image)

    sounds = ["shut", "explosion", "touch"]
    sounds_wav = {}
    for sound in sounds:
        source_sound = ["snd", f"{sound}.wav"]
        source = os.path.join(*source_sound)
        sound_wav = pygame.mixer.Sound(source)
        sounds_wav[sound] = sound_wav


def get_coord_sight(start_x, start_y, end_x, end_y, length):
    """Поиск координаты указателя пушки"""

    Rab = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
    k = length / Rab
    x3 = start_x + (end_x - start_x) * k
    y3 = start_y + (end_y - start_y) * k
    return x3, y3


def find_neighbors(field, row, col, lst, prichina=None):
    """
    Поиск соседей по трем разным критериям вызова:
    None - Любой сосед
    color_ball - поиск шаров одинакового цвета
    free_ball - поиск любых шаров после взрыва
    [X  X  .]
    [X  О  X] для нечетного ряда
    [X  X  .]

    [.  X  Х]
    [X  О  X] для четного ряда
    [.  X  Х]
    """
    field[row][col].flag = True
    cell_j = 1 + (field[row][col].row % 2 * (-2))  # Колонка, углы которой не нужно проверять
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Проверка относительно четного или нечетного ряда.
            # Некоторые ячейки не нужно проверять
            if j == cell_j and i != 0:
                continue

            # Координаты соседа
            neighbor_row = row + i
            neighbor_col = col + j

            # Ячейки за пределами поля - не проверять!
            if not 0 <= neighbor_row <= FIELD_HEIGHT - 1:
                continue
            if not 0 <= neighbor_col <= FIELD_WIDTH - 1:
                continue

            if field[neighbor_row][neighbor_col]:
                if prichina == "color_ball":
                    # Проверка совпадения цветов с соседними шарами
                    if field[row][col].color == field[neighbor_row][neighbor_col].color:
                        # Добавление координат помеченных шаров в список
                        if (neighbor_row, neighbor_col) not in lst:
                            lst.append((neighbor_row, neighbor_col))
                        # Вызов рекурсии у ячейки, если шар еще не помечен
                        if not field[neighbor_row][neighbor_col].flag:
                            find_neighbors(field=field,
                                           row=neighbor_row,
                                           col=neighbor_col,
                                           lst=lst,
                                           prichina="color_ball")

                if prichina == "free_ball":
                    # Добавление координат помеченных шаров в список
                    if (neighbor_row, neighbor_col) not in lst:
                        lst.append((neighbor_row, neighbor_col))
                    # Вызов рекурсии у ячейки, если шар еще не помечен
                    if not field[neighbor_row][neighbor_col].flag:
                        find_neighbors(field=field,
                                       row=neighbor_row,
                                       col=neighbor_col,
                                       lst=lst,
                                       prichina="free_ball")

                # Добавление координат помеченных шаров в список
                if prichina == None:
                    if (neighbor_row, neighbor_col) not in lst:
                        lst.append((neighbor_row, neighbor_col))
