import argparse
import configparser
import os
from subprocess import run

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("path")
args, unknownargs = parser.parse_known_args()

config = configparser.ConfigParser()
config.read(os.path.expanduser("~") + "/.s3")

cmd_prefix = f"aws s3 --endpoint-url={config['default']['endpoint_url']} "
s3path = config["default"]["bucket"] + os.path.realpath(args.path)


def isdir(s3path):
    cmd = cmd_prefix + f"ls {s3path}"
    return run(cmd.split(), capture_output=True).stdout.strip().startswith(b"PRE")


def main():
    if args.action == "download":
        if isdir(s3path):
            cmd = cmd_prefix + f"sync {s3path} {args.path}"
        else:
            cmd = cmd_prefix + f"cp {s3path} {args.path}"
    elif args.action == "upload":
        if os.path.isdir(args.path):
            cmd = cmd_prefix + f"sync {args.path} {s3path}"
        else:
            cmd = cmd_prefix + f"cp {args.path} {s3path}"
    elif args.action == "rm":
        cmd = cmd_prefix + f"rm {s3path}" + (" --recursive" if isdir(s3path) else "")
    elif args.action == "ls":
        cmd = cmd_prefix + f"ls {s3path}"
        if args.path != "/" and isdir(s3path):
            cmd += "/"

    run(cmd.split() + unknownargs)
