"""A module to hold the data that will be used to create PloneHelpCenter
content objects.  I'm not sure whether I can depend on relative file paths,
so we store the data in a Python module where I'm sure that it can be
imported by other modules in the same Python package.
"""

class PropertyHolder:
    """A dummy struct-like class for holding properties"""
    pass

# HelpCenter folderish object ----------------------------------------
Hc = PropertyHolder()
Hc.Id = 'hc'
Hc.Title = 'Test Help Center'
Hc.Desc = 'A help center instance for functional testing of PHC.'
Hc.Versions = ('Version 1.0', 'Version 2.0', 'Different Version 1.0')
Hc.Sections =  ('Topic1', 'Topic1: Section1', 'Topic1: Section2 - \xc3\xa1'.decode('utf8'), 'Topic2', 'Topic2: Section1', 'Topic2: Section2')

# Alternate HelpCenter folderish object ----------------------------------------
AltHc = PropertyHolder()
AltHc.Id = 'althc'
AltHc.Title = 'Alternate Test Help Center'
AltHc.Desc = 'An alternate help center instance for functional testing of PHC.'
AltHc.Versions = ('Version 1.0', 'Version 2.0', 'Different Version 1.0')

# Transitions  -------------------------------------------------------
Transition = PropertyHolder()
Transition.publish = 'publish'
Transition.submit = 'submit'
Transition.obsolete = 'mark_obsolete'

# Users --------------------------------------------------------------
User1 = PropertyHolder()
User1.Id = 'tester1'
User1.Password = 'tester1'
User1.Roles = ['Member',]

User2 = PropertyHolder()
User2.Id = 'tester2'
User2.Password = 'tester2'
User2.Roles = ['Member',]

User3 = PropertyHolder()
User3.Id = 'test_manager'
User3.Password = 'test_manager'
User3.Roles = ['Member','Manager',]

User4 = PropertyHolder()
User4.Id = 'test_reviewer'
User4.Password = 'test_reviewer'
User4.Roles = ['Member','Reviewer',]

User = PropertyHolder()
User.list = [User1, User2, User3, User4]

# HowtoFolder settings -----------------------------------------------
HowtoFolder = PropertyHolder()
HowtoFolder.Sections = ('Topic1: Section1', 'Topic1: Section2 - \xc3\xa1'.decode('utf8'), 'Topic2: Section1', 'Topic2: Section2', 'General')

# TutorialFolder settings --------------------------------------------
TutorialFolder = PropertyHolder()
TutorialFolder.Sections = ('Topic1: Section1', 'Topic1: Section2 - \xc3\xa1'.decode('utf8'), 'Topic2: Section1', 'Topic2: Section2')

# FAQFolder settings --------------------------------------------
FAQFolder = PropertyHolder()
FAQFolder.Sections = ('General', 'FAQ Section1', 'FAQ - \xc3\xa1 - Section2'.decode('utf8') )

# ErrorReferenceFolder settings --------------------------------------------
ErrorReferenceFolder = PropertyHolder()
ErrorReferenceFolder.Sections = ('General', 'Error Ref Section1 - \xc3\xa1'.decode('utf8') )

# Glossary settings --------------------------------------------
Glossary = PropertyHolder()
Glossary.Sections = ('General', )

# LinkFolder settings --------------------------------------------
LinkFolder = PropertyHolder()
LinkFolder.Sections = ('General', 'Link Section1', 'Link Section2 - \xc3\xa1'.decode('utf8'), 'Link Section3' )

# ReferenceManualFolder settings --------------------------------------------
ReferenceManualFolder = PropertyHolder()
ReferenceManualFolder.Sections = ('Topic1: Section1', 'Topic1: Section2 - \xc3\xa1'.decode('utf8'), 'Topic2: Section1', 'Topic2: Section2')

# VideoFolder settings --------------------------------------------
VideoFolder = PropertyHolder()
VideoFolder.Sections = ('General', )

# Sample Howto content 1 ---------------------------------------------
Howto1 = PropertyHolder()
Howto1.Id = 'howto1'
Howto1.Title = 'Test Howto 1'
Howto1.Summary = 'A sample Howto for functional testing of PloneHelpCenter.  A howto that is published; only in one section.'
Howto1.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is only
attached to one Section.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto1.Format = 'text/x-rst'
Howto1.Versions = ( Hc.Versions[1], )
Howto1.Sections = ( HowtoFolder.Sections[1], )
Howto1.Transition = Transition.publish
Howto1.Owner = User1

