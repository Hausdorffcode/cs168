import os
import sys

import client
import wan

def partial_file_sending(middlebox_module, testing_part_1):
    middlebox1 = middlebox_module.WanOptimizer()
    middlebox2 = middlebox_module.WanOptimizer()
    wide_area_network = wan.Wan(middlebox1, middlebox2)

    # Initialize client connected to middlebox 1.
    client1_address = "1.2.3.4"
    client1 = client.EndHost("client1", client1_address, middlebox1)

    # Initialize client connected to middlebox 2.
    client2_address = "5.6.7.8"
    client2 = client.EndHost("client2", client2_address, middlebox2)

    filename = "sample.txt"
    # Make sure that the files have the same contents.
    with open(filename, "r") as input_file:
        input_data = input_file.read()

    file_size = len(input_data)
    break_point = file_size // 2

    # Send a file from client 1 to client 2.
    
    client1.send_partial_file(filename, 
        client2_address, 0, break_point, False)
    bytes_sent = wide_area_network.get_total_bytes_sent()
    client1.send_partial_file(filename, 
        client2_address, break_point, file_size, True)

    output_file_name = "{}-{}".format("client2", filename)
    with open(output_file_name, "r") as output_file:
        result_data = output_file.read()
    # Removing the output file just created
    os.remove(output_file_name)

    if not (input_data == result_data and bytes_sent > break_point // 4):
        raise Exception(
            "partial_file_sending failed, because the file " + 
            "received did not match the file sent.")
