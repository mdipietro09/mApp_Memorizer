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
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

import sqlite3  
import random



# app
class App(MDApp):
    ## basics
    dialog = None

    def alert_dialog(self, error):
        if not self.dialog:
            self.dialog = MDDialog(text=error)
        self.dialog.open()
        self.dialog = None

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
        q = "CREATE TABLE if not exists SAVED (category text, left text, right text, unique (category,left,right))"
        self.query_db(q)
        return Builder.load_file("main.kv")


    ## play game
    def play(self):
        try:
            category = "1"
            q = f"SELECT left,right FROM SAVED WHERE category=={category}"
            lst_tuples_rows = self.query_db(q, data=True)
            tupla = random.choice(lst_tuples_rows)
            question, self.answer = tupla[0], tupla[1]
            self.root.get_screen('play').ids.question.text = f'{question}'
            self.root.get_screen('play').ids.answer.text = ''
        
        except Exception as e:
            if "empty" in str(e): 
                self.alert_dialog("First you need to save something")

    def show(self):
        self.root.get_screen('play').ids.answer.text = self.answer


    ## save
    def save(self):
        try:
            category = self.root.get_screen('save').ids.category.text
            left = self.root.get_screen('save').ids.left_input.text
            right = self.root.get_screen('save').ids.right_input.text
            if "" in [category.strip(), left.strip(), right.strip()]:
                self.alert_dialog("Fields are required")
            else:
                q = f"INSERT INTO SAVED VALUES('{category}','{left}','{right}')"
                self.query_db(q)

        except Exception as e:
            if "UNIQUE" in str(e):
                self.alert_dialog("This is already saved")


    ## edit
    def dropdown(self):
        lst_categories = [i[0] for i in self.query_db(q="SELECT DISTINCT category FROM SAVED", data=True)]
        items = [{"text":f"{i}", 
                  "viewclass":"OneLineListItem",
                  "on_release": lambda x=f"{i}": self.edit(x)
                  } for i in lst_categories]
        self.all_categories = MDDropdownMenu(caller=self.root.get_screen('edit').ids.category_dropdown, items=items, width_mult=4)
        self.all_categories.open()

    def edit(self, category=None):
        self.all_categories.dismiss()
        self.category = category if category is not None else self.category
        
        q = f"SELECT left,right FROM SAVED WHERE category=='{category}'"
        lst_tuples_rows = self.query_db(q, data=True)
        table = MDDataTable(column_data=[("",dp(20)), ("",dp(20))], row_data=lst_tuples_rows,
                            size_hint=(0.9, 0.6), pos_hint={'center_x':0.5, 'center_y':0.4},
                            check=True, use_pagination=True, rows_num=20)
        table.bind(on_check_press=self.selected)
        self.root.get_screen('edit').add_widget(table)

    def selected(self, table, row):
        if row not in self.lst_rows:
            self.lst_rows.append(row)
        else:
            self.lst_rows.remove(row)

    def delete(self):
        if len(self.lst_rows) > 0:
            for row in self.lst_rows:
                left, right = row[0], row[1]
                q = f"DELETE FROM SAVED WHERE left=='{left}' AND right=='{right}'"
                self.query_db(q)
        self.edit()       



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
    def on_enter(self):
        App.lst_rows = []
        App.empty_msg = "No rows selected"



########################## Run ##########################
if __name__ == "__main__":
    App().run()
