# This file is used to configure gunicorn, used for production workloads.

# Restart after this many requests, to limit memory usage
max_requests = 10000

prod_name = "hedy"

def worker_exit(server, worker):
    # When the worker is being exited (perhaps because of a timeout),
    # give the query_log handler a chance to flush to disk.
    from website import querylog, user_activity
    import app
    querylog.emergency_shutdown()
    app.parse_logger.emergency_shutdown()
    user_activity.logger.emergency_shutdown()
