## Script (Python) "fetchStaleItems"
##title=Query for "stale" HelpCenter items, i.e. unchanged for a specified interval
##parameters=stale_interval

# Construct a catalog query using the specified interval (count back from
# the current date-time) and return the list of matching result objects.
# This will populate the stale-HelpCenter-items portlet.
thresholdValues = {
    '1_day': 1,
    '1_week': 7,
    '2_weeks': 14,
    '1_month': 30,
    '3_months': 90,
    '6_months': 180,
    '1_year': 365,
}

stale_threshold_time = DateTime() - thresholdValues[ stale_interval ]

results = context.portal_catalog.searchResults(
    modified = { 'query': stale_threshold_time, 'range': 'max' },
    review_state=['published'], 
    portal_type=[
        'HelpCenterDefinition',
        'HelpCenterErrorReference',
        'HelpCenterFAQ',
        'HelpCenterHowTo',
        'HelpCenterLink',
        'HelpCenterTutorial',
    ],
    sort_on='portal_type',
)

return results
