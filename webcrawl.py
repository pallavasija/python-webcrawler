#!/usr/bin/python
import re
import urllib2
import urllib
import os
import sys
import time
try:
       os.remove('crawled.txt')
       os.remove('clean.txt')
except:
       pass
lnum=0
name=raw_input("Enter the domain name of the website: \n Example format: northeastern.edu, yext.com, yelp.com\n==>")
urlnam="http://"+name
with open("crawled.txt", "a") as outfile:
	#print "Writing "+urlnam+" to list of crawled pages..."
	outfile.write(urlnam+"\n")
	outfile.close()
def codecheck(url):							#checks the code returned from the URL, if 200, then proceeds the parsing
	#print "Checking URL status code..."
	#time.sleep(1)
	try:
		a=urllib.urlopen(url)
		return(a.getcode())
	except:
		return(0)
def webpage_download(url):						#fetches the webpage html data
	#print "Fetching HTML content...\n"
	#time.sleep(1)
	response = urllib2.urlopen(url)
	output=response.read()
	with open("webpage.txt", "w") as outfile:
		outfile.write(output)
def seekbody():								#repositions the cursor to start reading from page body to avoid link hrefs
	#print "Restricting crawl activity to body of the page...\n"
	#time.sleep(1)
	pattern1="(\<body|\<BODY)"
	regex1=re.compile(pattern1)
	bodystart = open("webpage.txt","r")
	try:
		for m in regex1.finditer(bodystart.read()):
		        startpos=m.start()
		bodystart.seek(startpos)
		with open("webpagebody.txt", "w") as rewrite:
	                rewrite.write(bodystart.read())
			rewrite.close()
		os.remove('webpage.txt')
	except:
		print "No body in this page. This could be a file"
	bodystart.close()
def relativepath():							#hunts the relative URLs in the webpage body
	#print "Looking for relative links...\n"
	#time.sleep(1)
	try:
		flinks = open("webpagebody.txt","r")
		relativepattern="href=\"(\/[^\/\s].*?)(?:\")"
		relativecompile=re.compile(relativepattern)
		for relativematch in relativecompile.finditer(flinks.read()):
		        with open("links.txt", "a") as output:
		                output.write(urlname+relativematch.group(1)+"\n")
		        output.close()
		flinks.seek(1)
		flinks.close()
	except:
		pass
def findlinks():							#hunts the absolute URLs in webpage body
	#print "Gathering all URLs on the webpage...\n"
	#time.sleep(1)
	flinks = open("webpagebody.txt","r")
	pattern=r"href=\"https?\:\/\/(.*?)(?:\")"
	regex=re.compile(pattern)
	for match in regex.finditer(flinks.read()):
	        with open("links.txt", "a") as outp:
	                outp.write("http://"+match.group(1)+"\n")
	        outp.close()
	flinks.close()
def domaincleanup():							#cleans up URLs to limit to domain name specified
	#print "Filtering for URLs with same domain...\n"
	#time.sleep(1)
	url1,url2=name.split(".")
	cleanpattern="http:\/\/.*\.?"+url1+"\."+url2+"\/?(?:\S*)"
	cleancomp=re.compile(cleanpattern)
	try:
		cleanf=open("links.txt","r")
		for cleanmatch in cleancomp.finditer(cleanf.read()):
			with open("clean.txt", "a") as out:
				out.write(cleanmatch.group(0)+"\n")
	    		out.close()
		cleanf.close()
	except:
		print "No URLs were found on this webpage"
def removeduplicate():							#removes duplicates from the list of URLs
	#print"Removing duplicate links found...\n"
	#time.sleep(1)
	content=open('clean.txt','r').readlines()
	content_set=set(content)
	uniqdata=open('new.txt','w')
	for line in content_set:
		uniqdata.write(line)
	os.rename('new.txt', 'clean.txt')
def remove():								#removes unnecessary files created in the process
	#print "Removing extra files..."
	#time.sleep(1)
	try:
		os.remove('webpagebody.txt')
		os.remove('links.txt')
	except:
		pass
def countl():								#keeps a count of number of URLs
	numlines = 0
	with open('clean.txt', 'r') as f:
    		for line in f:
        		numlines += 1
	return(numlines)

def disp():								#displays the file at the end	
	fp=open('clean.txt','r')
	for i,line in enumerate(fp,1):
		if  i<=25:
			print i,line
def parse(url):								#basically the main function, calls all other functions
	#print "\n==>"+url
	if codecheck(url)==200:
		#print "Crawling "+url
		webpage_download(url)
		seekbody()
		relativepath()
		findlinks()
		domaincleanup()
		removeduplicate()
		remove()
	else:
		print "Webpage "+url+" returned an error code"
def checkparsed(line1):							#checks if current URL is already parsed
	flag=0
	with open('crawled.txt','r') as fsearch:
		for lin in fsearch:
        		temp2=lin.split("\\")
                	line2=temp2[0]
                	if line1 in line2:
				flag=1
				return(flag)
			else:
				continue
	fsearch.close()
	outfile.close
def drill():								#drills deeper into URLs found
	count=0
	parse(urlnam)
	with open('clean.txt','r') as f:
                for line in f:
			if countl()>=25:
				disp()
                        	sys.exit()
			else:
				uname=line.split("\\")
				urlname=uname[0]
				print "Not reached received at least 25 yet. \n Now parsing==>"+urlname
				fl=checkparsed(urlname)
				#time.sleep(1)
				if fl==1:
					print "URL "+urlname+" has already been crawled. Skipping...\n"
				else:
					with open("crawled.txt", "a") as outfile:
                                       		#print "Writing "+urlname+" to crawled..."
                                       		outfile.write(urlname+"\n")
					try:
						parse(urlname)
					except:
						pass
drill()

