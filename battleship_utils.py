import json

def send_json(socket, data):
	try:
		serialized = json.dumps(data)
	except (TypeError, ValueError), e:
		raise Exception('You can only send JSON-serializable data')
	# send the length of the serialized data first
	socket.send('%d\n' % len(serialized))
	# send the serialized data
	socket.sendall(serialized)

def receive_json(socket):
	# read the length of the data, letter by letter until we reach EOL
	length_str = ''
	char = socket.recv(1)
	if char == '':
		return char
	while char != '\n':
		length_str += char
		char = socket.recv(1)
	total = int(length_str)
	# use a memoryview to receive the data chunk by chunk efficiently
	view = memoryview(bytearray(total))
	next_offset = 0
	while total - next_offset > 0:
		recv_size = socket.recv_into(view[next_offset:], total - next_offset)
		next_offset += recv_size
	try:
		deserialized = json.loads(view.tobytes())
	except (TypeError, ValueError), e:
		raise Exception('Data received was not in JSON format')
	return deserialized