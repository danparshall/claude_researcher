---
name: academic-slides
description: "Use this skill when the user asks to create, edit, or work on academic presentation slides — conference talks, seminar presentations, paper presentations, workshop slides. Do NOT use for internal coordination slides (unit meetings, strategic planning) — those use an institutional slides skill of your own."
triggers: >-
  Creating or editing academic Beamer slides (conference, seminar)
---

# Academic Slides Skill

Beamer template and formatting conventions for academic presentations — conference talks, seminars, paper presentations, workshops.

**Technology:** LaTeX Beamer (Boadilla theme with custom colors), compiled via Overleaf or local LaTeX installation.

**Rule:** Read this skill before creating or editing any academic slides. Do not rely on memory of its contents from prior conversations.

---

## Before Starting — Ask the user

1. **Language:** Default is English. Ask which language the deck is in; for a language other than English load the matching `babel` option.
2. **Confirm the following:**
   - Paper title
   - Authors and affiliations
   - Conference/seminar name and date
   - Whether this is co-authored (affects "I" vs. "we" in slide text)

---

## Claude Design keeps the markdown text

**The rule.** When a deck built from repo markdown goes into Claude
Design, the tool is told to **keep the text written in the `.md` exactly as it is** and to
iterate from that text. It is never left free to rewrite the prose. Design work is layout,
hierarchy and visual treatment; the words are already decided.

**Why.** A design tool left free to rewrite regenerates the prose. The repo's markdown carries prose that has been
through review rounds and voice work; a design tool regenerating it discards that and
reintroduces wording nobody approved.

**If text genuinely has to change to fit a slide,** that is a change to raise with the user, not
one to absorb silently.

## Color Palette

