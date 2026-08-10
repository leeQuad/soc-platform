def parse_logs(log_file_path: str, report_path: str | None = "security_report.txt") -> dict:
    """
    Parses a login log file and returns security metrics.

    Same detection logic as the original parser.py (failed-login counting,
    per-IP suspicious-activity levels, success rate) — refactored into a
    function that returns structured data instead of printing to stdout,
    so it can be served over an API.

    If report_path is provided, also writes the original-format text report.
    """
    success_count = 0
    failed_count = 0
    failed_times = {}
    ip_count = {}

    with open(log_file_path, "r") as file:
        logs = file.readlines()

    for line in logs:
        if "LOGIN_SUCCESS" in line:
            success_count += 1

        if "LOGIN_FAILED" in line:
            failed_count += 1

            date = line.split()[0]
            time = line.split()[1]
            timestamp = date + " " + time
            ip = line.split()[-1]

            if ip in ip_count:
                ip_count[ip] += 1
            else:
                ip_count[ip] = 1
                failed_times[ip] = timestamp

    suspicious_ips = []
    for ip, count in ip_count.items():
        if count >= 2:
            if count >= 5:
                level = "HIGH"
            elif count >= 3:
                level = "MEDIUM"
            else:
                level = "LOW"
            suspicious_ips.append(
                {
                    "ip": ip,
                    "count": count,
                    "level": level,
                    "first_seen": failed_times[ip],
                }
            )

    total = success_count + failed_count
    success_rate = round(success_count / total * 100, 2) if total > 0 else 0.0

    # NOTE: the original script assumed at least one failed login and would
    # crash on max(ip_count, ...) with an empty dict. Guarded here so the
    # API doesn't 500 on a clean log file with zero failed attempts.
    most_attacked_ip = max(ip_count, key=ip_count.get) if ip_count else None
    most_attacked_ip_count = ip_count[most_attacked_ip] if most_attacked_ip else 0

    result = {
        "success_count": success_count,
        "failed_count": failed_count,
        "total_attempts": total,
        "success_rate": success_rate,
        "unique_suspicious_ips": len(ip_count),
        "ip_count": ip_count,
        "suspicious_ips": suspicious_ips,
        "most_attacked_ip": most_attacked_ip,
        "most_attacked_ip_count": most_attacked_ip_count,
    }

    if report_path:
        _write_report(result, report_path)

    return result


def _write_report(result: dict, report_path: str) -> None:
    """Writes the same plain-text report format as the original script."""
    with open(report_path, "w") as report:
        report.write("SECURITY LOG ANALYZER\n")
        report.write("=" * 30 + "\n")
        report.write(f"Total failed login attempts: {result['failed_count']}\n")
        report.write(f"Unique suspicious IPs: {result['unique_suspicious_ips']}\n")
        report.write(f"Most attacked IP: {result['most_attacked_ip']}\n")
        report.write("Failed login attempts by IP:\n")
        for ip, count in result["ip_count"].items():
            report.write(f"{ip} - {count}\n")
        report.write("\nSuspicious IPs:\n")
        for entry in result["suspicious_ips"]:
            report.write(
                f"[{entry['level']}] {entry['ip']} - {entry['count']} failed attempts\n"
            )
        report.write(f"\nSuccessful logins: {result['success_count']}\n")
        report.write(f"Failed logins: {result['failed_count']}\n")
        report.write(f"Total login attempts: {result['total_attempts']}\n")
        report.write(f"Success rate: {result['success_rate']}%\n")


if __name__ == "__main__":
    print("=" * 50)
    print("CYBERSECURITY SECURITY LOG ANALYZER")
    print("=" * 50)

    results = parse_logs("mock_logs.txt")

    print("Failed login attempts by IP:")
    for ip, count in results["ip_count"].items():
        print(ip, "-", count)

    print("\nSuspicious IPs:")
    for entry in results["suspicious_ips"]:
        print(
            f"[{entry['first_seen']}][{entry['level']}] "
            f"WARNING: {entry['ip']} - {entry['count']} failed attempts"
        )

    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print("Total failed login:", results["failed_count"])
    print("Unique suspicious IPs:", results["unique_suspicious_ips"])
    print("Most attacked IP:", results["most_attacked_ip"])
    print("Failed attempts:", results["most_attacked_ip_count"])
    print("Successful logins:", results["success_count"])
    print("Failed logins:", results["failed_count"])
    print("Total login attempts:", results["total_attempts"])
    print("Success rate:", results["success_rate"], "%")
    print("\nSecurity report generated successfully!")
