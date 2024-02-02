import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Zmienna globalna do przechowywania okna zaawansowanego wyszukiwania
global advanced_search_window
advanced_search_window = None


# Funkcja do nawiazywania polaczenia z baza danych
def db_connect():
    # Ustawienia polaczenia: host, uzytkownik, haslo, nazwa bazy danych
    return mysql.connector.connect(
        host="localhost", user="QBE", password="qbe", database="school"
    )


# Funkcja pobierania danych z okreslonej tabeli
def fetch_data_from_table(table_name):
    try:
        # Utworzenie polaczenia i kursora do bazy danych
        conn = db_connect()
        cursor = conn.cursor()
        # Wykonanie zapytania SQL i pobranie wynikow
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        # Zamkniecie kursora i polaczenia
        cursor.close()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        # Wyswietlenie komunikatu o bledzie na pasku stanu
        status_bar.config(text=f"Error: {err}")
        return []


# Inicjalizacja widoku drzewa (TreeView)
def setup_treeview():
    treeview.column("#0", width=0, stretch=tk.NO)


# Reakcja na wybor tabeli przez uzytkownika
def on_table_select(event):
    selected_table = table_select_combo.get()
    update_treeview_columns(selected_table)
    populate_treeview_with_data(selected_table)


# Wypelnianie TreeView danymi z wybranej tabeli
def populate_treeview_with_data(table_name):
    update_treeview_columns(table_name)
    data = fetch_data_from_table(table_name)
    print(f"Data from {table_name}: {data}")
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=row)


# Aktualizacja kolumn TreeView na podstawie struktury tabeli
def update_treeview_columns(table_name):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()
    conn.close()

    for col in treeview["columns"]:
        treeview.heading(col, text="")
        treeview.column(col, width=0)

    treeview["columns"] = columns
    for col in columns:
        treeview.column(col, anchor=tk.W, width=100)
        treeview.heading(col, text=col)

    treeview.delete(*treeview.get_children())


# Funkcja do parsowania zapytania QBE i tworzenia zapytania SQL
def parse_qbe_query(query, table_name):
    # Rozdzielenie warunkow zapytania QBE
    conditions = query.split(",")
    where_clause = []
    for cond in conditions:
        # Obsluga roznych typow warunkow
        if "=" in cond:
            column, value = cond.split("=")
            where_clause.append(f"{column} = '{value}'")
        elif "%" in cond:
            column, value = cond.split("%")
            where_clause.append(f"{column} LIKE '{value}'")
    # Utworzenie zapytania SQL
    sql_query = f"SELECT * FROM {table_name} WHERE {' AND '.join(where_clause)}"
    return sql_query


# Wykonywanie zapytania QBE
def execute_qbe_query():
    table_name = table_select_combo.get()
    qbe_query = qbe_query_entry.get()
    sql_query = parse_qbe_query(qbe_query, table_name)

    # Zaktualizuje pasek stanu, aby wyswietlic biezace zapytanie
    status_bar.config(text=f"Current Query: {sql_query}")
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)


# Eksport danych do formatu PDF
def export_data():
    data_to_export = [treeview.item(item, "values") for item in treeview.get_children()]
    if data_to_export:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            export_to_pdf(file_path, data_to_export)
            status_bar.config(text=f"Data exported successfully to {file_path}.")
        else:
            status_bar.config(text="Export cancelled.")
    else:
        status_bar.config(text="No data to export.")