# Sample Howto content 2 ---------------------------------------------
Howto2 = PropertyHolder()
Howto2.Id = 'howto2'
Howto2.Title = 'Test Howto 2'
Howto2.Summary = 'A howto that is published in two sections'
Howto2.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is 
attached to two Howto Sections.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto2.Format = 'text/x-rst'
Howto2.Versions = ( Hc.Versions[1], )
Howto2.Sections = ( HowtoFolder.Sections[1], HowtoFolder.Sections[2], )
Howto2.Transition = Transition.publish
Howto2.Owner = User1

# Sample Howto content 3 ---------------------------------------------
Howto3 = PropertyHolder()
Howto3.Id = 'howto3'
Howto3.Title = 'Test Howto 3'
Howto3.Summary = 'A howto that is published in one section by a different owner than howto1.'
Howto3.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is only
attached to one Section.  It should be owned by a different user than
howto1.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto3.Format = 'text/x-rst'
Howto3.Versions = ( Hc.Versions[1], )
Howto3.Sections = ( HowtoFolder.Sections[1], )
Howto3.Transition = Transition.publish
Howto3.Owner = User2

# Sample Howto content 4 ---------------------------------------------
Howto4 = PropertyHolder()
Howto4.Id = 'howto4'
Howto4.Title = 'Test Howto 4'
Howto4.Summary = 'A howto that is in-progress in one section'
Howto4.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe in-progress state and is only
attached to one Section.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto4.Format = 'text/x-rst'
Howto4.Versions = ( Hc.Versions[1], )
Howto4.Sections = ( HowtoFolder.Sections[1], )
Howto4.Transition = None
Howto4.Owner = User1

# Sample Howto content 5 ---------------------------------------------
Howto5 = PropertyHolder()
Howto5.Id = 'howto5'
Howto5.Title = 'Test Howto 5'
Howto5.Summary = 'A howto that is in-progress in two sections'
Howto5.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe in-progress state and is 
attached to two Howto Sections.  It is also owned by a different user
than the other test howto that is in-progress.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto5.Format = 'text/x-rst'
Howto5.Versions = ( Hc.Versions[1], )
Howto5.Sections = ( HowtoFolder.Sections[1], HowtoFolder.Sections[2], )
Howto5.Transition = None
Howto5.Owner = User2

# Sample Howto content 6 ---------------------------------------------
Howto6 = PropertyHolder()
Howto6.Id = 'howto6'
Howto6.Title = 'Test Howto 6'
Howto6.Summary = 'A howto that is pending review in one section'
Howto6.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts in the pending state and is only
attached to one Section.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto6.Format = 'text/x-rst'
Howto6.Versions = ( Hc.Versions[1], )
Howto6.Sections = ( HowtoFolder.Sections[1], )
Howto6.Transition = Transition.submit
Howto6.Owner = User1

# Sample Howto content 7 ---------------------------------------------
Howto7 = PropertyHolder()
Howto7.Id = 'howto7'
Howto7.Title = 'Test Howto 7'
Howto7.Summary = 'A howto that is published in (a different) one section'
Howto7.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is only
attached to one Section.  The section is different from the section
to which howto1 is attached.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto7.Format = 'text/x-rst'
Howto7.Versions = ( Hc.Versions[1], )
Howto7.Sections = ( HowtoFolder.Sections[2], )
Howto7.Transition = Transition.publish
Howto7.Owner = User1

# Sample Howto content 8 ---------------------------------------------
Howto8 = PropertyHolder()
Howto8.Id = 'howto8'
Howto8.Title = 'Test Howto 8'
Howto8.Summary = 'A howto that is published in (a different) one section by a different owner than howto7.'
Howto8.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is only
attached to one Section.  The section is different from the section
to which howto1 is attached.  It is owned by a different user from howto7.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto8.Format = 'text/x-rst'
Howto8.Versions = ( Hc.Versions[1], )
Howto8.Sections = ( HowtoFolder.Sections[2], )
Howto8.Transition = Transition.publish
Howto8.Owner = User2

# Sample Howto content 9 ---------------------------------------------
Howto9 = PropertyHolder()
Howto9.Id = 'howto9'
Howto9.Title = 'Test Howto 9'
Howto9.Summary = 'A howto that is in-progress in (a different) one section'
Howto9.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe in-progress state and is only
attached to one Section.  The section is different from the section
to which howto1 is attached.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto9.Format = 'text/x-rst'
Howto9.Versions = ( Hc.Versions[1], )
Howto9.Sections = ( HowtoFolder.Sections[2], )
Howto9.Transition = None
Howto9.Owner = User1

