
#!/usr/bin/env bash
# report.sh — таблица «модуль → число сообщений» по логам
set -euo pipefail

usage() {
    echo "Usage: $0 <dir> <ERROR|WARN> [--top N]" >&2
    exit 1
}

[ "$#" -ge 2 ] || usage
DIR=$1; LEVEL=$2; shift 2
TOP=0
if [ "${1:-}" = "--top" ]; then
    [ -n "${2:-}" ] || usage
    TOP=$2
fi

[ -d "$DIR" ] || { echo "Error: directory '$DIR' not found" >&2; exit 1; }

grep -h " $LEVEL " "$DIR"/*.log 2>/dev/null \
  | awk '{for (i=1; i<=NF; i++) if ($i ~ /^module=/) {split($i, a, "="); print a[2]; break}}' \
  | sort | uniq -c | sort -rn \
  | awk -v top="$TOP" 'top == 0 || NR <= top {printf "%-10s %s\n", $2, $1}'
