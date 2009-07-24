========================
Products.PloneHelpCenter
========================

If you are upgrading an existing PHC installation, you *must* read
INSTALL.txt.

Overview
========

Plone Help Center is an application designed to aid the documentation of
Plone, and is used on plone.org to categorize and keep documentation up to
date. It should be usable for documenting other open source products
(such as Plone Product add-ons) or even for other documentation projects.

Usage
=====

Plone Help Center has inline documentation, just add a help center.

What's New in 3.0
=================

The underlying architecture of previous versions of PHC was basically
Plone 2.0. It was built on Archetypes without ATContentTypes. Features
like next/previous navigation and automatic tables of contents were all
built in. In many way, PHC was a test center for new Plone features.

However, Plone advanced and PHC did not.

PHC 3 is much less ambitious. Rather than trying to add new features
to Plone, this version seeks to inherit Plone 3 features by reimplementing
most of the PHC content types as ATCT-derived classes that automatically
implement Plone 3 behavior. PHC-specific features are added via sub-classing
or interfaces/adapters.