# Sample Howto content 10 --------------------------------------------
Howto10 = PropertyHolder()
Howto10.Id = 'howto10'
Howto10.Title = 'Test Howto 10'
Howto10.Summary = 'A howto that is published in a third section'
Howto10.Body = '''
============
Howto Title
============

.. _Plone: http://www.plone.org/

This howto is a document that starts inthe published state and is only
attached to one Section.  The section is different from the section used
by howto1 or the section used by howto7.
The rest of the content below this description was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

Section 1
=========

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone_ Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories


Section 2
=========

How to get a local copy of code for a Product from the Plone_ Collective.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone_ Product.  See the list of 
folders in the CVS web interface for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you wouldd replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone_ Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you wouldd replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename

End of test document content.
'''
Howto10.Format = 'text/x-rst'
Howto10.Versions = ( Hc.Versions[1], )
Howto10.Sections = ( HowtoFolder.Sections[0], )
Howto10.Transition = Transition.publish
Howto10.Owner = User1


# Sample Howto content -----------------------------------------------
Howto = PropertyHolder()
Howto.list = [ Howto1, Howto2, Howto3, Howto4, Howto5, Howto6, Howto7, Howto8, Howto9, Howto10 ]

# Sample Tutorial Page content ---------------------------------------
Page1 = PropertyHolder()
Page1.Id = 'page1'
Page1.Title = 'Sample Tutorial Page1'
Page1.Summary = 'This tutorial page simply serves as sample content for the tutorial.'
Page1.Body = '''
Section 1
=========

The rest of the content below this point was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

This document was spawned from conversations on the #plone IRC channel. 
A new version of the PloneHelpCenter from the Plone Collective was 
undergoing testing, but some developers wanted to start working on brand 
new code.  The danger was that the new code would delay the deployment 
of some of the much-needed bug fixes and changes that were almost ready 
for deployment on plone.org.  The obivous choice was to create a branch, 
but no one seemed comfortable enough with CVS to make a branch.  I 
volunteered to make a minimal HOWTO that would explain the essential 
CVS commands for getting day to day work done, up to and including 
creating branches and merging code between branches.

I assume that you are familiar with revision control in general and
have CVS client software installed and working.  We just provide a
quick explanation of the most common commands that you will need.  While
there are some great CVS GUIs (Win CVS, Tortois CVS, Cervisia, etc.),
I will only cover the cvs command line here.  

Please see the end of this document for links to more complete CVS 
documentation and to some useful CVS tools.

General syntax
--------------

CVS command line syntax looks like this::

    cvs [global-options] command [command-options] [command-arguments]

The ``command`` is one of the CVS commands, such as checkout, update, or
commit.  To see a brief list of the available commands, use the
following option::

    cvs --help-commands 

The ``global-options`` are the same for all commands.  Each command has 
a different set of ``command-options`` and ``command-arguments``.

The most common ``global-options`` are listed here for later reference.

``-d``
    specifies the root of the CVS tree and possibly also identifies a 
    remote repository, account name, and connection method for the 
    remote repository; overrides the CVSROOT environment variable; 
    generally only used with the checkout command (after that, cvs 
    reads this information from the CVS/Root file in your personal 
    copy of the files)
``-n``
    do not execute anything that would change the disk; for many commands, 
    this options shows what would be done, but does not actually do it
``-z``
    specifies a compression level for network traffic; recommended for 
    remote repositories
'''
Page1.Format = 'text/x-rst'
Page1.Transition = Transition.publish

# Sample Tutorial Page content ---------------------------------------
Page2 = PropertyHolder()
Page2.Id = 'page2'
Page2.Title = 'Sample Tutorial Page2'
Page2.Summary = 'More sample content for the tutorial.'
Page2.Body = '''
Initial Checkout
================

The rest of the content below this point was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

The CVS command to get a local working copy of code from a central CVS 
repository is ``checkout``.  This command is normally abbreviated as ``co``.
This command will give you a copy of all of the files of a directory 
tree on your machine.  This local copy is sometimes called your 
sandbox (you get to play in your sandbox).  A checkout works on a module, 
which will just be a top-level folder in the Collective for our purposes.


You just want the latest version of a Product
---------------------------------------------

If you do not need to develop or modify code, you can use anonymous 
check out from SourceForge.  An anonymous checkout permits you to 
get and update a local copy of the code in CVS.  You do not need a 
SourceForge account.  You can also make local changes and view the 
diffs between your local code and the repository code.  You will be 
unable to submit your changes.  See also the Collective CVS page.

Enter the following line command exactly as written.  When prompted for a 
password, just press enter:: 

    cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective login

Once you are logged into the pserver, you can checkout (co) the Product 
you need.  For the next command, you will need to replace *modulename* 
with the name of the module you want to checkcout.   The *modulename* is 
generally the top level folder for a Plone Product.  See the list of 
folders in the CVS web interfoce for the Collective.  For example, if you 
wanted a copy of PloneHelpCenter, you would replace *modulename* with the 
word ``PloneHelpCenter``::

    cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/collective co -P modulename


You want to do development work on a Product
--------------------------------------------

Anonymous checkout does not permit you to commit changes to a Product 
in the Collective.  If you need to modify and submit code to the 
Collective, you will need to get an account on SourceForge.  Once 
you have that account, someone will need to add you to the list of 
developers for the Plone Collective project on SourceForge.  You 
will  be checking out code over a secure SSH tunnel.  SourceForge 
provides decent documentation concerning configuration of client 
software for accessing their CVS repositories over SSH.

The command to checkout code for development follows.  Remember to replace 
*developername* with your name and *modulename* with the folder of code 
you want.  For example, if you wanted to check out a copy of 
PloneHelpCenter, you would replace *modulename* with the word 
``PloneHelpCenter``::
 
    cvs -z3 -d:ext:developername@cvs.sourceforge.net:/cvsroot/collective co -P modulename
'''
Page2.Format = 'text/x-rst'
Page2.Transition = Transition.publish

