from QuantumTools import __version__

version = __version__
project = 'QuantumTools'
copyright = '2023, DoryeLEsteras'
author = 'DoryeLEsteras'

extensions = []

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'press'
html_static_path = ['_static']

variables_to_export = [
    "version",
]

html_context = {
    "default_mode": "light",
    "display_github": False,
    "github_user": "DoryeLEsteras",
    "github_repo": "QuantumTools",
    "doc_path": "docs/source",
}