---
name: academic-paper-latex
description: "Use this skill when the user asks to create, edit, or set up a LaTeX academic paper — working papers, journal submissions, research documents. Covers any academic document in LaTeX (not a policy note or institutional document — those use an institutional format skill of your own). Do NOT use for slides (use academic_slides_skill.md) or for Word documents (a Word format skill, bring your own)."
triggers: >-
  Setting up or editing an academic LaTeX paper (working paper, journal submission)
---

# Academic Paper LaTeX Skill

Template and conventions for academic economics papers in LaTeX. Designed for working papers, journal submissions, and research documents compiled in Overleaf or a local LaTeX installation.

**Rule:** Read this skill before setting up or editing any academic paper LaTeX file. Do not rely on memory of its contents from prior conversations.

---

## Before Starting — Confirm with the user

1. **Paper title**
2. **Authors and affiliations** (determines title page layout and "I" vs. "we")
3. **Is there a `.bib` file?** If not, create one. All citations go through BibTeX — no hardcoded references.
4. **Journal or submission requirements?** (formatting constraints, word limits, citation style)
5. **Working language:** Default is English.

---

## Preamble

The full LaTeX preamble lives in `academic_paper_preamble.tex`. When
setting up a paper, **copy the preamble's contents into the top of the main
`.tex` file** you produce — do not `\input{}` it. The preamble begins with
`\documentclass{article}` and is designed to be the literal start of a
standalone `.tex` file, not an included fragment.

### Key preamble rules

- **This is an ACADEMIC preamble.** Document chrome (title, section
  headers, links) follows academic conventions — black titles, default-blue
  links via `blue!60!black`. No institutional branding: no branded header,
  no logo footer, no colored title.
- **A color palette IS defined for figures.** The preamble includes a
  color palette (PrimaryBlue, SecondaryBlue, LightBlue, DarkBlue,
  SoftBlue, DarkGreen, LightGreen, WarmCream, and two grays)
  for use in figures, TikZ diagrams, and pgfplots charts. Figures often
  travel between an academic working paper and a policy note as the same
  chart, so the same palette is available in both contexts. Do NOT use
  these colors for document chrome.
