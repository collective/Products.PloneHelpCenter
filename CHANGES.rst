HISTORY
=======

4.0.1 (unreleased)
------------------

- Add items to 'No section' for which getSection returns an empty list.
  [pbauer]

- Allow 'internally_published' for items.
  [pbauer]

- Fix german translations.
  [pbauer]


4.0 (2013-09-21)
----------------

- Compatible with Plone 4.2 and 4.3.  Should still work on 4.0 and
  4.1.
  [maurits]

- Types: switch from content_icon to icon_expr.
  [maurits]

- Switch the sample manual text to html.  This way you can edit it
  properly with TinyMCE.  It used to be structured text, which is
  not accepted as mimetext by default, so you would actually lose
  the layout when you edit it.
  [maurits]

- Register png icons from standard Plone for HelpCenterHowToFolder
  and HelpCenterLinkFolder.  Add upgrade step to apply the
  typeinfo and recatalog these two portal_types.  Otherwise on
  Plone 4.3 these items miss icons in listings.
  [maurits]

- Fixed faqfolder_view error by checking if item brain returns a value
  when asking for getSections
  [ichim-david]

- Removed ancient patch for CMFCore 1.4.7 or lower, which was last
  used in Plone 2.0.5.
  [maurits]

- Fix test for knowledge base type not globally addable.
  [ale-rt]

- Replace rss.gif with rss.png
  [ale-rt]

- Removed unused to remove dependency from zope.app.publisher.
  [ale-rt]

- Make ManualPage addable through tempfolder
  [tiberiuichim]

- Make the knowledge base type not globally addable.
  [davisagli]

- Make it possible to filter phc_search by getVersions
  [davisagli @ cioppino]

- Improved styling of portlet_phc_about
  [davisagli, hennaheto @ cioppino]


PloneHelpCenter 4.0b3 (2011-05-12)
----------------------------------

- Clean up package and release
  [aclark]

- Update discussion_reply.cpy to keep in sync with Plone.
  [davisagli]

- Add subnavigation to most templates.
  [smcmahon]

- Revamp helpcenter_topicview_main to show start-here items,
  topic counts.
  [davisagli]

- Add getPHCSubNav method for PloneHelpCenter to create subnavigation.
  [stevem]

- Added metadata.xml file, used by QuickInstaller when upgrading
  [afd]


PloneHelpCenter 4.0b2 (2010-12-28)
----------------------------------

- Fix phc_stats template in Plone 4.
  [davisagli]

- Fix import error in Plone 3.
  [miohtama]

- Use the containment acquisition chain to get the parent
  attributes in ReferenceManualSection type.
  [dukebody]

- Make listings respect the subtopics order set in the HelpCenter
  or type folders, instead of sorting alphabetically.
  Fixes http://plone.org/products/plonehelpcenter/issues/127.
  [dukebody]


PloneHelpCenter 4.0b1 (2010-12-09)
----------------------------------

- Use ordering adapters in Plone 4 to sort items in sections.
  [dukebody]

- Make the default view for PHC folders obey the items ordering
  set using the Contents tab. Formerly, they were sorted
  alphabetically by title.
  Fixes http://plone.org/products/plonehelpcenter/issues/121.
  [dukebody]

- Allow all site-enabled markup types for PHC content, instead of
  a fixed list.
  Fixes http://plone.org/products/plonehelpcenter/issues/117.
  [dukebody]

- Modify workflow definitions to disallow Anonymous users to see
  content inside hidden Help Centers.
  Fixes http://plone.org/products/plonehelpcenter/issues/118.
  [dukebody]

- Remove the "Properties" tab for content-types, that was
  duplicating the Metadata schemata already present in the edit
  view in Plone 3.
  Fixes http://plone.org/products/plonehelpcenter/issues/119.
  [dukebody]

- Make mail sending code compatible with Plone 3. PHC 4 is now
  compatible with both Plone 3 and 4.
  [dukebody]


PloneHelpCenter 4.0a1 (2010-12-07)
----------------------------------

- Use lxml to turn image relative links into absolute for the
  one-page version of manuals. This introduces a new install
  dependency on lxml.
  Fixes http://plone.org/products/plonehelpcenter/issues/136.
  [dukebody]

- Include numbering in the section title.
  Fixes http://plone.org/products/plonehelpcenter/issues/137.
  [dukebody]

- Rename type titles: "Page" to "Tutorial Page" and "Link" to
  "Help Center Link".
  Fixes http://plone.org/products/plonehelpcenter/issues/140.
  [dukebody]

- Made it possible to query contentIds via XML-RPC for
  collective.developermanual uploads [miohtama]

- Use the aq_parent function instead of the attribute to avoid
  AttributeErrors when not using an acquisition wrapper (newer
  Zope versions).
  [dukebody]

- Fix next/previous custom adapter to visit the same items as appear in
  the navigation dropdown. Also make sure this adapter is used for legacy
  ReferenceManuals. This fixes
  http://plone.org/products/plonehelpcenter/issues/152/.
  [dukebody, davisagli]

- Don't fail when trying to acquire getCurrentVersions if not in
  a container that includes currentVersions in its schema. [davisagli]

- Fix the imports to use always Zope 3 style interfaces, making
  the code work both in Plone 3 and 4 simultaneuslly.
  [dukebody, thanks davisagli]

- Merge relevant changes from the Plone 4 migration branch from
  Fabio Rizzo. [dukebody]

- Reverted obsolete code from the referencemanual_view.pt fix. [acsr]

- Updated INSTALL.txt with step by step upgrade guide related to
  issue #142 "upgrade steps order unclear" and issue #132 "errata
  mentioning Ploneboard". [acsr]

- Fixed an issue with failure to display referencemanual_view when
  files are present in the reference manual. [acsr, thanks dukebody]

- Update the whole product to work with Plone 4.0a2. [dukebody]

- Removed "global allow" for Reference Manual. This closes
  http://plone.org/products/plonehelpcenter/issues/150.
  [keul]

- updated INSTALL.txt with step by step upgrade guide related to
  issue #142 "upgrade steps order unclear" and issue #132 "errata
  mentioning Ploneboard". [acsr]

- Respect exclude_from_nav setting in the reference manual
  table of contents generation [miohtama]

For older history, see ``docs/HISTORY.txt``.
