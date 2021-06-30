#!/bin/env python3
""" Usage: batchhedy.py [--help] [--level <level>]... [--output <output>]
         [--report <csvfile>] [--check <checkfile>] <filename>...

Batch transpiling of Hedy files with option to check the results and
benchmark it. If <output> is set the resulting python files
will be written in that directory if not the result will be print.

-h, --help                           Show this help
-l <level>, --level <level>          Only do those levels
-o <output>, --output <output>       Directory were to output python files
-r <csvfile, --report <csvfile>      Write report info in <csvfile>
-c <checkfile>, --check <checkfile>  Compare with a previous report
"""

# Python standard lib
from pathlib import Path
from time import perf_counter
from typing import Optional, List, Tuple, ClassVar
import csv

# Hedy lib
import hedy

# External lib
from docopt import docopt
from pydantic import BaseModel, ValidationError, FilePath
from lark.exceptions import GrammarError, UnexpectedEOF
from lazy.lazy import lazy


class RunHedy(BaseModel):
    """ For each file in `filename`, do a timed transpilling from Hedy code
    to Python code.

    After the object creating, use RunHedy.run(self) to do the transpiling.

    Arguments:
        filename: List[FilePath]
            A list of .hedy file to transpile/test. The first line need to
            be the Hedy level in the format "# level X" or "# level = X" (case
            insensitive) where 'X' is a valid level.
        report: Optional[Path]
            If present and a valid path, will save information of the
            transpilings (timing, error, line of code,...) in csv format.
        check: Optional[FilePath]
            If present and a valid csv file from a previous run, will
            compare the results from this run with the one from the file and
            report any change in error and the time difference.
        level: Optional[List[int]]
            If present, only file with Hedy level in `level` will be
            transpiled/tested.
        output: Optional[Path]
            If present, the resulting python code will be save in the
            direction `output`. The name of the python files will be the same
            than the Hedy files, with the extension changed from .hedy to .py.
            If the path doesn't exist, it will be created.
    """
    filename: List[FilePath]
    report: Optional[Path]
    check: Optional[FilePath]
    level: Optional[List[int]]
    output: Optional[Path]
    help: Optional[bool]       # no used, but needed for CLI interface

    jobs: ClassVar[None]
    checkdata: ClassVar[None]

    def run(self):
        """ Execute runhedy with the validated parameters """

        if self.output:
            self.output.mkdir(parents=True, exist_ok=True)

        # for display
        maxfilelength = max(len(str(f.stem)) for f in self.filename)

        # For table display
        sep = "  "
        header = sep.join([
            f"{'filename':{maxfilelength}}",
            f"{'lev.':>3}",
            f"{'loc':>4}",
            f"{'0loc':>4}",
            f"{'tokens':>6}",
            f"{'time':>14}",
            f"{'time/tokens':>14}",
            f"{'pyloc':>5}",
            f"{'error msg':>10}",
        ])

        if self.checkdata is not None:
            header = sep.join([
                header,
                f"{'time diff.':>9}",
                f"{'error msg':>10}",
            ])

        # This will print any errors or warning before the header
        jobs = self.jobs

        print(header)

        for job in jobs:
            # Basic info on the file
            print(sep.join([f"{str(job.filename.stem):{maxfilelength}}",
                            f"{job.level:3}",
                            f"{job.src_loc:4}",
                            f"{job.src_loc_empty:4}",
                            f"{job.src_tokens:6}", ]), end=sep)

            job.transpile()

            if self.output is not None:
                # Write python file
                with open(self.output / (job.filename.stem + ".py"), "w") as f:
                    f.write(job.pycode)

            # Run info
            infos = [
                f"{job.transpile_time:13.8f}s",
                (f"{'-':>14}" if job.src_tokens == 0 else
                    f"{job.transpile_time/job.src_tokens:13.8f}s"),
                f"{job.py_loc:5}",
                f"{job.error_msg[:10]:10}"]

            if self.checkdata is not None:
                # Compare with previous run
                chkjob = self.checkdata[job.filename.stem]
                chktime = float(chkjob["transpile time"])
                diff = 100 * job.transpile_time / chktime
                infos.append(f"{diff:9.2f}%")

                if (job.error is True) and (chkjob["error"] == "False"):
                    infos.append(f"{'no error->error':15}")
                elif (job.error is True) and (chkjob["error"] == "True"):
                    # only check the first line, args position change
                    if (job.error_msg.splitlines()[0] !=
                            chkjob["error message"].splitlines()[0]):
                        infos.append(f"{'error diff.':15}")
                elif (job.error is False) and (chkjob["error"] == "True"):
                    infos.append(f"{'error->no error':15}")
                elif job.py_loc != int(chkjob["py_loc"]):
                    infos.append(f"{'loc different':15}")

            print(sep.join(infos))

        # Reprint header for easy read
        print(header)

        if self.report is not None:
            self._save_report()

        # print run informations
        runtimes = [r.transpile_time for r in self.jobs]
        maxvalue = max(runtimes)
        minvalue = min(runtimes)
        maxfilename = self.jobs[runtimes.index(maxvalue)].filename

        if self.checkdata is None:
            # Simple run
            print(f"Total transpile time: {sum(runtimes):10f}s ")
        else:
            # Compare with previous data
            previoustotaltime = sum(float(
                self.checkdata[job.filename.stem]["transpile time"]
                ) for job in self.jobs)
            diff = 100 * sum(runtimes) / previoustotaltime
            print(f"Total transpile time: {sum(runtimes):10f}s ({diff:6.2f}%)")

        print(f"Max transpile time:   {maxvalue:10f}s (file: {maxfilename})")
        print(f"Min transpile time:   {minvalue:10f}s")

    @lazy
    def jobs(self):
        """ The list of jobs to be run """
        # Create object list
        jobs = [TranspileJob(f) for f in self.filename]

        if self.level and len(self.level) > 0:
            jobs = [r for r in jobs if r.level in self.level]

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
        if self.check is None:
            return None

        comparedata = {}
        with open(self.check, newline="") as csvfile:
            reader = csv.reader(csvfile)
            fields = None
            for row in reader:
                if fields is None:
                    fields = row
                else:
                    comparedata[row[0]] = ({k: v for k, v in zip(fields, row)})
        return comparedata

    def _save_report(self, file=None):
        with open(file or self.report, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "filename",
                "level",
                "transpile time",
                "error",
                "error message",
                "src_loc",
                "src_loc_empty",
                "src_tokens",
                "py_loc",
            ])

            writer.writeheader()
            for job in self.jobs:
                writer.writerow({
                    "filename": str(job.filename.stem),
                    "level": self.level,
                    "transpile time": job.transpile_time,
                    "error": job.error,
                    "error message": job.error_msg,
                    "src_loc": job.src_loc,
                    "src_loc_empty": job.src_loc_empty,
                    "src_tokens": job.src_tokens,
                    "py_loc": job.py_loc,
                })


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

        # Get the level and code position
        try:
            with open(filename) as f:
                firstline = f.readline()
                self.codestart = f.tell()

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
        with open(self.filename) as f:
            f.seek(self.codestart)
            code = f.read()
        code = "\n".join(line for line in code.splitlines() if len(line) > 0)
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
            pycode = hedy.transpile(self.code, self.level)
        except hedy.HedyException as e:
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

    @lazy
    def src_tokens(self) -> int:
        """ Tokens in the Hedy file """
        return (len(self.code.split()))

    @lazy
    def py_loc(self) -> int:
        """ Lines of code in the Python file """
        return len(self.pycode.split("\n"))


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


if __name__ == "__main__":
    try:
        RunHedy(**{
            # Remove unwanted characters from the parsed args
            "".join([k for k in key if k not in "-<>"]): value
            for key, value in docopt(__doc__).items()
        }).run()
        exit(0)
    except ValidationError as e:
        print(e)
        exit(1)
