## Script (Python) "queryForStaleItems"
##title=Final query for "stale" HelpCenter items, i.e. unchanged for a specified interval and type
##parameters=type,stale_interval

# Expects two additional items on the query-string:
#  type is the chosen portal_type, e.g. 'HelpCenterFAQ'
#  stale_interval is how old the items need to be, e.g. '3_months'

# Construct a catalog query using the specified interval (count back from
# the current date-time) and return the list of matching result objects
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
# print "Items unchanged since %s" % stale_threshold_time

time_string = '%s' % stale_threshold_time
date_string = time_string.split(' ')[0]

context.REQUEST.response.redirect(
        "search?review_state=published&portal_type:list=%s&modified:date=%s&modified_usage=range:max&submit=Search"
        % (type, date_string)
)
