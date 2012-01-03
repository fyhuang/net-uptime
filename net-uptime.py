import datetime
import time

import ping

# User configurable settings
LOG_FILENAME = "uptime_log.txt"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

ROUTER_IP = "192.168.1.1"
RECORD_INTERVAL_SECS = 30

PING_SITES = [
        "google.com",
        "yahoo.com",
        ]

# End settings

pings = [ping.Ping(hn, 1000, 55, print_stats=False) for hn in PING_SITES]
rp = ping.Ping(ROUTER_IP, 55, print_stats=False)

with open(LOG_FILENAME, "w") as lf:
    while True:
        successes = [False for p in PING_SITES]
        for i,p in enumerate(pings):
            p.run(1)
            if p.send_count == p.receive_count:
                successes[i] = True

        # if all false
        internet = True
        router = True
        if all((not a for a in successes)):
            internet = False

        rp.run(1)
        if rp.send_count != rp.receive_count:
            router = False

        # log this run
        dt = datetime.datetime.now()
        lf.write(dt.strftime(DATETIME_FORMAT))
        lf.write("/")
        lf.write(str(internet))
        lf.write("/")
        lf.write(str(router))
        lf.write("\n")

        time.sleep(RECORD_INTERVAL_SECS)
