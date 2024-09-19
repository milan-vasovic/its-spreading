import pygame, random

#Initialize pygame
pygame.init()

#Set display window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#Set color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 143, 255)
GREEN = (95, 242, 78)
PURPLE = (240, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 236, 0)

#Set title
pygame.display.set_caption("It's spreading")

#Set FPS clock and condition
FPS = 60
clock = pygame.time.Clock()
running = True

#Define Classes

class Game:
    def __init__(self, player, slime_group):
        #Set game values
        self.score = 0
        self.round = 0
        self.round_time = 0
        self.frame_count = 0
        self.is_saved = False
        self.glory = 0
        self.player = player
        self.slime_group = slime_group
        self.current_active_life_sprite = 0
        self.current_inactive_life_sprite = 0
        self.current_character_sprite = 0
        self.current_idle_sprite = 0

        #Try to read data from glory.txt to get glory
        try:
            with open('storage/glory.txt', 'r') as file:
                self.glory = int(file.readline())
        except IOError as e:
            print(f"Error writing to the file: {e}")

        #Set fonts
        self.font_small = pygame.font.Font('assets/rests/Abrushow.ttf', 16)
        self.font = pygame.font.Font("assets/rests/Abrushow.ttf", 24)
        self.font_cinematic = pygame.font.Font("assets/rests/Abrushow.ttf", 32)
        self.font_title = pygame.font.Font("assets/rests/Abrushow.ttf", 36)

        #Set music
        self.next_level_sound = pygame.mixer.Sound("music/next_level.wav")
        self.next_level_sound.set_volume(0.02)

        #Set animations
        #Target
        self.blue_idle_sprites = []
        self.green_idle_sprites = []
        self.purple_idle_sprites = []
        self.red_idle_sprites = []
        self.yellow_idle_sprites = []

        #Character
        self.character_1_sprites = []
        self.character_2_sprites = []
        self.character_3_sprites = []
        self.character_4_sprites = []

        #Set life animation
        self.life_active_sprites = []
        self.life_inactive_sprites = []

        #Load images
        for i in range(0,4):
            self.life_active_sprites.append(pygame.image.load("assets/rests/heart/active_sprite_{}.png".format(i)))

        for i in range(0,5):
            self.life_inactive_sprites.append(pygame.image.load("assets/rests/heart/losing_sprite_{}.png".format(i)))

        for i in range(0,7):
            self.character_1_sprites.append(pygame.image.load("assets/characters/my_knight_front/sprite_{}.png".format(i)))
            self.character_2_sprites.append(pygame.image.load("assets/characters/my_wizard_front/sprite_{}.png".format(i)))
            self.character_3_sprites.append(pygame.image.load("assets/characters/my_prist_front/sprite_{}.png".format(i)))
            self.character_4_sprites.append(pygame.image.load("assets/characters/my_druid_front/sprite_{}.png".format(i)))

        for i in range(0,7):
            self.blue_idle_sprites.append(pygame.image.load("assets/slimes/blue_slime_idle/sprite_{}.png".format(i)))
            self.green_idle_sprites.append(pygame.image.load("assets/slimes/green_slime_idle/sprite_{}.png".format(i)))
            self.purple_idle_sprites.append(pygame.image.load("assets/slimes/purple_slime_idle/sprite_{}.png".format(i)))
            self.red_idle_sprites.append(pygame.image.load("assets/slimes/red_slime_idle/sprite_{}.png".format(i)))
            self.yellow_idle_sprites.append(pygame.image.load("assets/slimes/yellow_slime_idle/sprite_{}.png".format(i)))

        #Set current sprite as starting image
        self.active_life_image = self.life_active_sprites[self.current_active_life_sprite]
        self.inactive_life_image = self.life_inactive_sprites[self.current_inactive_life_sprite]

        self.my_knight_image = self.character_1_sprites[self.current_character_sprite]
        self.my_wizard_image = self.character_2_sprites[self.current_character_sprite]
        self.my_prist_image = self.character_3_sprites[self.current_character_sprite]
        self.my_druid_image = self.character_4_sprites[self.current_character_sprite]

        blue_slime_idle_image = self.blue_idle_sprites[self.current_idle_sprite]
        green_slime_idle_image = self.green_idle_sprites[self.current_idle_sprite]
        purple_slime_idle_image = self.purple_idle_sprites[self.current_idle_sprite]
        red_slime_idle_image = self.red_idle_sprites[self.current_idle_sprite]
        yellow_slime_idle_image = self.yellow_idle_sprites[self.current_idle_sprite]

        #This list cooresponds to the slime_type attributes int 0 -> blue, 1 -> green, 2 -> purple, 3 -> red, 4 -> yellow
        self.target_slime_images = [blue_slime_idle_image, green_slime_idle_image, purple_slime_idle_image, red_slime_idle_image, yellow_slime_idle_image]
        
        self.target_slime_type = random.randint(0, len(self.target_slime_images)-1)
        self.target_slime_image = self.target_slime_images[self.target_slime_type]


    def play_music(self):
        pygame.mixer.music.set_volume(0.05)
        if self.player.character == 0:
            pygame.mixer.music.load("music/my_music1.wav")
        elif self.player.character == 1:
            pygame.mixer.music.load("music/my_music2.wav")
        elif self.player.character == 2:
            pygame.mixer.music.load("music/my_music3.wav")
        else:
            pygame.mixer.music.load("music/music4.wav")
            pygame.mixer.music.set_volume(0.02)

        #The main game loop
        pygame.mixer.music.play(-1, 0.0)
        
    #Create update method for our game
    def update(self):
        #Increment frame count
        self.frame_count += 1

        #Every 60 ticks increas round time
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        #Update animations
        self.animateLife(self.life_active_sprites)
        self.animateLosingLife(self.life_inactive_sprites)

        #Check slime tipe and show right animation
        if self.target_slime_type == 0:
            self.animateTarget(self.blue_idle_sprites, .05)
        elif self.target_slime_type == 1:
            self.animateTarget(self.green_idle_sprites, .05)
        elif self.target_slime_type == 2:
            self.animateTarget(self.purple_idle_sprites, .05)
        elif self.target_slime_type == 3:
            self.animateTarget(self.red_idle_sprites, .05)
        elif self.target_slime_type == 4:
            self.animateTarget(self.yellow_idle_sprites, .05)

        #Check for collisions
        self.check_collisions()

    def animateTarget(self, sprite_list, speed):
     #Loop trough the sprite list changing the current sprite
        if self.current_idle_sprite < len(sprite_list) - 1:
            self.current_idle_sprite += speed
        else:
            self.current_idle_sprite = 0

        self.target_slime_image = sprite_list[int(self.current_idle_sprite)]

    def animateLife(self, sprite_list):
        if self.current_active_life_sprite < len(sprite_list)-1:
            self.current_active_life_sprite += .04
        else:
            self.current_active_life_sprite = 0
        
        self.active_life_image = sprite_list[int(self.current_active_life_sprite)]

    def animateLosingLife(self, sprite_list):
        if self.current_inactive_life_sprite < len(sprite_list)-1:
            self.current_inactive_life_sprite += 0.1
        else:
            self.current_inactive_life_sprite = 4

        self.inactive_life_image = sprite_list[int(self.current_inactive_life_sprite)]

    #Function that will draw our HUD and other things to the display
    def draw(self):
        #Add the slime colors to a list where the index of the color match target_slime_images
        colors = [BLUE, GREEN, PURPLE, RED, YELLOW]
        
        #Set game background
        background_image = pygame.image.load("assets/maps/map_outside_wall.png")
        if self.round >= 5:
            background_image = pygame.image.load("assets/maps/map_inside_wall.png")
        if self.round >= 10:
            if self.player.character == 0:
                background_image = pygame.image.load("assets/maps/map_training_ground.png")
            if self.player.character == 1:
                background_image = pygame.image.load("assets/maps/map_wizard_tower.png")
            if self.player.character == 2:
                background_image = pygame.image.load("assets/maps/map_cemetery.png")
            if self.player.character == 3:
                background_image = pygame.image.load("assets/maps/map_flower_garden.png")
                
        if self.round >= 15:
            if self.player.character == 0:
                background_image = pygame.image.load("assets/maps/map_sleeping_quarters.png")
            if self.player.character == 1:
                background_image = pygame.image.load("assets/maps/map_ritual_chamber.png")
            if self.player.character == 2:
                background_image = pygame.image.load("assets/maps/map_holy_chapel.png")
            if self.player.character == 3:
                background_image = pygame.image.load("assets/maps/map_secret_garden.png")            
        background_rect = background_image.get_rect()
        background_rect.topleft = (0, 100)

        #Set texts
        catach_text = self.font.render("Current Target", True, WHITE)
        catach_rect = catach_text.get_rect()
        catach_rect.centerx = WINDOW_WIDTH // 2
        catach_rect.top = 5

        self.target_slime_rect = self.target_slime_image.get_rect()
        self.target_slime_rect.centerx = WINDOW_WIDTH // 2
        self.target_slime_rect.top = 30
        
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        lives_image_active = self.active_life_image
        lives_image_active_rect = lives_image_active.get_rect()
        lives_image_active_rect.topleft = (85, 30)

        lives_image_inactive = self.inactive_life_image
        lives_image_inactive_rect = lives_image_inactive.get_rect()
        lives_image_inactive_rect.topleft = (245, 30)

        round_text = self.font.render("Current Round: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round Time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Abilities: " + str(self.player.abilities) + " | Cost: " + str(self.player.ability_cost), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        glory_text = self.font.render("Glory: " + str(self.glory), True, WHITE)
        glory_rect = glory_text.get_rect()
        glory_rect.topright = (WINDOW_WIDTH - 10, 70)

        #Blit the HUD
        display_surface.blit(background_image, background_rect)
        display_surface.blit(catach_text, catach_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)

        for i in range (0, self.player.lives):
            display_surface.blit(lives_image_active, lives_image_active_rect)
            lives_image_active_rect.left += 40

        if self.player.lives < 5:
            for a in range(0, 5-self.player.lives):
                display_surface.blit(lives_image_inactive, lives_image_inactive_rect)
                lives_image_inactive_rect.left -= 40

        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(glory_text, glory_rect)
        display_surface.blit(self.target_slime_image, self.target_slime_rect)

        pygame.draw.rect(display_surface, colors[self.target_slime_type], (WINDOW_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_slime_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

    #Check for collision between a player and individual slime
    def check_collisions(self):
        #WE must test the type of the slime to see if it matches the type of our target slime
        collided_slime = pygame.sprite.spritecollideany(self.player, self.slime_group, pygame.sprite.collide_mask)
        
        #We collided with slime
        if collided_slime:
            #Caught the corrected slime
            if collided_slime.type == self.target_slime_type:
                self.glory += 1
                self.score += 100 * self.round
                #Remove caught slime
                collided_slime.remove(self.slime_group)
                if (self.slime_group):
                    #There are more slime to catch
                    self.player.catach_sound.play()
                    self.choose_new_target()
                else: 
                    #The round is complete
                    self.player.catach_sound.play()
                    self.start_new_round()
                    self.player.resize(0)
            #Caught the wrong slime
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                self.current_inactive_life_sprite = 0

                #Check for game over
                if self.player.lives <= 0:
                    self.player.ability_cost = 1
                    self.pause_game("Final Score: " + str(self.score) + " | Round: " + str(self.round), "Press 'Enter' to play again", 3)
                    self.reset_game()

                self.player.resize(1)

    def start_new_round(self):
        """Populate board with new slimes"""
        #Provide a score bonus on how quickly the round was finished
        self.score += int(10000 * self.round / (1 + self.round_time))

        #Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round += 1
        self.player.ability_cost = 1
        self.player.abilities += 1
        self.player.velocity = 8

        #Remove any remainig slimes from a game reset
        for slime in self.slime_group:
            self.slime_group.remove(slime)

        #Add slimes to slime group
        for i in range(self.round):
            choise = random.randint(0, 4)
            self.slime_group.add(Slime(random.randint(1, WINDOW_WIDTH - 70), random.randint(101, WINDOW_HEIGHT - 170), choise))

        #Check what round and what character is and show right cinematic
        if self.round == 5:
            self.pause_game("Press 'ENTER' to continue", "Attention! Gate's down! They're multiplying fast, it's spreading!", 2)

        if self.round == 10:
            if self.player.character == 0:
                self.pause_game("Press 'ENTER' to continue", "Enemies at the Training Ground! It's battle time!", 2)
            if self.player.character == 1:
                self.pause_game("Press 'ENTER' to continue", "Trespassers at the Wizard Tower! Protect the potions at all costs!", 2)
            if self.player.character == 2:
                self.pause_game("Press 'ENTER' to continue", "Intruders breach the Cemetery! Defend its honor!", 2)
            if self.player.character == 3:
                self.pause_game("Press 'ENTER' to continue", "Uninvited guests in the Flower Garden! Protect the lawn's beauty!", 2)

        if self.round == 15:
            if self.player.character == 0:
                self.pause_game("Press 'ENTER' to continue", "Trespassers at the Sleeping Quarters! No bed jumping allowed, keep order!", 2)
            if self.player.character == 1:
                self.pause_game("Press 'ENTER' to continue", "Intruders in the Ritual Chamber! Keep focus, no disruptions!", 2)
            if self.player.character == 2:
                self.pause_game("Press 'ENTER' to continue", "Intruders in the Chapel! Protect the sacred scroll, keep them away!", 2)
            if self.player.character == 3:
                self.pause_game("Press 'ENTER' to continue", "Secret Garden located! Defend its tranquility, no trespassing tolerated!", 2)

        #Choose a new target slime
        self.choose_new_target()

        self.next_level_sound.play()

    #Function to chose next target that we need to caught
    def choose_new_target(self):
        """Choose a new target slime for the player"""
        target_slime = random.choice(self.slime_group.sprites())
        self.target_slime_type = target_slime.type
        self.target_slime_image = self.target_slime_images[self.target_slime_type]

    #Helper function to draw author info
    def draw_author(self):
        author_text = self.font.render("Author: Milan Vasovic", True, WHITE)
        author_rect = author_text.get_rect()
        author_rect.right = WINDOW_WIDTH
        author_rect.bottom = WINDOW_HEIGHT - 20

        contact_text = self.font_small.render("Contact: milan.vasovic.work@gmail.com", True, WHITE)
        contact_rect = contact_text.get_rect()
        contact_rect.right = WINDOW_WIDTH
        contact_rect.bottom = WINDOW_HEIGHT

        display_surface.blit(author_text, author_rect)
        display_surface.blit(contact_text, contact_rect)

    def draw_score_board(self):
        with open("storage/results.txt", 'r') as file:
            lines = file.readlines()

        try:
            results = [tuple(map(int, line.strip().split('|'))) for line in lines]
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        except ValueError as e:
            sorted_results = []
        
        x = 70
        y = 0

        score_board_text = self.font_cinematic.render("Top 10", True, WHITE)
        score_board_rect = score_board_text.get_rect()
        score_board_rect.topleft = (x, y)
        display_surface.blit(score_board_text, score_board_rect)

        for i in range(0, 10):
            y += 32
            try:
                if i < len(sorted_results):
                    text = sorted_results[i]
                    score, round_num = map(int, text)
                    result_text = self.font.render("Score: {} | Round: {}".format(score, round_num), True, WHITE)
                else:
                    result_text = self.font.render("Score: ____ | Round: ____", True, WHITE)
            except ValueError as e:
                result_text = self.font.render("Score: ____ | Round: ____", True, WHITE)

            result_rect = result_text.get_rect()
            result_rect.topleft = (0, y)
            display_surface.blit(result_text, result_rect)


    #Function that works like menu and handle diffrent scenarios and pause the main game loop
    def pause_game(self, s_text, m_text, state):
        """Pause the game, with keys inputs change state of the pause and show realted texts and actions.
        State 0, caracter selection and press enter to continue
        State 1, show selected character, controls, abilitiy, press enter to continue
        state 2, show cinematic, press enter to start game
        state 3, show end cinematic, stats, save and press enter to restart,
        """
        pygame.mixer.music.pause()
        global running
        state = state

        display_surface.fill(BLACK)

        #Set game background
        welcome_image = pygame.image.load("assets/maps/map_gate.png")
        welcome_image_rect = welcome_image.get_rect()
        welcome_image_rect.topleft = (0, 0)
            
        display_surface.blit(welcome_image, welcome_image_rect)

        #Define main text and sub text that is for the most same postion
        #But blit it later in case when we change stuff in specific scenarios
        main_text = self.font_title.render(m_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 )

        sub_text = self.font_cinematic.render(s_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)

        #Check diffrent states
        if state == 0:
            character_1_image = pygame.transform.scale(self.my_knight_image, (128, 128))
            character_1_rect =  character_1_image.get_rect()
            character_1_rect.topleft = (150, 450)

            character_2_image = pygame.transform.scale(self.my_wizard_image, (128, 128))
            character_2_rect =  character_2_image.get_rect()
            character_2_rect.topleft = (350, 450)

            character_3_image = pygame.transform.scale(self.my_prist_image, (128, 128))
            character_3_rect =  character_2_image.get_rect()
            character_3_rect.topleft = (700, 450)

            character_4_image = pygame.transform.scale(self.my_druid_image, (128, 128))
            character_4_rect =  character_2_image.get_rect()
            character_4_rect.topleft = (900, 450)

            display_surface.blit(character_1_image, character_1_rect)
            display_surface.blit(character_2_image, character_2_rect)
            display_surface.blit(character_3_image, character_3_rect)
            display_surface.blit(character_4_image, character_4_rect)

            key_1_image = pygame.transform.scale(pygame.image.load("assets/rests/1_Key_Light.png"), (64, 64))
            key_1_rect = key_1_image.get_rect()
            key_1_rect.topleft = (182, 580)

            glory_text = self.font_cinematic.render("Glory: " + str(self.glory), True, WHITE)
            glory_rect = glory_text.get_rect()
            glory_rect.topright = (WINDOW_WIDTH,0)

            display_surface.blit(glory_text, glory_rect)

            #Deepending on vale of glory give player option to select other characters
            if self.glory > 50:
                if self.glory > 200:
                    key_4_image = pygame.transform.scale(pygame.image.load("assets/rests/4_Key_Light.png"), (64, 64))
                    key_4_rect = key_4_image.get_rect()
                    key_4_rect.topleft = (932, 580)
                
                    display_surface.blit(key_4_image, key_4_rect)
                
                else:
                    need_3_text = self.font.render("Need 100 glory", True, RED)
                    need_3_rect = need_3_text.get_rect()
                    need_3_rect.topleft = (890, 580)

                    display_surface.blit(need_3_text, need_3_rect)

                if self.glory > 100:
                    key_3_image = pygame.transform.scale(pygame.image.load("assets/rests/3_Key_Light.png"), (64, 64))
                    key_3_rect = key_3_image.get_rect()
                    key_3_rect.topleft = (732, 580)

                    display_surface.blit(key_3_image, key_3_rect)
                else:
                    need_2_text = self.font.render("Need 100 glory", True, RED)
                    need_2_rect = need_2_text.get_rect()
                    need_2_rect.topleft = (690, 580)

                    display_surface.blit(need_2_text, need_2_rect)

                key_2_image = pygame.transform.scale(pygame.image.load("assets/rests/2_Key_Light.png"), (64, 64))
                key_2_rect = key_2_image.get_rect()
                key_2_rect.topleft = (382, 580)

                display_surface.blit(key_2_image, key_2_rect)
            else:
                need_1_text = self.font.render("Need 50 glory", True, RED)
                need_1_rect = need_1_text.get_rect()
                need_1_rect.topleft = (340, 580)

                need_2_text = self.font.render("Need 100 glory", True, RED)
                need_2_rect = need_2_text.get_rect()
                need_2_rect.topleft = (690, 580)
                
                need_3_text = self.font.render("Need 200 glory", True, RED)
                need_3_rect = need_3_text.get_rect()
                need_3_rect.topleft = (890, 580)

                display_surface.blit(need_1_text, need_1_rect)
                display_surface.blit(need_2_text, need_2_rect)
                display_surface.blit(need_3_text, need_3_rect)

            display_surface.blit(key_1_image, key_1_rect)

            #Draw author info
            self.draw_author()
            self.draw_score_board()

            #Draw rectangle that indicate what character is selected
            if self.player.character == 0:
                pygame.draw.rect(display_surface, WHITE, (148, 448, 128, 128), 2)

            elif self.player.character == 1:
                pygame.draw.rect(display_surface, WHITE, (348, 448, 128, 128), 2)

            elif self.player.character == 2:
                pygame.draw.rect(display_surface, WHITE, (698, 448, 128, 128), 2)
            
            else:
                pygame.draw.rect(display_surface, WHITE, (898, 448, 128, 128), 2)

            #Check value of glory and if its lesser then draw red rectangle to indicate that they can't be selected
            if self.glory < 200:
                pygame.draw.rect(display_surface, RED, (898, 448, 128, 128), 2)
                if self.glory < 100:
                    pygame.draw.rect(display_surface, RED, (698, 448, 128, 128), 2)

                if self.glory < 50:
                    pygame.draw.rect(display_surface, RED, (348, 448, 128, 128), 2)
                 
        
        if state == 1:
            #Check wich character is chosen
            if self.player.character == 0:
                character_image = pygame.transform.scale(self.my_knight_image, (160, 160))
                ablilty_text = self.font.render("Ability: Shrink & Slow", True, WHITE)
                desc_text = self.font_small.render("Max use x2 in row", True, WHITE)

            if self.player.character == 1:
                character_image = pygame.transform.scale(self.my_wizard_image, (160, 160))
                ablilty_text = self.font.render("Ability: Warp", True, WHITE)
                desc_text = self.font_small.render("Teleport to safe zone", True, WHITE)

            if self.player.character == 2:
                character_image = pygame.transform.scale(self.my_prist_image, (160, 160))
                ablilty_text = self.font.render("Ability: Heal", True, WHITE)
                desc_text = self.font_small.render("Bring back 1 life max 5 lives", True, WHITE)

            if self.player.character == 3:
                character_image = pygame.transform.scale(self.my_druid_image, (160, 160))
                ablilty_text = self.font.render("Ability: Grow & Speed", True, WHITE)
                desc_text = self.font_small.render("Max use x2 in row", True, WHITE)

            character_rect =  character_image.get_rect()
            character_rect.topleft = (100, WINDOW_HEIGHT//2 - 80)
            ablilty_rect = ablilty_text.get_rect()
            ablilty_rect.topleft = (80, WINDOW_HEIGHT//2 + 100)
            desc_rect = desc_text.get_rect()
            desc_rect.topleft = (80, WINDOW_HEIGHT// 2 + 130)

            #Movement controls
            key_w = pygame.transform.scale(pygame.image.load("assets/rests/W_Key_Light.png"), (64, 64))
            key_w_rect = key_w.get_rect()
            key_w_rect.topleft = (360, WINDOW_HEIGHT//2 + 100)

            key_a = pygame.transform.scale(pygame.image.load("assets/rests/A_Key_Light.png"), (64, 64))
            key_a_rect = key_a.get_rect()
            key_a_rect.topleft = (290, WINDOW_HEIGHT//2 + 170)

            key_s = pygame.transform.scale(pygame.image.load("assets/rests/S_Key_Light.png"), (64, 64))
            key_s_rect = key_s.get_rect()
            key_s_rect.topleft = (360, WINDOW_HEIGHT//2 + 170)

            key_d = pygame.transform.scale(pygame.image.load("assets/rests/D_Key_Light.png"), (64, 64))
            key_d_rect = key_d.get_rect()
            key_d_rect.topleft = (436, WINDOW_HEIGHT//2 + 170)

            or_text = self.font_cinematic.render("OR", True, WHITE)
            or_rect = or_text.get_rect()
            or_rect.topleft = (WINDOW_WIDTH // 2 - 16, WINDOW_HEIGHT//2 + 135)

            key_space = pygame.transform.scale(pygame.image.load("assets/rests/Space_Key_Light.png"), (128, 96))
            key_space_rect = key_space.get_rect()
            key_space_rect.topleft = (WINDOW_WIDTH//2 - 64, WINDOW_HEIGHT//2 + 200)

            ablilty_use_text = self.font_cinematic.render("Ability", True, WHITE)
            ablilty_use_rect = ablilty_use_text.get_rect()
            ablilty_use_rect.topleft = (WINDOW_WIDTH// 2 - 48, WINDOW_HEIGHT//2 + 280)

            key_arrow_up = pygame.transform.scale(pygame.image.load("assets/rests/Arrow_Up_Key_Light.png"), (64, 64))
            key_arrow_up_rect = key_arrow_up.get_rect()
            key_arrow_up_rect.topleft = (770, WINDOW_HEIGHT//2 + 100)

            key_arrow_left = pygame.transform.scale(pygame.image.load("assets/rests/Arrow_Left_Key_Light.png"), (64, 64))
            key_arrow_left_rect = key_arrow_left.get_rect()
            key_arrow_left_rect.topleft = (700, WINDOW_HEIGHT//2 + 170)

            key_arrow_down = pygame.transform.scale(pygame.image.load("assets/rests/Arrow_Down_Key_Light.png"), (64, 64))
            key_arrow_down_rect = key_arrow_down.get_rect()
            key_arrow_down_rect.topleft = (770, WINDOW_HEIGHT//2 + 170)

            key_arrow_right = pygame.transform.scale(pygame.image.load("assets/rests/Arrow_Right_Key_Light.png"), (64, 64))
            key_arrow_right_rect = key_arrow_right.get_rect()
            key_arrow_right_rect.topleft = (840, WINDOW_HEIGHT//2 + 170)

            display_surface.blit(character_image, character_rect)
            display_surface.blit(ablilty_text, ablilty_rect)
            display_surface.blit(desc_text, desc_rect)

            display_surface.blit(key_w, key_w_rect)
            display_surface.blit(key_a, key_a_rect)
            display_surface.blit(key_s, key_s_rect)
            display_surface.blit(key_d, key_d_rect)
            display_surface.blit(key_arrow_up, key_arrow_up_rect)
            display_surface.blit(key_arrow_left, key_arrow_left_rect)
            display_surface.blit(key_arrow_down, key_arrow_down_rect)
            display_surface.blit(key_arrow_right, key_arrow_right_rect)
            display_surface.blit(or_text, or_rect)
            display_surface.blit(key_space, key_space_rect)
            display_surface.blit(ablilty_use_text, ablilty_use_rect)

            self.draw_author()

        if state == 2:
            #Check what round and what character and show right cinematic
            if self.round < 4:
                if self.player.character == 0:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_knight_outside_wall.png"), (1200, 700))
                if self.player.character == 1:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_wizard_outside_wall.png"), (1200, 700))
                if self.player.character == 2:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_prist_outside_wall.png"), (1200, 700))
                if self.player.character == 3:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_druid_outside_wall.png"), (1200, 700))
                    
            if self.round > 3:
                if self.player.character == 0:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_knight_inside_wall.png"), (1200, 700))
                if self.player.character == 1:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_wizard_inside_wall.png"), (1200, 700))
                if self.player.character == 2:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_prist_inside_wall.png"), (1200, 700))
                if self.player.character == 3:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_druid_inside_wall.png"), (1200, 700))

            if self.round > 8:
                if self.player.character == 0:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_knight_trainig_ground.png"), (1200, 700))
                if self.player.character == 1:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_wizard_wizard_tower.png"), (1200, 700))
                if self.player.character == 2:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_prist_cemetery.png"), (1200, 700))
                if self.player.character == 3:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_druid_flower_garden.png"), (1200, 700))

            if self.round > 13:
                if self.player.character == 0:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_knight_sleeping_quarters.png"), (1200, 700))
                if self.player.character == 1:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_wizard_ritual_chamber.png"), (1200, 700))
                if self.player.character == 2:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_prist_holy_chapel.png"), (1200, 700))
                if self.player.character == 3:
                    cinematic_image = pygame.transform.scale(pygame.image.load("assets/cinematics/cinematic_druid_secret_garden.png"), (1200, 700))
                                
            cinematic_image_rect = cinematic_image.get_rect()
            cinematic_image_rect.topleft = (0, 0)
            display_surface.blit(cinematic_image, cinematic_image_rect)

        if state == 3:
            #Check what round and what character and show right end cinematic
            if self.round < 5:
                end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_outside_wall.png"), (1200, 700))

            if self.round > 4:
                end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_inside_wall.png"), (1200, 700))

            if self.round > 9:
                if self.player.character == 0:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_trainig_ground.png"), (1200, 700))
                if self.player.character == 1:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_wizard_tower.png"), (1200, 700))
                if self.player.character == 2:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_cemetery.png"), (1200, 700))
                if self.player.character == 3:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_flower_garden.png"), (1200, 700))

            if self.round > 14:
                if self.player.character == 0:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_sleeping_quarters.png"), (1200, 700))
                if self.player.character == 1:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_ritual_chamber.png"), (1200, 700))
                if self.player.character == 2:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_holy_chapel.png"), (1200, 700))
                if self.player.character == 3:
                    end_image = pygame.transform.scale(pygame.image.load("assets/cinematics/end_secret_garden.png"), (1200, 700))
            
            end_image_rect = end_image.get_rect()
            end_image_rect.topleft = (0, 0)
                
            display_surface.blit(end_image, end_image_rect)

            #Create the main pause text
            save_text = self.font.render("Press 'S' to save score", True, WHITE)
            save_rect = save_text.get_rect()
            save_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90)

            if self.score != 0:
                display_surface.blit(save_text, save_rect)

        #Blit main and sub text
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)

        pygame.display.update()

        #Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if state == 0:
                            is_paused = False
                            if self.round < 1:
                                self.pause_game("Press 'ENTER' to continue", "Character Details and Controls", 1)
                            else:
                                self.pause_game("Press 'ENTER' to begin", "It's spreading..  They are coming!!!", 2)
                            
                        if state == 1:
                            is_paused = False
                            self.pause_game("Press 'ENTER' to begin", "It's spreading..  They are coming!!!", 2)
                        
                        if state == 2:
                            is_paused = False
                            
                        if state == 3:
                            is_paused = False
                            self.round = 0
                            self.pause_game("Press 'ENTER' to continue", "It's Spreading", 0)
                        
                        self.play_music()
                        #pygame.mixer.music.unpause()
                    
                    if event.key == pygame.K_1:
                        if state == 0:
                            self.player.change_character(0)
                            is_paused = False
                            self.pause_game("Press 'ENTER' to continue", "It's Spreading", 0)

                    if event.key == pygame.K_2:
                        if state == 0:
                            if self.glory > 50:
                                self.player.change_character(1)
                                is_paused = False
                                self.pause_game("Press 'ENTER' to continue", "It's Spreading", 0)

                    if event.key == pygame.K_3:
                        if state == 0:
                            if self.glory >100:
                                self.player.change_character(2)
                                is_paused = False
                                self.pause_game("Press 'ENTER' to continue", "It's Spreading", 0)

                    if event.key == pygame.K_4:
                        if state == 0:
                            if self.glory > 200:
                                self.player.change_character(3)
                                is_paused = False
                                self.pause_game("Press 'ENTER' to continue", "It's Spreading", 0)

                    if event.key == pygame.K_s:
                        if self.score != 0:
                            if state == 3:
                                self.save_score(str(self.score) + "|" + str(self.round))
                    
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #Function that restart game after loosing
    def reset_game(self):
        #Try to save collected glory to file
        try:
            with open('storage/glory.txt', 'w') as file:
                file.write(str(self.glory))
        except IOError as e:
            print(f"Error writing to the file: {e}")

        """Reset the game"""
        self.score = 0
        self.round = 0
        self.is_saved = False

        self.player.lives = 5
        self.player.abilities = 1
        self.player.ability_cost = 1

        #Restart player position and size if needed
        self.player.resize(0)

        self.start_new_round()
        self.play_music()

    def save_score(self, text):
        """Save score to file"""
        while not self.is_saved:
            try:
                with open('storage/results.txt', 'a') as file:
                    file.write(text + "\n")
                    self.is_saved = True
            except IOError as e:
                print(f"Error writing to the file: {e}")
                                 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Set values
        self.character = 0
        self.player_width = 72
        self.palyer_height = 96

        self.player_knight_idle_front_sprites = []
        self.player_knight_idle_back_sprites = []
        self.player_knight_walk_front_sprites = []
        self.player_knight_walk_back_sprites = []
        self.player_wizard_idle_front_sprites = []
        self.player_wizard_idle_back_sprites = []
        self.player_wizard_walk_front_sprites = []
        self.player_wizard_walk_back_sprites = []
        self.player_prist_idle_front_sprites = []
        self.player_prist_idle_back_sprites = []
        self.player_prist_walk_front_sprites = []
        self.player_prist_walk_back_sprites = []
        self.player_druid_idle_front_sprites = []
        self.player_druid_idle_back_sprites = []
        self.player_druid_walk_front_sprites = []
        self.player_druid_walk_back_sprites = []

        self.current_sprite = 0

        self.lives = 5
        self.abilities = 1
        self.ability_cost = 1
        self.velocity = 8

        # Set sounds
        self.catach_sound = pygame.mixer.Sound("music/catch.wav")
        self.catach_sound.set_volume(0.01)
        self.die_sound = pygame.mixer.Sound("music/die.wav")
        self.die_sound.set_volume(0.07)
        self.warp_sound = pygame.mixer.Sound("music/warp.wav")
        self.warp_sound.set_volume(0.07)

        #Load images for differnt characters and states such as idle and walknig
        for i in range(0, 7):
            self.player_knight_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_knight_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_wizard_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_wizard_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_wizard_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_wizard_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_prist_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_prist_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_prist_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_prist_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_druid_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

        for i in range(0, 8):
            self.player_knight_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_knight_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_wizard_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_wizard_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_wizard_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_wizard_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_prist_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_prist_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_prist_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_prist_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

            self.player_druid_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
        
        self.image = self.player_knight_idle_front_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT
    
    #Function that change current character
    def change_character(self, par):
        self.character = par

    #Function that animate character
    def animate(self, sprite_list, speed):
        #Loop trough the sprite list changing the current sprite
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

    def update(self):
        """Update the player"""
        #Create a mask
        self.mask = pygame.mask.from_surface(self.image)

        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen
        if self.character == 0:
            #LEFT
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x -= self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_knight_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x -= self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_knight_walk_front_sprites, 0.1)
                else:
                    self.rect.x -= self.velocity
                    self.animate(self.player_knight_walk_front_sprites, 0.1)
            #RIGHT
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x += self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_knight_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x += self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_knight_walk_front_sprites, 0.1)
                else:
                    self.rect.x += self.velocity
                    self.animate(self.player_knight_walk_front_sprites, 0.1)
            #UP
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                self.rect.y -= self.velocity
                self.animate(self.player_knight_walk_back_sprites, 0.1)
            #DOWN
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:        
                self.rect.y += self.velocity
                self.animate(self.player_knight_walk_front_sprites, 0.1)
            else:
                self.animate(self.player_knight_idle_front_sprites, 0.05)
        elif self.character == 1:
            #LEFT
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x -= self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_wizard_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x -= self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_wizard_walk_front_sprites, 0.1)
                else:
                    self.rect.x -= self.velocity
                    self.animate(self.player_wizard_walk_front_sprites, 0.1)
            #RIGHT
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x += self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_wizard_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x += self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_wizard_walk_front_sprites, 0.1)
                else:
                    self.rect.x += self.velocity
                    self.animate(self.player_wizard_walk_front_sprites, 0.1)
            #UP
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                self.rect.y -= self.velocity
                self.animate(self.player_wizard_walk_back_sprites, 0.1)
            #DOWN
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:        
                self.rect.y += self.velocity
                self.animate(self.player_wizard_walk_front_sprites, 0.1)
            else:
                self.animate(self.player_wizard_idle_front_sprites, 0.05)
        elif self.character == 2:
            #LEFT
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x -= self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_prist_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x -= self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_prist_walk_front_sprites, 0.1)
                else:
                    self.rect.x -= self.velocity
                    self.animate(self.player_prist_walk_front_sprites, 0.1)
            #RIGHT
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x += self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_prist_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x += self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_prist_walk_front_sprites, 0.1)
                else:
                    self.rect.x += self.velocity
                    self.animate(self.player_prist_walk_front_sprites, 0.1)
            #UP
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                self.rect.y -= self.velocity
                self.animate(self.player_prist_walk_back_sprites, 0.1)
            #DOWN
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:        
                self.rect.y += self.velocity
                self.animate(self.player_prist_walk_front_sprites, 0.1)
            else:
                self.animate(self.player_prist_idle_front_sprites, 0.05)
        
        else:
            #LEFT
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x -= self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_druid_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x -= self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_druid_walk_front_sprites, 0.1)
                else:
                    self.rect.x -= self.velocity
                    self.animate(self.player_druid_walk_front_sprites, 0.1)
            #RIGHT
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                    self.rect.x += self.velocity
                    self.rect.y -= self.velocity/2
                    self.animate(self.player_druid_walk_back_sprites, 0.1)
                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
                    self.rect.x += self.velocity
                    self.rect.y += self.velocity/2
                    self.animate(self.player_druid_walk_front_sprites, 0.1)
                else:
                    self.rect.x += self.velocity
                    self.animate(self.player_druid_walk_front_sprites, 0.1)
            #UP
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
                self.rect.y -= self.velocity
                self.animate(self.player_druid_walk_back_sprites, 0.1)
            #DOWN
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:        
                self.rect.y += self.velocity
                self.animate(self.player_druid_walk_front_sprites, 0.1)
            else:
                self.animate(self.player_druid_idle_front_sprites, 0.05)

    def ability(self):
        #Check can player use ability
        if (self.abilities - self.ability_cost) >= 0:
            #Check size of player
            if self.player_width > 32 and self.palyer_height > 64:
                #Deepending on character ability is diferent
                if self.character == 0:
                    self.resize(3)
                    self.velocity -= 1.5
                    self.abilities -= self.ability_cost
                    self.ability_cost *= 2
                    self.warp_sound.play()

            if self.character == 1:
                self.resize(0)
                self.abilities -= self.ability_cost
                self.ability_cost *= 2
                self.warp_sound.play()

            if self.character == 2:
                if self.lives < 5:
                    self.lives += 1
                    self.abilities -= self.ability_cost
                    self.ability_cost *= 2
                    self.warp_sound.play()
                 
            if self.character == 3:
                if self.player_width < 88 and self.palyer_height < 128:
                    self.resize(2)
                    self.velocity += 1
                    self.abilities -= self.ability_cost
                    self.ability_cost *= 2
                    self.warp_sound.play()
                
    #Function that restart character size and position
    def resize(self, value):
        self.current_sprite = 0
        if value == 0:
            self.player_width = 72
            self.palyer_height = 96
            pos_x = WINDOW_WIDTH//2
            pos_y = WINDOW_HEIGHT - 90

        #Set character position to bottom center after life lost
        if value == 1:
            pos_x = WINDOW_WIDTH//2
            pos_y = WINDOW_HEIGHT - 90

        #Make character bigger
        if value == 2:
            self.player_width += 8
            self.palyer_height += 16
            pos_x = self.rect.centerx
            pos_y = self.rect.top

        #Make character smaller
        #Its not finished difrent check is needed in ability
        if value == 3:
            self.player_width -= 8
            self.palyer_height -= 16
            pos_x = self.rect.centerx
            pos_y = self.rect.top

        #Redifne sprites and images and transform size
        self.player_knight_idle_front_sprites = []
        self.player_knight_idle_back_sprites = []
        self.player_knight_walk_front_sprites = []
        self.player_knight_walk_back_sprites = []
        self.player_druid_idle_front_sprites = []
        self.player_druid_idle_back_sprites = []
        self.player_druid_walk_front_sprites = []
        self.player_druid_walk_back_sprites = []

        for i in range(0, 7):
            self.player_knight_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_knight_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_idle_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_back/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_idle_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_front/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))        
        
        for i in range(0, 8):
            self.player_knight_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_knight_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_knight_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_walk_back_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_back_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))
            self.player_druid_walk_front_sprites.append(pygame.transform.scale(pygame.image.load("assets/characters/my_druid_front_walk/sprite_{}.png".format(i)), (self.player_width, self.palyer_height)))

        if self.character == 0:
            self.image = self.player_knight_idle_front_sprites[int(self.current_sprite)]
        if self.character == 3:
            self.image = self.player_druid_idle_front_sprites[int(self.current_sprite)]
            
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.top = pos_y

class Slime(pygame.sprite.Sprite):
    """A class to create enemy slime objects"""
    def __init__(self, x, y, slime_type):
        """Initialize the slime"""
        super().__init__()

        #Set slime animations
        self.blue_sprites = []
        self.green_sprites = []
        self.purple_sprites = []
        self.red_sprites = []
        self.yellow_sprites = []

        #Walking
        for i in range(0,8):
            self.blue_sprites.append(pygame.image.load("assets/slimes/slime_blue/sprite_{}.png".format(i)))
            self.green_sprites.append(pygame.image.load("assets/slimes/slime_green/sprite_{}.png".format(i)))
            self.purple_sprites.append(pygame.image.load("assets/slimes/slime_purple/sprite_{}.png".format(i)))
            self.red_sprites.append(pygame.image.load("assets/slimes/slime_red/sprite_{}.png".format(i)))
            self.yellow_sprites.append(pygame.image.load("assets/slimes/slime_yellow/sprite_{}.png".format(i)))

        self.current_walking_sprite = 0

        #Slime type is an int 0 -> blue, 1 -> green, 2 -> purple, 3 -> red, 4 -> yellow   
        if slime_type == 0:
            self.image = self.blue_sprites[self.current_walking_sprite]
        elif slime_type == 1:
            self.image = self.green_sprites[self.current_walking_sprite]
        elif slime_type == 2:
            self.image = self.purple_sprites[self.current_walking_sprite]
        elif slime_type == 3:
            self.image = self.red_sprites[self.current_walking_sprite]
        elif slime_type == 4:
            self.image = self.yellow_sprites[self.current_walking_sprite]

        self.type = slime_type
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

        self.bounce = pygame.mixer.Sound("music/bounce.wav")
        self.bounce.set_volume(0.008)

    def update(self):
        """Update the slime obejct"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity
        
        if self.type == 0:
            self.animate(self.blue_sprites, self.velocity)
        elif self.type == 1:
            self.animate(self.green_sprites, self.velocity)
        elif self.type == 2:
            self.animate(self.purple_sprites, self.velocity)
        elif self.type == 3:
            self.animate(self.red_sprites, self.velocity)
        else:
            self.animate(self.yellow_sprites, self.velocity)

        #Bounce the slime oof the edges of the display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            #Idea of diffrent behaviours of diferent type of slimes its not finished and have some bugs
            # if self.type == 1 or self.type == 3:
            #     if self.velocity + 1 < 11:
            #         self.velocity += 0.5
            # if self.type == 2 or self.type == 4:
            #     if self.velocity * 0.05 > 0.5:
            #         self.velocity -= 0.25
            
            self.dx = -1 * self.dx
            self.bounce.play()
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            # if self.type == 1 or self.type == 3:
            #     if self.velocity + 1 < 11:
            #         self.velocity += 0.5
            
            # if self.type == 2 or self.type == 4:
            #     if self.velocity * 0.05 > 0.5:
            #         self.velocity -= 0.25
            self.dy = -1 * self.dy
            self.bounce.play()
            
    def animate(self, sprite_list, speed):
        #Loop trough the sprite list changing the current sprite
        if self.current_walking_sprite < len(sprite_list) - 1:
            self.current_walking_sprite += 0.05 * speed
        else:
            self.current_walking_sprite = 0

        self.image = sprite_list[int(self.current_walking_sprite)]

#Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#Create a slime group
my_slime_group = pygame.sprite.Group()

#Create a game object
my_game = Game(my_player, my_slime_group)
my_game.pause_game("Press 'ENTER' to continue", "It's Spreading",0)
my_game.start_new_round()
my_game.play_music()

while running:
    #Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Player wants to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.ability()
            if event.key == pygame.K_p:
                my_game.pause_game("Press 'ENTER' to continue", "It's Spreading",0)

    #Fill the display
    display_surface.fill((50, 50, 50))

    #Update and draw the game
    my_game.update()
    my_game.draw()

    #Update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_slime_group.update()
    my_slime_group.draw(display_surface)

    #Update displkay and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()
    