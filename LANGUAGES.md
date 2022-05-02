## Languages
Hedy currently supports a total of 23 languages, for which some are partly translated. 
All translations are handled by Weblate, enabling contributors to contribute within an nice UI instead of a code editor. 
Non-translated strings are automatically shown in English. Adding new languages is completely automated in the translation pipeline.
You can add a new language in Weblate and start translating. After merging the language can automatically be found on the Hedy website.

Hedy currently supports a total of 9 keyword languages. The keyword language is the actual programming language and the language of the Hedy commands.
Each programming situation has only two valid keyword languages: the currently selected language and English.
So when the user language is set to Norsk the user can use both English and Norsk keywords, even in the same program! 
When a language does not have translated keywords English is the valid keyword language. The user set keyword language can only be English or the selected user language.
So for example, when the profile language is set to Dutch only Dutch and English are valid keyword languages.

All examples, adventures, quizzes and code snippets are shown with the selected keyword language by dynamically parsing at runtime.
All these translations are stored with _placeholders_ like this `{print}`. 
When requesting a specific keyword language the placeholder is replaced by the corresponding translated keyword.
This only counts for the examples as in all cases the set language and English are both valid keyword languages.
When translating the placeholders should always stay in place with the English keyword between the brackets, otherwise the parser is unable to find the corresponding translation.

As said the current user language and English are valid keyword languages when programming in Hedy.
For example, when having your keyword language set to `nl` (Dutch) the following programs are both valid in level 1:

#### English Keywords
```
print Hello World!
ask How are you doing?
echo So you are doing 
```
#### Dutch keywords
```
print Hello World!
vraag How are you doing?
herhaal So you are doing 
```

Lastly, when a non-English language is set as the keyword language a _language switcher_ is shown on the code editor.
In all other cases no switcher is shown.
This switcher enables users to translate the current program between the keyword language and English (and back!).
The code in the editor will automatically translate when using the switcher.