#!/usr/bin/env bash
# Print Markdown release notes for TAG: commits since the previous v* tag,
# grouped by Conventional Commit type.
# Usage: release-notes.sh <tag>
set -euo pipefail

tag="${1:?usage: release-notes.sh <tag>}"
prev="$(git describe --tags --abbrev=0 --match 'v*' "${tag}^" 2>/dev/null || true)"
range="${prev:+${prev}..}${tag}"
repo_url="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-}"

declare -A sections=(
  [breaking]="" [feat]="" [fix]="" [docs]="" [other]=""
)

while IFS=$'\t' read -r hash subject body_flag; do
  type=""; desc="$subject"
  if [[ "$subject" =~ ^([a-z]+)(\([^\)]*\))?(!)?:\ (.*)$ ]]; then
    type="${BASH_REMATCH[1]}"; desc="${BASH_REMATCH[4]}"
    [[ -n "${BASH_REMATCH[2]}" ]] && desc="**${BASH_REMATCH[2]:1:-1}:** ${desc}"
    [[ -n "${BASH_REMATCH[3]}" ]] && body_flag=1
  fi
  line="- ${desc} ([\`${hash}\`](${repo_url}/commit/${hash}))"
  if [[ "$body_flag" == "1" ]]; then
    sections[breaking]+="${line}"$'\n'
    continue
  fi
  case "$type" in
    feat) sections[feat]+="${line}"$'\n' ;;
    fix)  sections[fix]+="${line}"$'\n' ;;
    docs) sections[docs]+="${line}"$'\n' ;;
    *)    sections[other]+="${line}"$'\n' ;;
  esac
done < <(git log --no-merges --reverse --format='%h%x09%s%x09%(trailers:key=BREAKING CHANGE,valueonly,separator=)' "$range" \
          | awk -F'\t' '{ print $1 "\t" $2 "\t" ($3 != "" ? 1 : 0) }')

if [[ -n "$prev" ]]; then
  echo "Changes since ${prev}:"
else
  echo "First release."
fi
echo

print_section() {
  if [[ -n "${sections[$1]}" ]]; then
    printf '### %s\n\n%s\n' "$2" "${sections[$1]}"
  fi
}
print_section breaking "⚠ Breaking changes"
print_section feat "Features"
print_section fix "Fixes"
print_section docs "Documentation"
print_section other "Other"

if [[ -n "$prev" && -n "${GITHUB_REPOSITORY:-}" ]]; then
  echo "**Full changelog:** ${repo_url}/compare/${prev}...${tag}"
fi
