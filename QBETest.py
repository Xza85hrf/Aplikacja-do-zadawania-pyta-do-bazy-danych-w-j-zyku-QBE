import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from QBESchool import (
    db_connect,
    fetch_data_from_table,
    execute_qbe_query,
    export_to_pdf,
    open_advanced_search,
    apply_advanced_search,
    setup_treeview,
    on_table_select,
    populate_treeview_with_data,
    update_treeview_columns,
    export_data,
)


# Klasa testowa do testowania aplikacji bazy danych szkoly
class TestSchoolDatabaseApp(unittest.TestCase):
    def setUp(self):
        # Przygotowanie srodowiska testowego
        self.root = tk.Tk()
        self.root.withdraw()  # Ukrycie glownego okna aplikacji

    def test_db_connect(self):
        # Test polaczenia z baza danych
        with patch("mysql.connector.connect") as mock_connect:
            db_connect()
            mock_connect.assert_called_with(
                host="localhost", user="QBE", password="qbe", database="school"
            )

    def test_fetch_data_from_table(self):
        # Test pobierania danych z tabeli
        with patch("QBESchool.db_connect") as mock_db_connect:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [("1", "Test Student", 10, 1)]
            mock_db_connect.return_value.cursor.return_value = mock_cursor

            result = fetch_data_from_table("Students")
            self.assertEqual(result, [("1", "Test Student", 10, 1)])

    def test_execute_qbe_query(self):
        # Test wykonania zapytania QBE
        with patch("QBESchool.db_connect") as mock_db_connect, patch(
            "QBESchool.treeview", MagicMock()
        ) as mock_treeview:
            mock_treeview.get.return_value = ["columns"]
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [("1", "Test Student", 10, 1)]
            mock_db_connect.return_value.cursor.return_value = mock_cursor

            result = execute_qbe_query("Students", "name=Test Student")
            self.assertEqual(result, [("1", "Test Student", 10, 1)])

    def test_open_advanced_search(self):
        # Test otwierania okna zaawansowanego wyszukiwania
        with patch("tkinter.Toplevel"):
            open_advanced_search()
            self.assertTrue(tk.Toplevel.called)

    def test_apply_advanced_search(self):
        # Test aplikowania zaawansowanego wyszukiwania
        with patch("QBESchool.db_connect") as mock_db_connect, patch(
            "QBESchool.treeview", MagicMock()
        ) as mock_treeview, patch(
            "QBESchool.status_bar", MagicMock()
        ) as mock_status_bar:
            mock_treeview.get.return_value = ["columns"]
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [("1", "Test Student", 10, 1)]
            mock_db_connect.return_value.cursor.return_value = mock_cursor

            apply_advanced_search("name", "equal", "Test Student")
            mock_cursor.execute.assert_called_with(
                "SELECT * FROM name WHERE name = 'Test Student'"
            )
            self.assertEqual(
                mock_status_bar.config.call_args[1]["text"],
                "Current Query: SELECT * FROM name WHERE name = 'Test Student'",
            )

    def test_setup_treeview(self):
        # Test konfiguracji TreeView
        with patch("QBESchool.treeview", MagicMock()) as mock_treeview:
            setup_treeview()
            mock_treeview.column.assert_called_with("#0", width=0, stretch=tk.NO)

    def test_on_table_select(self):
        # Test obslugi wyboru tabeli
        with patch("QBESchool.table_select_combo", MagicMock()) as mock_combo, patch(
            "QBESchool.update_treeview_columns"
        ) as mock_update_columns, patch(
            "QBESchool.populate_treeview_with_data"
        ) as mock_populate_data:
            mock_combo.get.return_value = "Students"
            on_table_select(None)
            mock_update_columns.assert_called_with("Students")
            mock_populate_data.assert_called_with("Students")

    def test_populate_treeview_with_data(self):
        # Test wypelniania TreeView danymi
        with patch(
            "QBESchool.fetch_data_from_table",
            return_value=[("1", "Test Student", 10, 1)],
        ) as mock_fetch, patch("QBESchool.treeview", MagicMock()) as mock_treeview:
            populate_treeview_with_data("Students")
            mock_fetch.assert_called_with("Students")
            mock_treeview.insert.assert_called_with(
                "", "end", values=("1", "Test Student", 10, 1)
            )

    def test_update_treeview_columns(self):
        # Test aktualizacji kolumn TreeView
        with patch("QBESchool.db_connect") as mock_db_connect, patch(
            "QBESchool.treeview", MagicMock()
        ) as mock_treeview:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                ("id",),
                ("name",),
                ("grade_level",),
                ("classroom_id",),
            ]
            mock_db_connect.return_value.cursor.return_value = mock_cursor

            update_treeview_columns("Students")
            mock_treeview.heading.assert_called()
            mock_treeview.column.assert_called()

    def test_export_data(self):
        # Test eksportu danych do PDF
        with patch(
            "QBESchool.filedialog.asksaveasfilename", return_value="test.pdf"
        ) as mock_save_dialog, patch(
            "QBESchool.export_to_pdf"
        ) as mock_export_pdf, patch(
            "QBESchool.treeview", MagicMock()
        ) as mock_treeview:
            mock_treeview.get_children.return_value = ["item1", "item2"]
            mock_treeview.item.return_value = {"values": ("1", "Test Student", 10, 1)}

            export_data()
            mock_save_dialog.assert_called()
            mock_export_pdf.assert_called_with(
                "test.pdf", [("1", "Test Student", 10, 1)]
            )

    def test_export_to_pdf(self):
        # Test funkcji eksportu do PDF
        with patch("reportlab.platypus.SimpleDocTemplate.build") as mock_build:
            export_to_pdf("test.pdf", [("1", "Test Student", 10, 1)])
            mock_build.assert_called()

    def tearDown(self):
        # Zakonczenie i zamkniecie srodowiska testowego
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
