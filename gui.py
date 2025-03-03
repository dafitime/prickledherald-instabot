import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import config
from article_fetcher import fetch_articles, extract_article_details, download_image
from image_processing import process_image, add_logo
from text_processing import wrap_text, draw_text
from tkinter import filedialog
import re
from instabot import Bot
import os
from instagram_poster import upload_to_imgur, upload_to_instagram  # ✅ Add upload_to_instagram

print("Starting InstagramPostApp...")


class InstagramPostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Post Generator")
        self.root.geometry("600x800")
        self.root.configure(bg="#f4f4f4")
        self.root.minsize(600, 800)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)





        # **Create a Scrollable Canvas and Frame**
        self.canvas = tk.Canvas(self.root, bg="#f4f4f4")  # ✅ Use self.canvas instead of canvas
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # The frame inside the canvas that holds all UI elements
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f4f4f4")

        # Ensure the frame resizes properly
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Embed the frame inside the canvas correctly
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=580)

        # **Enable Mouse Scrolling**
        self.canvas.bind("<Enter>", lambda e: self._bind_mouse_scroll())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mouse_scroll())

        # ✅ Pack canvas and scrollbar using self.canvas
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # **Article Storage**
        self.articles = []
        self.current_article_index = 0

        # Featured Image
        tk.Label(self.scrollable_frame, text="Featured Image:", font=("Arial", 12), bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_featured_image = tk.Entry(self.scrollable_frame, width=40, font=("Arial", 12))
        self.entry_featured_image.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.scrollable_frame, text="Browse", font=("Arial", 12), command=self.browse_featured_image).grid(row=0, column=2, padx=5, pady=5)

        # Title Text
        tk.Label(self.scrollable_frame, text="Title Text:", font=("Arial", 12), bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_title = tk.Text(self.scrollable_frame, width=40, height=2, font=("Arial", 12), wrap="word")
        self.entry_title.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="ew")


        # Caption & Hashtags Box
        tk.Label(self.scrollable_frame, text="Caption & Hashtags:", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_caption_hashtags = tk.Text(self.scrollable_frame, width=40, height=5, font=("Arial", 12), wrap="word")
        self.entry_caption_hashtags.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

        # Font Size Controls
        self.font_size_var = tk.IntVar(value=config.DEFAULT_FONT_SIZE)  # ✅ Add this if missing
        tk.Label(self.scrollable_frame, text="Font Size:", font=("Arial", 12), bg="#f4f4f4").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        font_buttons_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f4")
        font_buttons_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tk.Button(font_buttons_frame, text="▲", font=("Arial", 12), command=self.increase_font_size).pack(side="left", padx=2)
        tk.Button(font_buttons_frame, text="▼", font=("Arial", 12), command=self.decrease_font_size).pack(side="left", padx=2)

        # Image Zoom Slider
        tk.Label(self.scrollable_frame, text="Image Zoom:", font=("Arial", 12), bg="#f4f4f4").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.zoom_var = tk.IntVar(value=config.DEFAULT_ZOOM)
        self.zoom_slider = tk.Scale(self.scrollable_frame, from_=50, to=200, orient="horizontal", variable=self.zoom_var, length=300, font=("Arial", 10), command=self.update_zoom)
        self.zoom_slider.grid(row=3, column=1, columnspan=2, pady=5, sticky="w")

        # (Everything else like article navigation, preview, etc. comes after)


        # **Article Navigation**
        nav_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f4")
        nav_frame.grid(row=4, column=0, columnspan=3, pady=5)

        tk.Button(nav_frame, text="⬅️ Previous Article", font=("Arial", 12), command=self.previous_article).pack(side="left", padx=10)
        tk.Button(nav_frame, text="Next Article ➡️", font=("Arial", 12), command=self.next_article).pack(side="left", padx=10)


        # **Fetch & Generate Buttons**
        button_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f4")
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)

        ##tk.Button(button_frame, text="Fetch Latest", font=("Arial", 14, "bold"), bg="#2196F3", fg="white", width=18, height=2, command=self.fetch_articles).pack(side="left", padx=10)
        tk.Button(button_frame, text="Generate Preview", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=18, height=2, command=self.generate_preview).pack(side="left", padx=10)



        # **Preview Area**
        self.preview_label = tk.Label(self.scrollable_frame, bg="#f4f4f4")
        self.preview_label.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")  # Centered preview

        # Image Position Frame (Center both sliders)
        position_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f4")
        position_frame.grid(row=7, column=0, columnspan=3, pady=10)

        tk.Label(position_frame, text="Image X Position:", font=("Arial", 12), bg="#f4f4f4").pack()
        self.x_position_var = tk.IntVar(value=0)
        self.x_position_slider = tk.Scale(position_frame, from_=-200, to=200, orient="horizontal", variable=self.x_position_var, length=300, font=("Arial", 10), command=self.update_position)
        self.x_position_slider.pack()

        tk.Label(position_frame, text="Image Y Position:", font=("Arial", 12), bg="#f4f4f4").pack()
        self.y_position_var = tk.IntVar(value=0)
        self.y_position_slider = tk.Scale(position_frame, from_=0, to=100, orient="horizontal", variable=self.y_position_var, length=300, font=("Arial", 10), command=self.update_position)
        self.y_position_slider.pack()


        buttons_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f4")
        buttons_frame.grid(row=9, column=0, columnspan=3, pady=10)

        # Centered Post to Instagram Button
        tk.Button(buttons_frame, text="Post to Instagram", font=("Arial", 14, "bold"), bg="#C13584", fg="white",
                width=20, height=2, command=self.send_to_instagram).pack(side="top", pady=5)
        
        self.fetch_articles()



    def update_position(self, event=None):
        self.generate_preview()

    def increase_font_size(self):
        self.font_size_var.set(self.font_size_var.get() + 2)
        self.generate_preview()

    def decrease_font_size(self):
        if self.font_size_var.get() > 10:
            self.font_size_var.set(self.font_size_var.get() - 2)
            self.generate_preview()

    def update_zoom(self, event=None):
        self.generate_preview()



    def load_article(self, index):
        """Loads an article by index and ensures '- The Prickled Herald' is completely removed."""
        if not self.articles:
            return

        article = self.articles[index]
        title, img_url, hashtags, caption = extract_article_details(article["url"])

        if not title or not img_url:
            return

        # Clean title
        title = re.sub(r"\s*[-–—]\s*The\s*Prickled\s*Herald", "", title, flags=re.IGNORECASE).strip()

        # Update title field
        self.entry_title.delete("1.0", tk.END)  # ✅ Use "1.0" instead of 0 for multi-line Text
        self.entry_title.insert("1.0", title)  # ✅ Insert title properly

        # Update hashtag field
        self.entry_caption_hashtags.delete("1.0", tk.END)  # ✅ Fix to use correct variable name
        self.entry_caption_hashtags.insert("1.0", f"{title}\n\n{hashtags}")  # ✅ Insert caption & hashtags



        # Update caption field
        

        # Download image and update field
        local_image_path = download_image(img_url)
        if local_image_path:
            self.entry_featured_image.delete(0, tk.END)
            self.entry_featured_image.insert(0, local_image_path)

        self.generate_preview()



    def previous_article(self):
        if self.articles and self.current_article_index > 0:
            self.current_article_index -= 1
            self.load_article(self.current_article_index)

    def next_article(self):
        if self.articles and self.current_article_index < len(self.articles) - 1:
            self.current_article_index += 1
            self.load_article(self.current_article_index)


    def save_image(self):
        """Saves the generated image to a user-specified location."""
        if not hasattr(self, "preview_image"):  # Ensure an image exists
            messagebox.showerror("Error", "No image generated to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                self.final_image.save(file_path)  # Save the actual image file
                messagebox.showinfo("Success", f"Image saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def send_to_instagram(self):
        """Handles posting the generated image to Instagram with custom caption and hashtags."""
        featured_image_path = "instagram_post.jpg"
        caption_text = self.entry_caption_hashtags.get("1.0", tk.END).strip()  # ✅ Get full caption & hashtags
        title_text = self.entry_title.get("1.0", tk.END).strip()  # ✅ Get multi-line title properly


        hashtags = ""
        
        if not os.path.exists(featured_image_path):
            messagebox.showerror("Error", "No processed image found to upload.")
            return

        # ✅ Upload image to Imgur
        imgur_url = upload_to_imgur(featured_image_path)
        
        if not imgur_url:
            messagebox.showerror("Error", "Failed to upload image to Imgur.")
            return

        # ✅ Upload to Instagram with caption and hashtags
        full_caption = f"{caption_text}\n\n{hashtags}"  # ✅ Combine both
        post_id = upload_to_instagram(imgur_url, caption=full_caption)
        
        if post_id:
            messagebox.showinfo("Success", "Image successfully posted to Instagram!")
        else:
            messagebox.showerror("Error", "Failed to post image.")
                        
    def on_close(self):
        self.root.quit()
        self.root.destroy()

    def browse_featured_image(self):
        """Opens a file dialog to select an image."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.entry_featured_image.delete(0, tk.END)
            self.entry_featured_image.insert(0, file_path)

    def fetch_articles(self):
        """Fetch all articles and load the first one."""
        self.articles = fetch_articles()
        if not self.articles:
            messagebox.showerror("Error", "Failed to fetch articles.")
            return

        self.current_article_index = 0
        self.load_article(self.current_article_index)

            
    def _bind_mouse_scroll(self):
        """Binds mouse scrolling when the mouse enters the canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_scroll)  # Windows & macOS
        self.canvas.bind_all("<Button-4>", self._on_mouse_scroll)  # Linux Scroll Up
        self.canvas.bind_all("<Button-5>", self._on_mouse_scroll)  # Linux Scroll Down

    def _unbind_mouse_scroll(self):
        """Unbinds mouse scrolling when the mouse leaves the canvas."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

        
    def _on_mouse_scroll(self, event):
        if event.delta:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")





    def generate_preview(self):
        """Generates and updates the preview image with the three-tier layout, applying X and Y positioning."""
        image_path = self.entry_featured_image.get().strip()

        if not image_path:
            messagebox.showerror("Error", "No image selected.")
            return

        try:
            # Load the image
            base_image = Image.open(image_path)
            base_image = process_image(image_path, self.zoom_var.get())  # Preserve zoom functionality

            # Create a new canvas for the final design
            final_image = Image.new("RGB", (config.FINAL_WIDTH, config.FINAL_HEIGHT), "white")

            # Get X and Y slider values for positioning
            x_offset = self.x_position_var.get()
            y_offset = self.y_position_var.get()

            # Apply position offset when pasting image
            final_image.paste(base_image, (x_offset, y_offset))

            # Overlay the logo
            add_logo(final_image)

            # Generate wrapped text and font
            text_lines, text_font = wrap_text(self.entry_title.get("1.0", tk.END).strip(), self.font_size_var.get())

            # Draw text on the image
            draw_text(final_image, text_lines, text_font)

            # Save the final image before previewing
            save_path = "instagram_post.jpg"
            final_image.save(save_path, "JPEG")
            print(f"✅ Image saved at {save_path}")

            # Resize for preview
            preview_image = final_image.resize((400, 400), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(preview_image)

            self.preview_label.config(image=self.preview_image)
            self.preview_label.image = self.preview_image  # Keep reference


        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {e}")
            
