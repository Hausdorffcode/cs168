# Measurement

In this project, you'll use three command-line tools to analyze the behavior of the Internet.  You'll use `ping` to measure round trip times and drop rates, `traceroute` to examine routes, and `dig` to understand how names are mapped to IP addresses.  The assignment is centered around studying the connection from you to each of top 100 most commonly accessed websites (as measured by [Alexa](http://www.alexa.com/)).  In some cases, we'll ask you to do more detailed measurements on a smaller set of websites to drill down into a particular measurement.

#### Logistics

- This project is due on Wednesday 11/9 at 11:59pm
- This project should be completed individually or in pairs (refer to the [course website](https://netsys.github.io/cs168fa16/about.html) for collaboration policies).  As described on the course website, you may not share *code* with any classmates other than your partner.  For this assignment, much of the work will be analyzing and thinking about the measurements that you've made; you are welcome to discuss the findings from your measurements with other students who you are not partnered with for the assignment.
- The skeleton code for this project is available on [Github](https://github.com/NetSys/cs168_student/blob/master/projects/proj3_measurement). You can download the code manually from that page, or use git.

##### What should I submit?

- Submit your code and data using `ok`.  You should submit the following, described in more detail below:

  Code:
    - `rtts.py`
    - `traceroute.py`
    - `dns.py`

  Json data:
  	- `rtt_a_raw.json`
 	- `rtt_a_agg.json`
  	- `rtt_b_raw.json`
 	- `rtt_b_agg.json`
	- `tr_a.json`
	- `tr_b.json`
    - `dns_output_1.json`
    - `dns_output_2.json`
    - `dns_output_other_server.json`

- In addition to submitting your code to `ok`, you should submit a set of short answers and graphs to gradescope.  The specific short answers and graphs you should generate are listed in the sections that follow.  We will update the link to submit this shortly.  This must be submitted as a PDF; you can create the PDF using whatever tool is most convenient for you.

##### Provided files

We have provided the following files for your use:

- `alexa_top_100`: The top 100 most popular websites.  This is the real top 100 alexa websites; we have not censored this. As a result, use caution before visiting any of the websites.
- `project3_tests.py`: A set of tests for you to run on your code. This file mostly tests json data formats, so feel free to write your own correctness tests.
- The `examples` directory contains example output, described in more detail in the sections that follow.

##### Resources

If you have questions, take a look at the [FAQ section](#faq).  If your question isn't answered there, post to Piazza.

### Part 1. Round trip time

In this part of the assignment, you will use [ping](https://linux.die.net/man/8/ping) to measure the round trip time to different websites.

**Scripts**

You should write a Python script called `rtts.py` that has three functions: `run_ping`, `plot_median_rtt_cdf`, and `plot_ping_cdf`. 

`run_ping` should run ping commands and generate json output. It should take in 4 parameters:

- `hostnames`: list of hostnames to be ping'd
- `num_packets`: number of ping packets to send to each host
- `raw_ping_output_filename`: name of a filename to output the raw ping results to (as json)
- `aggregated_ping_output_filename`: name of a filename to output the aggregated ping results to (as json)

For example, if `hostnames = ["www.google.com"]` and `num_packets = 100`, then you should ping Google 100 times.
You can do so by calling the `ping` shell command from python using the subprocess module:

``` ping -c 100 google.com ```

`run_ping` should generate two json outputs.

- Raw ping results. This file includes the detailed result on a per packet level. The data format is:
  ```
  {
		hostname1:  [rtt_1, rtt_2...],
		hostname2:  [rtt_1, rtt_2...],
		...
  }
  ```
  Each hostname is mapped to a list of RTTs. Following the previous example, if you ping `google.com` 100 times, then there should be one hostname "google.com" mapped to a list of 100 RTTs. The hostname should be string, and the list of RTTs should be floats and measured in milliseconds. Note that not all websites will respond to pings, and some may drop packets. If an ICMP packet times out, then please use `-1.0` for the RTT instead.

- Aggregated ping results. For each website, you should aggregate the raw ping results to produce the median RTT, the maximum RTT, as well as the packet loss rate. The format should be

  ```
  {
		hostname1: {“drop_rate”: drop_rate1, “max_rtt”: max_rtt1, “median_rtt”: median_rtt1},
    	hostname2: {“drop_rate”: drop_rate2, “max_rtt”: max_rtt2, “median_rtt”: median_rtt2},
		...
  }
  ```

  The hostnames are again strings and are each mapped to three aggregated numbers: drop rate, maximum RTT, and median RTT. Drop rate should be specified in percentage between 0.0 and 100.0 (e.g. if you observe 5 packets dropped in a ping run of 500, the percentage is 1.0). Max RTT and median RTT should be in milliseconds. All three numbers should be floats.
If a website does not respond to pings at all, then max and median RTT should be -1.0, and drop rate should be 100.0.

For example outputs, please take a look at `examples/sample_ping.txt` and `examples/sample_ping.json`. The text file shows the raw text output from pinging google.com 10 times, and the json file shows the json formatted raw ping results. 

The other two functions should should generate CDF graphs using the json data produced from `rtts.py`.  They should work as follows:

- `plot_median_rtt_cdf(agg_ping_results_filename, output_cdf_filename)`: this function should take in a filename with the json formatted aggregated ping data and plot a CDF of the median RTTs for each website that responds to ping
- `plot_ping_cdf(raw_ping_results_filename, output_cdf_filename)`: this function should take in a filename with the json formatted raw ping data for a particular hostname, and plot a CDF of the RTTs

**Experiments**

Using your scripts, please run the following experiments.

a) Ping each each Alexa top 100 website 10 times. You should store `rtts.py`'s output in two files: `rtt_a_raw.json` (with raw json data only) and `rtt_a_agg.json` (with aggregated json data only). 

b) Next, we want to take a look at a few websites’ ping behavior in more detail. The websites are: google.com, todayhumor.co.kr, zanvarsity.ac.tz, taobao.com. Ping each website 500 times. Again, generate two json files: `rtt_b_raw.json` and `rtt_b_agg.json`.

**Short answer questions**

1. Questions on experiment a:
   - What percentage of the websites do not respond to pings at all? What percentage have at least one failed ping?
   - Using the plot functions and `rtt_a_agg.json`, please plot a CDF of the *median* RTT of the websites that respond to ping.
2. Questions on experiment b:
   - What are the median RTT and maximum RTT for each website? What loss rate do you observe?
   - Using the plot functions to and `rtt_b_raw.json`, please plot a CDF of the RTT for *each* website (i.e. there should be 4 different graphs).
3. In this question, you will analyze the ping times to two websites and compare the results to the expected speed-of-light times. The websites are google.com (located in Mountain View, CA, USA) and zanvarsity.ac.tz (located in Zanzibar, Tanzania). You can use your ping data from experiment b. The distance from Berkeley to Mountain view is 35.23 miles, and the distance from Berkeley to Zanzibar is 9,953.50 miles.
   - Compare the median ping time to the speed of light time.  What’s the multiplier for each server (calculate as [ping time / speed of light time])?
   - Using one sentence each, list two reasons why the ping time is not equal to the speed of light time.  Plausible but unlikely answers (e.g., “a bear chewed through the wire, causing a long delay) will not receive full credit.
   - [Optional] Repeat #3 for any website you might be curious about. How much route inflation do you observe? This [tool](http://pythonhosted.org/python-geoip/) might be useful in identifying a website’s physical location.

##### Part 1 hints
- Be careful with parsing pings that fail because the output data format will be different.
- Some servers do not respond to pings at all (i.e., all of the packets are dropped).
- Note that packets may drop even with servers that do respond to ping. Be sure to capture *which* packet was dropped in your parsing script.
- Ping prints out aggregated results at the end of a run. You can use this to sanity check your scripts!

### Part 2. Routing

While ping is useful for identifying end-to-end behavior, [traceroute](https://linux.die.net/man/8/traceroute) is a tool that can give you more detailed information about internet routing. In particular, traceroute allows you to trace the entire route from your machine to a remote machine.

**Scripts**

You should write a Python script named `traceroute.py`. Similar to `rtts.py`, this file should run traceroute for a list of of websites and produce json output.
The file should also be able to parse the shell traceroute command output directly (this will be used in experiment b).
The script should contain two functions:

- `run_traceroute(hostnames, num_packets, output_filename)`: used to run the traceroute command on a list of hostnames. Outputs the traceroute command's results.
  * `hostnames`: a  filename containing a list of hostnames for traceroute
  * `num_packets`: how many packets to send to each hop
  * `output_filename`: where to save the traceroute command's results 
- `parse_traceroute(raw_traceroute_filename, output_filename)`: this function should be able to take in outputs from a traceroute run (either from `traceroute()` or from a separate run) and write out json data.
  * `raw_traceroute_filename`: name of the file that stores traceroute output from the shell command
  * `output_filename`: where to store the output json data 

You can traceroute to a website by running the `traceroute` shell command from Python using the subprocess module:

``` traceroute -a -q 5 google.com ```

The option `-a` tells the command to return AS numbers (note that this option may be slightly different on different operating systems), and the option `-q` tells the command how many packets to use.

Your script should produce json output in the following format: 

```
{
    “timestamp”: unix_time_stamp,
    hostname1: [
     [{“name”: name, “ip”: ip, “ASN”: as_number}, {“name”: name, “ip”: ip, “ASN”: as_number}],
     [{“name”: name, “ip”: ip, “ASN”: as_number}],
     …
     ],
     hostname2: [...],
     ....
}
```

Each run has a unix timestamp (you can use the`time` module in python), and it should be a string. The timestamp indicates when a specific run is started. Each hostname should also be formatted as a string. The value corresponding to each hostname is a list of routers encountered on the path. The first item in the list corresponds to the first hop, second item is the second hop, etc. Each hop is also a list (traceroute may encounter multiple routers within the same hop!). Finally, each router should have three fields: name, IP, and AS number. Everything should be string formatted, including the AS number. Unfortunately, not every router will respond to traceroute. If this is the case, simply output “None” for each field.

For example outputs (both raw text output and json output), please take a look at `traceroute_sample.txt` and `traceroute_sample.json`.
The text file contains text output from the traceroute command, and the json file contains the corresponding parsed json output.

**Experiments**

a) For part a, you will look at the routing behvaior to the following websites: google.com, facebook.com, www.berkeley.edu, allspice.lcs.mit.edu, todayhumor.co.kr, www.city.kobe.lg.jp, www.vutbr.cz, zanvarsity.ac.tz. For this experiment, please try to run traceroute from campus. You should run `traceroute.py` 5 times (with 5 packets each time), and each consecutive run should be at least 1 hour apart.
You should generate a json file named `tr_a.json`.
This file should be 5 lines long, where *each line* is a single run of `traceroute.py` on the above websites. You should be able to generate this file by appending output from your script to `tr_a.json`.

b) There are many [public route servers](http://www.traceroute.org/#Route%20Servers) hosted in different regions that are useful for measuring internet routing state. We will use several of these servers to observe *route symmetry*. For this question, please use the folloawing list of public servers: tpr-route-server.saix.net, route-server.ip-plus.net, route-views.oregon-ix.net, route-server.eastern.allstream.com.

- Run traceroute from your computer to the public route servers. 
- Run traceroute from the public servers to your computer. *Note: if your computer does not have a public IP address, try to run traceroute to its first hop router*
  * You can log into these servers directly using telnet (e.g. `telnet tpr-route-server.saix.net`). Note that some of them may require you to use a username/password.
- You should produce a json file named `tr_b.json`. This file should be 2 lines long. The first line should be the json data from the run from your computer to the public route servers, and the second line should be the json data from traceroute run in the reverse direction.

**Short answer questions**

1. Answer the following questions using the results obtained from experiment a.
   * Which ASes are Berkeley directly connected to?
   * Which traceroute traverses the most number of ASes? How about the least number of ASes?
   * Which websites are load-balanced?
   * Are the observed routes stable over multiple runs?  For each website, how many unique routes did you observe?
   * Using one sentence, please explain one advantage of having stable routes.
   * [Optional] Make a graph of the ASes and their connectivity.

2. Answer the following questions using the results obtained from experiment b.
   * How many hops do you observe in each route when you run traceroute *from* your computer? How many hops do you observe in the reverse direction? 
   * Are these routes symmetric? How many are symmetric and how many are not?
   * What might cause asymmetric routes? List one or two reasons.



##### Part 2 hints
Again, be careful with parsing the traceroute text because there are corner cases. Traceroute’s raw text output is more complex than ping’s output. Make sure your script is able to correctly parse the following situations:
- A particular hop does not respond at all (usually you will see “* * * * *”)
- A particular hop has multiple routers that respond
- A particular hop has a couple packets that are dropped, but the rest are returned

## Part 3. Naming

In this part of the assignment, you’ll use the dig command to understand DNS latencies.

**Scripts**

First, write a script `dns.py` that resolves IP addresses and generates json output summarizing the results. Your script should have several functions for running dig, as well as processing the dig outputs.

Your script should contain a function named `run_dig(hostname_filename, output_filename, dns_query_server=None)` that resolves the IP addresses corresponding to the top 100 websites. This function should resolve each address 5 times.
- `hostname_filename`: the file containing the list of hostnames, e.g. `alexa_top_100`
- `output_filename`: name of the json output file
- `dns_query_server`: an optional argument that specifies the DNS server to query

Your script should resolve each site starting from the root (i.e., first query the root domain server, then the TLD domain server, and so on).  You should do this by calling the following shell command from python:

    dig +trace +tries=1 +nofail www.google.com
    
Note that this command also includes some extra flags.  The `+tries=1` and `+nofail` flags signal to dig not to failover when the DNs lookup fails, so that you can count how many lookups fail.

If the `dns_query_server` is specified, your script should send DNS requests to the specified server, and should not use the `+trace` argument; e.g.:

    dig www.google.com @1.2.3.4

where `1.2.3.4` is the DNS server's address.

`run_dig` should generate json output with a list of json dictionaries each representing a single call to “dig”, and save the output to `output_filename`.  The representation of each call to “dig” should be structured as follows:

- “Name”:  name being resolved
- "Success": whether the dig call was successful (if this is false, there should be no other fields in the json output)
- “Queries”: list of all of the queries made for a single dig call.  The format of each query is:
  - “Time”: integer representing the time taken to complete the query
  - “Answers”: a list of answers for the query.  The format of each answer is:
    - “Queried name”: The name that was queried for (e.g., “.” or “.com.”). This is the first field in the dig output.
    - “Data”: result (e.g., for NS records, the name of a DNS server, or for A records, an IP address)
    - “Type”: type of the answer (e.g., “CNAME” or “A”)
    - “TTL”: Integer representing the TTL of the answer

We’ve provided each of these key names in `utils.py`, and we’ve also provided an example of 5 iterations for one website (www.google.com) in `examples/dig_sample_output.json`.  See `examples/readme.md` for more information about this file.  There's also a test for your dig dns output in `project3_tests.py`.

`dns.py` should also include the following processing functions:

- `get_average_ttls(filename)`: This function should accept the name of a json file with output as specified above as input.  It should return a 4-item list that contains the following averages, in this order:
    - What’s the average TTL of the root servers?
    - What’s the average TTL for the tld servers?
    - What’s the average TTL for any other name servers? (e.g., for google.com, this includes the google.com name server).
    - What’s the average TTL for the terminating CNAME or A entry?

  In other words, it should return `[average_root_ttl, average_TLD_ttl, average_other_ttl, average_terminating_ttl]`.  All times should be in seconds.

  One thing that's tricky here is how to deal with queries that return multiple answers.  For example, suppose your json output had queries for just two sites.  For the sake of example, let's look at just the terminating entries for these sites:
  
  www.google.com:
    
  `www.google.com.		300	IN	A	172.217.5.100`
  
  weibo.com:
  
  `weibo.com.		60	IN	A	180.149.134.141`
  `weibo.com.		60	IN	A	180.149.134.142`
  
  Here, the DNS request for `weibo.com` returned two different terminating records, which is often done to help load balance and handle failures.  To compute the average TTL, you should first compute the average TTL for each query.  Here, that would give you two averages: 300 (for google) and 60 (for weibo).  Then you should take the average over those, giving you a result of 180 in this case.  The reason for doing this is to avoid giving more weight to the TTLs from queries that return multiple answers.
  
- `get_average_times(filename)`: This function should accept the name of a json file with output as specified above as input.  It should return a 2-item list that contains the following averages, in this order:
    - The average of the total time to resolve a site.  This should include the time to resolve all steps in the hierarchy.  For example, for google.com, it should include the time to contact a root server to determine the top level domain server (com) location, and the time to contact the com TLD server to resolve google, and the time to contact the google name server to resolve google.com.
    - The average of the time for just the final request that resulted in the A (or CNAME) record.
- `generate_time_cdfs(json_filename, output_filename)`: This function should accept `json_filename`, the name of a json file with output as specified above as input.  It should generate a graph with a CDF of the distribution of each of the values described in the previous function (the total time to resolve a site and the time to resolve just the final request) and save it to `output_filename`.  It should not return anything.
- `count_different_dns_responses(filename1, filename2)`: This function should take the name of two files that each contain json dig output.  The idea of this function is to count the number of changes that occur between the two sets of dig runs in the two different filenames.  The function should return a list of two values.

    The first value should be the number of names that had a different answer just within the traced queries in `filename1`.  Since you'll have 5 iterations of each query, it's possible you'll have queries that returned different answers -- for example, in one of our trial runs, the first 4 dig calls to `google.co.kr` returned 172.217.5.99, and the last call returned 216.58.219.67.  In this case, `google.co.kr` is counted as one entry that changed within the first trial.

    The second value should be the number of names that had a different answer if you inclue the data in `filename1` *and* the data in `filename2`.  This value should be greater than or equal to the previous value (because it includes all of the previous cases).

    One complexity to consider here is that queries often return a set of answers. For example, one query to `www.scottshenker.com` might return `1.2.3.4` and `5.6.7.8`, and a later query might return `5.6.7.8` and `9.10.11.12`.  You should consider two query answers to be different if the sets of answers are different.  So for example, if one query returns two answers `1.2.3.4` and `5.6.7.8`, and the next query returns the same two answers (even in different order): `5.6.7.8` and `1.2.3.4` these are considered the same.  If a 3rd query returned a different set: `1.2.3.4` and `5.6.7.8` and `9.10.11.12`, then this you should consider this different. The reason for this behavior is you're trying to get a sense of what time to live value is necessary -- in other words, how often do DNS servers change their minds about the answer to give to clients?

Python's `set` class and the associated `==` functionality will likely be helpful for this.

**Short answer questions**

In addition to turning in `dns.py`, you should submit the following with your short answers:

a) What's the average root TTL in the 5 iterations of the top Alexa websites?  Average TLD TTL? Average other name server TTL? Average terminating entry TTL?

b) Plot a CDF of your 5 iterations from the Alexa top 100 websites using your `generate_time_cdfs` function (this should have two lines, as described above).

c) Run `run_dig` twice at least 1 hour apart.  How many answers change within the first trial?  How many names gave different answers at some point in the two trials (i.e., what values does `count_different_dns_responses` return?)?

d) Run `run_dig` using the name of a server in a different country.  You can find public DNS servers in other countries [here](http://public-dns.info/).  Run `count_different_dns_responses` with your original trace and the one from the new country.  What does it return?

e) Take a look at a few of the names that returned different answers when you queried a different name server in part d.  Use `ping` to measure the round trip time to the different IP addresses returned.  What's the most likely reason that the different DNS server returned a different IP address?  Answer in one sentence (you do not need to provide your ping output).

f) We asked you to use the `+trace` argument when running dig, which causes your local machine to resolve all requests iteratively starting from the root DNS server.  How would the DNS resolution times have been different, and why if you hadn’t used the “+trace argument”?  Answer in 1 sentence.

