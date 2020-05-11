import os
import re
from typing import Any, Dict

# Override much of pygments' CMakeLexer.
# We need to parse CMake syntax definitions, not CMake code.

# For hard test cases that use much of the syntax below, see
# - module/FindPkgConfig.html (with "glib-2.0>=2.10 gtk+-2.0" and similar)
# - module/ExternalProject.html (with http:// https:// git@; also has command options -E --build)
# - manual/cmake-buildsystem.7.html (with nested $<..>; relative and absolute paths, "::")

from pygments.lexers import CMakeLexer
from pygments.token import Name, Operator, Punctuation, String, Text, Comment, Generic, Whitespace, Number
from pygments.lexer import bygroups

# Notes on regular expressions below:
# - [\.\+-] are needed for string constants like gtk+-2.0
# - Unix paths are recognized by '/'; support for Windows paths may be added if needed
# - (\\.) allows for \-escapes (used in manual/cmake-language.7)
# - $<..$<..$>..> nested occurence in cmake-buildsystem
# - Nested variable evaluations are only supported in a limited capacity. Only
#   one level of nesting is supported and at most one nested variable can be present.

CMakeLexer.tokens["root"] = [
  (r'\b(\w+)([ \t]*)(\()', bygroups(Name.Function, Text, Name.Function), '#push'),     # fctn(
  (r'\(', Name.Function, '#push'),
  (r'\)', Name.Function, '#pop'),
  (r'\[', Punctuation, '#push'),
  (r'\]', Punctuation, '#pop'),
  (r'[|;,.=*\-]', Punctuation),
  (r'\\\\', Punctuation),                                   # used in commands/source_group
  (r'[:]', Operator),
  (r'[<>]=', Punctuation),                                  # used in FindPkgConfig.cmake
  (r'\$<', Operator, '#push'),                              # $<...>
  (r'<[^<|]+?>(\w*\.\.\.)?', Name.Variable),                # <expr>
  (r'(\$\w*\{)([^\}\$]*)?(?:(\$\w*\{)([^\}]+?)(\}))?([^\}]*?)(\})',  # ${..} $ENV{..}, possibly nested
    bygroups(Operator, Name.Tag, Operator, Name.Tag, Operator, Name.Tag, Operator)),
  (r'([A-Z]+\{)(.+?)(\})', bygroups(Operator, Name.Tag, Operator)),  # DATA{ ...}
  (r'[a-z]+(@|(://))((\\.)|[\w.+-:/\\])+', Name.Attribute),          # URL, git@, ...
  (r'/\w[\w\.\+-/\\]*', Name.Attribute),                    # absolute path
  (r'/', Name.Attribute),
  (r'\w[\w\.\+-]*/[\w.+-/\\]*', Name.Attribute),            # relative path
  (r'[A-Z]((\\.)|[\w.+-])*[a-z]((\\.)|[\w.+-])*', Name.Builtin), # initial A-Z, contains a-z
  (r'@?[A-Z][A-Z0-9_]*', Name.Constant),
  (r'[a-z_]((\\;)|(\\ )|[\w.+-])*', Name.Builtin),
  (r'[0-9][0-9\.]*', Number),
  (r'(?s)"(\\"|[^"])*"', String),                           # "string"
  (r'\.\.\.', Name.Variable),
  (r'<', Operator, '#push'),                                # <..|..> is different from <expr>
  (r'>', Operator, '#pop'),
  (r'\n', Whitespace),
  (r'[ \t]+', Whitespace),
  (r'#.*\n', Comment),
  #  (r'[^<>\])\}\|$"# \t\n]+', Name.Exception),            # fallback, for debugging only
]

def setup(app: "Sphinx") -> Dict[str, Any]:
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
