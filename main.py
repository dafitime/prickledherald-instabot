# main.py

#{
#  "instagram_business_account": {
#    "id": "17841461793452461"
#  },
#  "id": "105152777637855"
#}


import tkinter as tk
from gui import InstagramPostApp

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramPostApp(root)
    root.mainloop()
