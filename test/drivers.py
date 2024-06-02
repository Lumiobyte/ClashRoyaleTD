import pygame

from classes import GridCoordinate


def drive_surrounding_gc():
    new_gc = GridCoordinate(5, 5)
    return new_gc.get_surrounding()


def main():
    print(drive_surrounding_gc())


if __name__ == "__main__":
    main()
