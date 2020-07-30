import csv


def read_downloaded_zip_zones():
    zip_zones_dict = {}
    with open('zone_information/zip_zones_downloaded.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            zip_code = row[0].rjust(5, '0')
            zone = row[1]
            zip_zones_dict.update({zip_code: zone})
    return zip_zones_dict


def write_zip_zones():
    zip_zones_dict = read_downloaded_zip_zones()
    with open('zone_information/zip_zones.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(zip_zones_dict.items())


def read_zip_zones():
    zip_zones_dict = {}
    with open('zone_information/zip_zones.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            zip_zones_dict.update({row[0]: row[1]})
    return zip_zones_dict


def build_zones():
    zones = {}
    for zone_number in range(1, 14):
        for half_zone, half_temp in {'a': 0, 'b': 5}.items():
            low_temp = (zone_number * 10 - 70 + half_temp)
            zones.update({f"{str(zone_number)}{half_zone}": low_temp})
    return zones


def get_zone_temps(zone: str) -> (int, int):
    zones = build_zones()
    return zones[zone], zones[zone] + 5


def print_zone_temp_ranges():
    for zone_number in range(1, 14):
        for half_zone in ['a', 'b']:
            zone = f"{str(zone_number)}{half_zone}"
            temp_lo, temp_hi = get_zone_temps(zone)
            print(f"{zone}: {temp_lo} to {temp_hi}")


if __name__ == '__main__':
    # print(read_downloaded_zip_zones())
    # write_zip_zones()
    # print_zone_temp_ranges()
    zip_zones = read_zip_zones()
    print(zip_zones)
