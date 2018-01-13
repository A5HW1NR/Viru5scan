import os

def BoyerSearch(pattern, text):				#using the faster Boyer search algorithm
    m = len(pattern)
    n = len(text)
    if m > n: return -1						#return if sig pattern is larger than file data
    skip = []
    for k in range(256): skip.append(m)	
    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1	#setting pattern window
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:		#windows character checking
            j -= 1; i -= 1
        if j == -1: return 0					#if the pattern successfully matches return 0
        k += skip[ord(text[k])]
    return -1									#pattern is not present return -1


def main():
	virus_count = 0
	file_list = []
	viralert = 0
	root_path = raw_input("Enter the desired directory to scan.\n")		#input directory to scan
	sig_db = raw_input("Enter path to signature file database. \n")		#input the signature file for pattern matching
	for root,_,filenames in os.walk(root_path):							#directory traversal
		for filename in filenames:
			file_list.append(os.path.join(root,filename))
	with open(sig_db, "rb") as s:
		pattern = s.read().splitlines()									#read signature file line by line
	for x in file_list:
		viralert = 0
		f = open(x, "rb")												#open files to scan in binary
		try:
			data = f.read()												#read entire binary file for matching 
			for y in pattern:
				res = BoyerSearch(y, data)
				if res != -1:											#if return is not -1 then there is a match thus a virus
					print "Virus found in file %s with the following signature matching: %s" % (x, y)
					viralert = 1	
			if viralert == 1:
				virus_count +=1											#keep a count of all unique infected files
		finally:	
			f.close()
	print "Total number of viruses found: %d" % virus_count
	if virus_count == 0: 
		print "Congrats your computer is clean"	
			
if __name__ == "__main__": main()

raw_input("Press Enter to exit .. .. ..")								#user input to close executable
