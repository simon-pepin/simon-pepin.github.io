---
layout: page
title: "Machine learning, singularity theory and phase transitions"
permalink: /organisation/singular_learning_theory_sep23
---

This is the webpage of an informal workshop organised at the University of Amsterdam on September 18th-21st 2023 around **Singular Learning Theory** and its burgeoning applications to the training dynamics of deep neural networks. This is a topic at the interface of machine learning, statistics and singularity theory in real-analytic geometry, so we expect a diverse audience, and the talks on Monday will provide some background from each discipline.

Singular learning theory is an application of the tools of singularity theory to Bayesian statistics. Our aim will be to survey the recent paper [Quantifying degeneracy in singular models via the learning coefficient](https://arxiv.org/abs/2308.12108), both at a theoretical and practical level, and discuss work-in-progress on other deep learning systems. See the [program](/organisation/SLT/slt-amsterdam-sep23-program.pdf) for more details.

### _Practical details:_

- The workshop will take place from Monday 18th to Thursday 21st, from 10:00 to 17:00 **except on Monday where we start at 09:30**

- Everything will take place Room F1.15, in the building Science Park 107 of the Science Park campus of the University of Amsterdam.

### Program and schedule:

Here is the current version of the [program](/organisation/SLT/slt-amsterdam-sep23-program.pdf).

### Extended description:

Modern machine learning systems attempt - and, to a surprising degree, succeed - to "learn" from large datasets collected from many sources (text, images, scientific data about the natural world, records of human behaviours, sensors from large human-made processes) A key lesson of the **"deep learning revolution"** of the last ten years has been that, given enough data and computational power, relatively simple but very large hierarchical models can learn to classify and generate very complicated data.

Unfortunately, large trained deep neural networks are essentially "black boxes" whose internal learned representations and computational structure is almost impenetrable. Even worse, classical theoretical frameworks from statistics and optimization struggle to explain why such models work at all!

The key difference between deep neural networks and more classical statistical models is their highly hierarchical structure and the fact that they are highly degenerate, in the sense that many of their internal states gives rise to the same function. Moreover, they often have enough parameters that they can *perfectly* classify their training data, and yet still perform well on new data points! This implies that many conventional statistical ideas and results (identifiability, overfitting, asymptotic normality, Cramer-Rao inequality...) are not applicable to such \emph{singular models}. Singular learning theory explains that the (Bayesian) learning process of singular models is to a large extent controlled by the geometry of the singularities of the loss function of the model. In particular, the asymptotic behaviour of how well the model generalizes to new data is controlled by
the **real log-canonical threshold** (RLCT) of the loss function, a standard invariant of real-analytic functions in singularity theory which is tightly linked to **resolution of singularities**. The RLCT is a measure of effective dimension of the system which explains the fact that singular models generally "do not overfit". Another remarkable consequence is that the learning dynamics of singular models exhibit **phase transitions** as the size of the dataset increases - matching empirical observations from real deep-learning systems. These phase transitions refine certain classical analogies between statistical learning and statistical mechanics.

Singular learning theory has been developped for 25 years by the statistician Sumio Watanabe as a theoretical framework for Bayesian inference, but it has very recently started to be applied directly to deep learning systems. This requires developping efficient and scalable estimates for the RLCT, the main topic of the [paper](https://arxiv.org/abs/2308.12108). We will see that this works in practice and already provides some insights into the behaviour and phase transitions of some simple neural networks, with many more applications in the pipeline. This is the starting of a more ambitious research program of [Developmental Interpretability](https://devinterp.com/) aimed at understanding the formation of the computational structure of neural networks along the course of training, which we will only have time to briefly touch on.

### Ressources:

Besides the [paper](https://arxiv.org/abs/2308.12108) and the [two](https://www.cambridge.org/core/books/algebraic-geometry-and-statistical-learning-theory/9C8FD1BDC817E2FC79117C7F41544A3A) [textbooks](https://www.routledge.com/Mathematical-Theory-of-Bayesian-Statistics/Watanabe/p/book/9780367734817) of Watanabe, there is an extensive list of references at the [Developmental Interpretability](https://devinterp.com/resources) website.
