from pyspark import StorageLevel


def main():
    storage_levels = {
        "MEMORY_ONLY": StorageLevel.MEMORY_ONLY,
        "MEMORY_AND_DISK": StorageLevel.MEMORY_AND_DISK,
        "DISK_ONLY": StorageLevel.DISK_ONLY,
    }

    for name, level in storage_levels.items():
        print(f"\n{name}")
        print("Description:", level)
        print("Use memory:", level.useMemory)
        print("Use disk:", level.useDisk)
        print("Deserialized:", level.deserialized)
        print("Replication:", level.replication)


if __name__ == "__main__":
    main()
