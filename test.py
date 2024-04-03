"""
This file is only setup to check coding standards using flake
"""

def greet(name):
  print(f"Hello, {name}!")  # Missing parenthesis around f-string

# Missing docstring for the function
def calculate_area(length, width):
  return lenght * width  # Typo in 'length'

# Long line exceeding recommended character limit
long_variable_name = "This is a very long variable name that exceeds the recommended character limit"

# Unused variable
unused_var = 5