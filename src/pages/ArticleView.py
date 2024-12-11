# src/pages/ArticleView.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from logic.DatabaseManager import DatabaseManager
from config import COLOR_BACKGROUND, COLOR_TEXT

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class ArticleView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.selected_article_id = None
        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Articles", font=("Arial", 16, "bold"), foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        title_label.pack(pady=10)

        content_frame = ttk.Frame(self, style='MainContent.TFrame')
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.article_listbox = tk.Listbox(content_frame, width=30)
        self.article_listbox.pack(side="left", fill="y")
        self.article_listbox.bind('<<ListboxSelect>>', self.on_article_select)

        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.article_listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.article_listbox.config(yscrollcommand=scrollbar.set)

        self.preview_area = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=60, bg=COLOR_BACKGROUND, fg=COLOR_TEXT, state=tk.DISABLED)
        self.preview_area.pack(side="left", fill="both", expand=True, padx=10)

        self.load_articles()

    def load_articles(self):
        db.connect()
        articles = db.read("ArticleDatabase", ["article_id", "article_name", "article_author"], None, False)
        db.disconnect()

        self.article_list = articles
        self.article_listbox.delete(0, tk.END)
        for article in articles:
            self.article_listbox.insert(tk.END, f"{article[1]} by {article[2]}")

    def on_article_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            article = self.article_list[index]
            self.display_article(article[0])

    def display_article(self, article_id):
        db.connect()
        article = db.read("ArticleDatabase", ["text"], {"article_id": article_id}, True)
        db.disconnect()

        if article:
            self.preview_area.config(state=tk.NORMAL)
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.insert(tk.END, article[0])
            self.preview_area.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Failed to retrieve the article.")

    def refresh_articles(self):
        self.load_articles()
