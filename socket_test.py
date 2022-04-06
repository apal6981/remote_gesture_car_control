import networking


car_sock = networking.create_car_command_server_socket("10.37.0.5", 12345)

input_gen = networking.car_input_receive_generator(car_sock)
# send_sock = networking.create_car_controller_socket("10.37.0.5", 12345)
# networking.send_car_drive_info(send_sock, -1.2)

for data in input_gen:
    print(data)
    # networking.send_car_drive_info(send_sock, -1.5)
