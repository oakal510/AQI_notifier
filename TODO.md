Priorities
- Update Docker files to use slim build
- update Docker file and then AWS lambda with my sensor list instead of test list when deployed
- create events in AWS for my program to run daily
- refactor code / reorganize to move functions from init
- sessionize the sensor api requests to improve program speed
- maybe log if sensors are not online during runtime and other errors for review

Future features / considerations
- add feature to notify Google Home of high average aqi readings and then turn on smart plugs for air purifiers
- record historic aqi records in sql for analysis
- create alternative recommendation messages / either randomize or allow user to select a type of recommendation
- create a bot to publish data for my program runs to public webpage
- create a data class from the purple air json objects
- write to sql database when checking on sensor list to capture historic data
- consider filtering out "untrustworthy" sensors (a versus b sensor data) (or does purple air already do this in the stats? is there a need?)

