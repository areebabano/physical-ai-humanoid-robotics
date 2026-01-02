---
id: 1
title: Resolve Docusaurus build circular dependency errors
stage: fix
date: 2026-01-03
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 001-physical-ai-textbook
user: owner
command: npm run build
labels: [docusaurus, build, webpack, circular-dependency]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/theme/NavbarItem/Type/custom-AuthButtons.js
  - src/theme/DocItem/Layout/index.js
  - src/components/HomepageFeatures/index.tsx
  - docusaurus.config.ts
tests:
  - npm run clear && npm run build
---

## Prompt

build errors resolve kro Microsoft Windows [Version 10.0.19045.6466]
(c) Microsoft Corporation. All rights reserved.

D:\AI Book\physical-ai-humanoid-robotics>npm run build

> physical-ai-humanoid-robotics@0.0.0 build
> docusaurus build

[INFO] Website will be built for all these locales:
- en
- ur
[INFO] [en] Creating an optimized production build...

* Client █████████████████████████ building (18%) 0/1 entries 3489/3537 dependencies 815/1195 m
odules 321 active
 node_modules\is-nan\implementation.js

× Server
  Compiled with some errors in 42.05s


× Client
  Compiled with some errors in 1.61m

× Server


[ERROR] Client bundle compiled with errors therefore further build is impossible.
Self-reference dependency has unused export name: This should not happen

--------------------------

Self-reference dependency has unused export name: This should not happen

D:\AI Book\physical-ai-humanoid-robotics>

## Response snapshot

I have resolved the build errors in your Docusaurus project. The primary issue was a "Self-reference dependency" error caused by circular imports in swizzled theme components and non-theme components using theme aliases inappropriately. I also fixed a build error for the Urdu locale by disabling the search index for that language as it was missing required dependencies.

## Outcome

- ✅ Impact: The project now builds successfully for both English and Urdu locales.
- 🧪 Tests: Verified with `npm run clear && npm run build`.
- 📁 Files: Modified `src/theme/NavbarItem/Type/custom-AuthButtons.js`, `src/theme/DocItem/Layout/index.js` (backed up to `.backup`), `src/components/HomepageFeatures/index.tsx`, and `docusaurus.config.ts`.
- 🔁 Next prompts: None.
- 🧠 Reflection: The circular dependency errors in Docusaurus often stem from swizzled components trying to import from themselves via the `@theme` alias loop. Using `@theme-original` or restoring default components is the most reliable fix.

## Evaluation notes (flywheel)

- Failure modes observed: Initial patches to theme files were insufficient due to deeper circularity in complex swizzled layouts.
- Graders run and results (PASS/FAIL): Final build PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