The colors live in the color block of the preamble file
(`academic_slides_preamble.tex`). That block is self-contained — it is the
definition for this template. The palette is three hues, each in a few
shades, plus grays: the user sets four base colors (`BaseBlue`, `BaseGreen`,
`BaseYellow`, `BaseGray`) and the shades are derived from them. The package
ships generic placeholder values, so a deck compiles as shipped. Before the
first real deck, ask the user for their four base colors (or align the block
with the project's own color reference, if it has one). Keep the color
*names* stable, since the Beamer theme settings and the role assignments
below refer to them.

**Slide-specific role assignments:**
- Frame title bar: PrimaryBlue background, white text
- Bullet markers: SecondaryBlue
- Section divider text: PrimaryBlue
- Block titles: PrimaryBlue (via Boadilla theme)
- Table highlights: `\rowcolor{LightBlue}`
- TikZ diagrams: PrimaryBlue for points/lines, DarkGreen for curves/frontiers, SecondaryBlue for annotations
- Heatmaps / conditional formatting: WarmCream (high), SoftBlue (mid), LightGreen (low)

---

## Beamer Preamble

The full Beamer preamble lives in `academic_slides_preamble.tex`. When
generating a slide deck, **copy the preamble's contents into the top of the
main `.tex` file** you produce — do not `\input{}` it. The preamble begins
with `\documentclass{beamer}` and is designed to be the literal start of a
standalone `.tex` file, not an included fragment.

### Key preamble rules

- **The color block in the preamble is the definition.** To change the
  palette, set the four base colors in `academic_slides_preamble.tex`
  (aligning them with the project's own color reference, if it has one); a
  new shade is one more `\colorlet` line derived from a base. Keep the color
  names stable so the theme settings keep working.
- **Beamer theme colors are set explicitly** (`\setbeamercolor{...}`) rather
  than relying on Boadilla defaults. If overriding, edit the preamble file,
  not the skill.
- **No logo overlay by default.** The preamble carries a commented-out
  `\addtobeamertemplate{frametitle}` block for projects that do have a logo.
  If a project uses one, uncomment that block rather than placing the image
  frame by frame.
- **Hyperref must be loaded last among packages** that interact with links.
  The preamble file orders packages accordingly.

---

## Title Page

The title page includes: title, authors with affiliations, conference/seminar name, and date.

```latex
\title[Short Title]{Full Paper Title}
\author[LastName et al.]{
  Author One\inst{1} \and Author Two\inst{2} \and Author Three\inst{1}
}
\institute[]{
  \scriptsize{
    \inst{1} Institution One
    \and \inst{2} University Name, Department
  }
}
\date[MM-DD-YYYY]{Conference or Seminar Name \\ Month Day, Year}
```

**Rules:**
- Full title in the main `\title{}`, short title in brackets for the footer bar.
- Authors listed with `\inst{}` markers linking to affiliations.
- `\date{}` carries both the conference/seminar name and the date — conference name on the first line, date on the second.
- No logo on the title page by default. If a project has one, add a
  `\titlegraphic{}` block pointing at its image file (0.35in height works
  well) and uncomment the matching overlay block in the preamble so title and
  non-title slides stay consistent.
- Some authors prefer `\inst{$*$}` and `\inst{$\ddagger$}` symbols rather than numbers — either convention is fine, confirm with the user.

---

## Presentation Structure

Academic presentations follow this arc:

### 1. Title slide

```latex
\begin{frame}
\titlepage
\end{frame}
```

### 2. Motivation (1–2 slides)

Set up the problem. Why does this matter? End with the research question, often as a `\begin{block}` or a direct question.

### 3. Outline slide

List the remaining sections. Keep it simple — 4–6 items.

```latex
\begin{frame}{Outline}
\begin{itemize}
\item Background
\item Hypotheses
\item Empirical Strategy
\item Results
\item Conclusion
\end{itemize}
\end{frame}
```

### 4. Section divider slides

Every time the presentation moves to a new section from the outline, insert a divider slide. These are visually distinct — large PrimaryBlue text, centered, no other content. **Must use `[plain]` to suppress the frametitle bar overlay**, and `\vfill` above and below to vertically center the text.

```latex
\begin{frame}[plain]
\vfill
{\Huge \textcolor{PrimaryBlue}{
\begin{center}
Section Name
\end{center}}}
\vfill
\end{frame}
```

Use `\section{Section Name}` before the divider for navigation bar tracking.

### 5. Content slides

The body of the presentation. See Slide Types below.

### 6. Conclusion (1–2 slides)

Main findings, then policy implications. Each as a separate slide.

### 7. Thank you slide

```latex
\begin{frame}{Thank you!}
\begin{center}
\vspace{1cm}
Contact: \\
\texttt{email@example.org}
\end{center}
\end{frame}
```

### 8. Appendix (optional)

Detailed derivations, extra tables, robustness checks. Use `\appendix` and `\section*{Appendix}`. Link to appendix slides from the main presentation using `\beamergotobutton` and back using `\beamerreturnbutton`.

---

## Slide Types

### Text + bullets

The most common type. Standard presentation conventions: bold lead-ins, 1–2 line bullets, max two nesting levels.

### Two-column layout

Use when showing a figure alongside interpretation, or two related charts.

```latex
\begin{columns}[t]
\begin{column}{0.48\textwidth}
  % Left content (figure or text)
\end{column}
\begin{column}{0.48\textwidth}
  % Right content (interpretation or second figure)
\end{column}
\end{columns}
```

**Prefer two-column layouts when possible** — they use slide space efficiently and keep figures next to their interpretation.

### Block slides

For hypotheses, key questions, or highlighted results. Boadilla theme styles these with PrimaryBlue headers.

```latex
\begin{block}{Hypothesis 1: Fragmentation}
Statement of the hypothesis.
\end{block}
```

### Equation slides

Equations in `\begin{equation}` with variable definitions below in an indented `\begin{minipage}`.

```latex
\begin{equation}
C_{it} = f(X_{it}, Z_{it})
\end{equation}

\hspace{2.5cm}\begin{minipage}{0.78\textwidth}
\begin{itemize}
\item $C_{it}$: Description
\item $X_{it}$: Description
\end{itemize}
\end{minipage}
```

### Table slides

Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). Highlight key rows with `\rowcolor{LightBlue}`. Wrap in `\begin{small}` if the table is dense.

### Heatmap / conditional-color tables

For tables where cells should be colored by category (e.g., high/mid/low), use `\cellcolor` with the heatmap colors and `\makecell` for multi-line cell content (requires `\usepackage{makecell}`). Add a legend below the table.

```latex
\cellcolor{WarmCream}\makecell{$-$12.3\% \\ {\tiny ($-$15.0, $-$9.6)}}
```

Convention for three tiers:
- `WarmCream` — highest intensity
- `SoftBlue` — middle
- `LightGreen` — lowest intensity

Legend at the bottom of the table:
```latex
{\tiny \colorbox{WarmCream}{\strut} Higher ($>$X\%) \quad
\colorbox{SoftBlue}{\strut} Middle (Y--X\%) \quad
\colorbox{LightGreen}{\strut} Lower ($<$Y\%)}
```

### TikZ diagram slides

For conceptual frameworks, frontier illustrations, process diagrams. Use the color conventions from the preamble's color block. Scale diagrams with `scale=0.63` or similar to fit the slide.

### Navigation buttons

Use `\beamergotobutton` and `\beamerreturnbutton` with `\hyperlink` and `\label` to connect main slides to appendix detail. Place buttons at the bottom-right of the slide.

```latex
\hyperlink{TargetLabel}{\beamergotobutton{Button Text}}
% and on the target slide:
\hyperlink{SourceLabel}{\beamerreturnbutton{Back}}
```

---

## Formatting Rules

- **`\pause` for sequential reveals.** Use within slides to build arguments step by step. Especially useful for hypotheses (reveal one at a time) and results (show finding, then interpretation).
- **Significance stars** in tables: `* p<0.10, ** p<0.05, *** p<0.01` as a footnote below the table.
- **Bold for emphasis** within bullets: `\textbf{key term}` for the most important phrase in each bullet.
- **Equations are motivated.** Before showing an equation, explain in words what it captures. After, define each term.
- **Figures get interpretation.** Never show a figure without text explaining what the audience should see in it — either in a column next to it or in a line below.

---

## Required Assets

None. The template compiles as shipped with no external image files.

Figure files (charts, maps, density plots) are project-specific. If a project
uses a logo, it supplies the image itself and wires it in via the preamble's
commented-out overlay block plus a `\titlegraphic{}` on the title slide.

---

## Markdown Mirror Convention

When creating a slide deck, also create a `_text.md` file alongside the `.tex` file. This markdown file contains the plain-text content of every slide, one section per slide. It serves two purposes: (1) easy diffing in GitHub when the slide content changes, and (2) a readable reference for reviewing slide text without opening LaTeX. Update the markdown mirror whenever the `.tex` file is updated. Include a version number and date at the top.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
