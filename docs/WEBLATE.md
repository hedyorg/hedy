This page contains information on various Weblate issues.

# Fixing Weblate Merge conflicts

If there are too many changes, Weblate might not be able to resolve them automatically. You will then have to fix stuff locally, to do so, follow these steps:

**Gather the commits from weblate by adding an extra remote to your local repo**

`git remote add weblate https://hosted.weblate.org/git/hedy/adventures/`

This enables us to contact the weblate repo.

**Now grab the Weblate commits**

With `git fetch weblate` you get all commits that exist in weblate.

**Make a new branch**

Switch to a fresh branch with `git checkout -b newbranchname`

**Merge Weblate commits in**

Now with `git merge weblate/main` you can merge the Weblate commits into the current branch. This can lead to merge conflicts (in fact, it will, cause why otherwise would you be going through all this trouble?) that you will have to manually fix.

**Push the fixed branch**

Now push newbranchname and Weblate is happy again again, because it will see that all its commits are in the repo.

**Accept but do not click merge!**

If all is in order (all tests pass), you can accept the PR. But! Do not merge it with the button since Webalte PRs require a merge commit instead of a squash merge. Mergify will do this automatically.

# Fixing Weblate Merge snippet errors

Sometimes, translators make mistakes in the code snippets, often small syntax issues such as a missing quote or a misspelled variable name. Sadly at this point, Weblate does not run our tests so the translators do not get feedback.
There are two options to fix this:
1. With code: You can pull the branch locally and fix the issues or even use the GitHub website. However, there are a few things to be aware of.
If new changes occur in Weblate, it will force push and your commits will be gone! This is not really a problem, because you will have the commits locally and you can repush them. But if you are making complex changes, you can also consider pausing Weblate, but of course that can be annoying to translators.
2. Within Weblate. Search the snippet and fix it there. A bit more hassle but there will not be conflicts and also no force push issues.

# Investigating double keys

Sometimes Weblate gets angry because we accidentally repeat a certain key. Since Babel does not care about that, we only see this when we have merged into main and Weblate is updated. Maybe there is a setting that can fix that but for now, this little bash magic will also tell you where the problem lies:

For the po files:
`for x in */LC_MESSAGES/messages.po;do echo $x ; sort $x | uniq -c | grep "2 msgid"; done`

For `messages.pot`:
`sort messages.pot | uniq -c | grep "2 msgid"`

# New strings versus fuzzy strings

There are a few Weblate peculiarities that are handy to know in working with the strings. If you add a new string in the code base in English, it will be automatically copied to ll languages in English, and then shown in English in the UI. However if you _update_ a string, the original (even if it is still the original, untranslated English one) will remain as is in Weblate, and will just be shown as #fuzzy (which is not visible to users of the Hedy site)

# Working with Weblate locally

Installing wlc (`pip install wlc`) gives you some control over the Weblate environment. To use this, create a .weblate file in the root and put the following content in there:

```
[weblate]
url = https://hosted.weblate.org/api/
translation = hedy/adventures
key = <personal key>
```

The personal key can be found in your profile on Weblate.

