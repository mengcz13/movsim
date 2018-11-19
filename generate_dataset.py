import os
import sys
import subprocess
import logging
import shlex
from multiprocessing import Pool
from pathlib import Path
from argparse import ArgumentParser

COMMAND_PATTERN = '/usr/bin/java -jar /home/mengcz/movsim/core/target/MovsimCore-1.7.0-SNAPSHOT-jar-with-dependencies.jar -o {} -f {}'

def run_comm_log(comm, logfilename):
    logging.info('Running {}, writting log to {}'.format(comm, logfilename))
    args = shlex.split(comm)
    print(args)
    with open(logfilename, 'w') as f:
        p = subprocess.Popen(args, stdout=f, stderr=f)
        p.wait()

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser()
    parser.add_argument('prjpath', help='path to the xprj file')
    parser.add_argument('sample_num', type=int, help='number of samples to generate')
    parser.add_argument('output_path', help='path folder for output')
    parser.add_argument('--worker_num', type=int, default=1, help='number of workers')
    args = parser.parse_args()

    prjpath = args.prjpath
    sample_num = args.sample_num
    worker_num = args.worker_num
    output_path = args.output_path
    logging.info('prjpath: {}, sample_num: {}, worker_num: {}'.format(prjpath, sample_num, worker_num))
    logging.info('Writting data to {}'.format(output_path))

    command_logs = []
    for t in range(sample_num):
        outputdir = Path(output_path) / str(t)
        if not outputdir.exists():
            outputdir.mkdir(parents=True)
        command = COMMAND_PATTERN.format(outputdir, prjpath)
        logpath = Path(output_path) / 'run_{}.log'.format(t)
        command_logs.append((command, logpath))

    p = Pool(worker_num)
    for command, logpath in command_logs:
        p.apply_async(run_comm_log, args=(command, logpath))
    p.close()
    p.join()


if __name__ == '__main__':
    main()
