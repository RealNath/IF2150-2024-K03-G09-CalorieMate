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

        self.main_frame = ttk.Frame(self, style='MainContent.TFrame')
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.article_list = []
        self.current_mode = "listing"

        self.load_articles()
        self.create_listing_view()

    def load_articles(self):
        db.connect()
        articles = db.read("ArticleDatabase", ["article_id", "article_name", "article_author"], None, False)
        db.disconnect()
        self.article_list = articles

    def create_listing_view(self):
        # Clear main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = ttk.Label(self.main_frame, text="Articles", font=("Roboto", 16, "bold"), foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        title_label.pack(pady=10)

        # Scrollbar
        canvas_frame = tk.Frame(self.main_frame, bg=COLOR_BACKGROUND)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=COLOR_BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(fill="both", expand=True)

        list_container = tk.Frame(canvas, bg=COLOR_BACKGROUND)
        canvas.create_window((0,0), window=list_container, anchor="nw")

        def on_configure(event):
            canvas.config(scrollregion=canvas.bbox("all"))
        list_container.bind("<Configure>", on_configure)

        for article in self.article_list:
            article_id, article_name, article_author = article
            segment_frame = tk.Frame(list_container, bg="white", bd=1, relief="solid", padx=10, pady=10)
            segment_frame.pack(fill="x", pady=5)

            title_label = tk.Label(segment_frame, text=article_name, font=("Roboto", 14, "bold"), bg="white", fg="black")
            title_label.pack(anchor="w")

            author_label = tk.Label(segment_frame, text=f"by {article_author}", font=("Roboto", 12), bg="white", fg="black")
            author_label.pack(anchor="w")

            view_button = tk.Button(segment_frame, text="View", command=lambda aid=article_id: self.show_article(aid))
            view_button.pack(anchor="e", pady=5)

        self.current_mode = "listing"

    def show_article(self, article_id):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        db.connect()
        article = db.read("ArticleDatabase", ["article_name", "article_author", "text"], {"article_id": article_id}, True)
        db.disconnect()

        if not article:
            messagebox.showerror("Error", "Failed to retrieve the article.")
            self.show_listing_view()
            return

        article_name, article_author, article_text = article

        header_frame = tk.Frame(self.main_frame, bg=COLOR_BACKGROUND)
        header_frame.pack(fill="x", pady=10)

        title_label = tk.Label(header_frame, text=article_name, font=("Roboto", 16, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_TEXT)
        title_label.pack(anchor="w", padx=5)

        author_label = tk.Label(header_frame, text=f"by {article_author}", font=("Roboto", 12), bg=COLOR_BACKGROUND, fg=COLOR_TEXT)
        author_label.pack(anchor="w", padx=5)

        article_frame = tk.Frame(self.main_frame, bg=COLOR_BACKGROUND)
        article_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.preview_area = scrolledtext.ScrolledText(article_frame, wrap=tk.WORD, width=60, 
                                                      bg="white", fg="black", font=("Roboto", 14), 
                                                      state=tk.NORMAL, padx=10)
        self.preview_area.pack(fill="both", expand=True)
        self.preview_area.insert(tk.END, article_text)
        self.preview_area.config(state=tk.DISABLED)

        back_button_frame = tk.Frame(self.main_frame, bg=COLOR_BACKGROUND)
        back_button_frame.pack(fill="x", pady=10)

        back_button = tk.Button(back_button_frame, text="Back to Articles", command=self.show_listing_view)
        back_button.pack(anchor="e", padx=5)

        self.current_mode = "view"

    def show_listing_view(self):
        self.load_articles()
        self.create_listing_view()

    def refresh_articles(self):
        if self.current_mode == "listing":
            self.load_articles()
            self.create_listing_view()
