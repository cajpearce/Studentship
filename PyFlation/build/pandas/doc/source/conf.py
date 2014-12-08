# -*- coding: utf-8 -*-
#
# pandas documentation build configuration file, created by
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import re
from pandas.compat import u, PY3

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.append(os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../sphinxext'))

sys.path.extend([

    # numpy standard doc extensions
    os.path.join(os.path.dirname(__file__),
                 '..', '../..',
                 'sphinxext')

])

# -- General configuration -----------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.  sphinxext.

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.doctest',
              'sphinx.ext.extlinks',
              'sphinx.ext.todo',
              'numpydoc', # used to parse numpy-style docstrings for autodoc
              'ipython_sphinxext.ipython_directive',
              'ipython_sphinxext.ipython_console_highlighting',
              'sphinx.ext.intersphinx',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.pngmath',
              'sphinx.ext.ifconfig',
              'matplotlib.sphinxext.only_directives',
              'matplotlib.sphinxext.plot_directive',
              ]



with open("index.rst") as f:
    lines = f.readlines()

# only include the slow autosummary feature if we're building the API section
# of the docs

# JP: added from sphinxdocs
autosummary_generate = False

if any([re.match("\s*api\s*",l) for l in lines]):
    autosummary_generate = True

ds = []
for f in os.listdir(os.path.dirname(__file__)):
    if (not f.endswith(('.rst'))) or (f.startswith('.')) or os.path.basename(f) == 'index.rst':
        continue

    _f = f.split('.rst')[0]
    if not any([re.match("\s*%s\s*$" % _f,l) for l in lines]):
        ds.append(f)

if ds:
    print("I'm about to DELETE the following:\n%s\n" % list(sorted(ds)))
    sys.stdout.write("WARNING: I'd like to delete those to speed up processing (yes/no)? ")
    if PY3:
        answer = input()
    else:
        answer = raw_input()

    if answer.lower().strip() in ('y','yes'):
        for f in ds:
            f = os.path.join(os.path.join(os.path.dirname(__file__),f))
            f= os.path.abspath(f)
            try:
                print("Deleting %s" % f)
                os.unlink(f)
            except:
                print("Error deleting %s" % f)
                pass

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u('pandas')
copyright = u('2008-2014, the pandas development team')

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import pandas

# version = '%s r%s' % (pandas.__version__, svn_version())
version = '%s' % (pandas.__version__)

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'nature_with_gtoc'

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'statsmodels.css'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['themes']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'pandas'


# -- Options for LaTeX output --------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', 'pandas.tex',
     u('pandas: powerful Python data analysis toolkit'),
     u('Wes McKinney\n\& PyData Development Team'), 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'statsmodels': ('http://statsmodels.sourceforge.net/devel/', None),
    'matplotlib': ('http://matplotlib.org/', None),
    'python': ('http://docs.python.org/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None)
}
import glob
autosummary_generate = glob.glob("*.rst")

# extlinks alias
extlinks = {'issue': ('https://github.com/pydata/pandas/issues/%s',
                      'GH'),
            'wiki': ('https://github.com/pydata/pandas/wiki/%s',
                     'wiki ')}

ipython_exec_lines = [
    'import numpy as np',
    'import pandas as pd',
    # This ensures correct rendering on system with console encoding != utf8
    # (windows). It forces pandas to encode its output reprs using utf8
    # whereever the docs are built. The docs' target is the browser, not
    # the console, so this is fine.
    'pd.options.display.encoding="utf8"'
    ]

# remove the docstring of the flags attribute (inherited from numpy ndarray)
# because these give doc build errors (see GH issue 5331)
def remove_flags_docstring(app, what, name, obj, options, lines):
    if what == "attribute" and name.endswith(".flags"):
        del lines[:]

def setup(app):
    app.connect("autodoc-process-docstring", remove_flags_docstring)
