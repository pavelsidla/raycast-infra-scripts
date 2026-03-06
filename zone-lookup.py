#!/usr/bin/env python3
"""
zone-lookup — environment zone → DNS / AWS profile mapping

Reads live from your infrastructure repo's locals.tf and account.hcl files.
No cache, always reflects what's in Terraform.

Configuration (checked in this order):
  1. INFRA_REPO_PATH environment variable
  2. ~/.config/raycast-infra/config  (line: INFRA_REPO_PATH=/your/path)
  3. Auto-detection from common checkout paths

Usage:
  python3 zone-lookup.py slave-eu1-production    # exact or partial match
  python3 zone-lookup.py eu1                     # shows all eu1 zones
  python3 zone-lookup.py --list                  # flat table (used by fzf)
  python3 zone-lookup.py --profile eu1-prod      # returns only the AWS profile name
"""

import os
import re
import sys
from pathlib import Path

# ── Path resolution ────────────────────────────────────────────────────────────

COMMON_PATHS = [
    '~/projects/infra',
    '~/work/infra',
    '~/code/infra',
    '~/projects/infrastructure',
    '~/work/infrastructure',
    '~/code/infrastructure',
    '~/infra',
    '~/dev/infra',
    '~/src/infra',
]

CONFIG_FILE = Path.home() / '.config' / 'raycast-infra' / 'config'


def resolve_infra_repo() -> Path:
    # 1. Environment variable
    env_path = os.environ.get('INFRA_REPO_PATH')
    if env_path:
        p = Path(env_path).expanduser()
        if p.exists():
            return p
        print(f'Error: INFRA_REPO_PATH is set to "{env_path}" but that path does not exist.',
              file=sys.stderr)
        sys.exit(1)

    # 2. Config file
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith('INFRA_REPO_PATH='):
                value = line.split('=', 1)[1].strip().strip('"').strip("'")
                p = Path(value).expanduser()
                if p.exists():
                    return p
                print(f'Error: config file sets INFRA_REPO_PATH="{value}" but path does not exist.',
                      file=sys.stderr)
                print(f'Config file: {CONFIG_FILE}', file=sys.stderr)
                sys.exit(1)

    # 3. Auto-detect
    for candidate in COMMON_PATHS:
        p = Path(candidate).expanduser()
        if p.exists() and (p / 'accounts').exists():
            return p

    print('Error: could not find your infrastructure repo checkout.', file=sys.stderr)
    print('', file=sys.stderr)
    print('Fix one of the following:', file=sys.stderr)
    print('  a) Run setup.sh — it will ask for your path and save it', file=sys.stderr)
    print('  b) Create ~/.config/raycast-infra/config with:', file=sys.stderr)
    print('       INFRA_REPO_PATH=/full/path/to/your/infra-repo', file=sys.stderr)
    print('  c) Set an env var: export INFRA_REPO_PATH=/full/path/to/your/infra-repo', file=sys.stderr)
    sys.exit(1)


# ── Parsing ────────────────────────────────────────────────────────────────────

GLOB = 'accounts/*/*/*/099_from_control_server/locals.tf'

LOCALS_FIELDS = [
    'aws_account_name',
    'dns_zone',
    'imt_zone',
    'aws_region',
    'deployment_kind',
    'deployment_type',
]
ACCOUNT_FIELDS = ['aws_profile_name', 'aws_account_id']


def parse_hcl(path: Path, fields: list) -> dict:
    text = path.read_text(errors='replace')
    result = {}
    for field in fields:
        m = re.search(rf'\b{field}\s*=\s*"([^"]*)"', text)
        result[field] = m.group(1).strip() if m else ''
    return result


def load_zones(infra_repo: Path) -> dict:
    zones = {}
    for tf in sorted(infra_repo.glob(GLOB)):
        data = parse_hcl(tf, LOCALS_FIELDS)
        account_hcl = tf.parent.parent / 'account.hcl'
        if account_hcl.exists():
            data.update(parse_hcl(account_hcl, ACCOUNT_FIELDS))
        name = data.get('aws_account_name') or tf.parts[-3]
        if name:
            zones[name] = data
    if not zones:
        print('No zones found — check your infra repo path', file=sys.stderr)
        sys.exit(1)
    return zones


# ── Formatting ─────────────────────────────────────────────────────────────────

CYAN   = '\033[1;36m'
GRAY   = '\033[0;90m'
GREEN  = '\033[0;32m'
YELLOW = '\033[0;33m'
RESET  = '\033[0m'


def fmt_detail(name: str, data: dict) -> str:
    lines = [f'{CYAN}{name}{RESET}']

    def row(label, value, colour=''):
        if value:
            lines.append(f'  {label:<18}{colour}{value}{RESET}')

    row('dns_zone',    data.get('dns_zone', ''),         GREEN)
    row('imt_zone',    data.get('imt_zone', ''))
    row('aws_profile', data.get('aws_profile_name', ''), YELLOW)
    row('account_id',  data.get('aws_account_id', ''))
    row('region',      data.get('aws_region', ''))
    kind  = data.get('deployment_kind', '')
    dtype = data.get('deployment_type', '')
    env   = '/'.join(filter(None, [dtype, kind]))
    row('environment', env)
    return '\n'.join(lines)


def fmt_list_row(name: str, data: dict, col_w: int) -> str:
    dns  = data.get('dns_zone', '')
    reg  = data.get('aws_region', '')
    kind = data.get('deployment_kind', '')
    return f'{name:<{col_w}} {GREEN}{dns}{RESET}  {GRAY}[{reg}] [{kind}]{RESET}'


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    args         = sys.argv[1:]
    list_mode    = '--list'    in args
    profile_mode = '--profile' in args
    query_args   = [a for a in args if not a.startswith('--')]
    query        = query_args[0] if query_args else None

    infra_repo = resolve_infra_repo()
    zones      = load_zones(infra_repo)
    col_w      = max(len(n) for n in zones) + 2

    if list_mode:
        for name, data in sorted(zones.items()):
            print(fmt_list_row(name, data, col_w))
        return

    if profile_mode and query:
        matches = {k: v for k, v in zones.items() if query.lower() in k.lower()}
        if not matches:
            print(f'No zone matching "{query}"', file=sys.stderr)
            sys.exit(1)
        if len(matches) > 1:
            print(f'Ambiguous: {", ".join(sorted(matches))}', file=sys.stderr)
            sys.exit(1)
        profile = list(matches.values())[0].get('aws_profile_name', '')
        if not profile:
            print(f'No profile found for "{query}"', file=sys.stderr)
            sys.exit(1)
        print(profile)
        return

    if query:
        q = query.lower()
        matches = {
            k: v for k, v in zones.items()
            if q in k.lower() or q in v.get('dns_zone', '').lower()
        }
        if not matches:
            print(f'No zone matching "{query}"')
            sys.exit(1)
        for i, (name, data) in enumerate(sorted(matches.items())):
            if i:
                print()
            print(fmt_detail(name, data))
    else:
        for name, data in sorted(zones.items()):
            print(fmt_list_row(name, data, col_w))


if __name__ == '__main__':
    main()
