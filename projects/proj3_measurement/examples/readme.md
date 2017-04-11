This directory contains sample output that may be useful to understand the format we're expecting your code to produce.

`sample_ping.txt`: This file contains the raw output of a single run of `ping` on `google.com`. Each packet's RTT is on a separate line. Note that there is aggregate statistics at the end of each run!

`sample_ping.json`: This file contains the json formatted data that corresponds to the output from `sample_ping.txt`.

`traceroute_sample.txt`: This file contains traceroute output for `twitter.com`. Note that hop 11 does not respond at all, so be sure to take care of this corner case in your parsing script.

`traceroute_sample.json`: This file contains the json formatted data that corresponds to the output from `traceroute_sample.txt`. This additionally has a timestamp indicating when the run was executed.

`dig_sample_raw_output`: This contains the raw output of the dig command that was used to generate the data in `dig_sample_output.json`.  The output of different calls to dig is separated by a line of equals signs ("======...").  This file contains the output of 5 calls to dig to resolve `google.com`. Your dig output won't match this exactly: you may have slightly different formatting of the response on your computer, and the answers to each query will likely be different.

`dig_sample_output.json`: This contains the json generated from parsing the dig output in `dig_sample_raw_output` (your code should directly call dig to generate the json, rather than parsing an input data file; we provided `dig_sample_raw_output` only as an example so you can see how the dig output corresponds to json).
