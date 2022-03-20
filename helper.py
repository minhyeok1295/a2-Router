import pickle



def make_packet(src_ip, dest_ip, message, ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)