# Sample Tutorial Page content ---------------------------------------
Page3 = PropertyHolder()
Page3.Id = 'page3'
Page3.Title = 'Sample Tutorial Page3'
Page3.Summary = 'Yet more sample content.  Somebody move that developer to the QA team!'
Page3.Body = '''
Related links
=============

The rest of the content below this point was basically stolen from
the CVS tutorial on Plone.org just to give us a non-trivial document.
It is one of the few reStructured Text documents for which I have the
source format.

This cheatsheet used a command line interface to CVS since it is easy
to explain and consistent across multiple platforms.  While some
operations may continue to be easier from the command line, even some
of us who generally prefer the command line like to use a graphical
CVS client when browsing file histories and looking at diffs between
revisions.  

http://www.wincvs.org/
    An excellent starting point for CVS and GUIs.  Links to multiple
    CVS client and visual diff GUIs for various platforms.
http://www.tortoisecvs.org/
    Recommended by multiple Plone developers who develop on Windows.
    This plugin enables CVS operations directly from Microsoft Windows
    file explorer. 
http://www.kde.org/apps/cervisia/
    I generally use Cervisia when I want a CVS client other than the
    command line or Emacs PCL-CVS mode under KDE on my Linux machines.

Hey, all of this CVS stuff is fascinating, right?  If you were one
of the two people who did not just fall out of your chair laughing,
then here are some links to get you started learning more.  Until
everyone stops using CVS in favor of some other revision control
software, there will be a need for developers who have a thorough
knowledge of CVS.  (Not everyone is content to be a faker!)

http://cvsbook.red-bean.com/ 
    My favorite CVS books.  Very practical.  Lots of "best practices"
    advice.  Also available in print.
https://www.cvshome.org/  
    The official home for all things CVS.
https://www.cvshome.org/docs/manual/ 
    The official CVS Manual originally by Per Cederqvist.
http://www.cmcrossroads.com/bradapp/acme/
    A nice starting point for SCM information in general, including 
    links to software other than CVS (Subversion, Perforce, ClearCase, etc.)
'''
Page3.Format = 'text/x-rst'
Page3.Transition = None

# Sample Tutorial content 1 ------------------------------------------
Tutorial1 = PropertyHolder()
Tutorial1.Id = 'tutorial1'
Tutorial1.Title = 'Test Tutorial 1'
Tutorial1.Summary = 'A sample Tutorial for functional testing of PloneHelpCenter.  A tutorial that is published; only in one section; has only a single tutorial page.'
Tutorial1.Versions = ( Hc.Versions[0], )
Tutorial1.Sections = ( TutorialFolder.Sections[1], )
Tutorial1.Pages = ( Page1, )
Tutorial1.Transition = Transition.publish
Tutorial1.Owner = User1

# Sample Tutorial content 1 ------------------------------------------
Tutorial2 = PropertyHolder()
Tutorial2.Id = 'tutorial2'
Tutorial2.Title = 'Test Tutorial 2'
Tutorial2.Summary = 'A sample Tutorial that is pending; only in one section; has three tutorial pages.'
Tutorial2.Versions = ( Hc.Versions[1], )
Tutorial2.Sections = ( TutorialFolder.Sections[1], )
Tutorial2.Pages = ( Page1, Page2, Page3, )
Tutorial2.Transition = Transition.submit
Tutorial2.Owner = User1