- **The color block in the preamble is the definition.** The color block
  in `academic_paper_preamble.tex` is self-contained — it is the source of
  truth for this package. The palette is three hues, each in a few shades,
  plus grays: the user sets four base colors (`BaseBlue`, `BaseGreen`,
  `BaseYellow`, `BaseGray`) and the shades are derived from them. The
  package ships generic placeholder values; before the first real figure,
  ask the user for their four base colors (or align the block with the
  project's own color reference, if it has one). Keep the color *names*
  stable so the rest of the template keeps working.
- **Add packages BEFORE the `\hyperref` block.** Hyperref must be loaded
  last.
- **`natbib` for citations.** Use `\citet{}` for in-text citations ("Author
  (2003)") and `\citep{}` for parenthetical citations ("(Author, 2003)").
  The bibliography style can be changed per journal — `aer` for American
  Economic Review style is the default. Confirm with the user.
- **No hardcoded citations.** All references go through the `.bib` file.
  If a paper doesn't have a BibTeX entry yet, create one.
- **Line numbers** are available via `\linenumbers` — uncomment for draft
  review, comment out for submission.

---

## Title Page

The title page is a custom `\begin{titlepage}` with centered elements. Not the standard `\maketitle`.

```latex
\begin{titlepage}
\centering
\vspace*{1.5cm}
{\LARGE\bfseries Paper Title\par}
\vspace{1cm}

% Authors — one minipage per author, side by side
\begin{minipage}[t]{0.4\textwidth}
\centering
{\large Author One\par}
\vspace{0.3cm}
{\normalsize Affiliation One\\
\href{mailto:email@example.com}{email@example.com}}
\end{minipage}
\hspace{0.75cm}
\begin{minipage}[t]{0.4\textwidth}
\centering
{\large Author Two\par}
\vspace{0.3cm}
{\normalsize Affiliation Two}
\end{minipage}

\vspace{1cm}

% Abstract
\begin{minipage}{0.9\textwidth}
\begin{center}{\large\bfseries Abstract}\end{center}
\vspace{0.3cm}
\small
\onehalfspacing
\noindent Abstract text here.
\end{minipage}

\vspace{0.8cm}

% JEL codes and keywords
\begin{minipage}{0.85\textwidth}
\noindent\textbf{JEL Codes}: X00, Y00\\
\noindent\textbf{Keywords}: keyword1, keyword2, keyword3
\end{minipage}
\end{titlepage}
```

**Rules:**
- Title in `\LARGE\bfseries`, no color — black on white.
- Authors side by side in minipages. For 3+ authors, use three minipages or stack into rows.
- Abstract in a 0.9-width minipage, `\small`, 1.5-spaced.
- JEL codes and keywords below the abstract.
- A `\footnotemark`/`\footnotetext` on the title can point to a replication package, acknowledgments, or version URL.

---

## Paper Structure

Standard empirical economics:

1. **Introduction** — self-contained summary: question, contribution, mechanism, strategy, key results, implications
2. **Framework / Literature** — conceptual framework, literature positioning
3. **Data and Empirical Strategy** — data description, identification, estimation
4. **Results** — main results, robustness, heterogeneity
5. **Conclusion** — findings, policy implications, limitations

Adapt to the paper. Theory papers, reviews, and measurement papers have different structures — follow the user's outline.

---

## Tables

**Default convention: tables live in external files.** Each table is a standalone `.tex` file in a `tables/` subfolder, included in the main document via `\input{}`. This makes it easy to regenerate tables from Stata, R, or Python without editing the paper.

In the main `.tex` file:
```latex
\input{tables/table_results.tex}
```

The external table file (`tables/table_results.tex`) is self-contained:
```latex
\begin{table}[htbp]
    \centering
    \caption{Table Title}
    \label{tab:label}
    \footnotesize
    \begin{tabular}{@{}lcc@{}}
        \toprule
        Variable & Model 1 & Model 2 \\
        \midrule
        \emph{Coefficient name} & 0.372*** & 0.372*** \\
         & (15.96) & (15.87) \\
        \bottomrule
        \multicolumn{3}{l}{\footnotesize * p<0.10, ** p<0.05, *** p<0.01} \\
    \end{tabular}
    \tablenote{Estimation details, sample, controls.}
\end{table}
```

**Rules:**
- Use `booktabs` exclusively (`\toprule`, `\midrule`, `\bottomrule`). No vertical lines.
- `\footnotesize` for table content.
- Standard errors in parentheses below coefficients.
- Significance stars as table footnote.
- `\tablenote{}` for substantive notes (data sources, sample restrictions, controls).
- `\label` immediately after `\caption` for correct cross-referencing.
- If the user provides a table directly in chat (not as an external file), it's fine to write it inline — but the default is external.

---

## Figures

**Same convention: figures live in a `figures/` subfolder.** Referenced by path in the main document.

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/density_scores.png}
    \caption{Figure Title}
    \label{fig:label}
    \figurenote{Description of what the figure shows, data source.}
    \figuresource{Source if applicable.}
\end{figure}
```

**Rules:**
- Every figure gets a `\figurenote{}` explaining what the reader should see.
- `\figuresource{}` when the data comes from an external source.
- For side-by-side figures, use `subcaption` with two `\begin{subfigure}` environments.

### Project folder structure

```
paper/
├── main.tex              ← the paper
├── references.bib        ← bibliography
├── tables/
│   ├── table_results.tex
│   ├── table_robustness.tex
│   └── ...
└── figures/
    ├── density_scores.png
    ├── spending_trends.png
    └── ...
```

---

## Citations

**Always use `natbib` commands**, never hardcode references.

| Pattern | Command | Output |
|---------|---------|--------|
| In-text | `\citet{Author2003}` | Author (2003) |
| Parenthetical | `\citep{Author2003}` | (Author, 2003) |
| Multiple | `\citep{Author2003, Other2024}` | (Author, 2003; Other, 2024) |
| With page | `\citep[p.~15]{Author2003}` | (Author, 2003, p. 15) |

End the document with:

```latex
\bibliography{references}  % or whatever the .bib file is named
\end{document}
```

---

## Equations

```latex
\begin{equation}
C_{it} = f(X_{it}, \varepsilon_{it})
\label{eq:cost}
\end{equation}
```

Define variables immediately after the equation in an indented minipage or inline text. Reference as `Equation~\eqref{eq:cost}`.

---

## Cross-Referencing

- Figures: `Figure~\ref{fig:label}`
- Tables: `Table~\ref{tab:label}`
- Equations: `Equation~\eqref{eq:label}`
- Sections: `Section~\ref{sec:label}`

Always use `~` (non-breaking space) before `\ref`.

---

## Format Specification at a Glance

| Feature | Academic paper |
|---------|---------------|
| Margins | 1 inch all around |
| Spacing | 1.5 (`\onehalfspacing`) |
| Font | Latin Modern (default) |
| Title page | Custom `\titlepage` with author minipages |
| Headers/footers | None (clean) |
| Section titles | Default LaTeX (black) |
| Link colors | `blue!60!black` (academic convention) |
| Color palette | Defined, but ONLY for figures/TikZ/pgfplots |
| Bibliography | `natbib` + `.bib` file |

**Key point:** the preamble defines a color palette so that figures and TikZ
diagrams can carry consistent colors across a project — a chart often appears
in both an academic paper and a policy note. But the document chrome (titles,
sections, links) stays academic and unbranded.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