Finally, you should submit dns_output_1.json (with the output of one call to `dns.py`), dns_output_2.json (with the output of a second call to `dns.py` at least one hour from the first call), and `dns_output_other_server.json` (with the output of a third acll to `dns.py` using a different DNS server).

##### Part 3 hints

When you call dig, extra information (e.g., the query sent, or the time it took) appear on lines that start with `;`.  To determine the total time for the query, you'll need to parse some of these lines.  Keep in mind that the output is different when using `+trace` compared to when not using trace (i.e., when you query a specific DNS server).  You'll need to handle both types of output.  In both cases, the easiest way to handle the output is typically to call python's `split()` function to get a list of each word in the output, and then get the item at the index you're looking for.

`dig` answers are found in lines that don't start with `;`.  Again, the python `split()` function will likely be useful for parsing the output.

One thing that can be difficult is determining whether the queried name is for a root server, a TLD server, or another DNS server.  One way to do this is to check the queried name in this order:

- Is the queried name just `.`? In this case, it's for the root server.
- Does the queried name contain only one `.`?  In this case, given that we already checked for the root server, it must be for a TLD server (e.g., `com.`).
- Any other `NS` records are for other name servers.
             
## FAQ

##### How can I call a shell command from Python?

The easiest way to call a shell command is to use the `subprocess` library's `check_output` call.  Be sure to pass in `shell=True`:

    import subprocess
    ls_output = subprocess.check_output("ls", shell=True)

##### How should I generate a plot?

We recommend using matplotlib to generate plots.  Suppose you have list x_values that contains all of the x values of points that you’d like to plot, and a second corresponding list (with the same length) y_values:

     import matplotlib.pyplot as plot
     plot.plot(y_values, x_values, label=”My data”)
     plot.legend() # This shows the legend on the plot.
     plot.grid() # Show grid lines, which makes the plot easier to read.
     plot.xlabel("x axis!") # Label the x-axis.
     plot.xlabel("y axis!") # Label the y-axis.
     plot.show()

##### How can I automatically save the result of my plot to a file?

     from matplotlib.backends import backend_pdf
     my_filepath = “dns_plot.pdf”
     with backendpdf.PdfPages(my_filepath) as pdf:
          pdf.savefig()

