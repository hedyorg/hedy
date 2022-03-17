from pathlib import Path
from time import perf_counter
from typing import Optional, List, Tuple, ClassVar
import csv
import os
from os import path
import glob

# Hedy lib
import hedy

# External lib
from pydantic import BaseModel, FilePath
from lark.exceptions import GrammarError, UnexpectedEOF
from lazy.lazy import lazy

def run(filenames, report, top, check = None, ):
        jobs = create_jobs(filenames)
        #skip empty programs
        jobs = [j for j in jobs if not is_empty(j.code)]

        number_of_error_programs = 0

        for job in jobs:
            job.transpile()
            if job.error_msg != '':
                number_of_error_programs += 1

            checkdata = create_checkdata(check)
            if checkdata is not None:
                # Compare with previous run
                try:
                    chkjob = checkdata[job.filename]
                    chktime = float(chkjob["transpile time"])
                    diff = 0 if chktime == 0 else 100 * job.transpile_time / chktime

                    if (job.error is True) and (chkjob["error"] == "False"):
                        job.error_change = f"{'no error->error':15}"
                    elif (job.error is True) and (chkjob["error"] == "True"):
                        # only check the first line, args position change
                        if (job.error_msg.splitlines()[0] !=
                                chkjob["error message"].splitlines()[0]):
                            job.error_change = f"{'error diff.':15}"
                    elif (job.error is False) and (chkjob["error"] == "True"):
                        job.error_change = f"{'error->no error':15}"
                except Exception as e:
                    print('checking failed')

        if report is not None:
            _save_report(jobs, report)

        # print run informations
        runtimes_and_files = [(r.filename, r.transpile_time) for r in jobs]
        ordered_runtimes = sorted(runtimes_and_files, key=lambda x: x[1], reverse = True)
        slowest_top_x = [x[0] for x in ordered_runtimes[:top]]

        runtimes = [x[1] for x in runtimes_and_files]

        maxvalue = max(runtimes)
        minvalue = min(runtimes)
        name_of_slowest_file = jobs[runtimes.index(maxvalue)].filename

        if checkdata is None:
            # Simple run
            print(f"Total transpile time: {sum(runtimes):10f}s ")
            print(f"Average transpile time: {sum(runtimes)/len(runtimes):10f}s ")
        else:
            # Compare with previous data
            previous_total_time = sum(float(
                checkdata[job.filename]["transpile time"]
                ) for job in jobs)
            diff = 100 * sum(runtimes) / previous_total_time
            print(f"Total transpile time: {sum(runtimes):10f}s ({diff:6.2f}%)")

        print(f"Number of files:  {len(jobs)}")
        print(f"Max transpile time:   {maxvalue:10f}s (files: {name_of_slowest_file})")
        print(f"Slowest files: {slowest_top_x})")
        print(f"Min transpile time:   {minvalue:10f}s")
        print(f"Number of error files:  {number_of_error_programs} ({100*number_of_error_programs/len(jobs):3f}) ")

def create_jobs(filenames):
    """ The list of jobs to be run """
    # Create object list
    jobs = [TranspileJob(f) for f in filenames]

    # Remove files with invalid level
    invalidjob = [j for j in jobs if j.level > hedy.HEDY_MAX_LEVEL]
    if len(invalidjob) > 0:
        print(f"WARNING: There are {len(invalidjob)} files with"
              f" invalid Hedy level (> {hedy.HEDY_MAX_LEVEL})")
        jobs = [j for j in jobs if j.level <= hedy.HEDY_MAX_LEVEL]

    return jobs