# Funkcja do eksportowania danych do pliku PDF
def export_to_pdf(file_path, data):
    try:
        # Utworzenie dokumentu PDF z danymi
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        table_data = [treeview["columns"]] + [list(item) for item in data]
        t = Table(table_data)
        # Stylizacja tabeli w dokumencie PDF
        t.setStyle(
            TableStyle(
                [
                    # Definicje stylow tabeli
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements = [t]
        doc.build(elements)
    except Exception as e:
        # Obsluga bledu przy generowaniu PDF
        status_bar.config(text=f"Error in exporting PDF: {e}")


# Funkcja otwierania okna zaawansowanego wyszukiwania
def open_advanced_search():
    global advanced_search_window

    if advanced_search_window is not None and advanced_search_window.winfo_exists():
        return  # Sprawdza czy zaawansowanego wyszukiwania okno już jest otwarte

    advanced_search_window = tk.Toplevel(root)
    advanced_search_window.title("Advanced Search")
    advanced_search_window.geometry("270x350")

    # Przechowywanie widzetow jako atrybutow okna
    advanced_search_window.label_column_name1 = ttk.Label(
        advanced_search_window, text="First Column:"
    )
    advanced_search_window.label_column_name1.pack(pady=5)
    advanced_search_window.column_name_combo1 = ttk.Combobox(
        advanced_search_window, state="readonly"
    )
    advanced_search_window.column_name_combo1["values"] = treeview["columns"]
    advanced_search_window.column_name_combo1.pack(pady=5)

    advanced_search_window.label_operator1 = ttk.Label(
        advanced_search_window, text="First Operator:"
    )
    advanced_search_window.label_operator1.pack(pady=5)
    advanced_search_window.operator_combo1 = ttk.Combobox(
        advanced_search_window, state="readonly"
    )
    advanced_search_window.operator_combo1["values"] = [
        "equal",
        "less than",
        "greater than",
        "begins with",
        "ends with",
    ]
    advanced_search_window.operator_combo1.pack(pady=5)

    advanced_search_window.value_entry1 = ttk.Entry(advanced_search_window)
    advanced_search_window.value_entry1.pack(pady=5)

    advanced_search_window.label_column_name2 = ttk.Label(
        advanced_search_window, text="Second Column:"
    )
    advanced_search_window.label_column_name2.pack(pady=5)
    advanced_search_window.column_name_combo2 = ttk.Combobox(
        advanced_search_window, state="readonly"
    )
    advanced_search_window.column_name_combo2["values"] = treeview["columns"]
    advanced_search_window.column_name_combo2.pack(pady=5)

    advanced_search_window.label_operator2 = ttk.Label(
        advanced_search_window, text="Second Operator:"
    )
    advanced_search_window.label_operator2.pack(pady=5)
    advanced_search_window.operator_combo2 = ttk.Combobox(
        advanced_search_window, state="readonly"
    )
    advanced_search_window.operator_combo2["values"] = [
        "equal",
        "less than",
        "greater than",
        "begins with",
        "ends with",
    ]
    advanced_search_window.operator_combo2.pack(pady=5)

    advanced_search_window.value_entry2 = ttk.Entry(advanced_search_window)
    advanced_search_window.value_entry2.pack(pady=5)

    advanced_search_window.search_button = ttk.Button(
        advanced_search_window,
        text="Search",
        command=lambda: apply_advanced_search(
            advanced_search_window.column_name_combo1.get(),
            advanced_search_window.operator_combo1.get(),
            advanced_search_window.value_entry1.get(),
            advanced_search_window.column_name_combo2.get(),
            advanced_search_window.operator_combo2.get(),
            advanced_search_window.value_entry2.get(),
        ),
    )
    advanced_search_window.search_button.pack(pady=10)


# Funkcja aplikowania zaawansowanego wyszukiwania
def apply_advanced_search(column1, operator1, value1, column2, operator2, value2):
    # Budowanie i wykonanie zapytania SQL na podstawie kryteriow wyszukiwania
    sql_query = "SELECT * FROM {table_name} WHERE "
    # Warunki zapytania
    conditions = []

    if column1 and value1:
        condition1 = create_condition(column1, operator1, value1)
        conditions.append(condition1)

    if column2 and value2:
        condition2 = create_condition(column2, operator2, value2)
        conditions.append(condition2)

    if conditions:
        sql_query += " AND ".join(conditions)
    else:
        sql_query = "SELECT * FROM {table_name}"

    # Zaktualizuje pasek stanu, aby wyswietlal biezace zapytanie wyszukiwania zaawansowanego
    status_bar.config(
        text=f"Advanced Search Query: {sql_query.format(table_name=table_select_combo.get())}"
    )

    # Wykonanie zaawansowanego zapytania wyszukiwania
    execute_advanced_search_query(sql_query)


# Tworzenie warunku SQL na podstawie operatora i wartosci
def create_condition(column, operator, value):
    # Mapowanie operatora na odpowiedni warunek SQL
    sql_operator = {
        "equal": "=",
        "less than": "<",
        "greater than": ">",
        "begins with": f"{value}%",
        "ends with": f"%{value}",
    }.get(operator, "=")
    if operator in ["begins with", "ends with"]:
        return f"{column} LIKE '{sql_operator}'"
    else:
        return f"{column} {sql_operator} '{value}'"


# Funkcja zaawansowanego zapytania wyszukiwania i aktualizacja widoku
def execute_advanced_search_query(sql_query):
    # Wykonanie zapytania SQL i wyswietlenie wynikow w TreeView
    try:
        # Pobranie nazwy tabeli, formatowanie i wykonanie zapytania
        table_name = table_select_combo.get()
        formatted_query = sql_query.format(table_name=table_name)
        # Aktualizacja paska stanu i wykonanie zapytania
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(formatted_query)
        rows = cursor.fetchall()
        # Wyswietlenie wynikow w Treeview
        treeview.delete(*treeview.get_children())
        for row in rows:
            treeview.insert("", "end", values=row)
        # Zamkniecie kursora i polaczenia
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        # Wyswietlenie komunikatu o bledzie
        status_bar.config(text=f"Error: {err}")


# Slowniki dla tlumaczen
english_labels = {
    "title": "School Database Management",
    "advanced_window_title": "Advanced Search",
    "select_table": "Select Table:",
    "export_data": "Export Data",
    "advanced_search": "Advanced Search",
    "ready": "Ready",
    "enter_query": "Enter QBE Query:",
    "execute_query": "Execute Query",
    "first_column": "First Column:",
    "first_operator": "First Operator:",
    "second_column": "Second Column:",
    "second_operator": "Second Operator:",
    "search": "Search",
}

polish_labels = {
    "title": "Zarządzanie Bazą Danych Szkoły",
    "advanced_window_title": "Wyszukiwanie Zaawansowane",
    "select_table": "Wybierz Tabelę:",
    "export_data": "Eksportuj Dane",
    "advanced_search": "Wyszukiwanie Zaawansowane",
    "ready": "Gotowe",
    "enter_query": "Wpisz Zapytanie QBE:",
    "execute_query": "Wykonaj Zapytanie",
    "first_column": "Pierwsza Kolumna:",
    "first_operator": "Pierwszy Operator:",
    "second_column": "Druga Kolumna:",
    "second_operator": "Drugi Operator:",
    "search": "Szukaj",
    "operators": [
        "równy",
        "mniejszy niż",
        "większy niż",
        "zaczyna się od",
        "kończy się na",
    ],
    "change_language": "Zmień Język: ",
}


# Aktualizacja etykiet i tytulow w oknie zaawansowanego wyszukiwania przy zmianie jezyka
def update_advanced_search_window_labels(language):
    # Aktualizacja etykiet na podstawie wybranego jezyka
    labels = english_labels if language == "English" else polish_labels
    operators = (
        ["equal", "less than", "greater than", "begins with", "ends with"]
        if language == "English"
        else polish_labels["operators"]
    )

    # Aktualizacja tekstu kazdego widzetu i tytulu okna
    advanced_search_window.title(labels["advanced_window_title"])
    advanced_search_window.label_column_name1.config(text=labels["first_column"])
    advanced_search_window.label_operator1.config(text=labels["first_operator"])
    advanced_search_window.label_column_name2.config(text=labels["second_column"])
    advanced_search_window.label_operator2.config(text=labels["second_operator"])
    advanced_search_window.search_button.config(text=labels["search"])

    # Zaktualizuj pola wyboru operatora
    advanced_search_window.operator_combo1["values"] = operators
    advanced_search_window.operator_combo2["values"] = operators


# Funkcja zmiana jezyka interfejsu uzytkownika
def change_language(language):
    # Aktualizacja etykiet i tytulow na podstawie wybranego jezyka
    global current_language, advanced_search_window
    current_language = (
        language  # Upewnia czy biezacy jezyk jest aktualizowany globalnie.
    )
    labels = english_labels if language == "English" else polish_labels

    root.title(labels["title"])
    table_select_label.config(text=labels["select_table"])
    language_label.config(text=labels["change_language"])
    export_button.config(text=labels["export_data"])
    advanced_search_button.config(text=labels["advanced_search"])
    qbe_query_label.config(text=labels["enter_query"])
    qbe_query_button.config(text=labels["execute_query"])

    # Zaktualizuj etykiety okna wyszukiwania zaawansowanego, jesli istnieje i jest otwarte
    if advanced_search_window is not None and advanced_search_window.winfo_exists():
        update_advanced_search_window_labels(language)

    status_bar.config(text=labels["ready"])


# Konfiguracja głównego okna aplikacji
root = tk.Tk()
root.title(english_labels["title"])
root.geometry("800x600")

# Obszar wyboru tabeli
table_select_label = tk.Label(root, text=english_labels["select_table"])
table_select_label.pack(pady=5)
table_select_combo = ttk.Combobox(
    root,
    state="readonly",
    values=[
        "Students",
        "Teachers",
        "Courses",
        "Grades",
        "Classrooms",
        "Subjects",
        "Attendance",
        "SchoolEvents",
        "ParentGuardian",
    ],
)
table_select_combo.pack(pady=5)
table_select_combo.bind("<<ComboboxSelected>>", on_table_select)

# Konfiguracja widoku drzewa (TreeView)
treeview = ttk.Treeview(root)
treeview.pack(expand=True, fill="both", padx=10, pady=10)
setup_treeview()

# Obszar zapytan QBE
qbe_query_frame = tk.Frame(root)
qbe_query_frame.pack(pady=10)
qbe_query_label = tk.Label(qbe_query_frame, text=english_labels["enter_query"])
qbe_query_label.grid(row=0, column=0, padx=5)
qbe_query_entry = tk.Entry(qbe_query_frame, width=50)
qbe_query_entry.grid(row=0, column=1, padx=5)
qbe_query_button = tk.Button(
    qbe_query_frame, text=english_labels["execute_query"], command=execute_qbe_query
)
qbe_query_button.grid(row=0, column=2, padx=5)

# Przyciski eksportu i wyszukiwania zaawansowanego
export_button = tk.Button(root, text=english_labels["export_data"], command=export_data)
export_button.pack(pady=5)
advanced_search_button = tk.Button(
    root, text=english_labels["advanced_search"], command=open_advanced_search
)
advanced_search_button.pack(pady=5)

# Menu wyboru jezyka
language_label = tk.Label(
    root, text=english_labels.get("change_language ", "Change Language: ")
)
language_label.place(relx=0.8, rely=0.01, anchor="ne")

language_menu = ttk.Combobox(
    root, values=["English", "Polish"], state="readonly", width=10
)
language_menu.place(relx=0.9, rely=0.01, anchor="ne")
language_menu.bind(
    "<<ComboboxSelected>>", lambda _: change_language(language_menu.get())
)

# Pasek stanu
status_bar = tk.Label(
    root, text=english_labels["ready"], bd=1, relief=tk.SUNKEN, anchor=tk.W
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
