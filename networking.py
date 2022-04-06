import socket


def create_car_command_server_socket(car_IP, car_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((car_IP, car_port))
    return sock


def car_input_receive_generator(sock):
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print("connection started")
        while True:
            data = conn.recv(8)
            if not data:
                print("connection closed")
                break
            yield data.decode()


def create_car_controller_socket(car_IP, car_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.create_connection((car_IP, car_port),timeout=1.0)


def send_car_drive_info(sock, speed):
    # speed_str = str(round(speed,1).zfill(4)
    sock.sendall(("SPD_" + str(round(speed, 1)).zfill(4)).encode("utf-8"))


def send_car_turn_info(sock, dir):
    sock.sendall(("DIR_" + str(int(dir)).zfill(4)).encode("utf-8"))
