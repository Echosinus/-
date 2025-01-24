from func import *

if __name__ == '__main__':

    #Основное окно и интерфейс
    root = TkinterDnD.Tk()
    root.title("")
    root.geometry("800x400")

    #Список папок
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    selected_dirs_listbox = tk.Listbox(left_frame, width=50, height=25)
    selected_dirs_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5)

    scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=selected_dirs_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    selected_dirs_listbox.config(yscrollcommand=scrollbar.set)

    selected_dirs_listbox.drop_target_register(DND_FILES)
    selected_dirs_listbox.dnd_bind('<<Drop>>', lambda event: add_folder_from_dragged(event, selected_dirs_listbox))

    #Параметры
    center_frame = tk.Frame(root)
    center_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

    extensions_label = tk.Label(center_frame, text="Введите форматы файлов (через запятую):", font=("Arial", 12))
    extensions_label.pack(pady=5)

    extensions_entry = tk.Entry(center_frame, font=("Arial", 12))
    extensions_entry.insert(0, "")
    extensions_entry.pack(pady=5)


    max_workers_label = tk.Label(center_frame, text="Количество потоков:", font=("Arial", 12))
    max_workers_label.pack(pady=5)

    max_workers_entry = tk.Entry(center_frame, font=("Arial", 12))
    max_workers_entry.insert(0, "1")
    max_workers_entry.pack(pady=5)
            

    include_subdirs_var = tk.IntVar(value=0)
    include_subdirs_checkbox = tk.Checkbutton(center_frame, text="Искать файлы в подпапках", variable=include_subdirs_var, font=("Arial", 12))
    include_subdirs_checkbox.pack(pady=5)

    remove_button = tk.Button(center_frame, text="Удалить выбранное", font=("Arial", 12), command=lambda: remove_selected_dirs(selected_dirs_listbox))
    remove_button.pack(pady=10)

    help_button = tk.Button(center_frame, text="Справка", font=("Arial", 12), command=show_help)
    help_button.pack(pady=10)

    #Управление
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

    start_button = tk.Button(right_frame, text="Начать", font=("Arial", 12), command=lambda: start_program(selected_dirs_listbox, max_workers_entry, extensions_entry, include_subdirs_var))
    start_button.pack(pady=20)

    exit_button = tk.Button(right_frame, text="Выход", font=("Arial", 12), command=root.quit)
    exit_button.pack(pady=20)

    root.mainloop()
