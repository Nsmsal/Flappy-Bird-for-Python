import pygame
import sys
import random
import os
import json

# Initialiseer Pygame
pygame.init()

# Scherminstellingen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Speler instellingen
bird_rect = pygame.Rect(50, screen_height // 2, 30, 30)  # Gebruik een zwart blokje als vogel
bird_velocity = 0
gravity = 0.5
flap_strength = -7  # Pas flapsterkte aan naar wens
terror_mode_active = False
terror_mode_speed = 10  # Snelheid van de vogel in terror mode
terror_mode_direction_change_rate = 0.05  # Hoe vaak de richting verandert

# Pijpen instellingen
pipe_width = 70
pipe_gap = 150
pipe_velocity = -5
pipes_with_status = []

# Score
score = 0

# Gebruikersgegevensbestand
data_file = 'user_data.json'

# Laad de logo afbeelding
def load_logo():
    try:
        logo = pygame.image.load('bird2.png')
        logo = pygame.transform.scale(logo, (400, 100))  # Schaal de afbeelding naar wens
        return logo
    except pygame.error as e:
        print(f"Error loading logo: {e}")
        return None

logo_image = load_logo()

# Functie om nieuwe pijpen te maken
def create_pipes():
    height = random.randint(150, screen_height - pipe_gap - 150)
    bottom_pipe = pygame.Rect(screen_width, height, pipe_width, screen_height - height)
    top_pipe = pygame.Rect(screen_width, 0, pipe_width, height - pipe_gap)
    return bottom_pipe, top_pipe

# Functie om het verliesbericht te tonen
def display_lost_message():
    screen.fill(WHITE)
    message = font.render("You lost! Press SPACE to restart or ESC to exit.", True, BLACK)
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - message.get_height() // 2))
    pygame.display.flip()

# Functie om de gebruikersnaam in te voeren
def enter_username(is_login):
    global username
    screen.fill(WHITE)
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text.strip():  # Zorg ervoor dat de gebruikersnaam niet leeg is
                        username = text
                        if not is_login:
                            set_pin_code()  # Nieuwe gebruiker, stel een pincode in
                        else:
                            if verify_login():
                                start_game()
                            else:
                                display_lost_message()
                        return
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.unicode.isprintable():
                    text += event.unicode
                # Display gebruikersnaam invoerveld
                screen.fill(WHITE)
                if logo_image:
                    screen.blit(logo_image, (screen_width // 2 - logo_image.get_width() // 2, 20))
                username_text = font.render(f"Enter username: {text}", True, BLACK)
                screen.blit(username_text, (screen_width // 2 - username_text.get_width() // 2, screen_height // 2 - username_text.get_height() // 2))
                pygame.display.flip()

# Functie om de pincode in te voeren
def set_pin_code():
    global pin_code
    screen.fill(WHITE)
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text.strip():
                        pin_code = text
                        save_user_data()
                        start_game()
                        return
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.unicode.isnumeric():
                    text += event.unicode
                # Display pincode invoerveld
                screen.fill(WHITE)
                if logo_image:
                    screen.blit(logo_image, (screen_width // 2 - logo_image.get_width() // 2, 20))
                pin_text = font.render(f"Set pincode: {'*' * len(text)}", True, BLACK)
                screen.blit(pin_text, (screen_width // 2 - pin_text.get_width() // 2, screen_height // 2 - pin_text.get_height() // 2))
                pygame.display.flip()

# Functie om gebruikersgegevens op te slaan
def save_user_data():
    if not os.path.isfile(data_file):
        with open(data_file, 'w') as file:
            json.dump({}, file)
    with open(data_file, 'r+') as file:
        data = json.load(file)
        data[username] = pin_code
        file.seek(0)
        json.dump(data, file)
        file.truncate()

# Functie om de pincode in te voeren bij het inloggen
def enter_pin_code():
    global cheat_mode_active
    screen.fill(WHITE)
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text.strip():
                        with open(data_file, 'r') as file:
                            data = json.load(file)
                            if username in data and text == data[username]:
                                start_game()
                                return
                            else:
                                print("Incorrect pin code.")
                                return
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.unicode.isnumeric():
                    text += event.unicode
                # Display pincode invoerveld
                screen.fill(WHITE)
                if logo_image:
                    screen.blit(logo_image, (screen_width // 2 - logo_image.get_width() // 2, 20))
                pin_text = font.render(f"Enter pincode: {'*' * len(text)}", True, BLACK)
                screen.blit(pin_text, (screen_width // 2 - pin_text.get_width() // 2, screen_height // 2 - pin_text.get_height() // 2))
                pygame.display.flip()

def verify_login():
    global username
    screen.fill(WHITE)
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text.strip():
                        with open(data_file, 'r') as file:
                            data = json.load(file)
                            if username in data:
                                enter_pin_code()
                            else:
                                print("User does not exist.")
                                return False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.unicode.isprintable():
                    text += event.unicode
                # Display gebruikersnaam invoerveld
                screen.fill(WHITE)
                if logo_image:
                    screen.blit(logo_image, (screen_width // 2 - logo_image.get_width() // 2, 20))
                username_text = font.render(f"Enter username: {text}", True, BLACK)
                screen.blit(username_text, (screen_width // 2 - username_text.get_width() // 2, screen_height // 2 - username_text.get_height() // 2))
                pygame.display.flip()

# Start de game
def start_game():
    global game_running, game_over, terror_mode_active
    game_running = True
    game_over = False
    terror_mode_active = False  # Zet terror mode uit bij het starten van het spel
    main_game_loop()

# Hoofdlus van de game
def main_game_loop():
    global bird_rect, bird_velocity, pipes_with_status, score, game_running, game_over, terror_mode_active

    # Voeg start_pijpen toe aan het begin
    if not pipes_with_status:
        bottom_pipe, top_pipe = create_pipes()
        pipes_with_status.append((bottom_pipe, False))
        pipes_with_status.append((top_pipe, False))

    # Hoofdlus
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset spel na verlies
                        score = 0
                        pipes_with_status = []
                        start_game()
                    else:
                        # Vogel omhoog laten gaan
                        bird_velocity += flap_strength
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Toggle terror mode
                    if not terror_mode_active:
                        print("Terror mode activated! Press ESC to exit.")
                        terror_mode_active = True
                    else:
                        print("Terror mode deactivated!")
                        terror_mode_active = False

        if terror_mode_active:
            # Terror mode: Vogel beweegt willekeurig en snel in alle richtingen
            bird_rect.x += random.uniform(-terror_mode_speed, terror_mode_speed)
            bird_rect.y += random.uniform(-terror_mode_speed, terror_mode_speed)
            # Zorg ervoor dat de vogel binnen het scherm blijft
            bird_rect.x = max(0, min(bird_rect.x, screen_width - bird_rect.width))
            bird_rect.y = max(0, min(bird_rect.y, screen_height - bird_rect.height))
        else:
            # Normale modus
            bird_velocity += gravity
            bird_rect.y += bird_velocity

            # Zorg ervoor dat de vogel binnen het scherm blijft
            if bird_rect.top < 0:
                bird_rect.top = 0
                bird_velocity = 0
            if bird_rect.bottom > screen_height:
                bird_rect.bottom = screen_height

        # Verplaats de pijpen en controleer op botsingen
        new_pipes = []
        for pipe, passed in pipes_with_status:
            pipe.x += pipe_velocity
            if not passed and pipe.x < bird_rect.x:
                passed = True
                score += 1
            if pipe.x + pipe_width > 0:
                new_pipes.append((pipe, passed))

        pipes_with_status = new_pipes

        # Voeg nieuwe pijpen toe als nodig
        if pipes_with_status[-1][0].x < screen_width - 200:
            bottom_pipe, top_pipe = create_pipes()
            pipes_with_status.append((bottom_pipe, False))
            pipes_with_status.append((top_pipe, False))

        # Controleer op botsingen
        if any(bird_rect.colliderect(pipe) for pipe, _ in pipes_with_status):
            if not terror_mode_active:
                game_running = False
                game_over = True

        # Scherm bijwerken
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, bird_rect)
        for pipe, _ in pipes_with_status:
            pygame.draw.rect(screen, GREEN, pipe)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(30)

        if game_over:
            # Toon verliesbericht
            display_lost_message()

# Toon scorebord met opties om te registreren of in te loggen
def display_scoreboard(options_text, scores=None):
    screen.fill(WHITE)
    if logo_image:
        screen.blit(logo_image, (screen_width // 2 - logo_image.get_width() // 2, 20))

    for i, option in enumerate(options_text):
        option_text = font.render(option, True, BLACK)
        screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, 200 + i * 50))

    if scores:
        # Toon scorebord onder de opties
        score_title = font.render("Scoreboard:", True, BLACK)
        screen.blit(score_title, (screen_width // 2 - score_title.get_width() // 2, 350))
        for i, (user, user_score) in enumerate(scores.items()):
            score_text = font.render(f"{user}: {user_score}", True, BLACK)
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 400 + i * 30))

    pygame.display.flip()

# Toon scorebord met opties om te registreren of in te loggen
def show_initial_screen():
    options_text = [
        "Press 1 to Register New User",
        "Press 2 to Login"
    ]
    display_scoreboard(options_text)

show_initial_screen()

# Hoofdlus voor registratie of inloggen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # Start registratie nieuwe gebruiker
                enter_username(is_login=False)
            elif event.key == pygame.K_2:
                # Start inloggen bestaande gebruiker
                enter_username(is_login=True)
