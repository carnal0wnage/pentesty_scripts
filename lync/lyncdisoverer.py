#!/usr/bin/python

import sys
import socket
import json, urllib2
from urllib2 import urlopen
import dns.resolver

print "\n\033[0;32m======================================================================"
print "\033[0;32mLync Discoverer and Brute-forcer helper 2016 - Written by @benpturner" 
print "\033[0;32m======================================================================"


def decoderesponse(response):
	string = response.read().decode('utf-8')
	try:
		json_obj = json.loads(string)
		json_obj = json.loads(string)
		userlink = json_obj['_links']['user']['href']
		lyncntlm=userlink.split(domainsuffix,1)[0]
		return lyncntlm
	except:
		pass
		print "\nFailed to decode JSON (Might need to look at this manually):\n"+string

domain = raw_input("\033[0;31mProvide an example target email address [test@example.com]: \033[0m")
domainsuffix=domain.split("@",1)[1]

print "\nLooking for Lync dicovery DNS records: "+domainsuffix+"\n"

lyncdiscoverinternal = ''
lyncdiscover = ''
my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = ['8.8.8.8']

try:
	lyncdiscoverinternalfull = my_resolver.query("lyncdiscoverinternal."+domainsuffix)
	lyncdiscoverinternal = lyncdiscoverinternalfull.response
	print lyncdiscoverinternal
	print "\033[0;32m[+] Successfully resolved DNS (lyncdiscoverinternal): "+lyncdiscoverinternal+"\033[0m" 
except:
	print "\033[0;31m[-] Could not resolve DNS: "+"lyncdiscoverinternal."+domainsuffix+"\033[0m"

try:
	lyncdiscoverfull = my_resolver.query("lyncdiscover."+domainsuffix)
	lyncdiscover = lyncdiscoverfull.response
	print "\033[0;32m[+] Successfully resolved DNS (lyncdiscover): "+lyncdiscover+"\033[0m\n" 
except:
	print "\033[0;31m[-] Could not resolve DNS: "+"lyncdiscover."+domainsuffix+"\033[0m\n"

if lyncdiscoverinternal:
	try:
		response = urlopen("http://lyncdiscoverinternal."+domainsuffix, timeout=2)
	except:
		print "Trying HTTPS"
	try:
		response = urlopen("https://lyncdiscoverinternal."+domainsuffix, timeout=2)
	except:
		print "\033[0;31m[-] Failed to find NTLM webpage for lyncdiscoverinternal\033[0m"
	
	lyncntlm=decoderesponse(response)
	if lyncntlm:
		print "\033[0;32m[+] Found NTLM webpage for lyncdiscoverinternal\033[0m"
		print "\033[0;32m[+] NTLM URL for brute-forcing is: "+lyncntlm+domainsuffix+"/WebTicket/WebTicketService.svc\033[0m"
		print "\n[+] Now use: \n\033[0;32mntlm-botherer.py -U users.txt -p Password1 -d <DOMAIN> "+lyncntlm+domainsuffix+"/WebTicket/WebTicketService.svc\033[0m"

if lyncdiscover:
	try:
		response = urlopen("http://lyncdiscover."+domainsuffix, timeout=2)
	except:
		pass
	try:
		response = urlopen("https://lyncdiscover."+domainsuffix, timeout=2)
	except:
		print "\033[0;31m[-] Failed to find NTLM webpage for lyncdiscover\033[0m"
	lyncntlm=decoderesponse(response)
	if lyncntlm:
		print "\033[0;32m[+] Found NTLM webpage for lyncdiscover\033[0m"
		print "\033[0;32m[+] NTLM URL for brute-forcing is: "+lyncntlm+domainsuffix+"/WebTicket/WebTicketService.svc\033[0m"
		print "\n[+] Now use: \n\033[0;32mntlm-botherer.py -U users.txt -p Password1 -d <DOMAIN> "+lyncntlm+domainsuffix+"/WebTicket/WebTicketService.svc\033[0m"

