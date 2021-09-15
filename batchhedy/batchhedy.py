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

class RunHedy(BaseModel):
    """ For each file in `filename`, do a timed transpilling from Hedy code
    to Python code.

    Arguments:
        output: Optional[Path]
            If present, the resulting python code will be save in the
            direction `output`. The name of the python files will be the same
            than the Hedy files, with the extension changed from .hedy to .py.
            If the path doesn't exist, it will be created.
    """

    output: Optional[Path]
    jobs: ClassVar[None]
    checkdata: ClassVar[None]

    def run(self):
        """ Execute runhedy with the validated parameters """

        if self.output:
            self.output.mkdir(parents=True, exist_ok=True)

        #skip empty programs
        jobs = [j for j in self.jobs if not is_empty(j.code)]

        number_of_error_programs = 0

        for job in jobs:

            job.transpile()

            if job.error_msg != '':
                number_of_error_programs += 1

            if self.output is not None:
                # Write python file
                with open(self.output / (job.filename.stem + ".py"), "w") as f:
                    f.write(job.pycode)

            # Run info
            infos = [
                f"{job.transpile_time:13.3f}s",
                f"{job.error_msg[:10]:10}"]

            if self.checkdata is not None:
                # Compare with previous run
                chkjob = self.checkdata[job.filename]
                chktime = float(chkjob["transpile time"])
                diff = 0 if chktime == 0 else 100 * job.transpile_time / chktime
                infos.append(f"{diff:1.0f}%")

                if (job.error is True) and (chkjob["error"] == "False"):
                    job.error_change = f"{'no error->error':15}"
                    infos.append(job.error_change)
                elif (job.error is True) and (chkjob["error"] == "True"):
                    # only check the first line, args position change
                    if (job.error_msg.splitlines()[0] !=
                            chkjob["error message"].splitlines()[0]):
                        job.error_change = f"{'error diff.':15}"
                        infos.append(job.error_change)
                elif (job.error is False) and (chkjob["error"] == "True"):
                    job.error_change = f"{'error->no error':15}"
                    infos.append(job.error_change)
                elif job.py_loc != int(chkjob["py_loc"]):
                    job.error_change = f"{'loc different':15}"
                    infos.append(job.error_change)


        if report is not None:
            _save_report(self.jobs)

        # print run informations
        runtimes = [r.transpile_time for r in self.jobs]
        maxvalue = max(runtimes)
        minvalue = min(runtimes)
        maxfilename = self.jobs[runtimes.index(maxvalue)].filename

        if self.checkdata is None:
            # Simple run
            print(f"Total transpile time: {sum(runtimes):10f}s ")
            print(f"Average transpile time: {sum(runtimes)/len(runtimes):10f}s ")
        else:
            # Compare with previous data
            previous_total_time = sum(float(
                self.checkdata[job.filename]["transpile time"]
                ) for job in self.jobs)
            diff = 100 * sum(runtimes) / previous_total_time
            print(f"Total transpile time: {sum(runtimes):10f}s ({diff:6.2f}%)")

        print(f"Max transpile time:   {maxvalue:10f}s (file: {maxfilename})")
        print(f"Min transpile time:   {minvalue:10f}s")
        print(f"Number of error files:  {number_of_error_programs} ({100*number_of_error_programs/len(jobs):3f}) ")


    @lazy
    def jobs(self):
        """ The list of jobs to be run """
        # Create object list
        jobs = [TranspileJob(f) for f in filenames_list]

        # Remove files with invalid level
        invalidjob = [j for j in jobs if j.level > hedy.HEDY_MAX_LEVEL]
        if len(invalidjob) > 0:
            print(f"WARNING: There are {len(invalidjob)} files with"
                  f" invalid Hedy level (> {hedy.HEDY_MAX_LEVEL})")
            jobs = [j for j in jobs if j.level <= hedy.HEDY_MAX_LEVEL]

        return jobs

    @lazy
    def checkdata(self):
        """ Data of a previous run. Return None is self.check is not set."""
        if check is None:
            return None

        comparedata = {}
        with open(check, newline="") as csvfile:
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
        src_loc: Number of lines of code in the Hedy code
        src_loc_empty: Number of empty line of code in the Hedy code
        src_tokens: Number of tokens in the Hedy code
        py_loc: Number of lines of code in the Python code
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

        self.filename = filename
        self.error = False
        self.error_msg = ""
        self.transpile_time = 0.0
        self.error_change = None

        # Get the level and code position
        try:
            with open(filename) as f:
                all_lines = f.readlines()
                # remove header info
                firstline = all_lines[0]
                self.code = '\n'.join(all_lines[3:])

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
        """ (Re)run the transpiling """
        try:
            del self.pycode   # force rerun of the transpiling
        except AttributeError:
            pass
        return self.pycode

    @lazy
    def code(self) -> str:
        """ The hedy code"""
        code = self.code

        # Make sure that the last line is "\n".
        if len(code) > 0:
            return code if code[-1] == "\n" else code + "\n"
        else:
            return ""

    @lazy
    def pycode(self) -> str:
        """ The transpiled code """
        if self.error:
            return ""
        try:
            pycode = ""
            t1 = perf_counter()
            pycode = hedy.transpile(self.code, self.level).code
        except hedy.HedyException as e:
            self.error = True
            self.error_msg = str(e)
            print(self.error_msg)
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

        #TODO: Catch any error ?
        finally:
            t2 = perf_counter()

        self.transpile_time = t2 - t1
        return pycode

    @lazy
    def src_loc(self) -> int:
        """ Lines of code in the Hedy file """
        return len(self.code.split("\n"))

    @lazy
    def src_loc_empty(self) -> int:
        """ Empty Line of code in the Hedy file """
        return len([line for line in self.code.split("\n") if len(line) == 0])



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

def _save_report(jobs):
        with open(report, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "filename",
                "level",
                "code",
                "transpile time",
                "error",
                "error message",
                "error_change"
            ])

            writer.writeheader()
            for job in jobs:
                writer.writerow({
                    "filename": job.filename,
                    "level": job.level,
                    "code": job.code,
                    "transpile time": job.transpile_time,
                    "error": job.error,
                    "error message": job.error_msg,
                    "error_change": job.error_change,
                })

filenames_list = glob.glob('../../input_one/*.hedy')
report = 'output_report_one.csv'
check = 'output_report_one.csv'

if __name__ == '__main__':
    os.chdir(path.dirname(path.abspath(__file__)))
    RunHedy().run()
