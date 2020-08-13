import argparse
import redis
import csv

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Upload imdb data has hashes into redis')
	parser.add_argument('-H', '--host', default='localhost', help='redis host')
	parser.add_argument('-P', '--port', default=6379, help='redis port')
	parser.add_argument('-F', '--imdb-file-path', default='./title.basics.tsv', help='path to imdb file data')
	parser.add_argument('--delimiter', default='\t', help='csv delimiter')
	parser.add_argument('--batch', default=10000, help='batch size')
	parser.add_argument('--num-hashes', default=30000, help='number of hashes to create')
	parser.add_argument('-v', '--verbose', action='count', default=0, help='print more information about the test')
	args = parser.parse_args()

	r = redis.Redis(args.host, args.port)

	with open(args.imdb_file_path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=args.delimiter)
		fields = csv_reader.__next__()
		numHashes = 1
		pipe = r.pipeline(transaction=False)
		for line in csv_reader:
			d = {}
			for i in range(len(line)):
				d[fields[i]] = line[i]
			pipe.hmset(d['tconst'], d)
			if(args.verbose > 1):
				print('added hash to batch: %d' % numHashes)
			if numHashes % int(args.batch) == 0:
				if(args.verbose > 0):
					print('sent batch: %d' % numHashes)
				pipe.execute()
				pipe = r.pipeline(transaction=False)
			if args.num_hashes != 'inf' and numHashes == int(args.num_hashes):
				break
			numHashes += 1
		pipe.execute()
		print('done')
