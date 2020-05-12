#NINJA GAME
#NINJA KILLING OPPONENTS

import random
import math
from superwires import games, color
import sys
import pygame
games.init(screen_width=640, screen_height=480, fps=50)



class Hero(games.Sprite):
    """Every hero in game, player and bots """
    SPEED = 5
    JUMP_SPEED = 5
    FALL = 5
    MISSILE_DELAY = 10
    direction = True
    HP = 5

    def update(self):
        """Dont leave the window screen """
        if self.bottom > games.screen.height:
            self.bottom = games.screen.height
        if self.top < 0:
            self.top = 0
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

    def die(self):
        """ Zniszcz się. """
        self.destroy()


class Collider(Hero):
    """If collider do functions """
    def update(self):
        """ Check overlaping spirits"""
        super(Collider, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        """ Zniszcz się i pozostaw po sobie eksplozję. """
        if self.HP == 0:
            self.destroy()

class Collider_2(Hero):
    """If collider do functions """
    def update(self):
        """ Check overlaping spirits"""
        super(Collider_2, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        """ Zniszcz się i pozostaw po sobie eksplozję. """
        self.destroy()

#Player hero_1
class Ninja(Collider):
    """Player ninja hero class"""
    image = games.load_image("ninja.png")

    def __init__(self, x, y):
        """Inicialization of ninja"""
        super(Ninja,self).__init__(image = Ninja.image, x = 40, y=games.screen.height)
        self.missile_wait = 0

    def update(self):
        """Move of ninja, change of look position, and attack """
        super(Ninja,self).update()
        #move when key is pressed
        if games.keyboard.is_pressed(games.K_a):
            self.x -= self.SPEED
            self.direction = False


        if games.keyboard.is_pressed(games.K_d):
            self.x += self.SPEED
            self.direction = True

        if games.keyboard.is_pressed(games.K_w):
            self.y -= self.JUMP_SPEED

        else:
            self.y += self.FALL

        # jeśli czekasz, aż statek będzie mógł wystrzelić następny pocisk,
        # zmniejsz czas oczekiwania
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # wystrzel pocisk, jeśli klawisz spacji jest naciśnięty i skończył się
        # czas oczekiwania

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0 and self.direction == False:
                new_missile = Missile(self.x, self.y, self.angle-90)
                games.screen.add(new_missile)
                self.missile_wait = Ninja.MISSILE_DELAY

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0 and self.direction == True:
            new_missile = Missile(self.x, self.y, self.angle + 90)
            games.screen.add(new_missile)
            self.missile_wait = Ninja.MISSILE_DELAY


    def end(self):
        """ Zakończ grę. """
        # pokazuj komunikat 'Koniec gry' przez 5 sekund
        end_message = games.Message(value="Koniec gry, wygrywa gracz 2",
                                    size=50,
                                    color=color.black,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)

    def die(self):
        """Hero dies"""
        self.end()
        self.destroy()

#Player hero_2
class Ninja_2(Collider):
    """Player ninja hero class"""
    image = games.load_image("ninja_2.png")
    def __init__(self, x, y):
        """Inicialization of ninja"""
        super(Ninja_2,self).__init__(image = Ninja_2.image, x = 600, y=games.screen.height)
        self.missile_wait = 0
    def update(self):
        """Move of ninja, change of look position, and attack """
        super(Ninja_2,self).update()
        #move when key is pressed
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= self.SPEED
            self.direction = False


        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += self.SPEED
            self.direction = True

        if games.keyboard.is_pressed(games.K_UP):
            self.y -= self.JUMP_SPEED

        else:
            self.y += self.FALL

        # jeśli czekasz, aż statek będzie mógł wystrzelić następny pocisk,
        # zmniejsz czas oczekiwania
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # wystrzel pocisk, jeśli klawisz spacji jest naciśnięty i skończył się
        # czas oczekiwania

        if games.keyboard.is_pressed(games.K_RCTRL) and self.missile_wait == 0 and self.direction == False:
                new_missile = Missile(self.x, self.y, self.angle-90)
                games.screen.add(new_missile)
                self.missile_wait = Ninja_2.MISSILE_DELAY

        if games.keyboard.is_pressed(games.K_RCTRL) and self.missile_wait == 0 and self.direction == True:
            new_missile = Missile(self.x, self.y, self.angle + 90)
            games.screen.add(new_missile)
            self.missile_wait = Ninja_2.MISSILE_DELAY


    def end(self):
        """ Zakończ grę. """
        # pokazuj komunikat 'Koniec gry' przez 5 sekund
        end_message = games.Message(value="Koniec gry, wygrywa gracz 1",
                                    size=50,
                                    color=color.black,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit,
                                    is_collideable=False)
        games.screen.add(end_message)

    def die(self):
        """Hero dies"""
        self.end()
        self.destroy()

class Missile(Collider_2):
    """Shuriken missilies"""
    image = games.load_image("shuriken.png")
    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 40


    def __init__(self, ninja_x, ninja_y, ninja_angle):
        """ Inicialize shurkien """

        #change to radians
        angle = ninja_angle * math.pi / 180
        #start missile position
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ninja_x + buffer_x
        y = ninja_y + buffer_y

        #calculate velocity dx and dy
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        #create missile
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME

    def update(self):
        """Movment of missile"""
        super(Missile, self).update()

        #destroy when lifetime is over
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

        self.check_catch()

    def check_catch(self):
        """Sprawdź czy gracz dostał pociskiem"""
        for Collider in self.overlapping_sprites:
            self.HP -= 1
            Collider.handle.caught()


class Kill(games.Animation):
    """ Animacja eksplozji. """
    sound = games.load_sound("eksplozja.wav")
    images = ["kill_1.png",
              "kill_2.png",
              "kill_3.png",
              "kill_4.png",
              "kill_5.png",
              "kill_6.png",
              "kill_7.png",
              "kill_8.png",]

    def __init__(self, x, y):
        super(Kill, self).__init__(images=Kill.images,
                                        x=x, y=y,
                                        repeat_interval=4, n_repeats=1,
                                        is_collideable=False)
        Kill.sound.play()






def main():
    #background
    background = games.load_image("tlo_ninjagame.png",transparent=False)
    games.screen.background = background


    new_ninja = Ninja(x = games.screen.width/2, y=games.screen.height)
    games.screen.add(new_ninja)

    new_ninja2 = Ninja_2(x=games.screen.width / 2, y=games.screen.height)
    games.screen.add(new_ninja2)

    games.screen.mainloop()
    sys.exit()

main()