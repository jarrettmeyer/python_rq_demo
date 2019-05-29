#!/usr/bin/env python

import os
from python_rq_demo import app, print_environment_variables
from python_rq_demo.config import DEBUG


def main():
    print_environment_variables()
    app.run('0.0.0.0', 5000, DEBUG)


if __name__ == '__main__':
    main()
