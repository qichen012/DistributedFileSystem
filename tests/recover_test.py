from controller.scheduler import recover_replicas


if __name__ == "__main__":
    file_id = 29
    recover_replicas(file_id, 4)