import json
import requests
import PySimpleGUI as sg
import shutil
import os
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

# OMDB public API with key to authenticate
imdb_title = 'http://www.omdbapi.com/?apikey=4ea39299&t='
imdb_search = 'http://www.omdbapi.com/?apikey=4ea39299&s='
auth_key = '4ea39299'

APP_NAME = 'Movietrck'

# Possible themes for GUI
THEME = ['Green', 'GreenTan', 'LightGreen', 'BluePurple', 'Purple',
         'BlueMono', 'GreenMono', 'BrownBlue', 'BrightColors',
         'NeutralBlue', 'Kayak', 'SandyBeach', 'TealMono', 'Topanga',
         'Dark', 'Black', 'DarkAmber']

# Background colors of every possible GUI
COLORS = {'Material1': '#E3F2FD',
          'Material2': '#FAFAFA',
          'Reddit': '#ffffff',
          'Topanga': '#282923',
          'GreenTan': '#9FB8AD',
          'Dark': '#404040',
          'LightGreen': '#B7CECE',
          'Dark2': '#404040',
          'Black': '#000000',
          'Tan': '#fdf6e3',
          'TanBlue': '#e5dece',
          'DarkTanBlue': '#242834',
          'DarkAmber': '#2c2825',
          'DarkBlue': '#1a2835',
          'Reds': '#280001',
          'Green': '#82a459',
          'BluePurple': '#A5CADD',
          'Purple': '#B0AAC2',
          'BlueMono': '#AAB6D3',
          'GreenMono': '#A8C1B4',
          'BrownBlue': '#64778d',
          'BrightColors': '#b4ffb4',
          'NeutralBlue': '#92aa9d',
          'Kayak': '#a7ad7f',
          'SandyBeach': '#efeccb',
          'TealMono': '#a8cfdd'}

ABOUT_MSG = '''
Movietrck

You can track your movie and TV series!
You just need to sign in or login and, 
then, you can access to IMDB, 
the biggest Movie Database in the world!

calax
All credits to IMDB/OMDB
2020
'''

# Title bar menu layout
menu = [
    ['&View', ['Profile',
               'Watchlist',
               'Wantlist']],
    ['&Theme', THEME],
    ['&Help', ['About']],
]


class ImageURL:

    def __init__(self, json_movie):
        """
        Loades and saves TV shows/movie posters from OMDB
        :param json_movie:
        """

        self.imageURL = json_movie['Poster']

    def getImage(self):

        resp = requests.get(self.imageURL, stream=True)

        local_file = open(os.getcwd() + '/local_image.jpg', 'wb')

        resp.raw.decode_content = True

        shutil.copyfileobj(resp.raw, local_file)

        im1 = Image.open(os.getcwd() + '/local_image.jpg')
        im1.save(os.getcwd() + '/local_image.png')

        path = os.getcwd() + '/local_image.png'

        return path


