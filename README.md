# GitHub Mining Starter for Your COSC 540 Project

This starter pack sets up the **GitHub mining** side of your project:

**Empirical Study of LLM-Generated Unit Tests for Real GitHub Bugs and When They Outperform Human Tests**

It is designed to help you do four things fast:

1. discover BugsInPy projects and bug counts
2. select a manageable bug subset
3. checkout buggy and fixed versions
4. extract bug patch metadata and human-written test information into JSON and CSV

## Recommended folder structure

```text
github_mining_starter/
  README.md
  config/
  data/
    metadata/
    patches/
    processed/
    raw/
  notebooks/
  outputs/
    per_bug_json/
  scripts/
    common.py
    00_discover_projects.py
    01_create_bug_list.py
    02_checkout_versions.py
    03_extract_diff.py
    04_extract_tests.py
    05_build_summary.py
```

## Before you run anything

You need a local BugsInPy clone.

The official BugsInPy repo documents this basic setup pattern:

- clone the repository
- add `framework/bin` to your `PATH`
- use commands such as `bugsinpy-checkout`, `bugsinpy-compile`, and `bugsinpy-test`
- optionally use Docker if dependency setup is painful

## Suggested setup

### 1. Clone BugsInPy

```bash
git clone https://github.com/soarsmu/BugsInPy
```

### 2. Add BugsInPy commands to PATH

```bash
export PATH="$PATH:/path/to/BugsInPy/framework/bin"
```

### 3. Test that it works

```bash
bugsinpy-checkout --help
```

## Step-by-step usage

Run these commands from the root of this starter folder.

### Step 0: discover available projects

```bash
python scripts/00_discover_projects.py \
  --bugsinpy-root /path/to/BugsInPy
```

This writes:

- `outputs/discovery/projects.csv`
- `outputs/discovery/projects.json`

### Step 1: select the first 5 bugs from pandas, ansible, and youtube-dl

```bash
python scripts/01_create_bug_list.py \
  --bugsinpy-root /path/to/BugsInPy \
  --projects pandas ansible youtube-dl \
  --limit-per-project 5
```

This writes:

- `outputs/selection/selected_bugs.csv`
- `outputs/selection/selected_bugs.json`

### Step 2: checkout buggy and fixed versions

```bash
python scripts/02_checkout_versions.py \
  --selected-bugs outputs/selection/selected_bugs.json
```

This writes:

- `outputs/checkout_manifest.json`
- checkout folders under `workspace/checkouts/`

> Note: the script defaults to `-v 0` for buggy and `-v 1` for fixed. If your local BugsInPy install behaves differently, override those flags in the command.

### Step 3: extract patch-level metadata

```bash
python scripts/03_extract_diff.py \
  --bugsinpy-root /path/to/BugsInPy \
  --selected-bugs outputs/selection/selected_bugs.json
```

This writes:

- copied `.patch` files under `data/patches/`
- one JSON file per bug under `outputs/per_bug_json/`

### Step 4: extract human-written test info

```bash
python scripts/04_extract_tests.py
```

This enriches each per-bug JSON file with:

- changed test files
- added test function names
- added assertions
- extracted test function bodies when available from the fixed checkout

### Step 5: build one summary CSV

```bash
python scripts/05_build_summary.py
```

This writes:

- `outputs/bug_summary.csv`

## What a good first run looks like

Start with **10 bugs total**:

- pandas: 5
- ansible: 5

Or:

- pandas: 5
- youtube-dl: 5

That gives you a realistic pilot dataset before scaling.

## What you will have at the end

For each bug, you will have:

- bug metadata
- patch file
- changed source files
- changed test files
- likely human regression tests
- test names
- assertion hints
- flat CSV summary for analysis

## Good next extensions

After this starter works, the next improvements are:

- parse failing test commands from `bug.info` more precisely
- classify bug type manually or semi-automatically
- measure patch size and test churn more deeply
- add a Docker wrapper for reproducibility
- generate LLM-ready context bundles per bug

