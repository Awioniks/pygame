import pgzero
import os
import random
import math

# Setting for the game
os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 800
HEIGHT = 600
MAX_BULLETS = 100
MAX_LEVEL = 10
BULLET_SPEED = 6
game_started = False
game_won = False
touch_timer = 0
music_enabled = False
level, score, lives, bullets_shots = 1, 0, 10, 0
player_direction = (1, 0)
player_facing = "right"


# Menu Button
start_button = Rect((300, 240), (200, 60))
music_button = Rect((300, 320), (200, 60))
exit_button = Rect((300, 400), (200, 60))

# Players
zombie_killer = Actor("zombie_killer")
zombies, obstacles, bullets = [], [], []


def create_obstacles():
    """Create non-overlapping obstacles in random places."""
    new_obstacles = []
    obstacle_width = 60
    obstacle_height = 40
    obstacle_gap = 20
    obstacle_count = min(20 + (level - 1) * 2, 32)
    starting_area = Rect(
        (WIDTH // 2 - 70, HEIGHT // 2 - 70),
        (140, 140),
    )

    attempts = 0

    while len(new_obstacles) < obstacle_count and attempts < 800:
        attempts += 1
        obstacle = Rect(
            (
                random.randint(40, WIDTH - 100),
                random.randint(40, HEIGHT - 80),
            ),
            (obstacle_width, obstacle_height),
        )

        # Keep a larger starting area clear for the player.
        obstacle_area = obstacle.inflate(obstacle_gap, obstacle_gap)

        if obstacle.colliderect(starting_area):
            continue

        if any(
            obstacle_area.colliderect(
                existing_obstacle.inflate(obstacle_gap, obstacle_gap)
            )
            for existing_obstacle in new_obstacles
        ):
            continue

        new_obstacles.append(obstacle)

    return new_obstacles


def place_characters():
    """Place the player in the center and zombies in random positions."""
    global zombies, level

    zombie_killer.pos = (WIDTH // 2, HEIGHT // 2)
    zombie_killer.image = "zombie_killer_right"
    for _ in range(10 + level * 2):
        for _ in range(100):
            position = (
                random.randint(40, WIDTH - 40),
                random.randint(40, HEIGHT - 40),
            )
            hitbox = Rect(
                (position[0] - 20, position[1] - 30),
                (40, 60),
            )

            far_from_player = (
                math.hypot(
                    position[0] - zombie_killer.x,
                    position[1] - zombie_killer.y,
                )
                > 120
            )

            if far_from_player and not any(
                hitbox.colliderect(obstacle) for obstacle in obstacles
            ):
                zombie = Actor("zombie")
                zombie.pos = position
                zombies.append(zombie)
                break


def start_level():
    """Generate a fresh layout and more zombies for the current level."""
    obstacles[:] = create_obstacles()
    zombies.clear()
    bullets.clear()
    place_characters()


obstacles = create_obstacles()
place_characters()


# Main Draw function
def draw():
    screen.fill((139, 0, 0))

    if not game_started:
        draw_menu()
    else:
        draw_game()
        draw_text()


# Main Update function
def update():
    if game_started:
        move_player()
        move_enemies()
        move_bullets()
        check_zombie_touch()
        check_level()


def draw_text():
    screen.draw.text(f"Level {level}", (0, 0), color="white", fontsize=30)
    screen.draw.text(f"Score {score}", (150, 0), color="white", fontsize=30)
    screen.draw.text(f"Life {lives}", (300, 0), color="white", fontsize=30)
    screen.draw.text(f"Bullets {bullets_shots}", (450, 0), color="white", fontsize=30)


def draw_game():
    screen.clear()

    for obstacle in obstacles:
        screen.draw.filled_rect(obstacle, "darkgray")
        screen.draw.rect(obstacle, "black")

    zombie_killer.draw()
    for zombi in zombies:
        zombi.draw()

    for bullet in bullets:
        screen.draw.filled_circle((bullet["x"], bullet["y"]), 5, "white")


def draw_menu():
    if game_won:
        screen.draw.text(
            "YOU WIN!",
            center=(WIDTH // 2, 80),
            fontsize=50,
            color="yellow",
        )

    screen.draw.text(
        "ZOMBIE KILLER",
        center=(WIDTH // 2, 130),
        fontsize=60,
        color="white",
    )

    screen.draw.filled_rect(start_button, "red")
    screen.draw.filled_rect(music_button, "darkblue")
    screen.draw.filled_rect(exit_button, "black")

    screen.draw.text("START", center=start_button.center, fontsize=30)
    screen.draw.text(
        "MUSIC: ON" if music_enabled else "MUSIC: OFF",
        center=music_button.center,
        fontsize=25,
    )
    screen.draw.text("EXIT", center=exit_button.center, fontsize=30)


def on_mouse_down(pos):
    global game_started, game_won, music_enabled, level, score, bullets_shots, lives, touch_timer

    if not game_started and start_button.collidepoint(pos):
        game_started = True
        game_won = False
        level = 1
        score = 0
        bullets_shots = 0
        lives = 10
        touch_timer = 0
        start_level()
    elif not game_started and music_button.collidepoint(pos):
        music_enabled = not music_enabled

        if music_enabled:
            music.play("zombie_music.wav")
        else:
            music.stop()
    elif not game_started and exit_button.collidepoint(pos):
        quit()


def on_key_down(key):
    if key == keys.ESCAPE:
        quit()

    if key == keys.SPACE and bullets_shots <= MAX_BULLETS and game_started:
        shoot()


def shoot():
    """Add bullets to list"""

    dx, dy = player_direction
    bullets.append(
        {
            "x": zombie_killer.x,
            "y": zombie_killer.y,
            "dx": dx * BULLET_SPEED,
            "dy": dy * BULLET_SPEED,
        }
    )


def move_bullets():
    """Move bullets with the set BULLET_SPEED check if it collides with zombie and obstacles"""
    global score, bullets_shots
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

        if (
            bullet["x"] < 0
            or bullet["x"] > WIDTH
            or bullet["y"] < 0
            or bullet["y"] > HEIGHT
        ):
            bullets.remove(bullet)
            continue

        bullet_rect = Rect(
            (bullet["x"] - 2, bullet["y"] - 2),
            (5, 5),
        )

        hit_obstacle = False

        for obstacle in obstacles:
            obstacle_area = obstacle.inflate(20, 20)
            if obstacle_area.colliderect(bullet_rect):
                bullets.remove(bullet)
                bullets_shots += 1
                hit_obstacle = True
                break

        if hit_obstacle:
            continue

        for zombie in zombies[:]:
            if zombie_hitbox(zombie).colliderect(bullet_rect):
                zombies.remove(zombie)
                bullets.remove(bullet)
                score += 1
                break


def move_player():
    """Move the player and keep it inside the game window."""

    step_x = 0
    step_y = 0

    if keyboard.right:
        step_x += 3
        set_player_direction((1, 0), "zombie_killer_right")

    if keyboard.left:
        step_x -= 3
        set_player_direction((-1, 0), "zombie_killer_left")

    if keyboard.up:
        step_y -= 3
        set_player_direction((0, -1), "zombie_killer_up")

    if keyboard.down:
        step_y += 3
        set_player_direction((0, 1), "zombie_killer_down")

    # Check horizontal and vertical movement separately so the player
    # can slide along the edge of an obstacle.
    zombie_killer.x += step_x
    zombie_killer.x = max(0, min(WIDTH, zombie_killer.x))

    if any(player_hitbox().colliderect(obstacle) for obstacle in obstacles):
        zombie_killer.x -= step_x

    zombie_killer.y += step_y
    zombie_killer.y = max(0, min(HEIGHT, zombie_killer.y))

    if any(player_hitbox().colliderect(obstacle) for obstacle in obstacles):
        zombie_killer.y -= step_y


def set_player_direction(direction, image_name):
    """Update the shooting direction and the player's directional image."""
    global player_direction, player_facing

    player_direction = direction
    player_facing = image_name.rsplit("_", 1)[-1]
    zombie_killer.image = image_name


def move_enemies():
    """Move every zombie horizontally and vertically toward the player."""
    global lives

    speed = 1.5

    for zombie in zombies:
        change_x = zombie_killer.x - zombie.x
        change_y = zombie_killer.y - zombie.y
        distance = math.hypot(change_x, change_y)

        if distance <= 0 or distance > 250:
            continue

        step_x = change_x / distance * speed
        step_y = change_y / distance * speed

        # Try to move horizontally first.
        zombie.x += step_x
        zombie.x = max(0, min(WIDTH, zombie.x))

        if any(zombie_hitbox(zombie).colliderect(obstacle) for obstacle in obstacles):
            zombie.x -= step_x

        # Try to move vertically separately, so obstacles do not freeze
        # the zombie completely.
        zombie.y += step_y
        zombie.y = max(0, min(HEIGHT, zombie.y))

        if any(zombie_hitbox(zombie).colliderect(obstacle) for obstacle in obstacles):
            zombie.y -= step_y


def zombie_hitbox(zombie):
    """Return a smaller collision area than the large zombie image."""
    return Rect((zombie.x - 20, zombie.y - 30), (40, 60))


def player_hitbox():
    """Return the player's collision area."""
    return Rect((zombie_killer.x - 18, zombie_killer.y - 22), (36, 44))


def check_level():
    """Check level status"""
    global level, game_started, game_won

    if len(zombies) == 0:
        if level < MAX_LEVEL:
            level += 1
            start_level()
        else:
            game_started = False
            game_won = True


def check_zombie_touch():
    """Remove one life after a zombie touches the player for one second."""
    global lives, touch_timer, game_started

    touching = any(
        zombie_hitbox(zombie).colliderect(player_hitbox()) for zombie in zombies
    )

    if not touching:
        touch_timer = 0
        return

    touch_timer += 1

    # Pygame Zero normally updates about 60 times per second.
    if touch_timer >= 20:
        lives -= 1
        touch_timer = 0

        if lives <= 0:
            game_started = False
