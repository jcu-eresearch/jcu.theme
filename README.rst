jcu.theme Package Readme
=========================

Overview
--------

A Plone theme based on the JCU style.  This version only works on Plone 4.1
and above from now on.

Keeping up with Plone
---------------------

Theme
^^^^^

Understandably, there will come times (almost every new version of Plone) where
new styles will be added to the default Plone theme (plonetheme.sunburst), and
changes will inevitably take place to the main_template and other templates
that we customise in this package.  In order to work with these changes, the
theme and its various customisations are built directly upon sunburst, such
that a visual merge with a tool like `meld` is possible against the
``skins/jcu_theme_styles`` directories like so::

    cd ./parts/omelette
    meld plonetheme/sunburst/skins/sunburst_styles/ jcu/theme/skins/jcu_theme_styles/

With this, you can visually compare each file and merge changes from sunburst
back into `jcu.theme`.  Most customisations that have been made are minor and
should be forward compatible.  YMMV with new Plone versions, though!

Templates
^^^^^^^^^

Similar to the styles above, we also need to keep in sync with templates.  This
theme customises some templates, in particular the `main_template`.  You should
also merge changes to these in too::

    cd ./parts/omelette
    meld plonetheme/sunburst/skins/sunburst_templates/ jcu/theme/skins/jcu_theme_custom_templates/
    meld plone/app/layout/viewlets/ jcu/theme/browser/templates/
    meld ./plone/app/controlpanel/usergroups_groupmembership.pt jcu/theme/browser/templates/usergroups_groupmembership.pt
    meld ./Products/CMFPlone/skins/plone_login/login_form.cpt ./jcu/theme/skins/jcu_theme_custom_templates/login_form.cpt
    meld ./Products/CMFPlone/skins/plone_login/logged_out.cpt ./jcu/theme/skins/jcu_theme_custom_templates/logged_out.cpt

If there are further new customisations, you need to add them here so people
know what to merge in.  Where possible, attempt to push changes back to the
Plone and other communities to avoid extra maintenance efforts.
