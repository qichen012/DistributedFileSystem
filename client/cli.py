import argparse
from .client_api import upload_file, download_file, delete_file

def main():
    parser = argparse.ArgumentParser(description="Distributed File System Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # upload 子命令
    upload_parser = subparsers.add_parser("upload")
    upload_parser.add_argument("filepath")
    upload_parser.add_argument("--replicas", type=int, default=2, help="副本数")
    upload_parser.add_argument("--strategy", type=str, choices=["round_robin", "random", "least_used"], default= "round_robin", help="节点选择策略")

    # download 子命令
    download_parser = subparsers.add_parser("download")
    download_parser.add_argument("file_id", type=int)
    download_parser.add_argument("output_path")

    # delete 子命令
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("file_id", type=int)

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.filepath, replica=args.replicas, strategy=args.strategy)
    elif args.command == "download":
        download_file(args.file_id, args.output_path)
    elif args.command == "delete":
        delete_file(args.file_id)


if __name__ == "__main__":
    main()