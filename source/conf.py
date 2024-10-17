# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
from pygments.lexer import RegexLexer, using, bygroups
from pygments.token import Token
from pygments.lexers.data import JsonLexer
from sphinx.highlighting import lexers

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'SECoP'
copyright = '2023-2024, ISSE'
author = 'ISSE'

root_doc = 'index'

# The full version, including alpha/beta/rc tags
release = '1.0'

# -- General configuration ---------------------------------------------------

highlight_language = 'secop'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
    'sphinx_design',
    'sphinx_favicon',
]

todo_include_todos = True

extlinks = {
    'issue' : ('https://github.com/SampleEnvironment/SECoP/blob/master/protocol/issues/%s.rst',
    'SECoP Issue %s')
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_title = 'SECoP'
html_logo = '_static/logo.svg'

html_additional_pages = {
    # Custom template for landing page
    #'landing': 'landing.html',
    #'': '',
}

html_theme = 'pydata_sphinx_theme'

html_css_files = [
    'custom.css',
]

html_theme_options = {
    'logo': {
        'image_light': 'logo.svg',
        'image_dark': 'logo.svg',
    },
    'secondary_sidebar_items': ['page-toc', 'sourcelink'],
    #"announcement": "<em>Important</em> announcement!",
    'header_links_before_dropdown': 5,
    # links with icons to the right of the search icon:
    #'external_links': [
    #    {}
    #]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


favicons = [
    {
        'rel': 'icon',
        'sizes': '16x16',
        'href': 'favicon16.png',
    },
    {
        'rel': 'icon',
        'sizes': '32x32',
        'href': 'favicon32.png',
    },
    {
        'rel': 'apple-touch-icon',
        'sizes': '180x180',
        'href': 'favicon.png',
        'color': '#000000',
    },
]


class SECoPLexer(RegexLexer):
    name = 'secop'
    flags = re.MULTILINE

    tokens = {
        'root': [
            # special: *IDN? and reply
            (r'(>)( +)(\*IDN\?)',
             bygroups(Token.Generic.Prompt, Token.Whitespace, Token.Keyword)),
            (r'(<)( +)(ISSE.*)',
             bygroups(Token.Generic.Prompt, Token.Whitespace, Token.String)),
            # generic request/reply with JSON reply potentially broken into
            # multiple lines
            (r'(?s)([><])( +)(\S+)(?:( )(\S+)(:\w+)?)?( )(\{)',
             bygroups(
                 Token.Generic.Prompt,
                 Token.Whitespace,
                 Token.Keyword,
                 Token.Whitespace,
                 Token.String,
                 Token.Name,
                 Token.Whitespace,
                 using(JsonLexer)
             ),
             'json'),
            # generic single line request/reply
            (r'([><])( +)(\S+)(?:( )(\S+)(:\w+)?)?(?:( )(.*?))?$',
             bygroups(
                 Token.Generic.Prompt,
                 Token.Whitespace,
                 Token.Keyword,
                 Token.Whitespace,
                 Token.String,
                 Token.Name,
                 Token.Whitespace,
                 using(JsonLexer)
             )),
            # just an ellipsis
            (r'\.\.\.', Token.Comment),
            # comment
            (r'# .*$', Token.Comment),
            (r'\s+', Token.Whitespace),
        ],
        'json': [
            # multi-line JSON (XXX does not work with braces in strings)
            (r'\{', Token.Punctuation, '#push'),
            (r'\}', Token.Punctuation, '#pop'),
            (r'[^{}]+', using(JsonLexer)),
        ]
    }


lexers['secop'] = SECoPLexer(startinline=True)

latex_documents = [
    ('spec/index', 'secop.tex', 'SECoP Specification', author, 'howto'),
]
