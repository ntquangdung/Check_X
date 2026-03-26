from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from checker import BatchChecker


def parse_usernames(raw_values: list[str]) -> list[str]:
    usernames: list[str] = []
    for raw in raw_values:
        for part in raw.replace(",", "\n").splitlines():
            cleaned = part.strip().lstrip("@")
            if cleaned and cleaned not in usernames:
                usernames.append(cleaned)
    return usernames


def load_usernames(args: argparse.Namespace) -> list[str]:
    raw_values: list[str] = []

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Khong tim thay file: {file_path}")
        raw_values.append(file_path.read_text(encoding="utf-8"))

    if args.usernames:
        raw_values.extend(args.usernames)

    if not raw_values:
        raise ValueError("Ban chua nhap username. Dung -u hoac -f.")

    return parse_usernames(raw_values)


def print_results(results: list[dict]) -> None:
    username_width = max(8, *(len(item["username"]) for item in results))
    status_width = max(10, *(len(item["status"]) for item in results))

    line = f"+-{'-' * username_width}-+-{'-' * status_width}-+-{'-' * 50}-+"
    print(line)
    print(
        f"| {'username'.ljust(username_width)} | "
        f"{'status'.ljust(status_width)} | {'reason'.ljust(50)} |"
    )
    print(line)
    for item in results:
        reason = item["reason"][:50]
        print(
            f"| {item['username'].ljust(username_width)} | "
            f"{item['status'].ljust(status_width)} | {reason.ljust(50)} |"
        )
    print(line)


def print_summary(results: list[dict]) -> None:
    summary = {
        "total": len(results),
        "live": sum(1 for item in results if item["status"] == "live"),
        "suspended": sum(1 for item in results if item["status"] == "suspended"),
        "die": sum(1 for item in results if item["status"] == "die"),
        "unknown": sum(1 for item in results if item["status"] == "unknown"),
    }
    print(
        "Tong: {total} | Live: {live} | Suspend: {suspended} | "
        "Die: {die} | Unknown: {unknown}".format(**summary)
    )


def write_csv(results: list[dict], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj,
            fieldnames=["username", "status", "reason", "profile_url"],
        )
        writer.writeheader()
        writer.writerows(results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Kiem tra hang loat username Twitter/X bang DrissionPage."
    )
    parser.add_argument(
        "-u",
        "--usernames",
        nargs="+",
        help="Danh sach username, co the cach nhau boi dau cach hoac dau phay.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Doc username tu file txt. Moi dong mot username hoac cach nhau boi dau phay.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Luu ket qua ra file CSV.",
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Hien browser trong luc chay.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=100,
        help="Timeout moi profile, mac dinh 100 giay.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        usernames = load_usernames(args)
    except Exception as exc:  # noqa: BLE001
        print(f"Loi input: {exc}", file=sys.stderr)
        return 1

    checker = BatchChecker(
        headless=not args.show_browser,
        timeout=args.timeout,
    )
    results = checker.check_many(usernames)

    print_results(results)
    print_summary(results)

    if args.output:
        write_csv(results, args.output)
        print(f"Da luu CSV: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
