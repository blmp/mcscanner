import sys
from mcstatus import JavaServer
import concurrent.futures

def readip(infile):
    with open(infile, 'r') as file:
        return list(set(line.strip() for line in file.readlines()))

def writeip(outfile, data):
    with open(outfile, 'w') as file:
        for ip, version in data:
            file.write(f"{ip} - {version}\n")

def check_minecraft_server(ip):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()
        return (ip, status.version.name)
    except Exception as e:
        print(f"IP: {ip} is not a valid Minecraft server. Error: {e}")
        return None

def check_minecraft_servers(ips, max_workers):
    valid_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(check_minecraft_server, ip): ip for ip in ips}
        for future in concurrent.futures.as_completed(future_to_ip):
            result = future.result()
            if result:
                valid_ips.append(result)
    return valid_ips

def main(infile, outfile, max_workers):
    ips = readip(infile)
    total_ips = len(ips)
    valid_ips = check_minecraft_servers(ips, max_workers)
    writeip(outfile, valid_ips)
    
    print(f"Found {len(valid_ips)} valid Minecraft servers out of {total_ips} IPs checked.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python scan.py <inputfile> <outputfile> <threads>")
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        max_workers = int(sys.argv[3])
        main(infile, outfile, max_workers)
