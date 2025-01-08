import math
import random
import pgzrun


# Размер окна
WIDTH = 800
HEIGHT = 600

# Создание танка игрока
player = Actor("player_tank", (400, 300))  # Спрайт танка
player.speed = 3
player.lives = 3  # Жизни игрока

# Список пуль
bullets = []

# Список врагов
enemies = []

# Список пуль врагов
enemy_bullets = []

# Размер тайла земли
TILE_SIZE = 64

# Загрузка изображений для тайлов земли
tile_image = "tile"  # Имя изображения для тайла (tile.png)


ICON = "./images/player_tank.png"


# Обновление состояния игры
def update():
    # Движение танка с помощью WASD
    if keyboard.a:  # Влево
        player.x -= player.speed
    if keyboard.d:  # Вправо
        player.x += player.speed
    if keyboard.w:  # Вверх
        player.y -= player.speed
    if keyboard.s:  # Вниз
        player.y += player.speed

    # Ограничение движения игрока в пределах экрана
    player.x = max(20, min(WIDTH - 20, player.x))
    player.y = max(20, min(HEIGHT - 20, player.y))

    # Обновление пуль игрока
    for bullet in bullets:
        bullet.x += bullet.vx
        bullet.y -= bullet.vy
        # Удаление пуль за пределами экрана
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

    # Обновление врагов
    for enemy in enemies:
        # Поворот врага в сторону игрока с использованием angle_to()
        angle_to_player = enemy.angle_to(player.pos)
        enemy.angle = angle_to_player  # Поворот врага с использованием angle_to()

        # Двигаемся в сторону игрока (направление вычисляем с помощью разницы координат)
        direction_x = player.x - enemy.x
        direction_y = player.y - enemy.y
        distance = math.sqrt(direction_x**2 + direction_y**2)  # Расстояние до игрока

        # Если расстояние не нулевое, двигаемся в сторону игрока
        if distance != 0:
            enemy.vx = (direction_x / distance) * 2  # Нормализованный вектор по X
            enemy.vy = (direction_y / distance) * 2  # Нормализованный вектор по Y

        # Обновляем положение врага
        enemy.x += enemy.vx
        enemy.y += enemy.vy

        # Стрельба врага
        if random.random() < 0.01:  # Враг стреляет с небольшой вероятностью
            shoot_enemy_bullet(enemy)

        # Проверка на столкновение с пулей игрока
        for bullet in bullets:
            if enemy.collidepoint(bullet.x, bullet.y):
                bullets.remove(bullet)
                enemies.remove(enemy)  # Удаляем врага при попадании
                break

    # Проверка на столкновение пули врага с игроком
    for bullet in enemy_bullets:
        bullet.x += bullet.vx
        bullet.y -= bullet.vy
        # Если пуля выходит за пределы экрана, удаляем ее
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)
        elif player.collidepoint(bullet.x, bullet.y):
            enemy_bullets.remove(bullet)
            player.lives -= 1
            if player.lives <= 0:
                print("Game Over!")
                quit()


# Стрельба игрока (при отпускании кнопки мыши)
def on_mouse_up(pos, button):
    if button == mouse.LEFT:  # Проверка на левую кнопку мыши
        # Получаем угол поворота танка
        angle = player.angle_to(pos)  # Поворот в сторону мыши

        # Создание новой пули
        bullet = Actor("player_bullet", (player.x, player.y))  # Спрайт пули
        bullet.angle = angle  # Устанавливаем угол пули в угол танка

        # Направление пули
        bullet.vx = math.cos(angle) * 5  # Скорость пули по x
        bullet.vy = math.sin(angle) * 5  # Скорость пули по y
        bullets.append(bullet)


# Стрельба врага
def shoot_enemy_bullet(enemy):
    angle_to_player = enemy.angle_to(player.pos)  # Поворот пули врага к игроку
    bullet = Actor("enemy_bullet", (enemy.x, enemy.y))  # Спрайт пули врага
    bullet.angle = angle_to_player  # Устанавливаем угол пули в угол врага
    bullet.vx = math.cos(angle_to_player) * 3
    bullet.vy = math.sin(angle_to_player) * 3
    enemy_bullets.append(bullet)


# Обработчик движения мыши (для поворота танка)
def on_mouse_move(pos):
    # Поворот танка в сторону курсора с использованием angle_to
    player.angle = player.angle_to(pos)


# Создание врагов
def create_enemies():
    for _ in range(5):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        enemy = Actor("enemy_tank", (x, y))  # Используем "enemy_tank" для врагов
        enemy.vx = 0
        enemy.vy = 0
        enemy.angle = 0  # Начальный угол врага
        enemies.append(enemy)


# Рисование тайлов земли
def draw_tiles():
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            screen.blit(tile_image, (x, y))  # Рисуем каждый тайл


# Отрисовка объектов
def draw():
    draw_tiles()  # Рисуем тайлы земли

    # Рисуем игрока
    player.draw()

    # Рисуем всех врагов
    for enemy in enemies:
        enemy.draw()

    # Рисуем пули игрока
    for bullet in bullets:
        bullet.draw()

    # Рисуем пули врагов
    for bullet in enemy_bullets:
        bullet.draw()

    # Отображение количества жизней игрока
    screen.draw.text(f"Lives: {player.lives}", (10, 10), color="white", fontsize=30)


# Инициализация врагов
enemy_bullets = []
create_enemies()

pgzrun.go()
