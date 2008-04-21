Overview

  Plone Help Center is an application designed to aid the documentation of
  Plone, and is used on plone.org to categorize and keep documentation up to
  date. It should be usable for documenting other open source products
  (such as Plone Product add-ons) or even for other documentation projects.

Installation

  You install it the usual way - using Plone Setup.
  
Upgrading

  If you are upgrading form a previous version, you must run migrations after
  re-installing the PloneHelpCenter product.
  
  1. Visit the archetypes_tool in your site root via the ZMI;

  2. Choose the "Update Schema" tab and select all the "PloneHelpCenter::"
     content types;
     
  3. Press the "Update schema" button and wait for the "Done" indication.

Usage

  Plone Help Center has inline documentation, just add a help center.

Requirements

  This version of PloneHelpCenter has been tested with Plone 3.0.2.
  
  Optional:
  
  - AddRemoveWidget -- PLEASE NOTE: if AddRemoveWidget is installed
  as a Zope product, you *must* also install it in Plone. If it is
  present without being installed, errors will occur.

Version 1.5 Notes

  This version is still experimental. Baseline functionality looks good, but
  there's work left to do.

Credits

  Project Architecture, Development, Content Types, Archetypes,
  Workflow -- "Joel Burton":mailto:joel@joelburton.com

  Development, User Interface, Project Architecture, Quality Assurance --
  Alexander Limi, "Plone Solutions":http://www.plonesolutions.com
  
  Development, persistence and all-round brilliance -- Martin "optilude" Aspeli

  Development, Assistance -- Christian 'Tiran' Heimes

  Original FAQ code -- "Tim Terlegard":mailto:tim@se.linux.org,
  "Edward Muller":mailto:edwardam@interlix.com - further enhancements
  by Jean-Paul Ladage and Ahmad Hadi from "Zest
  software":http://zestsoftware.nl

  Fixing various stuff, documentation -- The Sprinters: Christian Heimes,
  Dorneles Treméa, Daniel Nouri, Nate Aune

  Added optional 'see also' references to other Archetypes based types --
  Jens 'jensens' Klein, "jens quadrat":http://jensquadrat.com/

  i18n improvements and general fixes in some templates and brazilian
  translations by Jean Ferri <jeanferri@gmail.com>

  Bugfixes and occasional Quality Assurance -- 
  Geir Bækholt, "Plone Solutions":http://www.plonesolutions.com

  Topic, start-here, and 1.0 search options -- the 2007 documentation
  sprint participants, particularly aclark, joelburton, magnon and stevem.

