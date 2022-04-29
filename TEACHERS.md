Teacher functionalities
================

Hedy supports a lot of exciting features specially aimed at teachers to help them teaching Hedy.
As the amount of features keeps growing this document is used as a guideline and overview of all available Teacher features.
This document is updated when new functionality is added and should contain an up-to-date version of all possibilities. 

## Introduction
When creating an account users are able to apply for a "Teachers account". These are set manually by Felienne on request.
Another way to achieve a Teachers account is by using the correct `/invite` link. This link is set by Hedy people giving workshop to easily let participants achieve a Teachers account.
For example, when giving a workshop at a specific University we can set it to `/invite/UniversityBlaBla`. When a logged-in user visits this link they are automatically granted Teacher rights.
Teachers have additional functionalities over _normal_ users. All functionality is found on the `/for-teachers` page.
On this page you can also find a section called _Hedy documentation_, containing some guidelines and common mistakes as pointers for using Hedy in the classroom. 
We separate the features into three majors parts:

- Class management
    - Class creation, customizations and management
    - Class and student statistics
- Adventure creation
    - Create custom adventures, include through class customizations 
- Multiple account creation
    - Enable multiple mail-less account creation
    - Automatic class enrollment

## Class management
Teachers are able to create and manage personal classes. On the `/for-teachers` page there is a section called _My classes_.
A new class with a custom name can be created using the "_Create a class_" button. After class creation you are re-directed to the _Class overview_.
This page has all relevant information for the current class. Divided in students overview tabls and several buttons. Currently the following functionalities are supported:

- Customize class
- Rename class
- Invite students (by username)
    - Alternatively, there is also a _join link_ that can be copied 
- Class statistics

Within the students overview table general information on all students can be found. Such as _last login_, _highest level_ and _amount of programs_.
This table view is customizable with the corresponding header checkboxes at the top of the table. 
Teachers are also able to change the password of one of their students or remove them from the class all together.

When inviting a student the corresponding username should be entered. Accounts are only able to have one pending invite at a time.
When sent the students can find their invite under the _messages_ section, found on the `/my-profile` page.
Invitations have an expiration date of **7 days**.

### Customize class
Teachers are able to customize classes to limit functionalities for the students. 
They can visit the _class customizations_ by clicking the "_Customize class_" button on the class overview page.
All levels can be hidden/show as well as all adventures, custom adventures can be added on this page as well. Enabling teacher to enforce students to work on specific programs and don't get distracted easily.
Levels can be given a specific _opening date_, enabling teachers to set the customizations once and, for example, open a new level each week.
Lastly several relevant teaching customizations are supported, which are currently:

- Enforced developer's mode
- Hiding/showing cheatsheet
- Hiding/showing keyword language switcher
- Hiding/showing quiz adventure

### Class statistics
Teachers are able to view class statistics by pressing the "_Class statistics_" button on the class overview page.
The statistics page contains an overview of several relevant statistics such as _runs per level_ and _error rate_.
There are also statistics per week and divided by different errors, giving teachers more insight in their students struggles.
Lastly, teachers are able to filter the _logs_ on date, level or specific student to get more detailed statistics.

## Adventure creation
In addition to class customizations teachers are also able to create their own adventures. 
As with all teacher functionalities this can be found on the _for_teachers_ page as well, under the "_My adventures_" section.
Use the "_Create new adventure_" button to create a new adventure with a custom name, this name should be unique for your adventures.
By default the adventure is set to level 1 with a default explain text. When customized and saved it can be viewed, deleted and customized again.
To add to your class, navigate to the _class overview_ and then to _Customize class_. The adventure will be listed under "_Select own adventures_".
Note that your adventure will only be shown in the level for which it was created.

## Multiple account creation
When using Hedy in the classroom it can be cumbersome that all students manually have to create an account and join your class.
Therefore, we support "_Multiple account creation_" which can be found in the "_Make student accounts_" section on the class overview page.
Teachers are able to easily create multiple accounts by only providing a username and password, also giving the option to automatically add these students to a class.
Student accounts don't need a mail address as they are connected to the teacher account and mails such as _password reset_ are sent to the teacher.


