import ijson
import time
import os

def is_ny_url(url):
    ny_ids = {"254"}
    slash_split = url.split("/")
    if len(slash_split) > 3:
        underscore_split = slash_split[3].split("_")
        if len(underscore_split) > 1:
            return underscore_split[1] in ny_ids


def parse_file(file_name, out_path):
    output = open(out_path, "a")
    # 254 is the NY identifier for in network rates
    # Example https://anthembcbsco.mrf.bcbs.com/2024-02_254_39B0_in-network-rates_4_of_9.json.gz?&Expires=
    # 1711116038&Signature=IIVeQu04SRozXU8YyCtHRS6P4loGR5~lfpDYQesz7Yd5eMoNi7zmys-Nt69KGdZxEqnUcHJpUcrp0TVVDKa69jMTYXv
    # 4QqNI8UWIg1rpUnfJaZ59ZuW4DHbslo~yXrGzI3WPEU0qQGPsdOyayBNJQYEJc~T8a5Vq8wTIrC9TAdt6~WPO2fgOb9-SJJFBbzcvaLGsI2dzFjfj
    # 69s7Kvb6KkaNy4DJOQWoWcP3g36pTXaKXdl-HavEKwkYEGCRXr-MeW2ydXJv8uTdLvaRDIIPvS8Vj35vYRcOlNE9nVYiTLmL40~LL853txs-HvB71
    # kp-HWeD-AvYz1HyM8dVeOd8Zg__&Key-Pair-Id=K27TQMT39R1C8A

    # 800 is the NY identifier for Blue Cross Blue Shield Association Out-of-Area Rates Files
    # Example https://anthembcca.mrf.bcbs.com/2024-02_800_72A0_in-network-rates_03_of_03.json.gz?&Expires=
    # 1711116038&Signature=VcI0P~xtKZeBB7x~nQ2BSUkD8nce5l1uBDQd0R9PBI5OTE5bx6kZce7LxsawT6fdNHc-~QXbmfi165VZrYvOWR2E0G1s
    # 9qycaWpmfKwq1xfrPNFJVSWEbvTkFmnMeJ0oqlqIO6CXezfP7o7TcYLByTqlf35yKk6U1H1nDEzDA3qTOWWGs38Yjm8MiPg5L48Jzt8oRDN-Q~WL5
    # u-~-waePquRYtgNfUCwquLxq8Q8bvrKjwYNxZmW-oj2W5PuvysHPi9XAhwB3ddNNa6t1vRuGEH37jQ5DiQkR~b3SuDkehW0cnDEg9-qQNBM710lj-
    # d-MoGPYAtfulqhQAaqJpgvmA__&Key-Pair-Id=K27TQMT39R1C8A

    # 301 and 302 are other ids

    url_len = 0
    mult = 1

    with open(file_name, "rb") as f:
        for record in ijson.items(f, "reporting_structure.item.in_network_files.item"):
                url = record["location"]
                if is_ny_url(url):
                    new_url = url + "\n"
                    output.write(new_url)
                    url_len += 1
                    if url_len % 10000 == 0:
                        print("%s urls added" % url_len)

                        mult += 1

    output.close()

    return url_len


if __name__ == "__main__":
    output_path = "output.txt"
    if os.path.isfile(output_path):
        os.remove(output_path)

    start_time = time.time()
    total_urls = parse_file("/Users/jonaspeek/Downloads/2024-02-01_anthem_index.json", output_path)
    # total_urls = parse_file("test_data.json", output_path)

    print("The program took", round(time.time() - start_time, 2), "seconds to run.")
    print("There were", total_urls, "urls added to the output.")

    file_stats = os.stat(output_path)
    print(f'The output file size is {file_stats.st_size} bytes or '
          f'{file_stats.st_size / (1024 * 1024)} MB')


