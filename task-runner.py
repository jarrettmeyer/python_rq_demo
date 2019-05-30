#!/usr/bin/env python
from python_rq_demo import print_environment_variables
from python_rq_demo.tasks import rq_connection, rq_worker


def main():
    print_environment_variables()
    with rq_connection():
        worker = rq_worker()
        worker.work()


if __name__ == '__main__':
    main()
