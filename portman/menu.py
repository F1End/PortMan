
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
class Menu:
    def __init___(self, option_hierarchy: dict, starting_point: str):
        self.menu_options = option_hierarchy
        self.current_context = starting_point

    def run_menu(self):
        self.display(self.current_context, True)
        option_texts = enumerate(self.menu_options[self.current_context], start=1)


    def display(self, text, top: bool = False):
        if top:
            print("#####  ",text.upper(), "#####  ")
        else:
            print(text)


#follow top-down, left-to-right path
default_option_hierarchy = { "main": ["add_trade", "check_holdings", "update_prices", "exit"],
                             "add_trade": ["add_trade_full", "add_trade_without_price"],
                             "check_holdings": ["list_holdings"],
                             "update_prices": ["automatic_update", "manual_update", "update_from_file"],
                             "exit": "run_exit",
                             "add_trade_full": "run_add_trade_full",
                             "add_trade_without_price": "run_add_trade_without_price",
                             "list_holdings": "run_list_holdings",
                             "automatic_update": "run_automatic_update",
                             "manual_update": "run_manual_update",
                             "update_from_file": "run_update_from_file",
                             }