class OMDB_GUI:

    def __init__(self, user_file):

        """
        Main class representing GUI, logic, view and controller
        :param theme:
        :param user_file:
        """

        self.user_file = user_file
        self.menu_elem = None
        self.username = ''
        self.password = ''
        self.json_search = {}
        self.json_movie = {}
        self.watchlist = []
        self.want = []
        self.star_icon = os.getcwd() + "/star.png"

        # Default theme chosen
        self.gui_theme = 'DarkAmber'

    def add_to_watchlist(self, username):

        """
        Adds chosen TV show/movie to user personal watchlist
        :param username:
        """

        with open(self.user_file, 'r') as json_file:

            data = json.load(json_file)

        for i in range(len(data)):

            if data[i]['username'] == username:
                data[i]['watchlist'] = self.watchlist

                with open(self.user_file, 'w') as h:
                    json.dump(data, h, indent=4)

    def add_to_wantlist(self, username):

        """
        Adds chosen TV show/movie to user personal wantlist
        :param username:
        :return:
        """

        with open(self.user_file, 'r') as json_file:

            data = json.load(json_file)

        for i in range(len(data)):

            if data[i]['username'] == username:
                data[i]['wantlist'] = self.want

                with open(self.user_file, 'w') as h:
                    json.dump(data, h, indent=4)

    def init_user(self, username):

        """
        Inits user from configuration file (user_file)
        :param username:
        :return:
        """

        with open(self.user_file, 'r') as json_file:
            data = json.load(json_file)

        for i in range(len(data)):
            if data[i]['username'] == username:
                self.watchlist = data[i]['watchlist']
                self.want = data[i]['wantlist']

    def add_user(self, username, password):
        """
        Sign In case: if username doesn't exist in the configuration file, adds user, otherwise does not
        :param username:
        :param password:
        :return:
        """

        success = False

        with open(self.user_file, 'r') as json_file:
            data = json.load(json_file)

        present = False
        for i in range(len(data)):
            if data[i]['username'] == username:
                success = False
                present = True

                break

        if not present:
            self.username = username
            self.password = password
            data.append({'username': username, 'password': password, 'watchlist': '', 'wantlist': ''})
            success = True

            with open(self.user_file, 'w') as h:
                json.dump(data, h, indent=4)

        return success

    def check_user(self, username, password):
        """
        Log In case: check if user exists and/or password is correct, based on configuration file
        :param username:
        :param password:
        :return:
        """

        success = False

        with open(self.user_file, 'r') as json_file:
            data = json.load(json_file)

        present = False
        for i in range(len(data)):
            if data[i]['username'] == username:
                if data[i]['password'] == password:
                    present = True
                    success = True
                    break

        if not present:
            success = False

        return success

    def draw_figure(self, canvas, figure):

        """
        Draws/adds the figure in the canvas element of a window
        :param canvas:
        :param figure:
        :return:
        """

        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    def analyze_watchlist(self):

        """
        Analyze current watchlist in term of number of TV shows/movies
        :return:
        """

        tv_series = 0
        movie = 0
        movie_perc = 0
        tv_perc = 0

        if len(self.watchlist) > 0:
            for i in self.watchlist:

                r = requests.get(imdb_title + i)
                data = r.json()

                if data['Type'] == 'series':
                    tv_series = tv_series + 1
                elif data['Type'] == 'movie':
                    movie = movie + 1

        if len(self.watchlist) > 0:

            if movie > 0:
                movie_perc = (movie / (len(self.watchlist))) * 100

            if tv_series > 0:
                tv_perc = (tv_series / (len(self.watchlist))) * 100

        return tv_series, movie, movie_perc, tv_perc

    def create_new_window(self, window, login=False, signin=False, search=False, watchlist=False, wantlist=False,
                          main=False):

        """
            Create new window based on different layouts and close old one
            :param window:
            :param login:
            :param signin:
            :param search:
            :param watchlist:
            :param wantlist:
            :param main:
            :return:
            """

        loc = window.CurrentLocation()

        if signin == True:
            layout = self.build_signin_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

        if main == True:
            layout = self.build_main_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

        if wantlist == True:
            layout = self.build_wantlist_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

        if watchlist == True:
            layout = self.build_watchlist_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

        if login == True:

            layout = self.build_login_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

        elif search == True:

            layout = self.build_search_layout()

            w = sg.Window('{}'.format(APP_NAME),
                          layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          finalize=True,
                          location=(loc[0], loc[1]))

            window.Close()
            return w

    def create_title_window(self, window, json_movie):

        """
            Create new window in which chosen TV show/movie will be displayed
            :param window:
            :param json_data:
            :return:
            """

        loc = window.CurrentLocation()
        self.json_movie = json_movie
        layout = self.build_title_layout(json_movie=json_movie)

        w = sg.Window('{}'.format(APP_NAME),
                      layout,
                      grab_anywhere=True,
                      return_keyboard_events = True,
                      resizable = True,
                      default_button_element_size=(12, 1),
                      auto_size_buttons=False,
                      finalize=True,
                      location=(loc[0], loc[1]))

        window.Close()
        return w

    def create_show_match_window(self, window, json_data):

        """
            Create new window in which chosen TV show/movie will be displayed
            :param window:
            :param json_data:
            :return:
            """

        loc = window.CurrentLocation()
        self.json_data = json_data
        layout = self.build_show_match_layout(json_data=json_data)

        w = sg.Window('{}'.format(APP_NAME),
                      layout,
                      grab_anywhere=True,
                      return_keyboard_events = True,
                      resizable = True,
                      default_button_element_size=(12, 1),
                      auto_size_buttons=False,
                      finalize=True,
                      location=(loc[0], loc[1]))

        window.Close()
        return w

    def build_show_match_layout(self, json_data):

        """
        Creates Title (in which chosen TV show/movie will be displayed) window layout
        """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)
        titles = []

        json = json_data['Search']

        for j in json:

            titles.append(j['Title'])

        list = [self.single_list(x, titles, button=True) for x in range(0, len(titles))]

        menu_elem = sg.Menu(menu, tearoff=False)

        titles_layout = [
            [sg.Text("Search results:", font='Courier 25', key='title', size=(60, 1))],
            [sg.Text()],
            [sg.Column(list)],
            [sg.Text()],
            [sg.Button('Back')]
            ]

        layout = [[menu_elem],
                  [sg.Column(titles_layout, key='-COL1-', vertical_scroll_only=True, scrollable=True)]
                 ]

        return layout

    def build_profile(self, window):

        """
        Build layout and window for user profile (it can be chosen in titlebar)
        :param window:
        :return:
        """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)
        loc = window.CurrentLocation()

        menu_elem = sg.Menu(menu, tearoff=False)

        tv_series, movie, movie_perc, tv_perc = self.analyze_watchlist()

        if tv_series > 0 or movie > 0:

            values = [tv_series, movie]
            label = ['TV Shows', 'Movies']
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

            my_circle = plt.Circle((0, 0), 0.7, color=COLORS[self.gui_theme])

            fog, ax = plt.subplots()
            ax.grid(False)

            plt.pie(values, labels=label, colors=colors, autopct='%1.1f%%')
            fog.set_facecolor(COLORS[self.gui_theme])

            fig = plt.gcf()

            figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

            fig.gca().add_artist(my_circle)

            watchlist = [self.single_list(x, self.watchlist) for x in range(0, len(self.watchlist))]

            profile_layout1 = [
                [menu_elem],
                [sg.Text(f'{self.username}', font='Courier 40')],
                [sg.Text('')],
                [sg.Text('Watchlist', font='Courier 25', size = (30,1))],
                [sg.Text('')],
                [sg.Column(watchlist)]]

            wantlist = [self.single_list(x, self.want) for x in range(0, len(self.want))]

            profile_layout2 = [
                [sg.Text('')],
                [sg.Text('Wantlist', font='Courier 25', size = (30,1))],
                [sg.Text('')],
                [sg.Column(wantlist)]]

            profile_layout3 = [
                [sg.Text('')],
                [sg.Text(f'You\'ve watched {movie + tv_series} different productions:', font='Courier 20')],
                [sg.Text(f'{tv_series} TV shows ({round(tv_perc,1)}% of your total)', font='Courier 15')],
                [sg.Text(f'{movie} movies ({round(movie_perc,1)}% of your total)', font='Courier 15')],
                [sg.Canvas(size=(figure_w - 10, figure_h - 100), key='-CANVAS-', )],
                [sg.Button('Ok', bind_return_key=True)]
            ]

            layout = profile_layout1 + profile_layout2 + profile_layout3

            profile_layout = [

                [sg.Column(layout, vertical_scroll_only=True, scrollable=True)]

            ]

            w = sg.Window('{}'.format(APP_NAME),
                          profile_layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          location=(loc[0], loc[1]), finalize=True)

            self.draw_figure(w['-CANVAS-'].TKCanvas, fig)

        else:

            profile_layout = [
                [menu_elem],
                [sg.Text(f'{self.username}', font='Courier 40')],
                [sg.Text('')],
                [sg.Text('No titles in your lists yet!', font='Courier 16')],
                [sg.Text('')],
                [sg.Button('Ok', bind_return_key=True)]
            ]

            w = sg.Window('{}'.format(APP_NAME),
                          profile_layout,
                          grab_anywhere=True,
                          return_keyboard_events = True,
                          resizable = True,
                          default_button_element_size=(12, 1),
                          auto_size_buttons=False,
                          location=(loc[0], loc[1]))

        window.Close()
        return w

    def build_main_layout(self):

        """
         Creates main page layout
         """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        menu_elem = sg.Menu(menu, tearoff=False)

        search_layout = [
            [sg.Text('Welcome to your personal Movie Database', justification='center', font='Courier 20')],
            [sg.Text('')],
            [sg.Button('Login', font = 'Courier 20')],
            [sg.Button('Sign In', font = 'Courier 20')],
            [sg.Text('')],
        ]

        layout = [[menu_elem],
                  [sg.Column(search_layout, justification= 'center', element_justification='center', key='-COL1-')]
                  ]

        return layout

    def build_search_layout(self):

        """
            Creates search window layout
            """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        menu_elem = sg.Menu(menu, tearoff=False)

        search_layout = [
            [sg.Text('Look for a TV show or a movie', font='Courier 25')],
            [sg.Text('Insert the title:', font='Courier 20'), sg.Input(font="Courier 20")],
            [sg.Button('Ok', bind_return_key=True), sg.Button('Cancel')]
        ]

        layout = [[menu_elem],
                  [sg.Column(search_layout, key='-COL1-')]
                  ]

        return layout

    def build_login_layout(self):

        """
            Creates Log In window layout
            """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        menu_elem = sg.Menu(menu, tearoff=False)

        login_layout = [
            [sg.Text('Welcome back!', font='Courier 25')],
            [sg.Text('Username:', font='Courier 20'), sg.InputText(font="Courier 20")],
            [sg.Text('Password:', font='Courier 20'), sg.InputText(font="Courier 20",password_char='*')],
            [sg.Button('Ok', bind_return_key=True), sg.Button('Back'), sg.Button('Cancel')]
        ]

        layout = [[menu_elem],
                  [sg.Column(login_layout, key='-COL1-')]
                  ]

        return layout

    def build_signin_layout(self):

        """
        Creates Sign In window layout
        """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        menu_elem = sg.Menu(menu, tearoff=False)

        login_layout = [
            [sg.Text('Welcome!', font='Courier 25')],
            [sg.Text('Choose your username:', font='Courier 20'), sg.Input(font="Courier 20")],
            [sg.Text('Choose your password:', font='Courier 20'), sg.Input(font="Courier 20", password_char='*')],
            [sg.Button('Ok', bind_return_key=True), sg.Button('Back'), sg.Button('Cancel')]
        ]

        layout = [[menu_elem],
                  [sg.Column(login_layout, key='-COL1-')]
                  ]

        return layout

    def build_title_layout(self, json_movie):

        """
        Creates Title (in which chosen TV show/movie will be displayed) window layout
        """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        image = ImageURL(json_movie).getImage()

        menu_elem = sg.Menu(menu, tearoff=False)

        title_layout = [
            [sg.Text(json_movie['Title'] + " (" + json_movie['Year'] + ")", font='Courier 25', key='title', size=(70, 1)), sg.Image(self.star_icon, size=(16,16)), sg.Text(json_movie['imdbRating'], font='Courier 22')],
            [sg.Image(image, key='poster')],
            [sg.Text('Genre', font='Courier 20')],
            [sg.Text(json_movie['Genre'], font='Courier 15', key='genre', size=(60, 1))],
            [sg.Text('Plot', font='Courier 20')],
            [sg.Text(json_movie['Plot'], font='Courier 15', key='plot', size=(80, 3))],
            [sg.Text('Actors', font='Courier 20')],
            [sg.Text(json_movie['Actors'], font='Courier 15', key='actors', size=(80, 1))],
            [sg.Button('Add to watchlist'), sg.Button('Add to wantlist'), sg.Button('Back')]]

        layout = [[menu_elem],
                  [sg.Column(title_layout, key='-COL1-')]
                  ]

        return layout


    def single_list(self, i, list, button=False):

        """
        Defines the list of rows of a single list (watchlist or wantlist
        :param i:
        :param list:
        :return:
        """

        if button == True:

            return [sg.Button(list[i], font = 'Courier 20', size=(20,1))]

        else:

            return [sg.Text(list[i], font = 'Courier 20', size=(20,1))]

    def multi_list(self, i, list1, list2, button=False):

        """
        Defines the list of rows of a single list (watchlist or wantlist
        :param i:
        :param list:
        :return:
        """

        if button == True:

            return [sg.Button(list1[i] + " (" + list2[i] + ")", font = 'Courier 20', size=(20,1))]

        else:

            return [sg.Text(list1[i] + " (" + list2[i] + ")", font = 'Courier 20', size=(20,1))]


    def build_watchlist_layout(self):

        """
         Creates user watchlist window layout
         """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        tv_series, movie, movie_perc, tv_perc = self.analyze_watchlist()

        menu_elem = sg.Menu(menu, tearoff=False)

        watchlist = [self.single_list(x, self.watchlist) for x in range(0, len(self.watchlist))]

        watchlist_layout1 = [

            [sg.Text('Here\'s your watchlist!', font='Courier 25', key='genre', size=(30, 1))],
            [sg.Text('')],
            [sg.Column(watchlist, key='watch')]
                ]


        watchlist_layout2 = [
            [sg.Text('')],
            [sg.Text(f'{tv_series} TV shows ({round(tv_perc,1)}% of your total)', font='Courier 15')],
            [sg.Text(f'{movie} movies ({round(movie_perc,1)}% of your total)', font='Courier 15')],
            [sg.Button('Ok', bind_return_key=True)]
        ]

        watchlist_layout = watchlist_layout1 + watchlist_layout2

        if len(watchlist) > 15:

            layout = [[menu_elem],
                     [sg.Column(watchlist_layout, key='-COL1-', vertical_scroll_only=True, scrollable=True)]]

        else:

            layout = [[menu_elem],
                     [sg.Column(watchlist_layout, key='-COL1-')]]

        return layout

    def build_wantlist_layout(self):

        """
         Creates user wantlist window layout
         """

        sg.ChangeLookAndFeel(self.gui_theme)
        sg.SetOptions(margins=(0, 3), border_width=1)

        menu_elem = sg.Menu(menu, tearoff=False)

        wantlist = [self.single_list(x, self.want) for x in range(0, len(self.want))]

        wantlist_layout1 = [

            [sg.Text('Here\'s your wantlist!', font='Courier 25', key='genre', size=(30, 1))],
            [sg.Text('')],
            [sg.Column(wantlist, key='want')]
                ]

        wantlist_layout2 = [
            [sg.Text('')],
            [sg.Button('Ok', bind_return_key=True)]
        ]

        wantlist_layout = wantlist_layout1 + wantlist_layout2

        if len(wantlist) > 15:

            layout = [[menu_elem],
                     [sg.Column(wantlist_layout, key='-COL1-', vertical_scroll_only=True, scrollable=True)]]

        else:

            layout = [[menu_elem],
                     [sg.Column(wantlist_layout, key='-COL1-')]]

        return layout

    def check_user_interaction(self, window, signin=False, search=False, title=False, login=False, watchlist=False,
                               wantlist=False, main=False, profile=False, show_match=False):

        """
        Converts user interaction with windows in behaviours
        :param window:
        :param signin:
        :param search:
        :param title:
        :param login:
        :param watchlist:
        :param wantlist:
        :param main:
        :param profile:
        :return:
        """

        if profile == True:

            while True:

                button, values = window.read()

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    window = self.create_new_window(window, watchlist=True)
                    self.check_user_interaction(window, watchlist=True)

                if button == 'Wantlist':
                    window = self.create_new_window(window, wantlist=True)
                    self.check_user_interaction(window, wantlist=True)

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.build_profile(window)
                    continue

                if button == 'Ok':
                    window = self.create_new_window(window, search=True)
                    self.check_user_interaction(window, search=True)

        if show_match == True:

            titles = []

            json = self.json_data['Search']

            for j in json:

                titles.append(j['Title'])

            while True:

                button, values = window.read()

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    window = self.create_new_window(window, watchlist=True)
                    self.check_user_interaction(window, watchlist=True)

                if button == 'Wantlist':
                    window = self.create_new_window(window, wantlist=True)
                    self.check_user_interaction(window, wantlist=True)

                if button == 'Back':
                    window = self.create_new_window(window, search=True)
                    self.check_user_interaction(window, search=True)

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.build_profile(window)
                    continue

                if button in titles:

                    try:

                        r = requests.get(imdb_title + button)
                        json_movie = r.json()
                        self.json_movie = json_movie

                        window = self.create_title_window(window, self.json_movie)
                        self.check_user_interaction(window, title=True)

                    except:

                        sg.PopupError('This title doesn\'t exixt, try again!')
                        continue

        if signin == True:

            while True:

                button, values = window.Read()

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    sg.PopupError('Sign In first!')

                if button == 'Wantlist':
                    sg.PopupError('Sign In first!')

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, signin=True)
                    continue

                if button == 'Ok':

                    if self.add_user(values[1], values[2]) == True:

                        sg.Popup('Signed succesfully!')
                        window = self.create_new_window(window, search=True)
                        self.check_user_interaction(window, search=True)

                    else:

                        sg.PopupError('Username already in use!')
                        continue

                if button == 'Cancel':
                    window.Close()
                    break

                if button == 'Back':
                    window = self.create_new_window(window, main=True)
                    self.check_user_interaction(window, main=True)

        if main == True:

            while True:

                button, values = window.Read()

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    sg.PopupError('Access first!')

                if button == 'Wantlist':
                    sg.PopupError('Access first!')

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, main=True)
                    continue

                if button == 'Login':
                    window = self.create_new_window(window, login=True)
                    self.check_user_interaction(window, login=True)

                if button == 'Sign In':
                    window = self.create_new_window(window, signin=True)
                    self.check_user_interaction(window, signin=True)

        if watchlist == True:

            while True:

                button, values = window.Read()

                if button == 'Profile':
                    window = self.build_profile(window)
                    self.check_user_interaction(window, profile=True)

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    sg.PopupError('Already displaying!')

                if button == 'Wantlist':
                    window = self.create_new_window(window, wantlist=True)
                    self.check_user_interaction(window, wantlist=True)

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, watchlist=True)
                    continue

                if button == 'Ok':
                    window = self.create_new_window(window, search=True)
                    self.check_user_interaction(window, search=True)

        if wantlist == True:

            while True:

                button, values = window.Read()

                if button == 'Profile':
                    window = self.build_profile(window)
                    self.check_user_interaction(window, profile=True)

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    window = self.create_new_window(window, watchlist=True)
                    self.check_user_interaction(window, watchlist=True)

                if button == 'Wantlist':
                    sg.PopupError('Already displaying')

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, wantlist=True)
                    continue

                if button == 'Ok':
                    window = self.create_new_window(window, search=True)
                    self.check_user_interaction(window, search=True)

        if title == True:

            while True:

                button, values = window.Read()

                if button == 'Profile':
                    window = self.build_profile(window)
                    self.check_user_interaction(window, profile=True)

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    window = self.create_new_window(window, watchlist=True)
                    self.check_user_interaction(window, watchlist=True)

                if button == 'Wantlist':
                    window = self.create_new_window(window, wantlist=True)
                    self.check_user_interaction(window, wantlist=True)

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_title_window(window, self.json_data)
                    continue

                if button == 'Add to watchlist':

                    if self.json_movie['Title'] not in self.watchlist:

                        self.watchlist.append(self.json_movie['Title'])
                        self.add_to_watchlist(self.username)
                        sg.Popup('Title added to your watchlist!')

                    else:

                        sg.Popup('Title already in your watchlist')
                        continue

                if button == 'Add to wantlist':

                    if (self.json_movie['Title'] not in self.want) and (self.json_movie['Title'] not in self.watchlist):

                        self.want.append(self.json_movie['Title'])
                        self.add_to_wantlist(self.username)
                        sg.Popup('Title added to your wantlist!')

                    elif self.json_movie['Title'] in self.watchlist:

                        sg.Popup('Title already in your watchlist')
                        continue

                    elif self.json_movie['Title'] in self.want:

                        sg.Popup('Title already in your wantlist')
                        continue

                if button == 'Back':
                    window = self.create_new_window(window, search=True)
                    self.check_user_interaction(window, search=True)

        if login == True:

            while True:

                button, value = window.read()

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    sg.PopupError('Login first!')

                if button == 'Wantlist':
                    sg.PopupError('Login first!')

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, login=True)
                    continue

                if button == 'Ok':

                    if self.check_user(value[1], value[2]) == True:

                        sg.Popup('Successful login!')
                        self.username = value[1]
                        self.password = value[2]
                        self.init_user(self.username)
                        window = self.create_new_window(window, search=True)
                        self.check_user_interaction(window, search=True)

                    else:

                        sg.PopupError('Invalid username or password')
                        continue

                if button == 'Cancel':
                    window.Close()
                    break

                if button == 'Back':
                    window = self.create_new_window(window, main=True)
                    self.check_user_interaction(window, main=True)

        if search == True:

            while True:

                button, values = window.read()

                if button == 'Profile':
                    window = self.build_profile(window)
                    self.check_user_interaction(window, profile=True)

                if button == 'About':
                    sg.PopupScrolled(ABOUT_MSG, title='Help/About')
                    continue

                if button == 'Watchlist':
                    window = self.create_new_window(window, watchlist=True)
                    self.check_user_interaction(window, watchlist=True)

                if button == 'Wantlist':
                    window = self.create_new_window(window, wantlist=True)
                    self.check_user_interaction(window, wantlist=True)

                if button is None:

                    window.Close()
                    break

                if button in THEME:
                    self.gui_theme = button
                    window = self.create_new_window(window, search=True)
                    continue

                if button == 'Ok':

                   try:

                        r = requests.get(imdb_search + str(values[1]))
                        json_data = r.json()
                        self.json_data = json_data

                        window = self.create_show_match_window(window, json_data)
                        self.check_user_interaction(window, show_match=True)

                   except:

                        sg.PopupError('This title doesn\'t exixt, try again!')
                        continue

                if button == 'Cancel':
                    window.Close()
                    break

    def mainPage(self):

        """
        Defines the first window user will see
        :return:
        """

        layout = self.build_main_layout()

        window = sg.Window('{}'.format(APP_NAME),
                           layout,
                           grab_anywhere=True,
                           return_keyboard_events = True,
                           resizable = True,
                           default_button_element_size=(12, 1),
                           auto_size_buttons=False)

        self.check_user_interaction(window, main=True)


def main():

    user_file = os.getcwd() + '/user.json'

    imdb = OMDB_GUI(user_file)

    imdb.mainPage()


if __name__ == "__main__":
    main()
