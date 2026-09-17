    _    _          _
   | |  | |        | |
   | |__| | ___  __| |_   _
   |  __  |/ _ \/ _' | | | |
   | |  | |  __/ (_| | |_| |
   |_|  |_|\___|\__,_|\__, |
                       __/ |
      o f f l i n e   |___/

Welcome to Offline Hedy! In this document we shall explain how to properly
install and use Offline Hedy. For up-to-date instructions, please go to:
https://github.com/hedyorg/hedy/wiki/Offline-Hedy.



WAYS TO USE OFFLINE HEDY

There are two ways you can use Offline Hedy: you can either download the
application on the laptops of every student (individual hosts) or you can use
one machine to host the application and let each student connect to the host
machine via a (local) network (single host).

If you simply want your students to have access to and be able to work on the
problems, it is recommended to use this first mode where you download Offline
Hedy on every laptop. This is slightly more tedious to set up as you have to
download it on every computer, but will be easier during 'everyday use'. This
does come with the downside that you, the teacher, cannot check the work of
your students. (This mode is also recommended for use in outreach-like events
where access to the problems is more important than checking the code and
determining a grade.)

The single host mode might be preferred if you want to enjoy the full
capabilities our online service offers or if the operating system of the
student machines is not supported. In this mode the host computer acts as the
server on which the website is hosted. So, your students can easily connect to
Offline Hedy using only their browser and you will be able to use it as you
would our online service. You can create classes, alter which exercises are
shown to your students, and check the submitted code. However, to do this you
must still have a (local) network set up to which all laptops are connected.



INSTALLING OFFLINE HEDY

1. Launch the Hedy executable found in this folder.

2. (On first launch) you will probably get a security warning from Microsoft
   Defender SmartScreen warning you about the unrecognised app.

3. Press 'More info' and click 'Run anyway'.

4. This shall then open a Command Prompt window, which, in turn, will open a
   browser window.

5. You will most likely also get a notification from Windows Firewall asking
   whether or not you want Hedy to be able to access the local network.
   It is necessary to allow this if you want to use the aforementioned single
   host setup. For the individual hosts, it does not matter if you allow this
   or not.

6. If everything worked correctly you should now see the Hedy homepage. If no
   browser window was opened you can either ctrl+click one of the hyperlinks in
   the Command Prompt or go to 'http://localhost/' in your browser manually.



USING OFFLINE HEDY: INDIVIDUAL HOSTS

If every student machine has a copy of Offline Hedy installed, launching Hedy,
going to 'http://localhost/' in their browser (which should happen
automatically) and pressing **Let's get started!** on the homepage is enough to
get started with Hedy!

If the browser is accidentally closed, reopening the browser and going back to
'http://localhost/' should reopen Hedy.
To fully close Hedy please use ctrl+C in the command prompt/terminal and close
the terminal window if this did not happen automatically.

At outreach-like events if you connect to Offline Hedy using a private browser
window, you can reset progress made on the computer by simply closing the
private window and reopening it (the terminal/command prompt can keep running
and does not need to be relaunched). User progress is stored in the cookies, so
reopening the private window should forget any progress made.



USING OFFLINE HEDY: SINGLE HOST

When launching Offline Hedy, the terminal will list some websites from which
you will be able to access the hosted service.

'http://localhost/' will only work on this machine, but the other links should
be accessible from other computers on your local network. Make sure the student
laptops and the host machine are on the same network, your students will then
be able to connect to the hosted Offline Hedy just as they would be able to
connect to the online service. Please keep in mind that the address might
change each time you re-launch Offline Hedy.

Since the host computer is simply replacing our servers, you still need to
follow all the steps of setting up a teacher account, creating student accounts
for your class and distributing them among your students, just as you would on
'https://hedy.org/'.

You can set up a teacher account by going to
'http://localhost/invite/newteacher' and selecting 'Create account'.
Then, select 'Teacher' and continue the sign-up process.
You can also use the built-in teacher account we have, with username 'teacher1'
and password '123456'.

All data concerning the teachers, the students, and their submissions is stored
in the 'database.json' file which is located in the same folder as the
executable.

If you wish to upgrade Offline Hedy to a newer version, you can simply download
the newest version from our Releases page and follow this guide once again to
properly install it. Finally, to transfer the data between versions, you should
replace the 'database.json' file in the folder containing the new version with
the 'database.json' from the folder containing the version you were previously
using. After launching the new version, double-check if all data is still there
by logging into your account. If this is not the case please try again!

If you wish to reset all data (for example when a new school year has begun),
simply download Offline Hedy once again from our Releases page.
