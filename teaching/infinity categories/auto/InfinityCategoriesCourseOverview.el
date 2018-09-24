(TeX-add-style-hook
 "InfinityCategoriesCourseOverview"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("amsart" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("xy" "arrow" "curve" "matrix") ("backref" "hyperpageref")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "amsart"
    "amsart10"
    "amssymb"
    "amscd"
    "enumitem"
    "hyperref"
    "inputenc"
    "newunicodechar"
    "varioref"
    "xy"
    "colortbl"
    "graphicx"
    "tikz"
    "mathrsfs"
    "backref")
   (TeX-add-symbols
    "salt"
    "stimes"
    "isom"
    "tensor"
    "Frac"
    "Gal"
    "Aut"
    "Fh"
    "Oh"
    "OO"
    "CC"
    "FF"
    "Fp"
    "LL"
    "NN"
    "PP"
    "QQ"
    "RR"
    "Z"
    "ZZ"
    "Q"
    "F"
    "Pe"
    "m"
    "p"
    "q"
    "val"
    "shval"
    "id"
    "rank"
    "trd")
   (LaTeX-add-bibitems
    "Hat"
    "Lur"
    "HTT"
    "DAGI"
    "DAGII"
    "May"
    "Gro"
    "Wei")
   (LaTeX-add-amsthm-newtheorems
    "thm"
    "thmU"
    "theo"
    "coro"
    "cor"
    "corU"
    "lemm"
    "lemma"
    "propo"
    "prop"
    "conj"
    "defi"
    "defn"
    "propdef"
    "obse"
    "rema"
    "rem"
    "remi"
    "exam"
    "summ"
    "nota"
    "warn"
    "ques")
   (LaTeX-add-color-definecolors
    "linkred"
    "linkblue"))
 :latex)

