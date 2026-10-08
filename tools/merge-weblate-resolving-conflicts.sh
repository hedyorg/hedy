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
# Weblate's branch is merged *into* 'main', not the other way round, and the result keeps
# its history: the workflow pushes this merge commit as the PR branch, and Mergify merges
# translations PRs with a merge commit too. Weblate's own commits so become ancestors of
# 'main', so its next pull finds them there and goes through without a reset. 'main' being
# the first parent also means the merge only adds translation changes on top of it.
#
# A markdown summary of what had to be decided is written to $WEBLATE_MERGE_REPORT, for
# the workflow to put in the pull request body. It is deliberately not written inside the
# repository.
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

weblate_head=$(git rev-parse HEAD)

# Merge into 'main'. No '-X' strategy option here: we want to see which files actually
# disagree, so that each kind can be resolved on its own terms below.
git fetch origin
git checkout -B weblate-conflict-resolution origin/main
conflicted_merge=0
git merge "$weblate_head" --no-commit --no-ff -m 'Merge translations from Hosted Weblate' \
  || conflicted_merge=1

unresolved=""
merge_base=$(git merge-base "$weblate_head" origin/main)

show_to() {
  git show "$1:$2" > "$3" 2>/dev/null
}

# Content YAML: every language file Weblate touched, whether git flagged it or not. While
# Weblate is stuck in conflict it cannot pull 'main', so its copy of the English files goes
# stale and translators keep translating levels the team has since removed. Such a file can
# merge cleanly as text and still fail tools/check-yaml-structure.py, so the YAML merge has
# to see it either way; it drops whatever the current English file no longer has.
for file in $(git diff --name-only "$merge_base" "$weblate_head" -- 'content/*.yaml'); do
  case "$file" in
    */en.yaml) continue ;;  # the English files are ours alone; git's merge stands
  esac
  base=$(mktemp); weblate=$(mktemp); upstream=$(mktemp); template=$(mktemp); notes=$(mktemp)

  if ! show_to "$weblate_head" "$file" "$weblate"; then
    # Weblate deleted it, which it does not do on its own; leave it to git.
    rm -f "$base" "$weblate" "$upstream" "$template" "$notes"
    continue
  fi
  show_to "$merge_base" "$file" "$base" || : > "$base"
  if ! show_to origin/main "$file" "$upstream"; then
    if [ -s "$base" ]; then
      # The team deleted a language file that Weblate went on to change. Whether it
      # should exist is a judgement call this script has no basis for making.
      unresolved="$unresolved $file"
      rm -f "$base" "$weblate" "$upstream" "$template" "$notes"
      continue
    fi
    : > "$upstream"  # a language only Weblate has so far
  fi

  # merge-weblate-yaml.py takes BASE OURS THEIRS with OURS meaning 'main'.
  template_args=()
  if show_to origin/main "$(dirname "$file")/en.yaml" "$template"; then
    template_args=(--template "$template")
  fi
  if python3 tools/merge-weblate-yaml.py ${template_args[@]+"${template_args[@]}"} \
      "$base" "$upstream" "$weblate" "$file" 2> "$notes"; then
    git add "$file"
  else
    unresolved="$unresolved $file"
  fi
  if [ -s "$notes" ]; then
    { echo "### \`$file\`"; echo; echo '```'; cat "$notes"; echo '```'; echo; } >> "$REPORT"
  fi

  rm -f "$base" "$weblate" "$upstream" "$template" "$notes"
done

# Everything else that conflicted -- the .po files especially -- is resolved hunk by hunk
# in favour of Weblate, as before. Git's index has the three sides as stages: 1 is the
# merge base, 2 is HEAD ('main', which we are on) and 3 is what is being merged (Weblate).
if [ "$conflicted_merge" = 1 ]; then
for conflicted in $(git diff --name-only --diff-filter=U); do
  base=$(mktemp); weblate=$(mktemp); upstream=$(mktemp)

  case "$conflicted" in
    content/*.yaml) unresolved="$unresolved $conflicted" ;;  # the loop above skipped it
    *)
      if show_to :3 "$conflicted" "$weblate" && show_to :2 "$conflicted" "$upstream"; then
        show_to :1 "$conflicted" "$base" || : > "$base"
        # 'git merge-file' writes its result into the first file it is given.
        git merge-file --ours "$weblate" "$base" "$upstream" || true
        cp "$weblate" "$conflicted"
        git add "$conflicted"
      else
        # Added or deleted on one side only: whether it should exist is not ours to guess.
        unresolved="$unresolved $conflicted"
      fi
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
# and the step after this one pushes a commit. There is no MERGE_HEAD at all when 'main'
# already has everything Weblate has, and committing then would have nothing to say.
if git rev-parse -q --verify MERGE_HEAD > /dev/null; then
  git commit --no-edit
else
  set +x
  echo "'main' already has everything on Weblate's branch; nothing was merged."
fi
