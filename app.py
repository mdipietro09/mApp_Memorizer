###############################################################################
#                            RUN MAIN                                         #
###############################################################################

# setup
import warnings
warnings.filterwarnings("ignore")

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

import sqlite3  
import random



# app
class App(MDApp):
    ## basics
    def query_db(self, q, data=False):
        conn = sqlite3.connect("db.db")
        db = conn.cursor()
        db.execute(q)
        if data is True:
            lst_tuples_rows = db.fetchall()
        conn.commit()
        conn.close()
        return lst_tuples_rows if data is True else None

    def build(self):
        self.theme_cls.theme_style = "Light"
        q = "CREATE TABLE if not exists SAVED (category text, left text, right text)"
        self.query_db(q)
        return Builder.load_file("main.kv")


    ## play game
    def play(self):
        category = "1"
        q = f"SELECT left,right FROM SAVED WHERE category=={category}"
        lst_tuples_rows = self.query_db(q, data=True)
        tupla = random.choice(lst_tuples_rows)
        question, self.answer = tupla[0], tupla[1]
        self.root.get_screen('play').ids.question.text = f'{question}'
        self.root.get_screen('play').ids.answer.text = ''

    def show(self):
        self.root.get_screen('play').ids.answer.text = self.answer


    ## save
    def save(self):
        category = self.root.get_screen('save').ids.category.text
        left = self.root.get_screen('save').ids.left_input.text
        right = self.root.get_screen('save').ids.right_input.text
        q = f"INSERT INTO SAVED VALUES('{category}','{left}','{right}')"
        self.query_db(q)


    ## edit
    def edit(self):
        category = "1"
        q = f"SELECT left,right FROM SAVED WHERE category=={category}"
        lst_tuples_rows = self.query_db(q, data=True)
        table = MDDataTable(column_data=[("",dp(20)), ("",dp(20))], row_data=lst_tuples_rows,
                            size_hint=(0.9, 0.6), pos_hint={'center_x':0.5, 'center_y':0.4},
                            check=True, use_pagination=True, rows_num=20)
        table.bind(on_check_press=self.checked)
        table.bind(on_row_press=self.row_checked)
        self.root.get_screen('edit').add_widget(table)

    def checked(self, table, row):
        print(table)
        print(row)

    def row_checked(self, table, row):
        print(table)
        print(row)



# screens
class IntroScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class PlayScreen(Screen):
    def on_enter(self):
        App.answer = 'Push the right button to start'

class SaveScreen(Screen):
    pass

class EditScreen(Screen):
    pass



########################## Run ##########################
if __name__ == "__main__":
    App().run()
