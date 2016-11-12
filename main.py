import pygame
from random import randint
import scipy.io.wavfile
from threading import Thread

# For Python 2.7

# Separate draw functions into Threads and leave the main thread for
# the event loop. Code different drawing options to produce wildly
# different visuals per .wav file.


class AudioPainter:

    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.display = pygame.display.set_mode((self.width, self.height))
        self.filename = "Pi.wav"
        self.audio_data = self.get_audio_data()

        self.threads = []

    def get_audio_data(self):
        audio_data = scipy.io.wavfile.read(self.filename)
        return audio_data[1]

    @staticmethod
    def number_handler(data):
        if data[0] < 0:
            data[0] *= -1
        if data[1] < 0:
            data[1] *= -1
        while data[0] > 255:
            data[0] -= 255
        while data[1] > 255:
            data[1] -= 255

    def create_rect(self, color, x, y, length, height):
        pygame.draw.rect(self.display, color, (x, y, length, height))

    def create_circle(self, color, x, y, radius):
        pygame.draw.circle(self.display, color, (x, y), radius)

    def create_ellipse(self, color, x, y, length, height):
        pygame.draw.ellipse(self.display, color, (x, y, length, height))

    def draw(self, num, color, x, y, length=None, height=None, radius=None):
        if num % 2 == 0 and num % 5 == 0:
            self.create_rect(color, x, y, length, height)
        elif num % 2 == 0 and num % 3 == 0:
            self.create_circle(color, x, y, radius)
        else:
            self.create_ellipse(color, x, y, length, height)

    def run(self):
        for i, data in enumerate(self.audio_data):
            self.number_handler(data)
            color = (data[1], data[0], data[1])

            x, y = randint(1, self.width), randint(1, self.height)
            length, height = randint(1, 5), randint(1, 5)
            radius = randint(1, 5)

            self.draw(i, color, x, y, length, height, radius)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        while True:
            for thread in self.threads:
                thread.join()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


def main():
    AudioPainter().run()

if __name__ == "__main__":
    main()
