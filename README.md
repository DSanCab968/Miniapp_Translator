# Miniapp Translator

A minimal AI translator used as the vehicle for the practice *Exploitation and deployment of an
AI application* (UD1). The goal of the practice is not the app itself but how it is **configured,
deployed, secured, tested and operated** on **Vercel** (serverless) and on **AWS EC2** (one Docker
container).

> Status: phase 0 (repository preparation). Sections marked *To be completed* are filled in as each
> milestone is closed.

## Table of contents

1. [Identification](#1-identification)
2. [Documentation plan](#2-documentation-plan)
3. [Architecture](#3-architecture)
4. [Requirements and local setup](#4-requirements-and-local-setup)
5. [Environment variables](#5-environment-variables)
6. [Vercel](#6-vercel)
7. [Clerk](#7-clerk)
8. [Docker](#8-docker)
9. [AWS](#9-aws)
10. [Operation and verification](#10-operation-and-verification)
11. [Problems and solutions](#11-problems-and-solutions)
12. [Git and evidence](#12-git-and-evidence)

## 1. Identification

| | |
|---|---|
| Practice | UD1 - Exploitation and deployment of an AI application |
| Module | Exploitation of Data Processing and Analytics Services (AI Specialization Course 2026-27) |
| Author | Daniel Sanchez Cabello |
| Team | Individual work (the practice is designed for groups of 2-3; all tasks were done by the author) |
| Mini app | **Translator**: the user writes a text in any language, picks a target language and the AI returns the translation and the detected source language |

**Individual contributions:** as this is individual work, every task (code, configuration, deployment,
tests, troubleshooting and documentation) was carried out by the author. The Git history shows the
evolution phase by phase.

## 2. Documentation plan

Before writing this README the documentation was planned following the ideas of the
[Diataxis guide](https://diataxis.fr/) and the
[GitHub Markdown guide](https://docs.github.com/en/get-started/writing-on-github).

| Question | Decision |
|---|---|
| Who reads it? | The teacher evaluating the practice, and anyone who wants to **reproduce** the deployment from this repository |
| What must they be able to do? | Run the app locally, deploy it to Vercel, build and run the Docker container, deploy it to EC2, and check that authentication works |
| Structure | A single README with the 12 sections required by the practice. Mostly *how-to* content (reproducible steps) plus short *explanation* parts (architecture, decisions) |
| Who maintains it? | The author |
| When is it updated? | At the end of **each milestone**, before creating its Git tag, so commands and problems are written down when they happen, not reconstructed at the end |
| Evidence | Screenshots in the `evidence/` folder (created when the first one is taken), linked from the related section with a short note of what each one proves. Secrets, tokens and personal data are hidden before saving them |
| Tools | Markdown (VS Code preview), tables and relative links, checklists, Mermaid for diagrams, Git for reviewing changes |

## 3. Architecture

*To be completed in phases 1-5.*

## 4. Requirements and local setup

*To be completed in phases 1-2.*

## 5. Environment variables

*To be completed in phases 1 and 4.* The template with fictitious values is [`.env.example`](.env.example).

## 6. Vercel

*To be completed in phase 3.*

## 7. Clerk

*To be completed in phase 4.*

## 8. Docker

*To be completed in phase 5.*

## 9. AWS

*To be completed in phase 6.*

## 10. Operation and verification

*To be completed in every phase.*

## 11. Problems and solutions

*Real incidents will be recorded here as they happen.*

## 12. Git and evidence

| Milestone | Tag | Status |
|---|---|---|
| Repository preparation | - | Done |
| Minimal backend | `v0.1-backend` | Pending |
| Frontend connected locally | `v0.2-frontend` | Pending |
| First Vercel deployment | `v0.3-vercel` | Pending |
| Clerk integrated and redeployed | `v0.4-auth` | Pending |
| Single container tested | `v0.5-docker` | Pending |
| Final AWS deployment | `v1.0-aws` | Pending |
