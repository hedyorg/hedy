# Working with Weblate

Installing wlc (pip install wlc) gives you some control over the Weblate environment. To use this, create a .weblate file in the root and put the following content in there:

```
[weblate]
url = https://hosted.weblate.org/api/
translation = hedy/level-defaults
key = <personal key>
```

The personal key can be found in your profile on Weblate.

# Fixing Weblate Merge conflicts

If there are too many changes, Weblate might not be able to resolve them automatically. You will then have to fix stuff locally, to do so, follow these stetps:

**Gather the commits from weblate by adding an extra remote to your local repo**

`git remote add weblate https://hosted.weblate.org/git/hedy/web-texts/`

This enables us to contact the weblate repo.

**Now grab the Weblate commits**

With `git fetch weblate` you get all commits that exist in weblate.

**Make a new branch**

Switch to a fresh branch with `git checkout -b newbranchname`

**Merge Weblate commits in**

Now with `git merge weblate/main` you can merge the Weblate commits into the current branch. This can lead to merge conflicts (in fact, it will, cause why otherwise would you be going trough all this trouble?) that you will have to manually fix.

**Push the fixed branch**

Now push newbranchname and Weblate is happy again again, because it will see that all its commits are in the repo.
 
