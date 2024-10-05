# this module is for create decorators for functions from database_management


# 1. Dodawanie nowej kategorii
# - wrapper dodaje mi do pliku informacje. (z funckją dodaj (automatyczna) oraz usuń-/ oraz zobacz.)

base_path = r'C:\Users\LENOVO\Desktop\budget_control_ application'


def add_new_category_wrapper(add_new_category_func):
    def safe_info_about_add_new_category():
        jakiś_resultat = add_new_category_func()
        print("New category was written into log_data_file.txt")
        return "jakiś rezultat z dodawania?"
    return safe_info_about_add_new_category()
