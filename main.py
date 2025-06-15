import random
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

# Deutsche Buchstabenverteilung laut Bananagrams
DE_BANANA_LETTERS = (
    'A'*5 + 'B'*2 + 'C'*2 + 'D'*3 + 'E'*15 + 'F'*2 + 'G'*3 + 'H'*4 + 'I'*6 +
    'J'*1 + 'K'*2 + 'L'*3 + 'M'*4 + 'N'*9 + 'O'*3 + 'P'*1 + 'Q'*1 + 'R'*6 +
    'S'*7 + 'T'*6 + 'U'*6 + 'V'*1 + 'W'*1 + 'X'*1 + 'Y'*1 + 'Z'*1 + 'Ä'*1 + 'Ö'*1 + 'Ü'*1 + 'ß'*1
)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        layout.add_widget(Label(text='Bananagrams\n(Copyright Wilhelm Gr\u00fcndler)', font_size=20))
        layout.add_widget(Button(text='Spiel starten', font_size=32, on_press=self.start_game))
        layout.add_widget(Button(text='Beenden', font_size=32, on_press=App.get_running_app().stop))
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hand = []
        self.board = [[None for _ in range(15)] for _ in range(15)]
        self.selected_letter = None

        self.main_layout = BoxLayout(orientation='vertical')
        self.grid = GridLayout(cols=15, size_hint=(1, 0.6))
        self.grid_buttons = []
        for y in range(15):
            for x in range(15):
                btn = Button(text='', font_size=24, background_color=[1, 1, 1, 1])
                btn.bind(on_press=self.grid_click)
                self.grid.add_widget(btn)
                self.grid_buttons.append(btn)

        self.hand_layout = GridLayout(cols=10, size_hint=(1, 0.2))
        self.hand_buttons = []

        self.controls = BoxLayout(size_hint=(1, 0.1))
        self.controls.add_widget(Button(text='Peel', on_press=self.peel))
        self.controls.add_widget(Button(text='Dump', on_press=self.dump))
        self.controls.add_widget(Button(text='Neu starten', on_press=self.confirm_restart))
        self.controls.add_widget(Button(text='Wörter prüfen', on_press=self.check_words))

        self.main_layout.add_widget(Label(text='Copyright Wilhelm Gründler', size_hint=(1, 0.05)))
        self.main_layout.add_widget(self.grid)
        self.main_layout.add_widget(self.controls)
        self.main_layout.add_widget(self.hand_layout)
        self.add_widget(self.main_layout)

        self.reset_game()

    def reset_game(self):
        letters = list(DE_BANANA_LETTERS)
        random.shuffle(letters)
        self.letter_pool = letters
        self.hand.clear()
        for _ in range(21):
            self.hand.append(self.letter_pool.pop())
        self.update_hand()
        for btn in self.grid_buttons:
            btn.text = ''

    def update_hand(self):
        self.hand.sort()
        self.hand_layout.clear_widgets()
        self.hand_buttons.clear()
        for l in self.hand:
            btn = Button(text=l, font_size=24)
            btn.bind(on_press=self.hand_click)
            self.hand_buttons.append(btn)
            self.hand_layout.add_widget(btn)

    def hand_click(self, instance):
        self.selected_letter = instance.text

    def grid_click(self, instance):
        if instance.text != '' and self.selected_letter is None:
            self.hand.append(instance.text)
            instance.text = ''
            self.update_hand()
        elif self.selected_letter:
            if instance.text == '':
                instance.text = self.selected_letter
                self.hand.remove(self.selected_letter)
                self.selected_letter = None
                self.update_hand()

    def peel(self, instance):
        if len(self.hand) > 0:
            popup = Popup(title='Fehler', content=Label(text='Du musst zuerst alle Buchstaben legen!'), size_hint=(0.8, 0.3))
            popup.open()
            return
        if len(self.letter_pool) >= 1:
            self.hand.append(self.letter_pool.pop())
            self.update_hand()

    def dump(self, instance):
        if self.selected_letter:
            self.letter_pool.insert(0, self.selected_letter)
            self.hand.remove(self.selected_letter)
            for _ in range(3):
                if self.letter_pool:
                    self.hand.append(self.letter_pool.pop())
            self.selected_letter = None
            self.update_hand()

    def confirm_restart(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Sicher? Spiel wirklich neu starten?'))
        btns = BoxLayout()
        popup = Popup(title='Bestätigung', content=content, size_hint=(0.8, 0.4))
        btns.add_widget(Button(text='Ja', on_press=lambda x: self.restart_game(popup)))
        btns.add_widget(Button(text='Nein', on_press=lambda x: popup.dismiss()))
        content.add_widget(btns)
        popup.open()

    def restart_game(self, popup):
        popup.dismiss()
        self.reset_game()

    def check_words(self, instance):
        if not self.is_board_connected():
            popup = Popup(title='Fehler', content=Label(text='Alle Wörter müssen verbunden sein!'), size_hint=(0.8, 0.3))
            popup.open()
            return
        words = self.get_board_words()
        invalid = [w for w in words if not self.is_valid_word(w)]
        text = 'Alle Wörter gültig!' if not invalid else f'Ungültig: {", ".join(invalid)}'
        popup = Popup(title='Wörterprüfung', content=Label(text=text), size_hint=(0.8, 0.4))
        popup.open()

    def get_board_words(self):
        words = set()
        for row in range(15):
            line = ''.join(self.grid_buttons[row * 15 + col].text or ' ' for col in range(15))
            words.update([w for w in line.split() if len(w) > 1])
        for col in range(15):
            line = ''.join(self.grid_buttons[row * 15 + col].text or ' ' for row in range(15))
            words.update([w for w in line.split() if len(w) > 1])
        return list(words)

    def is_valid_word(self, word):
        try:
            url = "https://de.wiktionary.org/w/api.php"
            params = {
                "action": "query",
                "titles": word.lower(),
                "format": "json"
            }
            r = requests.get(url, params=params, timeout=5)
            pages = r.json().get("query", {}).get("pages", {})
            return "-1" not in pages
        except:
            return False

    def is_board_connected(self):
        visited = set()

        def get_neighbors(x, y):
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 15 and 0 <= ny < 15:
                    yield nx, ny

        def dfs(x, y):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                for nx, ny in get_neighbors(cx, cy):
                    btn = self.grid_buttons[ny * 15 + nx]
                    if btn.text and (nx, ny) not in visited:
                        stack.append((nx, ny))

        for y in range(15):
            for x in range(15):
                if self.grid_buttons[y * 15 + x].text:
                    dfs(x, y)
                    break
            else:
                continue
            break

        total_letters = sum(1 for btn in self.grid_buttons if btn.text)
        return len(visited) == total_letters


class BananagramsApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    BananagramsApp().run()
