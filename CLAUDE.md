# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a GitHub **profile README** repository (`ichrakhamdi/ichrakhamdi`). GitHub renders `README.md` at the top of https://github.com/ichrakhamdi, so that file is the whole product. There is no code, build, lint or test tooling. Pushing to `main` publishes changes immediately.

## Editing README.md

- Centered blocks are raw HTML (`<div align="center">`) because GitHub Markdown can't center content. Badges are shields.io images. Everything else is GitHub-flavored Markdown.
- `assets/hero.svg` is a hand-written SVG banner, animated with CSS keyframes. GitHub serves it through its image proxy, so they can't load external fonts or scripts. It draws its own dark background so it reads the same in light and dark themes. To check the layout, render one with `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=1200,400 --screenshot=out.png file://$PWD/assets/hero.svg`.
- Sections in order: hero + badges → What I work on (2×2 table) → Toolbox → Selected work (spotlight projects + a `<details>` block with smaller ones) → Current direction (YAML) → Let's connect.
- **The PhD research is unpublished and confidential.** Describe it only at the level of the public summary (RL for safety-aware cyberattack response in industrial CPS). Don't add method details, architecture diagrams or pipeline descriptions, and don't mention hierarchical RL.
- No emoji anywhere in the README.
- Every project description must match what the linked repo actually contains. Check the repo before adding or rewording one.
- The profile presents the owner as a PhD researcher in Computer Science at Université Laval, working on reinforcement learning for intrusion response in industrial cyber-physical systems. Keep new content consistent with that framing and with the existing tone: first person, concise, professional.
- The LinkedIn URL appears twice (header and Connect section). When a link changes, update every place it appears.
- Before adding a repo to the Selected projects table, check that it exists and is public under the `ichrakhamdi` account.
- To check the rendering, use a GitHub-flavored Markdown previewer before pushing, since every push to `main` goes live.
