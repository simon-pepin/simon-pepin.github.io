---
layout: page
title: "Algebraic Geometry and motives"
header: 
permalink: "/research/algebraic-geometry/"
---
<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>

# Where it all came from

The study of functions of one complex variable, dating back from the XVIIIth century, leads naturally to questions about functions on more complicated geometric objects built with the complex numbers: e.g., if you want to understand integrals like
\\[
\int_{t=0}^{a} \frac{dz}{\sqrt{(1-z^2)(1-2 z^2)}}
 \\]
 for \\(a\\) moving around the complex plane \\(\mathbb{C}\\) (related to the length of an ellipse), mathematicians like Abel, Jacobi and Riemann were led to study an associated geometric object called an *algebraic curve*, that is, the locus of solutions 
\\[
C=\\{(x,y)\in \mathbb{C}^2|\ P(x,y)=0\\}
\\]
of *one* polynomial equation in *two* complex variables: for the integral above,
\\[
P(x,y)= y^2-2x^4+3x^2-1
\\]
which is the equation of an [elliptic curve](https://en.wikipedia.org/wiki/Elliptic_curve).

After a while, mathematicians realized that the loci of solutions of any number of polynomial equations in any number of variables were very interesting too, and they dubbed them *algebraic varieties*. Thus [Algebraic Geometry](https://en.wikipedia.org/wiki/Algebraic_geometry) was born.

Since the very beginning, a key question in the field is to understand the rough shape of algebraic variety through their [topological invariants](https://en.wikipedia.org/wiki/Algebraic_topology). In the elliptic curve example above, for instance, the shape of the curve is responsible for the *double periodicity of elliptic functions*, an [high point](https://en.wikipedia.org/wiki/Elliptic_function) of XIXth century complex analysis.

# What I did in my thesis

I worked on the latest incarnation of the ideas above. Namely, I studied a very refined topological invariants of algebraic varieties, called a *motive*, dreamed up by [Grothendieck](https://en.wikipedia.org/wiki/Alexander_Grothendieck) in the 1960s and put on a strong technical foundation by [Voevodsky](https://en.wikipedia.org/wiki/Vladimir_Voevodsky) in the early 2000s.

We still understand little above motives of general algebraic varieties. However, it turns out that in the classical case of an algebraic curve, the very starting point of the theory in the XIXth century, we understand the motive very well. This was already well understood by Voevodsky, building on ideas of [Deligne]().

My contribution was to study motives attached to *families of algebraic curves*, using the powerful machinery of the "six operations" for relative motives developed in [Ayoub's thesis](http://user.math.uzh.ch/ayoub/PDF-Files/THESE.PDF). This work is both a small piece of evidence of the general "motivic t-structure conjecture", and relates to many classical ideas in algebraic geometry about degenerations of curves and abelian varieties.
