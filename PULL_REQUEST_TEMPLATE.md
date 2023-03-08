Start the name of the PR with one of the relevant prefixed in the title of the PR:

* [LANGUAGE] -> changes related to grammars or the transpiler
* [FIX] -> solving a bug
* [CHORE] -> things unrelated to the code, such as mergify scripts
* [REFACTORING] -> should not change anything, cleanup of code
* [UI] -> improvements and changes of the Hedy user interface
* [TESTING] -> changes made to the test suite
* [BACKEND] -> changes to the internal logic of the Hedy website

Finish the name of the PR with a clear description of the changes and delete the lines above from the description.

**Now fill out the remainder of this template by replacing all _italic_ content**

**Description**

_Changes in detail. For example: "**Adds** translations of levels 1 to 12 to Polish" (note the use of present tense!)_

**Fixes _issue or discussion number_**

Always link the number of the issue or of the discussion that your PR concerns.
Tip, if you use the word `fixes` before the issue number in this description, the related issue will automatically close then the PR is merged! 

**How to test**

* If this is a UI change: _describe how to run your code to see it in action. See this https://github.com/Felienne/hedy/pull/880#issue-1016304308 for an example_
* If this is a language change: _add a few tests showing the difference_

**Checklist**
Done? Check if you have it all in place using this list:*
  
- [ ] Contains one of the PR categories in the name
- [ ] Describes changes in the format above
- [ ] Links to an existing issue or discussion 
- [ ] Has a "How to test" section

If you're unsure about any of these, don't hesitate to ask. We're here to help!
