from portman import dbmanager, menu

# Example usage
if __name__ == "__main__":
    # db_manager = dbmanager.DatabaseManager()
    menu = menu.MainMenu(option_hierarchy=menu.default_option_hierarchy, starting_point="main")
    menu.run_menu()
    # db_manager.close_connection()
