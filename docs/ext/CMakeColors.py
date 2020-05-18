# -*- coding: utf-8 -*-

from pygments.style import Style
from pygments.token import Name, Comment, String, Number, Operator, Whitespace,\
                           Keyword, Error, Literal

class CMakeTemplateStyle(Style):
    """
        for more token names, see pygments/styles.default
    """

    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        Comment:                "italic #408080",
        Comment.Single:         "italic #909693",   # end line comment
        Comment.Multiline:      "italic #408080",   # block comment
        Whitespace:             "#BBBBBB",
        String:                 "#217A21",
        String.Backtick:        "#217A21",          # bracket argument
        String.Double:          "#217A21",          # ""
        String.Escape:          "#9A890B",          # escape sequence
        Name.Function:          "#007020",          # function (user defined)
        Name.Function.Magic:    "#D0781C",          # function (CMake's internal)
        Operator:               "#555555",          # $<:> ,
        Operator.Word:          "italic #731728",   # regex operators
        Name.Class:             "bold", # ENV CACHE
        Name.Variable:          "#1080B0",          # name variable
        Name.Attribute:         "#906060",          # paths, URLs
        Number:                 "#105030",
        Keyword.Type:           "bold #d8349d",     # -o, --long-option
        Keyword:                "#eb07ef", 
        Keyword.Reserved:       "bold #861ce4",
        Keyword.Constant:       "bold #485f13",     # true false off on
        Keyword.Declaration:    "#4070a0",          # Uppercase only - unknown keywords
        Literal:                "#000000",          # lowercase
        Error:                  "border:#FF0000",
        Name.Builtin:           "#333333",          # anything lowercase
        Name.Tag:               "#bb60d5",          # ${..}
        Name.Constant:          "#4070a0",          # uppercase only
        Name.Entity:            "italic #70A020",   # @..@
        Name.Label:             "#A0A000",          # anything left over
        Name.Exception:         "bold #FF0000",     # for debugging only
    }
