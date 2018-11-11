#!/usr/bin/env python

import sys

# Lookup tables for column names for state, occupation, and case status
# for different years

lookup_st = ['WORKSITE_STATE','LCA_CASE_WORKLOC1_STATE','STATE_1']
lookup_oc = ['SOC_NAME','LCA_CASE_SOC_NAME','OCCUPATIONAL_TITLE']
lookup_status = ['CASE_STATUS','STATUS','APPROVAL_STATUS']

# This function is to find the top 10 categories for the field of interest
# in terms of the number of certified h1b petitions.
def top10_certified(infile, field):

# infile - input file path and name
# field - field name for applying the aggregation and couting analysisself.
#         Current options include 'state' and 'occupation.'

    total = 0  # Record total number of lines
    dic = {}   # Initiate a dictionary for counting the numbers

    # Open the input file, read line by line
    with open(infile,'rb') as f:
        for line in f:
            total += 1

            # Split line by delimiter
            line = line.strip()
            words = line.split(';')

            # Get the index of fields of interest
            if total == 1:
                # First find the right column names
                for item in lookup_status:
                    if item in words:
                        # Then determine the index in the list
                        status_index = words.index(item)
                        break

                if field == 'state':
                    for item in lookup_st:
                        if item in words:
                            field_index = words.index(item)
                            break
                elif field == 'occupation':
                    for item in lookup_oc:
                        if item in words:
                            field_index = words.index(item)
                            break
                else:
                    print 'Please use state or occupation to specify the field'
                    sys.exit(os.EX_SOFTWARE)

            # Use the index to access the value in each line starting from Line 2
            if total >= 2:
                if words[status_index] == 'CERTIFIED':
                    key = words[field_index].replace('"','')

                    if key in dic:
                        dic[key] += 1
                    else:
                        dic[key] = 1

        # Find the largest 10 numbers. Sort the dictionary by values first,
        # then by keys alphabetically. Pick the top 10 items.
        dic_top10 = sorted(dic.items(), key=lambda x: (-x[1],x[0]))[:10]

        # Calculate the sum of the top 10 values
        total_tomp10 = 0
        for i in xrange(len(dic_top10)):
            l = list(dic_top10[i])
            total_tomp10 += l[1]

        # Calculate the percentages of the 10 categories
        for i in xrange(len(dic_top10)):
            l = list(dic_top10[i])
            p = '{:.1%}'.format(float(l[1])/float(total_tomp10))
            l.append(p)
            dic_top10[i] = l

        # Return the ranked top 10 records
        return dic_top10

# This function is to output the ranked records to text files.
def write_output(top10, outfile, colname):
# top10 - python list of list with the top 10 ranked categories for the
#         field of interest in terms of certified h1b visasself.
# outfile - output file path and name
# colname - customize the column name for the field of interest in the output file

    with open(outfile, 'w') as f:
        header = 'TOP_'+colname+';NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'
        f.write(header)
        for i in xrange(len(top10)):
            item = top10[i]
            f.write("%s;%d;%s\n" % (item[0],item[1],item[2]))



def main():

    # Read input and output file names from system input
    INFILE = sys.argv[1]
    OUTFILE1 = sys.argv[2]
    OUTFILE2 = sys.argv[3]

    # Rank the top 10 states and occupations that had the top 10 number of
    # certified h1b visas
    st_top10 = top10_certified(INFILE, 'state')
    occ_top10 = top10_certified(INFILE, 'occupation')

    # Write results in output text files with the desired format
    write_output(st_top10, OUTFILE2, 'STATES')
    write_output(occ_top10, OUTFILE1, 'OCCUPATIONS')

if __name__ == '__main__':
	main()
