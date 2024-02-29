# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:06:16 2024

@author: Usuario
"""

conda env create  # Automatically creates environment based on environment.yml
activate prosumpy # for windows: activate prosumpy
pip install -e . # Install editable local version
pytest # Run the tests and ensure that there are no errors