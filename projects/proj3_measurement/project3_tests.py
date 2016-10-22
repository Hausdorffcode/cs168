import json
import argparse

import utils

def ping_format_check(output):
    for hostname, rtts in output.iteritems():
        if type(hostname) != str and type(hostname) != unicode:
            raise Exception("expected type str for hostname " + hostname + ", got type " + type(hostname))
        if type(rtts) != list:
            raise Exception("expected list type for RTTs")
        for rtt in rtts:
            if type(rtt) != float:
                raise Exception("expected float type for each RTT value")

def rtt_part_a_check(text):
    output = json.loads(text)
    ping_format_check(output)
    
    if len(output) != 100:
        raise Exception("expected 100 websites, got " + str(len(output)) + " websites")
    for h, rtts in output.iteritems():
        if len(rtts) != 10:
            raise Exception("expected 10 pings for website " + h + ", got " + str(len(rtts)) + " pings")
    
    top_100_sites = [x for x in open("./alexa_top_100", 'r').read().split('\n') if x != '']
    for h in top_100_sites:
        if h not in output:
            raise Exception(h + " is not in the data")

    print "RTT part a PASS"

def rtt_part_b_check(text):
    output = json.loads(text)
    ping_format_check(output)
    
    sites = ["google.com", "todayhumor.co.kr", "zanvarsity.ac.tz", "taobao.com"]
    
    if len(output) != len(sites):
        raise Exception("expected " + str(len(sites)) + " websites, got " + str(len(output)) + " websites")
    for h, rtts in output.iteritems():
        if len(rtts) != 10:
            raise Exception("expected 500 pings for website " + str(h) + ", got " + str(len(rtts)) + " pings")
    for h in sites:
        if h not in output:
            raise Exception("could not find %s in data" % (h))

    print "RTT part b PASS"

def path_check(path):
    if type(path) != list:
        msg = "expected list type for 'path' value, instead got type " + str(type(run_data["path"]))
        raise Exception(msg)
                
    for hop in path:
        if type(hop) != list:
            msg = "expected list type for each hop in 'path' value, instead got type " + str(type(hop))
            raise Exception(msg)

        for server in hop:
            if "name" not in server:
                msg = "'name' not found"
                raise Exception(msg)
            if "ip" not in server:
                msg = "'ip' not found"
                raise Exception(msg)
            if "asn" not in server:
                msg = "'asn' not found"
                raise Exception(msg)
            
def tr_single_run_check(output, sites):
    if len(output) != len(sites) + 1:
        msg = "expected %u sites, got %u sites" % (len(sites), len(output) - 1)
        raise Exception(msg)

    for site in sites:
        if site not in output:
            msg = "could not find %s" % (site)
            raise Exception(msg)

    if "timestamp" not in output:
        msg = "'timestamp' field not found in traceroute output"
        raise Exception(msg)

    for hostname, data in output.iteritems():
        if hostname == "timestamp":
            continue
        path_check(data)


def tr_part_a_check(text):
    sites = ["google.com", "facebook.com", "www.berkeley.edu", "allspice.lcs.mit.edu", "todayhumor.co.kr", "www.city.kobe.lg.jp", "www.vutbr.cz", "zanvarsity.ac.tz"]

    lines = text.split('\n')

    if (len(lines) != 5):
        msg = "expected 5 runs for traceroute part a, got %u lines instead" % (len(lines))
        raise Exception(msg)

    for line in lines:
        output = json.loads(line)
        tr_single_run_check(output, sites)

    print "Traceroute part a PASS"
                    
def tr_part_b_check(text):
    sites = ["tpr-route-server.saix.net", "route-server.ip-plus.net", "route-views.oregon-ix.net", "route-server.eastern.allstream.com"]
    
    lines = text.split('\n')

    if (len(lines) != 2):
        msg = "expected 2 runs for traceroute part a, got %u lines instead" % (len(lines))
        raise Exception(msg)

    for line in lines:
        output = json.loads(line)
        tr_single_run_check(output, sites)

    print "Traceroute part b PASS"

def dns_check(text):
    output = json.loads(text)
    if len(output) != 500:
        msg = ("Expected 500 dig commands (5 iterations for each of 100 " +
            "websites); got %u commands" % len(output))
        raise Exception(msg)

    error_msg_template = "%s not found in run %s"
    def check_key_exists(key_name, json_to_check):
        if key_name not in json_to_check:
            msg = error_msg_template % (key_name, json_to_check)
            raise Exception(msg)

    for dig_command in output:
        check_key_exists(utils.NAME_KEY, dig_command)
        check_key_exists(utils.SUCCESS_KEY, dig_command)
        if dig_command[utils.SUCCESS_KEY]:
            check_key_exists(utils.QUERIES_KEY, dig_command)
            all_queries = dig_command[utils.QUERIES_KEY]
            for query in all_queries:
                check_key_exists(utils.TIME_KEY, query)
                check_key_exists(utils.ANSWERS_KEY, query)
                for answer in query[utils.ANSWERS_KEY]:
                    check_key_exists(utils.QUERIED_NAME_KEY, answer)
                    check_key_exists(utils.TTL_KEY, answer)
                    check_key_exists(utils.TYPE_KEY, answer)
                    check_key_exists(utils.ANSWER_DATA_KEY, answer)

    print "DNS output a PASS"

def check_file(func, fname):
    try: 
        f = open(fname, 'r')
        text = f.read()
        f.close()
        func(text)
    except Exception as e:
        print e.message
    
def main():
    parser = argparse.ArgumentParser(description="CS168 Project 3 Tests")
    parser.add_argument("--rtt-part-a", dest="rtt_part_a", type=str, action="store")
    parser.add_argument("--rtt-part-b", dest="rtt_part_b", type=str, action="store")
    parser.add_argument("--tr-part-a", dest="tr_part_a", type=str, action="store")
    parser.add_argument("--tr-part-b", dest="tr_part_b", type=str, action="store")
    parser.add_argument("--dns", dest="dns", type=str, action="store")

    args = parser.parse_args()

    if (args.rtt_part_a):
        check_file(rtt_part_a_check, args.rtt_part_a)
    if (args.rtt_part_b):
        check_file(rtt_part_b_check, args.rtt_part_b)
    if (args.tr_part_a):
        check_file(tr_part_a_check, args.tr_part_a)
    if (args.tr_part_b):
        check_file(tr_part_b_check, args.tr_part_b)
    if (args.dns):
        check_file(dns_check, args.dns)

if __name__ == "__main__":
    main()
