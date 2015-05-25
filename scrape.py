from scrapeComments import scrapeComments
import argparse
import os
import json
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

def saveComments(format, comments):
    print format
    for i, comment in enumerate(comments):
        if format == 'json' or format is None:
            fileName = 'comments-{0}.json'.format(i)
            outFile = open(fileName,'w')
            json.dump(comment, outFile, indent=4)
            outFile.close()
        elif format == 'csv':
            keys = comment[0].keys()
            fileName = 'comments-{0}.csv'.format(i)
            with open(fileName, 'w') as f:
                w = csv.DictWriter(f, keys)
                w.writeheader()
                w.writerows(comment)


fileOrUrl = args.source
fileName, fileExtension = os.path.splitext(fileOrUrl)
comments = []

if fileExtension == '.txt':
    lines = [line.rstrip('\n') for line in open(fileOrUrl)]
    for line in lines:
        output = scrapeComments(line)
        comments.append(output)
else:
    output = scrapeComments(fileName)
    comments.append(output)

saveComments(args.output, comments)

