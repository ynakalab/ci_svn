# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CI Subversion'
copyright = '2023, '
author = 'ynaka'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.seqdiag",
    "sphinxcontrib.actdiag",
    "sphinxcontrib.nwdiag",
    "sphinxcontrib.rackdiag",
    "sphinxcontrib.packetdiag",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'sphinx_rtd_theme'
html_theme = 'cloud'
html_static_path = ['_static']

blockdiag_html_image_format = 'SVG'
seqdiag_html_image_format = 'SVG'
actdiag_html_image_format = 'SVG'
nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'

import os
blockdiag_fontpath = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
seqdiag_fontpath   = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
actdiag_fontpath   = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
nwdiag_fontpath    = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
rackdiag_fontpath    = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
packetdiag_fontpath    = os.path.join(os.path.abspath('.'), '_font/ipagp.ttf')
