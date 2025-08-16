import argparse
from .client_api import upload_file, download_file

def main():
    parser = argparse.ArgumentParser(description= "Distributed File System Client")
    parser.add_argument("command",choices=["upload", "download"], help="Command to run")
    parser.add_argument("filepath", help="File path for upload or output path for download")
    parser.add_argument("--file_id",type= int,help="File ID for download")

    args =parser.parse_args()

    if args.command == "upload":
        upload_file(args.filepath)
    elif args.command == "download":
        if not args.file_id:
            parser.error("-file_id. is required for download")
        download_file(args.file_id, args.filepath)

if __name__ == "__main__":
    main()