## Script (Python) "checkVersionOutdated"
##title=Return 1 if the version is outdated, 0 otherwise
##parameters=versions, currentVersions=None

if not versions:
    return 0
    
if not currentVersions:        
    # Acquire current versions if not given
    currentVersions = context.getCurrentVersions()
        
if not currentVersions:
    return 0

for v in versions:
    if v in currentVersions:
        # Not outdated - we match one of the current versions
        return 0
        
# Outdated - we didn't match anything
return 1