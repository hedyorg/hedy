# How to access query logs?


## Prerequisites

Ask someone in the team for the credentials of the `hedy-logs-viewer` IAM user. Add the following to the
`~/.aws/credentials` file:

```
[hedy-logs-viewer]
aws_access_key_id = AKIA**********
aws_secret_access_key = ***********
```

Install RecordStream (`recs`) using one of the methods described [here](https://metacpan.org/pod/App::RecordStream).
`lnav` is not the *best* tool, but it's usable for now.

Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html).

## Usage

Run:

```
$ tools/view-logs <APP> <YYYY-MM-DD>

# Example:
$ tools/view-logs hedy-beta 2021-05-10
```

NOTE: Time stamps will be in UTC.

The `view-logs` tool will give you a RecordStream command line to paste into shell.

