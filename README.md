# raycast-infra-scripts

Raycast script commands for infrastructure engineers.

**What's inside:**

| Script | What it does |
|---|---|
| **Zone Lookup** | Type a zone name (or partial name) → instantly see the DNS zone, AWS profile, and region. No digging through Terraform. |

---

## Table of Contents

1. [What is Raycast?](#what-is-raycast)
2. [What you need before starting](#what-you-need-before-starting)
3. [Step 1 — Install Homebrew](#step-1--install-homebrew)
4. [Step 2 — Install Python](#step-2--install-python)
5. [Step 3 — Install Raycast](#step-3--install-raycast)
6. [Step 4 — Clone this repository](#step-4--clone-this-repository)
7. [Step 5 — Run the setup script](#step-5--run-the-setup-script)
8. [Step 6 — Add scripts to Raycast](#step-6--add-scripts-to-raycast)
9. [Step 7 — Test it](#step-7--test-it)
10. [Using Zone Lookup](#using-zone-lookup)
11. [Custom infra repo path](#custom-infra-repo-path)
12. [Keeping data up to date](#keeping-data-up-to-date)
13. [Troubleshooting](#troubleshooting)

---

## What is Raycast?

[Raycast](https://raycast.com) is a free launcher for macOS — think of it as a smarter Spotlight. You open it with a hotkey, type a command name, and it runs things for you.

After this setup, you'll use it like this:
1. Press **`⌥ Space`** (Option + Space) — the Raycast search bar opens
2. Type **`Zone Lookup`**
3. Press Enter, type your query (e.g. `eu1` or a full zone name)
4. Press Enter — results appear instantly

You don't need to learn anything else about Raycast. These are the only steps you'll repeat.

---

## What you need before starting

| Tool | Why | Already have it? |
|---|---|---|
| **Homebrew** | Package manager — used to install Python | Run `brew --version` in Terminal |
| **Python 3** | Runs the lookup script | Run `python3 --version` in Terminal |
| **Raycast** | The launcher that shows results | Check if it's in your Applications |
| **Infra repo** | Source of zone data (your Terraform repo) | You probably already have it cloned |

If you have all four — skip to [Step 4](#step-4--clone-this-repository).

If you're unsure — go through each step below. They're quick.

---

## Step 1 — Install Homebrew

> Skip this step if `brew --version` works in your Terminal.

Homebrew is the standard package manager for macOS. Open **Terminal** (press `⌘ Space`, type `Terminal`, press Enter) and paste this command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The installer will ask for your Mac login password and may ask you to confirm a few times. This is normal — it's installing developer tools. The process takes 2–5 minutes.

**After it finishes**, the installer will print something like:

```
==> Next steps:
Run these commands in your terminal:
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Run those two commands** (copy them exactly from your terminal output — the path may differ on Intel Macs).

Then verify it worked:

```bash
brew --version
```

You should see something like `Homebrew 4.x.x`. If you do, Homebrew is ready.

---

## Step 2 — Install Python

> Skip this step if `python3 --version` shows `Python 3.x.x` in your Terminal.

With Homebrew installed, run:

```bash
brew install python
```

This takes about 1–2 minutes. When it's done, verify:

```bash
python3 --version
```

Expected output: `Python 3.12.x` (or any 3.x version).

> **Note:** macOS includes a very old Python 2 at `/usr/bin/python`. Always use `python3`, not `python`.

---

## Step 3 — Install Raycast

> Skip this step if Raycast is already in your `/Applications` folder.

1. Go to [raycast.com](https://www.raycast.com) and click **Download for Mac** (it's free)
2. Open the downloaded `.dmg` file
3. Drag **Raycast** into your **Applications** folder
4. Open Raycast from Applications
5. Follow the brief onboarding — it will ask you to set a hotkey

The default hotkey is **`⌥ Space`** (Option + Space). You can keep it or change it. This guide assumes `⌥ Space`.

> **Tip:** If Spotlight is currently on `⌥ Space`, Raycast will offer to take over that shortcut. Let it — Raycast can do everything Spotlight does plus more.

---

## Step 4 — Clone this repository

Open **Terminal** and run:

```bash
git clone https://github.com/pavelsidla/raycast-infra-scripts.git ~/projects/raycast-infra-scripts
```

> If you prefer a different location, change `~/projects/raycast-infra-scripts` to any path you like — just remember it for the next step.

---

## Step 5 — Run the setup script

```bash
cd ~/projects/raycast-infra-scripts
bash setup.sh
```

The setup script will:
1. **Check that Python is installed**
2. **Find your infrastructure repo** — it tries common locations automatically. If your repo is in a non-standard location, it will ask you to type the full path
3. **Save your config** to `~/.config/raycast-infra/config` (so you don't have to configure anything again)
4. **Run a quick test** to confirm the lookup script can read your zone data
5. **Mark the scripts as executable** so Raycast can run them

Example of what a successful run looks like:

```
┌─────────────────────────────────────────────────────┐
│   raycast-infra-scripts — Setup                     │
└─────────────────────────────────────────────────────┘

Checking prerequisites...

  ✓ Python found: Python 3.12.3
  ✓ Found infra repo at: /Users/yourname/projects/infra

  Use this path? [Y/n] Y
  ✓ Config saved to: /Users/yourname/.config/raycast-infra/config
  ✓ Scripts marked as executable

Running a quick test...

  ✓ Found 42 zones.

┌─────────────────────────────────────────────────────┐
│   Setup complete!                                    │
│                                                      │
│   Last step: add scripts/ folder to Raycast.        │
│   See README.md → Step 4 for instructions.          │
└─────────────────────────────────────────────────────┘
```

If setup fails, check the [Troubleshooting](#troubleshooting) section.

---

## Step 6 — Add scripts to Raycast

This tells Raycast where your scripts live.

1. Open Raycast with **`⌥ Space`**
2. Type `Script Commands` and press Enter
   _(or go to Raycast Preferences `⌘ ,` → Extensions → Script Commands)_
3. In the Script Commands window, click the **`+`** button in the top-right corner
4. Select **"Add Directory…"**
5. In the file picker that opens, navigate to:
   ```
   ~/projects/raycast-infra-scripts/scripts/
   ```
   _(If you cloned to a different location, navigate there instead)_
6. Click **"Open"** (or press Enter)

Raycast will scan the folder and register the **Zone Lookup** command. You should see it appear in the list immediately.

> **Tip:** You can also use the keyboard shortcut. In the file picker, press `⌘ Shift G`, paste the path `~/projects/raycast-infra-scripts/scripts/` and press Enter.

---

## Step 7 — Test it

1. Open Raycast with **`⌥ Space`**
2. Type `Zone Lookup`
3. Press Enter (or click it)
4. A text input appears — type a zone name or partial name
5. Press Enter

You should see colored output with zone details. If you see an error, check [Troubleshooting](#troubleshooting).

---

## Using Zone Lookup

### Search by full or partial zone name

Partial names work — you don't need to type the full name:

| What you type | What you get |
|---|---|
| `eu1` | All zones containing "eu1" |
| `us1` | All zones containing "us1" |
| `prod` | All production zones |
| `dev` | All development zones |
| `full-zone-name` | Exact details for that one zone |

### Search by DNS name

You can also type part of a DNS name and it will match:

| What you type | What you get |
|---|---|
| `example.com` | All zones with that domain in their DNS name |

### Understanding the output

When you search for a specific zone, you'll see:

```
zone-name-here
  dns_zone          the.dns.domain.for.this.zone
  aws_profile       your-aws-profile-name
  region            eu-west-1
  environment       slave/production
```

| Field | What it means | How to use it |
|---|---|---|
| `dns_zone` | The DNS domain for this environment | Use for filtering logs in your observability tool |
| `aws_profile` | AWS CLI profile name | `aws --profile <value> s3 ls` |
| `region` | AWS region | Know which region to look in for resources |
| `environment` | Deployment type and tier | Distinguish prod / dev / release at a glance |

---

## Custom infra repo path

If `setup.sh` couldn't find your repo automatically, you can configure the path manually.

**Option A — Re-run setup** (recommended):
```bash
bash ~/projects/raycast-infra-scripts/setup.sh
```
It will ask you to enter a path.

**Option B — Edit the config file directly**:
```bash
# Create the config directory if it doesn't exist
mkdir -p ~/.config/raycast-infra

# Write your path
echo 'INFRA_REPO_PATH=/full/path/to/your/infra-repo' > ~/.config/raycast-infra/config
```

Replace `/full/path/to/your/infra-repo` with the actual path to the directory that contains the `accounts/` folder.

Example:
```
INFRA_REPO_PATH=/Users/jane.doe/work/my-infra-repo
```

---

## Keeping data up to date

The script reads directly from your local infra repo every time you run it — there is no cache. To get new or updated zones, just pull the latest changes from your repo:

```bash
cd ~/path/to/your/infra-repo && git pull
```

---

## Troubleshooting

### "Error: could not find your infrastructure repo"

The script didn't find a directory with an `accounts/` folder. Fix:

1. Make sure your infra repo is cloned locally:
   ```bash
   ls ~/your/infra/path/accounts/
   ```
   If this shows a list of directories — the path is correct.

2. Tell the script where it is:
   ```bash
   bash ~/projects/raycast-infra-scripts/setup.sh
   ```

### "command not found: brew" when installing Homebrew

After the Homebrew installer finishes, it prints two follow-up commands you must run. Look for the **"Next steps:"** section in the installer output and run those commands. They look like:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```
After running them, open a new Terminal window and try `brew --version` again.

### "Error: python3 not found" in Raycast

Raycast may not have the same PATH as your Terminal. The script handles this by checking the standard Homebrew locations (`/opt/homebrew/bin/python3` for Apple Silicon, `/usr/local/bin/python3` for Intel). If Python was installed somewhere else, verify:

```bash
which python3
```

And check that the output matches one of those paths. If it's somewhere different (e.g. a conda or pyenv path), the easiest fix is to also install Python via Homebrew:
```bash
brew install python
```

### Script doesn't appear in Raycast after adding the directory

- Confirm the scripts are executable. Open Terminal and run:
  ```bash
  chmod +x ~/projects/raycast-infra-scripts/scripts/*.sh
  ```
- In Raycast → Script Commands, click the **↻ Reload** button
- Make sure you added the `scripts/` subfolder, not the root repository folder

### Run the script manually to see raw errors

Raycast sometimes hides error details. To see the full output, run the script directly in Terminal:

```bash
python3 ~/projects/raycast-infra-scripts/zone-lookup.py eu1
```

This will print any errors clearly so you can diagnose the issue.

### "No zone matching…"

Your query didn't match any zone name or DNS name. Try a shorter search term. To list all available zones:

```bash
python3 ~/projects/raycast-infra-scripts/zone-lookup.py --list
```
