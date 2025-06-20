import pickle
from typing import Annotated, Any, Tuple
from copy import deepcopy

import tkinter as tk
from PIL import Image, ImageTk

from medusa.picture import Picture
from medusa.loader import Loader

def create_thumbnail(image: Picture, size:Tuple[int,int]=(100,100)) -> ImageTk.PhotoImage:
    _thumbnail= deepcopy(image._thumbnail)
    _thumbnail.thumbnail(size)
    return ImageTk.PhotoImage(_thumbnail)

def display_thumbnails(frame: tk.Frame, title: str, pictures: list[Picture], across: int =10):
    _title = tk.Label(frame, text=title)
    _title.pack(side='left')
    first = True
    i = 1
    for picture in pictures:
        _t = create_thumbnail(picture)
        label = tk.Label(frame, image=_t)
        label.image = _t
        side = 'bottom' if first else 'left'
        label.pack(side=side)
        if i % across == 0:
            first = True
        else:
            first = False
            
        i += 1
        
    
if __name__ == "__main__":
    import pickle
    with open('./output/fotosvarias.pkl', 'rb') as infile:
        loaded_pictures = pickle.load(infile)
    
    print("Total pictures      : ", loaded_pictures.PictureCount)
    print("Duplicate groups    : ", len(loaded_pictures.Duplicate))
    print("Identical groups    : ", len(loaded_pictures.Identical))
    print("Color similar groups: ", len(loaded_pictures.ColorSimilar))
    root = tk.Tk()
    root.title = "Medusa"
    root.geometry("1024x576")
    duplicates_frame = []
    for i, (dup_group_id, dup_group_list) in enumerate(loaded_pictures.Duplicate.items()):
        duplicates_frame.append(tk.Frame(root, height=192, name=dup_group_id))
        duplicates_frame[i].pack()
        display_thumbnails(
        frame=duplicates_frame[i], 
        title=f"Duplicates - {dup_group_id}",
        pictures=dup_group_list)
        duplicates_frame[i].pack()

    root.mainloop()            

