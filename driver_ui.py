"""
Autor   : Mr Leopard
License : MIT
"""
import os
import sys
import time
import copy
from tkinter import Tk, Text, END, Scrollbar
import webbrowser
from content_provider import Provider


class NewUi(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title("cmder")
        # self.wm_attributes("-toolwindow", 2)
        self.geometry('800x600')
        self.bind("<Key>", self.on_key_event)
        self.full_screen = False
        self.attributes('-fullscreen', self.full_screen)

        ico = os.path.join(os.path.dirname(__file__), "myicon.ico")
        if os.path.exists(ico):
            if sys.platform == "win32":
                self.iconbitmap(ico)
            else:
                self.iconbitmap()

        scrollbar = Scrollbar(self, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.text_size = 12
        self.font = "msyh"
        self.text_area = Text(self, background="#323232", font=(self.font, self.text_size),
                              yscrollcommand=scrollbar.set, spacing1=5, spacing2=7, spacing3=7)
        self.text_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_area.yview)

        self.provider = Provider()
        self.text_color = "#D6D6D6"
        self.window_content = None
        self.insert(self.provider.get_dozen())

    def switch_color(self):
        if self.text_area["background"] == "#323232":
            self.text_area["background"] = "#D6D6D6"
            self.text_color = "#323232"

        else:
            self.text_area["background"] = "#323232"
            self.text_color = "#D6D6D6"

        # self.text_area.tag_configure(self.text_color, foreground=self.text_color)
        # self.text_area.tag_add(self.text_color, "1.0", END)
        # self.text_area.config(fg=self.text_color)
        # self.text_area.see(END)
        # self.insert_titles(self.provider.get_dozen("current"))

        self.insert(self.window_content)

    def clear_text(self):
        self.text_area.delete("1.0", END)

    def insert(self, content):
        self.clear_text()
        self.window_content = content
        if type(content) == list:
            n = 65
            for i in content:
                self.text_area.tag_configure(self.text_color, foreground=self.text_color)
                self.text_area.insert(END, f"{chr(n)}、 {i['title']}---[{i['time']}]\n", self.text_color)
                self.text_area.see(END)
                n += 1

        elif type(content) == dict:
            self.clear_text()
            self.text_area.insert(END, f'【{content["title"]}】\n', self.text_color)
            self.text_area.insert(END, f'{content["time"]} {content["url"]} \n', self.text_color)
            for t in self.provider.get_new_content_text(content):
                self.text_area.insert(END, f'{t}\n', self.text_color)
        # self.text_area.see(END)

    def insert_content(self, key):
        s = self.window_content[key - 65]
        self.clear_text()
        self.insert(s)

    def change_news(self, direction=""):
        step = 0
        if direction == "Next":
            step = 1
        elif direction == "Prior":
            step = -1
        __current_news = copy.deepcopy(self.window_content)
        # print(self.provider.get_dozen("current"))
        __news_index = self.provider.get_dozen("current").index(__current_news)
        point_index = __news_index + step
        if point_index < 0:
            if self.provider.content["index"] == 0:
                pass
            else:
                self.insert(self.provider.get_dozen("previous")[-1])

        elif point_index >= len(self.provider.get_dozen("current")):
            self.insert(self.provider.get_dozen("next")[0])
        else:
            self.insert(self.provider.get_dozen("current")[point_index])

    def on_key_event(self, event):
        # print(event.keycode, event.keysym)
        if event.keysym == "equal":
            if self.text_size < 60:
                self.text_size += 1
                self.text_area.configure(font=(self.font, self.text_size))
                time.sleep(0.1)
        elif event.keysym == "minus":
            if self.text_size > 2:
                self.text_size -= 1
                self.text_area.configure(font=(self.font, self.text_size))
            time.sleep(0.1)
        elif event.keysym == "slash":
            self.switch_color()
        elif event.keysym == "Right" and type(self.window_content) == list:
            self.title(self.title() + "  loading...")
            self.insert(self.provider.get_dozen("next"))
            self.title(self.title().replace("  loading...", ""))
        elif event.keysym == "Left" and type(self.window_content) == list:
            self.insert(self.provider.get_dozen("previous"))
        elif type(self.window_content) == list and \
                event.keycode in range(65, len(self.window_content) + 65):
            self.title(self.title() + "  loading...")
            self.insert_content(event.keycode)
            self.title(self.title().replace("  loading...", ""))
        elif event.keysym == "BackSpace":
            self.insert(self.provider.get_dozen("current"))
        elif type(self.window_content) == dict and event.keysym in ["b", "B"]:
            webbrowser.open(self.window_content["url"])

        elif type(self.window_content) == dict and event.keysym == "Down":
            self.text_area.yview_scroll(1, "unit")
        elif type(self.window_content) == dict and event.keysym == "Up":
            self.text_area.yview_scroll(-1, "unit")

        elif type(self.window_content) == dict and event.keysym == "Next":
            self.title(self.title() + "  loading...")
            self.change_news("Next")
            self.title(self.title().replace("  loading...", ""))

        elif type(self.window_content) == dict and event.keysym == "Prior":
            self.title(self.title() + "  loading...")
            self.change_news("Prior")
            self.title(self.title().replace("  loading...", ""))

        elif event.keysym == "0":
            self.full_screen = not self.full_screen
            self.attributes('-fullscreen', self.full_screen)


if __name__ == "__main__":
    nu = NewUi()
    nu.mainloop()
