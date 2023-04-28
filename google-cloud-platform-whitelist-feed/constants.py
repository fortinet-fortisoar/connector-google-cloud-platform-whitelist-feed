""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """


class Method:
    GET = "GET"
    POST = "POST"


FILE1 = "IP ranges that Google makes available to users on the internet"
FILE2 = "Global and regional external IP address ranges for customer's Google Cloud resources"


FILE_MAPPING = {
    FILE1: "goog.json",
    FILE2: "cloud.json",
}
