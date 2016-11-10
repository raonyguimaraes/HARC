import random

infile = "chrom22_50x_ordered_wh_random.dna"
outfile = "temp2.dna"
readlen = 100
no_reads = 17509271
matchlen = 80
maxmatch = 20

print "Reading file"
f = open(infile,'r')
lines = [f.readline().rstrip('\n') for i in range(no_reads)]
f.close()

print "Constructing dictionary"
d = {}
for i in range(no_reads):
	if lines[i][0:matchlen] in d:
		d[lines[i][0:matchlen]].add(i)
	else:
		d[lines[i][0:matchlen]] = set([i])

print "Ordering reads and writing to file"
remainingreads = set([i for i in range(no_reads)])
current = 0
fout = open(outfile,'w')
while True:
	flag = 0
	if len(remainingreads)%1000000 == 0:
		print str(len(remainingreads)//1000000)+'M reads remain'
	fout.write(lines[current]+'\n')
	d[lines[current][0:matchlen]].remove(current)
	remainingreads.remove(current)
	if(len(remainingreads)==0):
		break
	if len(d[lines[current][0:matchlen]]) == 0:
		del d[lines[current][0:matchlen]]
	else:
		for i in d[lines[current][0:matchlen]]:
			if lines[current][matchlen:] == lines[i][matchlen:]:
				current = i
				flag = 1
				break
	if flag == 1:
		continue
	for j in range(1,maxmatch):
		if lines[current][j:j+matchlen] in d:
			for i in d[lines[current][j:j+matchlen]]:
				if lines[current][j+matchlen:] == lines[i][matchlen:readlen-j]:
					current = i
					flag = 1
					break
			if flag == 1:
					break
	if flag == 1:
		continue
#	current = random.sample(remainingreads,1)[0]
	current = remainingreads.pop()
	remainingreads.add(current)

print "Done"
fout.close()
	
		

