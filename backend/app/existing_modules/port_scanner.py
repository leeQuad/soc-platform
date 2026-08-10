import socket


def scan_ports(
    target: str,
    start_port: int = 1,
    end_port: int = 10000,
    timeout: float = 0.5,
) -> list[int]:
    """
    Scans `target` for open TCP ports in the range [start_port, end_port].

    This is the exact same connect-scan algorithm from the original
    scanner.py — unchanged logic, just wrapped as a reusable function
    instead of a script that reads from input() and prints to stdout.

    Returns a list of open port numbers.
    """
    open_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)

        s.close()

    return open_ports


if __name__ == "__main__":
    # Preserves the original standalone CLI behavior for local testing
    target = input("Enter IP address to scan: ")
    print(f"\nScanning {target}...\n")

    found_ports = scan_ports(target)

    for port in found_ports:
        print(f"Port {port} is OPEN")

    print("\nScan complete.")
