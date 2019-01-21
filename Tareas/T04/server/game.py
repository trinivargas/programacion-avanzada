
from random import randint
import threading
from random import uniform
from time import sleep
from math import sin, cos


class Game(threading.Thread):

    def __init__(self, server, players_sockets, score):
        super().__init__()
        self.server = server
        self.players = players_sockets # dict de tipo {socket: number}
        self.n_players = len(players_sockets)
        self.started = False
        self.pause = True
        self.pplaying = {i: True for i in range(1, self.n_players + 1)}
        self.directions = {i: uniform(0, 6.34)
                           for i in range(1, self.n_players + 1)}
        self.score = score
        self.scores = {i: 0 for i in range(1, self.n_players + 1)}
        self.used_points = set()

    def pause_game(self):
        self.pause = not self.pause

    @property
    def end(self):
        playing = 0
        for value in self.pplaying.values():
            if value:
                playing += 1
        return playing < 1 # cambiar a 2

    def set_positions(self):
        positions = []
        while len(positions) <= self.n_players:
            x0, y0 = randint(100, 350), randint(100, 350)
            posible = True
            for x, y in positions:
                if x - 100 < x0 < x + 100 and y - 100 < y0 < y + 100:
                    posible = False
            if posible:
                positions.append([x0, y0])
        self.positions = {i: positions[i] for i in range(1, self.n_players + 1)}
        return {i: positions[i] for i in range(1, self.n_players + 1)}


    def run(self):
        update_position = threading.Thread(target=self.update_positions)
        update_position.start()


    def update_positions(self):
        sleep(1)
        while not self.end:
            if not self.pause:
                for i in range(1, self.n_players + 1):
                    # update positions
                    if self.pplaying[i]:
                        x, y = self.positions[i]
                        x += int(3 * cos(self.directions[i]))
                        y += int(3 * sin(self.directions[i]))
                        if not 0 <= x <= 450 or not 0 <= y <= 450 \
                                or (x, y) in self.used_points:
                            self.pplaying[i] = False
                        else:
                            self.positions[i] = [x, y]
                            self.used_points.add((x, y))

                self.server.update_positions(self.players.keys(), self.positions)
            sleep(0.09)


    def change_direction(self, direction, player_socket):
        player = self.players[player_socket]
        if direction == 'L':
            self.directions[player] += .15
        else:
            self.directions[player] -= .15

