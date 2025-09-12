import argparse
from .client_api import upload_file, download_file, delete_file, upload_file_parallel, download_file_parallel

def main():
    parser = argparse.ArgumentParser(description="Distributed File System Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # upload 子命令
    upload_parser = subparsers.add_parser("upload")
    upload_parser.add_argument("filepath")
    upload_parser.add_argument("--replicas", type=int, default=2, help="副本数")
    upload_parser.add_argument("--strategy", type=str, choices=["round_robin", "random", "least_used"], default= "round_robin", help="节点选择策略")
    upload_parser.add_argument("--parallel", action="store_true", help= "是否并行上传")
    upload_parser.add_argument("--workers", type= int, default=4, help= "并行上传的线程数")

    # download 子命令
    download_parser = subparsers.add_parser("download")
    download_parser.add_argument("file_id", type=int)
    download_parser.add_argument("output_path")
    download_parser.add_argument("--parallel", action="store_true", help= "是否并行下载")
    download_parser.add_argument("--workers", type= int, default=4, help= "并行下载的线程数")

    # delete 子命令
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("file_id", type=int)

    args = parser.parse_args()

    if args.command == "upload":
        if args.parallel:
            upload_file_parallel(args.filepath, replicas=args.replicas, strategy=args.strategy, workers=args.workers)
        else:
            upload_file(args.filepath, replicas=args.replicas, strategy=args.strategy)
    elif args.command == "download":
        if args.parallel:
            download_file_parallel(file_id= args.file_id, output_path=args.output_path, workers=args.workers)
        else:
            download_file(args.file_id, args.output_path)
    elif args.command == "delete":
        delete_file(args.file_id)


if __name__ == "__main__":
    main()