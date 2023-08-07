import argparse
import configparser
from pathlib import Path
from subprocess import run

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("path", type=Path)
args, unknownargs = parser.parse_known_args()

config = configparser.ConfigParser()
config.read(Path.home() / ".s3")

cmd_prefix = f"aws s3 --endpoint-url={config['default']['endpoint_url']} "
s3path = config["default"]["bucket"] + str(args.path.resolve())


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
        if args.path.is_dir():
            cmd = cmd_prefix + f"sync {args.path} {s3path}"
        else:
            cmd = cmd_prefix + f"cp {args.path} {s3path}"
    elif args.action == "rm":
        cmd = cmd_prefix + f"rm {s3path}" + (" --recursive" if isdir(s3path) else "")
    elif args.action == "ls":
        cmd = cmd_prefix + f"ls {s3path}"

    run(cmd.split() + unknownargs)
