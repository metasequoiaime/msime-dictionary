#!/usr/bin/env bash
# Check builder.lock.json and print its pinned msime commit.
#
# Usage: scripts/check_builder_lock.sh [path/to/builder.lock.json]
#
# The pin must be a full 40-character lowercase commit that is on msime develop (GitHub compare status ahead or identical), so it is reviewed builder code and not a pull request branch commit that a squash merge leaves behind. Needs jq and an authenticated gh (GH_TOKEN). The release workflow and the quality workflow both run this, so a bad pin fails the pull request instead of the release after merge.
set -euo pipefail

lock="${1:-builder.lock.json}"
pin="$(jq -er '.msime_commit' "$lock")" || { echo "$lock has no msime_commit" >&2; exit 1; }
[[ "$pin" =~ ^[0-9a-f]{40}$ ]] || { echo "$lock msime_commit must be a full 40-character lowercase commit, got '$pin'" >&2; exit 1; }
status="$(gh api "repos/metasequoiaime/msime/compare/${pin}...develop" --jq .status)" || { echo "cannot compare the pinned msime commit $pin with msime develop" >&2; exit 1; }
case "$status" in
  ahead|identical) ;;
  *) echo "pinned msime commit $pin is not on msime develop (compare status: $status)" >&2; exit 1 ;;
esac
echo "$pin"
