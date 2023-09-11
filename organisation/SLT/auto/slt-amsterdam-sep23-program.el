(TeX-add-style-hook
 "slt-amsterdam-sep23-program"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("amsart" "a4paper" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("euscript" "mathscr") ("xy" "ps" "all" "arc" "rotate") ("geometry" "lmargin=1in" "rmargin=1in" "tmargin=1in" "bmargin=1in") ("enumitem" "shortlabels")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "amsart"
    "amsart11"
    "amsfonts"
    "amssymb"
    "amsmath"
    "amsthm"
    "abstract"
    "color"
    "bbm"
    "euscript"
    "xy"
    "geometry"
    "fancyhdr"
    "pb-diagram"
    "enumitem"
    "hyperref"
    "stmaryrd")
   (TeX-add-symbols
    "lambdahat")
   (LaTeX-add-bibitems
    "green-book"
    "grey-book"
    "WBIC"
    "lambdahat"))
 :latex)

