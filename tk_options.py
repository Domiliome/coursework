def resize_window(root, wight, height):
    size = [wight, height]
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - (size[0] // 2)
    h = h - (size[1] // 2)
    root.geometry('{}x{}+{}+{}'.format(size[0], size[1], w, h))

def grid_region(root, rows, colums):
    for i in range(colums):
        root.grid_columnconfigure(i, weight=1)
    for j in range(rows):
        root.grid_rowconfigure(j, weight=1)