def create_checkdata(check):
    """ Data of a previous run. Return None is self.check is not set."""
    if check is None:
        return None

    comparedata = {}
    with open(check, newline="", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        fields = None
        for row in reader:
            if fields is None:
                fields = row
            else:
                comparedata[row[0]] = ({k: v for k, v in zip(fields, row)})
    return comparedata



class TranspileJob:
    """ Load an Hedy file and do a timed transpiling.

    Attributes:
        code: The Hedy code
        pycode: The Python code
        src_tokens: Number of tokens in the Hedy code
        error: True if there was an error during transpiling
        error_msg: The error message
        transpile_time: The time took for transpiling in seconds
        error_change: if the new error is different

    Functions:
        transpile: (re)run the transpiling
    """

    def __init__(self, filename: FilePath):
        """ Create a new transpiling job of the file `filename`.

        The transpiling job is not run immediately, only when a call
        to transpile() or pycode is made.
        """

        self.filename = os.path.basename(filename)
        self.error = False
        self.error_msg = ""
        self.transpile_time = 0.0
        self.error_change = None

        # Get the level and code position
        try:
            with open(filename, encoding='utf-8') as f:
                all_lines = f.readlines()
                # remove header info
                firstline = all_lines[0]
                self.date = all_lines[1]
                non_empty_lines = [a for a in all_lines[4:] if a != '']
                self.code = ''.join(non_empty_lines) + '\n'

            self.level = 0

            if firstline.find("=") > -1:
                self.level = int(firstline.split("=")[-1])
            else:
                self.level = int(firstline.split()[-1])

        except FileNotFoundError:
            self.error = True
            self.error_msg = "File not found."

        except ValueError as e:
            self.error = True
            self.error_msg = str(e)


    def transpile(self) -> str:
        if self.error:
            return ""
        try:
            pycode = ""
            t1 = perf_counter()
            pycode = hedy.transpile(self.code, self.level).code
        except hedy.exceptions.HedyException as e:
            self.error = True
            self.error_msg = str(e)
        except UnexpectedEOF as e:
            self.error = True
            self.error_msg = str(e)
        except GrammarError as e:
            self.error = True
            self.error_msg = str(e)
        except Exception as e:
            # Catch all
            self.error = True
            self.error_msg = str(e)

        # TODO: Catch any error ?
        finally:
            t2 = perf_counter()

        self.transpile_time = t2 - t1
        return pycode

    @lazy
    def code(self) -> str:
        """ The hedy code"""
        code = self.code

        # Make sure that the last line is "\n".
        if len(code) > 0:
            return code if code[-1] == "\n" else code + "\n"
        else:
            return ""





def extract_level_from_code(code: str) -> Tuple[int, str]:
    """ Return a (level, code) tuple of the level and the code without the
    level line. Return None for the level if it not found. """
    newline = code.find("\n")
    firstline = code[0:newline].strip().lower()
    if firstline[0] == "#":   # expecting level X or level = X
        idx = firstline.find("level")
        if idx > -1:  # string found
            try:
                if firstline.find("=") > -1:
                    level = int(firstline.split("=")[-1])
                else:
                    level = int(firstline[idx+5:])
                return level, code[newline+1:]
            except ValueError:
                pass
    return None, code

def is_empty(program):
    all_lines = program.split('\n')
    return all(line == '' for line in all_lines)

def _save_report(jobs, report):
        with open(report, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "filename",
                "date",
                "level",
                "code",
                "transpile time",
                "error",
                "error message",
                "error_change"
            ])


            writer.writeheader()
            for job in jobs:
                code = job.code.replace("\\n", "")
                writer.writerow({
                    "filename": job.filename,
                    "date": job.date,
                    "level": job.level,
                    "code": f'{code}',
                    "transpile time": job.transpile_time,
                    "error": job.error,
                    "error message": job.error_msg,
                    "error_change": job.error_change,
                })

os.chdir(path.dirname(path.abspath(__file__)))
filenames_list = glob.glob('../../input_small/*.hedy')

#report determines if we are generating a fresh report
#check determines if we are comparing against an existing report

if __name__ == '__main__':
    if len(filenames_list) == 0:
        print("no files found!")
    else:
        run(filenames=filenames_list, check = 'output_report_small.csv', report = 'output_report_small.csv', top=10)
