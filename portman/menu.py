
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
class MainMenu:
    def __init__(self, option_hierarchy: dict, starting_point: str):
        self.menu_options = option_hierarchy
        self.original_context = starting_point
        self.current_context = starting_point
        self.history = []
        self.run = True

    def run_menu(self):
        while self.run:
            self.display(self.current_context, True)
            option_texts = list(enumerate(self.menu_options[self.current_context], start=1))
            if self.current_context == self.original_context:
                self.display(option_texts, back=False)
            else:
                self.display(option_texts, back=True)
            print(f"option count: {option_texts}\nlen: {len(option_texts)}")
            user_selection = self.user_input(len(option_texts))
            self.history.append(self.current_context)
            self.update_menu_context(user_selection)
            print(f"Context: {self.current_context}")
            print(f"Options: {self.menu_options[self.current_context]}")

    def parent_option(self):
        """Need to find if want to go back to previous menu context"""
        key_list = [self.menu_options.keys()]
        val_list = [self.menu_options.values()]
        positition = val_list.index(self.current_context)
        return key_list[positition]

    def update_menu_context(self, user_selection: int):
        if len(self.menu_options[self.current_context]) == user_selection:
            self.current_context = self.parent_option()
        else:
            self.current_context = self.menu_options[self.current_context][int(user_selection)-1]

    def validate_selection(self, text: str, option_count: int):
        if int(text) in range(1,option_count+1):
            return text


    def user_input(self, option_count):
        validated = False
        while not validated:
            user_selection = input("Please enter a number to select option:\n")
            if self.validate_selection(user_selection, option_count):
                return int(user_selection)
            else:
                print("Invalid option! Please enter one of the numbers in the menu!")

    def display(self, text, top: bool = False, back: bool = False):
        if top:
            print("#####  ",text.upper(), "  #####")
        else:
            for item in text:
                print(f"{item[0]} - {item[1]}")
        if back:
            print(f"{len(text) + 1} - back")


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