# Sample Tutorial content 1 ------------------------------------------
Tutorial3 = PropertyHolder()
Tutorial3.Id = 'tutorial3'
Tutorial3.Title = 'Test Tutorial 3'
Tutorial3.Summary = 'A sample Tutorial that is in-progress; only in one section; has no tutorial pages.'
Tutorial3.Versions = ( Hc.Versions[1], )
Tutorial3.Sections = ( TutorialFolder.Sections[1], )
Tutorial3.Pages = ()
Tutorial3.Transition = None
Tutorial3.Owner = User1

# Sample Tutorial content 1 ------------------------------------------
Tutorial4 = PropertyHolder()
Tutorial4.Id = 'tutorial4'
Tutorial4.Title = 'Test Tutorial 4'
Tutorial4.Summary = 'A sample Tutorial that is published; only in (a different) one section; has a couple of tutorial pages and at least one non-tutorial page piece of content.'
Tutorial4.Versions = ( Hc.Versions[1], )
Tutorial4.Sections = ( TutorialFolder.Sections[0], )
Tutorial4.Pages = ( Page1, Page2, Page3)
Tutorial4.Transition = Transition.publish
Tutorial4.Owner = User1


# Sample Tutorial content --------------------------------------------
Tutorial = PropertyHolder()
Tutorial.list = [ Tutorial1 , Tutorial2, Tutorial3, Tutorial4, ]

# Sample FAQ content 1 -----------------------------------------------
FAQ1 = PropertyHolder()
FAQ1.Id = 'faq1'
FAQ1.Title = 'What is Test FAQ 1?'
FAQ1.Question = 'This would be a long form of the question.  Sample FAQ for functional testing; published; only in one section.'
FAQ1.Answer = 'Bogus answer here.  Just a lot of text to fill some space.  ' * 3
FAQ1.Format = 'text/plain'
FAQ1.Versions = ( Hc.Versions[1], )
FAQ1.Sections = ( FAQFolder.Sections[1], )
FAQ1.Transition = Transition.publish
FAQ1.Owner = User1

# Sample FAQ content 2 -----------------------------------------------
FAQ2 = PropertyHolder()
FAQ2.Id = 'faq2'
FAQ2.Title = 'What is Test FAQ 2?'
FAQ2.Question = 'This would be a long form of the question.  Sample FAQ for functional testing; pending; only in one section.'
FAQ2.Answer = 'Bogus answer here.  Just a lot of text to fill some space.  ' * 3
FAQ2.Format = 'text/plain'
FAQ2.Versions = ( Hc.Versions[1], )
FAQ2.Sections = ( FAQFolder.Sections[1], )
FAQ2.Transition = Transition.submit
FAQ2.Owner = User1

# Sample FAQ content 3 -----------------------------------------------
FAQ3 = PropertyHolder()
FAQ3.Id = 'faq3'
FAQ3.Title = 'What is Test FAQ 3?'
FAQ3.Question = 'This would be a long form of the question.  Sample FAQ for functional testing; in-progress; only in one section.'
FAQ3.Answer = 'Bogus answer here.  Just a lot of text to fill some space.  ' * 3
FAQ3.Format = 'text/plain'
FAQ3.Versions = ( Hc.Versions[1], )
FAQ3.Sections = ( FAQFolder.Sections[1], )
FAQ3.Transition = None
FAQ3.Owner = User1

# Sample FAQ content 4 -----------------------------------------------
FAQ4 = PropertyHolder()
FAQ4.Id = 'faq4'
FAQ4.Title = 'What is Test FAQ 4?'
FAQ4.Question = 'This would be a long form of the question.  Sample FAQ for functional testing; published; only in (a different) one section.'
FAQ4.Answer = 'Bogus answer here.  Just a lot of text to fill some space.  ' * 3
FAQ4.Format = 'text/plain'
FAQ4.Versions = ( Hc.Versions[1], )
FAQ4.Sections = ( FAQFolder.Sections[2], )
FAQ4.Transition = Transition.publish
FAQ4.Owner = User1

# Sample FAQ content -------------------------------------------------
FAQ = PropertyHolder()
FAQ.list = [FAQ1, FAQ2, FAQ3, FAQ4,]


# Sample ErrorReference content --------------------------------------
ErrorReference = PropertyHolder()
ErrorReference.list = []


# Sample Glossary content --------------------------------------------
Glossary = PropertyHolder()
Glossary.list = []


# Sample LinkFolder content ------------------------------------------
Link = PropertyHolder()
Link.list = []


# Sample ReferenceManualFolder content -------------------------------
ReferenceManual = PropertyHolder()
ReferenceManual.list = []


# Sample Video content -----------------------------------------------
Video = PropertyHolder()
Video.list = []


