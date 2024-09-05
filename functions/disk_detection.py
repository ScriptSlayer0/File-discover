import psutil

def detect_disks() -> list:
    """Detect and return a list of disk partitions, excluding system partitions."""
    partitions = psutil.disk_partitions()
    # print("Detected partitions:", partitions)
    return [partition.mountpoint for partition in partitions if not partition.mountpoint.startswith('/sys')]