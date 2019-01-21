import threading
from random import choice

class WaitingRoom:
    colors = ['red', 'yellow', 'green', 'magenta', 'cyan', 'white']

    def __init__(self):
        #super().__init__()
        self.players = {} # number: socket
        self.players_number = {} #socket: number
        self.usernames = {}
        self.colors = {color: None for color in WaitingRoom.colors}
        self.players_color = {}
        self.chief = None
        self.score = 10
        self.powers = list()
        self.speed = 2
        self.new_msgs = ''
        self.chosen_colors = set()
        self.arrival = []
        self.open = True
        self.count_down = False

    def add_player(self, client_socket, username):
        if not self.open:
            return False
        if self.players.get(1) is None:
            d = self._add_player(client_socket, 1, username)
        elif self.players.get(2) is None:
            d = self._add_player(client_socket, 2, username)
        elif self.players.get(3) is None:
            d = self._add_player(client_socket, 3, username)
        elif self.players.get(4) is None:
            d = self._add_player(client_socket, 4, username)
        else:
            self.open = False
            return False
        return d

    def _add_player(self, client_socket, number, username):
        self.players[number] = client_socket
        self.players_number[client_socket] = number
        self.set_color(number)
        self.set_chief(number)
        self.usernames[number] = username
        self.arrival.append(number)
        return number, self.data

    def set_color(self, number):
        chosen = False
        while not chosen:
            color = choice(WaitingRoom.colors)
            chosen = color not in self.chosen_colors
        self.chosen_colors.add(color)
        self.colors['color'] = number
        self.players_color[int(number)] = color
        return color

    def set_chief(self, number):
        if self.chief is None:
            self.chief = number
            return True
        return False

    @property
    def data(self):
        d = {'colors': self.colors, 'chief': self.chief, 'score': self.score,
             'new msgs': self.new_msgs,
             'powers': self.powers, 'usernames': self.usernames,
             'speed': self.speed, 'usernames colors': self.usernames_colors}
        return d

    @property
    def usernames_colors(self):
        d = dict()
        j = 1
        for i in self.arrival:
            if self.players.get(i) is not None:
                d[j] = [self.usernames[i], self.players_color[i]]
                j += 1
        return d

    @property
    def players_sockets(self):
        return self.players_number.keys()

    def change_color(self, client_socket, new_color, old_color):
        if new_color in self.chosen_colors:
            return False
        n = self.players_number[client_socket]
        self.colors[old_color] = None
        self.colors[new_color] = n
        self.chosen_colors.add(new_color)
        self.chosen_colors.remove(old_color)
        return new_color

    def exit_player(self, client_socket):
        if self.count_down:
            return 'countdown'
        n = int(self.players_number[client_socket])
        del self.players_number[client_socket]
        self.arrival.pop(self.arrival.index(n))
        change_chief = False
        if self.chief == n and len(self.arrival):
            self.chief = self.arrival[0]
            change_chief = True
            self.change_chief()
        elif self.chief == n:
            self.chief = None
        del self.players[n]
        color = self.players_color[n]
        self.chosen_colors.remove(color)
        del self.players_color[n]
        self.colors[color] = None
        del self.usernames[n]
        self.open = True
        if change_chief:
            return self.change_chief()

    def change_chief(self):
        return self.players[self.chief], self.chief, self.data

    def update_powers(self, powers):
        self.powers = powers

    def update_colors(self, h):
        pass

    def new_msg(self, msg):
        self.new_msgs += msg
        return self.players_number.keys(), msg

    def info_game(self):
        self.count_down = True
        self.open = False
        return self.players_number, self.players_color, self.usernames, \
               self.score











