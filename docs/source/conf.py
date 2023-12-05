from QuantumTools import __version__

version = __version__
project = 'QuantumTools'
copyright = '2023, DoryeLEsteras'
author = 'DoryeLEsteras'

extensions = [ 
    "sphinx_copybutton",
    ]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'press'

variables_to_export = [
    "version",
]

html_context = {
    "default_mode": "light",
    "display_version": True,
    "display_github": True,
    "github_user": "DoryeLEsteras",
    "github_repo": "QuantumTools",
    "doc_path": "docs/source",
}
