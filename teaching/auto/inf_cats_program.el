(TeX-add-style-hook
 "inf_cats_program"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("xy" "all" "cmtip") ("biblatex" "backend=biber" "doi=false" "isbn=false" "url=false")))
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
    "amscd"
    "color"
    "fontspec"
    "amsmath"
    "amsfonts"
    "amsthm"
    "amssymb"
    "bbm"
    "graphicx"
    "epstopdf"
    "bm"
    "xy"
    "csquotes"
    "hyperref"
    "enumerate"
    "enumitem"
    "mathrsfs"
    "vmargin"
    "verbatim"
    "cleveref"
    "stackrel"
    "epigraph"
    "chngcntr"
    "etoolbox"
    "biblatex"
    "stmaryrd")
   (TeX-add-symbols
    "hmmax"
    "bmmax"
    "BA"
    "BB"
    "BC"
    "BD"
    "BE"
    "BF"
    "BG"
    "BH"
    "BI"
    "BJ"
    "BK"
    "BL"
    "BM"
    "BN"
    "BO"
    "BP"
    "BQ"
    "BR"
    "BS"
    "BT"
    "BU"
    "BV"
    "BW"
    "BX"
    "BY"
    "BZ"
    "Fa"
    "Fb"
    "Fc"
    "Fd"
    "Fe"
    "Ff"
    "Fg"
    "Fh"
    "Fi"
    "Fj"
    "Fk"
    "Fl"
    "Fm"
    "Fn"
    "Fo"
    "Fp"
    "Fq"
    "Fr"
    "Fs"
    "Ft"
    "Fu"
    "Fv"
    "Fw"
    "Fx"
    "Fy"
    "Fz"
    "FA"
    "FB"
    "FC"
    "FD"
    "FE"
    "FF"
    "FG"
    "FH"
    "FI"
    "FJ"
    "FK"
    "FL"
    "FM"
    "FN"
    "FO"
    "FP"
    "FQ"
    "FR"
    "FS"
    "FT"
    "FU"
    "FV"
    "FW"
    "FX"
    "FY"
    "FZ"
    "Ca"
    "Cb"
    "Cc"
    "Cd"
    "Ce"
    "Cf"
    "Cg"
    "Ch"
    "Ci"
    "Cj"
    "Ck"
    "Cl"
    "Cm"
    "Cn"
    "Co"
    "Cp"
    "Cq"
    "Cr"
    "Cs"
    "Ct"
    "Cu"
    "Cv"
    "Cw"
    "Cx"
    "Cy"
    "Cz"
    "CA"
    "CB"
    "CC"
    "CE"
    "CF"
    "CG"
    "CH"
    "CI"
    "CJ"
    "CK"
    "CL"
    "CM"
    "CN"
    "CO"
    "CP"
    "CQ"
    "CR"
    "CS"
    "CT"
    "CU"
    "CV"
    "CW"
    "CX"
    "CY"
    "CZ"
    "Hom"
    "Homint"
    "Homsh"
    "RHom"
    "Ext"
    "Extsh"
    "YExt"
    "Lim"
    "Colim"
    "ra"
    "lra"
    "rap"
    "Spec"
    "Spm"
    "Spf"
    "Proj"
    "Th"
    "Sch"
    "Sm"
    "AnSm"
    "Ouv"
    "SmProj"
    "un"
    "Be"
    "Ob"
    "Gm"
    "Ga"
    "pointille"
    "card"
    "trace"
    "ord"
    "charact"
    "rank"
    "Gal"
    "SH"
    "DM"
    "DA"
    "AnDA"
    "Chow"
    "HI"
    "MM"
    "Cpl"
    "Spt"
    "PSh"
    "Sh"
    "Mod"
    "Mon"
    "CMon"
    "Cat"
    "id"
    "Ho"
    "PreShv"
    "Shv"
    "D"
    "Sym"
    "Coh"
    "Alt"
    "SmCor"
    "Var"
    "An"
    "Pic"
    "sPic"
    "NS"
    "Alb"
    "Div"
    "Aut"
    "Nis"
    "Et"
    "Zar"
    "Bor"
    "GL"
    "SL"
    "PGL"
    "Gr"
    "image"
    "imm"
    "coimage"
    "Lie"
    "End"
    "Isom"
    "Mor"
    "tildeExt"
    "UHom"
    "UAut"
    "Cent"
    "Norm"
    "Stab"
    "Quot"
    "Res"
    "Ind"
    "Frac"
    "Id"
    "CoInd"
    "Tot"
    "DTot"
    "Pro"
    "Sus"
    "LSus"
    "Ev"
    "REv"
    "Frob"
    "Tor"
    "Coker"
    "Ker"
    "supp"
    "Jac"
    "df"
    "JG"
    "DG"
    "CCG"
    "PG"
    "sNS"
    "NSL"
    "Picsm"
    "Picsmc"
    "adj"
    "basechange"
    "Lotimes"
    "loccit"
    "OFU"
    "Ug"
    "Un"
    "Ur"
    "Ux"
    "diag"
    "pr"
    "Cone"
    "CHo"
    "LAlb"
    "RPic"
    "Ab"
    "For"
    "Set"
    "corexp"
    "et"
    "eff"
    "qfh"
    "gm"
    "op"
    "aug"
    "coh"
    "homo"
    "dcoh"
    "red"
    "sm"
    "ssm"
    "gsm"
    "ins"
    "ind"
    "nc"
    "mode"
    "sep"
    "s"
    "nr"
    "tor"
    "opp"
    "steff"
    "Ex"
    "tr"
    "perf"
    "fr"
    "gr"
    "str"
    "ab"
    "num"
    "pure"
    "an"
    "psh"
    "adjo"
    "Top"
    "sSet"
    "Sing"
    "TODO"
    "REF"
    "cosimparrowone"
    "cosimparrowtwo")
   (LaTeX-add-bibliographies
    "infcats")
   (LaTeX-add-amsthm-newtheorems
    "theo"
    "cor"
    "prop"
    "lemma"
    "claim"
    "conj"
    "question"
    "defi"
    "remark"
    "notation"))
 :latex)

