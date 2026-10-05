#!/bin/bash
# This script will check out the Weblate repository, and automatically merge
# it with `main` resolving conflicts.
#
# Content YAML files are merged as YAML, by tools/merge-weblate-yaml.py, rather than as
# text. Resolving those textually in favour of Weblate (which is what this script used to
# do, with 'git merge -X ours') keeps the translations but silently reverts whatever the
# team changed in the same hunk, deletions of retired levels included. Merging the trees
# lets both intents through: the team decides which keys exist and what their value is,
# translators' new and updated strings come along, and anything genuinely contested is
# reported instead of being resolved out of sight.
#
# Everything else -- the .po files especially -- is still resolved hunk by hunk in favour
# of Weblate, which is what '-X ours' did for the whole tree.
#
# A markdown summary of what had to be decided is written to $WEBLATE_MERGE_REPORT, for
# the workflow to put in the pull request body. It is deliberately not written inside the
# repository, because 'create-pull-request' commits whatever it finds there.
set -eu
set -x

REPORT=${WEBLATE_MERGE_REPORT:-$(mktemp -t weblate-merge-report)}
: > "$REPORT"

# Checkout Weblate main repo
git remote add weblate-main https://hosted.weblate.org/git/hedy/adventures/ || true
git fetch weblate-main
git checkout -B weblate-hedy-adventures-conflicts weblate-main/main

# Normalize files in Weblate main repo
doit run _autopr _autopr_weblate
git commit -am 'Normalize Weblate branch' --allow-empty

# Merge from origin. No '-X ours' here: we want to see which files actually disagree, so
# that each kind can be resolved on its own terms below.
git fetch origin
conflicted_merge=0
git merge origin/main --no-commit --no-ff || conflicted_merge=1

unresolved=""

# 'git merge' leaves the three sides in the index: stage 1 is the merge base, stage 2 is
# HEAD (this branch, so the Weblate side) and stage 3 is what we are merging in (origin/
# main). A stage is missing when a file was added or deleted on only one side.
stage_to() {
  git show ":$1:$2" > "$3" 2>/dev/null
}

if [ "$conflicted_merge" = 1 ]; then
for conflicted in $(git diff --name-only --diff-filter=U); do
  base=$(mktemp); weblate=$(mktemp); upstream=$(mktemp)

  if ! stage_to 2 "$conflicted" "$weblate" || ! stage_to 3 "$conflicted" "$upstream"; then
    # Added on one side only, or deleted on one side and changed on the other. Both need
    # a judgement call about whether the file should exist at all, which this script has
    # no basis for making.
    unresolved="$unresolved $conflicted"
    rm -f "$base" "$weblate" "$upstream"
    continue
  fi
  # No stage 1 means both sides created the file; an empty base reads as "nothing here
  # before", which is exactly right.
  stage_to 1 "$conflicted" "$base" || : > "$base"

  case "$conflicted" in
    content/*.yaml)
      # merge-weblate-yaml.py takes BASE OURS THEIRS, where OURS is the 'main' side, so
      # the two stages go in swapped relative to git's sense of "ours" on this branch.
      {
        echo "### \`$conflicted\`"
        echo
        echo '```'
      } >> "$REPORT"
      if python3 tools/merge-weblate-yaml.py "$base" "$upstream" "$weblate" "$conflicted" \
          2>> "$REPORT"; then
        git add "$conflicted"
      else
        unresolved="$unresolved $conflicted"
      fi
      {
        echo '```'
        echo
      } >> "$REPORT"
      ;;
    *)
      # Hunk-by-hunk, preferring Weblate, which is what '-X ours' used to do everywhere.
      # 'git merge-file' writes its result into the first file it is given.
      git merge-file --ours "$weblate" "$base" "$upstream" || true
      cp "$weblate" "$conflicted"
      git add "$conflicted"
      ;;
  esac

  rm -f "$base" "$weblate" "$upstream"
done
fi

if [ -n "$unresolved" ]; then
  set +x
  echo "These files could not be resolved automatically:"
  for f in $unresolved; do echo "  $f"; done
  echo "Resolve them by hand, or teach this script how to."
  exit 1
fi

# Finish the merge. The '--no-commit' above means even a clean merge is still only staged,
# and the step after this one expects a committed tree. There is no MERGE_HEAD at all when
# origin/main held nothing new, and committing then would have nothing to say.
if git rev-parse -q --verify MERGE_HEAD > /dev/null; then
  git commit --no-edit
else
  set +x
  echo "Already up to date with origin/main; nothing was merged."
fi
