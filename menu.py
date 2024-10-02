#!/bin/python

from simple_term_menu import TerminalMenu
import sys
import os


class Prompt:
    @staticmethod
    def term_menu(options):
        terminal_menu = TerminalMenu(options)
        entry_index = terminal_menu.show()
        selection = options[entry_index]
        return selection
        #return entry_index
    
    @staticmethod
    def dict_menu(dict_options):
        selection = Prompt.term_menu(list(dict_options.keys())) # convert keys to list and make a menu
        selected_function = dict_options.get(selection) #get method that corresponds to selected key
        return selection #selected_function
