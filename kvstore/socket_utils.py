def receive_all(sock):
    block_size = 4096
    chunks = []
    current = sock.recv(block_size)
    while current != '':
        chunks.append(current)
        current = sock.recv(block_size)
    return ''.join(chunks)


def send_all(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent += sent