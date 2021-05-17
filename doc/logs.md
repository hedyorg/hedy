# How to access query logs?


## Prerequisites

Ask someone in the team for the credentials of the `hedy-logs-viewer` IAM user. Add the following to the
`~/.aws/credentials` file:

```
[hedy-logs-viewer]
aws_access_key_id = AKIA**********
aws_secret_access_key = ***********
```

Install The Log File Navigator (`lnav`) using one of the methods described [here](http://lnav.org/downloads).
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

In lnav, you can use some limited form of SQL on columns we have defined. Example:

```
;SELECT * FROM request WHERE duration_ms > 1000
```
