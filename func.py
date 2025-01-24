import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from concurrent.futures import ThreadPoolExecutor

"Перемещает файл в целевую папку."
def move_file(source_path, target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target_path = os.path.join(target_dir, os.path.basename(source_path))

        #Проверка дубликатов
        if os.path.exists(target_path):
            base, ext = os.path.splitext(os.path.basename(source_path))
            counter = 1
            while os.path.exists(target_path):
                target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                counter += 1

        shutil.move(source_path, target_path)
    except Exception as e:
        print(f"Ошибка при перемещении {source_path}: {e}")


"Поиск и перемещение файлов"
def find_and_move_files_multithreaded(source_dirs, target_dir, file_extensions, max_workers, include_subdirs):
    try:
        files_to_move = []
        for source_dir in source_dirs:
            for root, dirs, files in os.walk(source_dir):
                if not include_subdirs and root != source_dir:
                    continue
                for file in files:
                    if file.lower().endswith(file_extensions):
                        files_to_move.append(os.path.join(root, file))

        if not files_to_move:
            messagebox.showinfo("Информация", "Файлы заданных форматов не найдены.")
            return

        #Многопоток
        total_moved_files = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(move_file, file_path, target_dir) for file_path in files_to_move]
            for future in futures:
                try:
                    future.result()
                    total_moved_files += 1
                except Exception as e:
                    print(f"Ошибка при обработке: {e}")

        messagebox.showinfo("Готово", f"Файлы успешно перемещены! Всего перемещено: {total_moved_files}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


"Диалоговое окно выбора целевой папки."
def select_target_dir():
    dir = filedialog.askdirectory(title="Выберите целевую папку")
    return dir


"Добавляет папки в список при перетаскивании."
def add_folder_from_dragged(event, listbox):
    raw_data = event.data.strip()
    if raw_data.startswith("{") and raw_data.endswith("}"):
        raw_data = raw_data[1:-1]
    paths = raw_data.split("}")  # Разделяем пути, если есть пробелы

    for path in paths:
        path = path.strip()
        if path.startswith("{") and path.endswith("}"):  # Убираем оставшиеся скобки
            path = path[1:-1]
        if os.path.isdir(path):
            listbox.insert(tk.END, path)
        else:
            messagebox.showwarning("Предупреждение", f"{path} не является папкой!")

"Запускает основной процесс поиска и перемещения."
def start_program(selected_dirs_listbox, max_workers_entry, extensions_entry, include_subdirs_var):
    source_dirs = list(selected_dirs_listbox.get(0, tk.END))
    if not source_dirs:
        messagebox.showwarning("Предупреждение", "Вы не выбрали исходные папки!")
        return

    target_dir = select_target_dir()
    if not target_dir:
        messagebox.showwarning("Предупреждение", "Вы не выбрали целевую папку!")
        return

    try:
        max_workers = int(max_workers_entry.get())
        if max_workers < 1:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Предупреждение", "Введите корректное число потоков!")
        return

    extensions = extensions_entry.get().strip()
    if not extensions:
        messagebox.showwarning("Предупреждение", "Введите хотя бы одно расширение файлов!")
        return

    file_extensions = tuple(ext.strip().lower() for ext in extensions.split(",") if ext.strip())
    include_subdirs = include_subdirs_var.get() == 1
    find_and_move_files_multithreaded(source_dirs, target_dir, file_extensions, max_workers, include_subdirs)

"Удаляет выбранные папки из списка."
def remove_selected_dirs(selected_dirs_listbox):
    selected_items = selected_dirs_listbox.curselection()
    for index in reversed(selected_items):
        selected_dirs_listbox.delete(index)

"Окно справки"
def show_help():
    """Открывает окно справки с возможностью копирования текста и гиперссылками."""
    import webbrowser

    def open_link(event):
        webbrowser.open("https://github.com/Echosinus/File-mover")

    help_window = tk.Toplevel()
    help_window.title("Справка")
    help_window.geometry("700x400")

    help_text = tk.Text(help_window, wrap=tk.WORD, font=("Arial", 12))
    help_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Текст справки
    help_content = """Справочная информация:

1. Для добавления папок перетащите их в левую область окна.
2. Введите расширения файлов через запятую (например: .png, .jpg, .mp4).
3. Выберите количество потоков (чем больше потоков, тем больше скорость, но исходите из возможностей процессора и диска).
4. Если нужно достать файлы из папок внутри основной папки, поставьте галочку на поиск в подпапках.

Ссылка на GitHub: https://github.com/Echosinus/File-mover
"""
    help_text.insert(tk.END, help_content)
    help_text.config(state=tk.DISABLED)

    start_index = help_content.find("https://github.com/Echosinus/File-mover")
    if start_index != -1:
        end_index = start_index + len("https://github.com/Echosinus/File-mover")
        line_start = help_content[:start_index].count("\n") + 1
        column_start = start_index - help_content.rfind("\n", 0, start_index) - 1
        line_end = help_content[:end_index].count("\n") + 1
        column_end = end_index - help_content.rfind("\n", 0, end_index) - 1

        start_tag = f"{line_start}.{column_start}"
        end_tag = f"{line_end}.{column_end}"

        help_text.tag_add("github", start_tag, end_tag)
        help_text.tag_config("github", foreground="blue", underline=True)
        help_text.tag_bind("github", "<Button-1>", open_link)