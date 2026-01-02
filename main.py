import argparse
import sys

from devbox import Container


def cmd_list(container: Container) -> None:
    """List all available state changers."""
    changes = container.main_changes()
    print("Available changes:")
    for name, changer in changes.items():
        print(f"  {name:<15} - {changer.description()}")


def cmd_apply(container: Container, names: str, verbose: bool) -> None:
    """Apply specified state changers."""
    log = container.log()
    engine = container.change_engine()
    changes = container.main_changes()

    requested = [n.strip() for n in names.split(",")]
    for name in requested:
        if name not in changes:
            log.error(f"Unknown changer: {name}")
            log.info(f"Available: {', '.join(changes.keys())}")
            sys.exit(1)
        engine.add_state_changer(changes[name])

    engine.apply_changes(verbose)


def cmd_rollback(container: Container, names: str, verbose: bool) -> None:
    """Rollback specified state changers."""
    log = container.log()
    changes = container.main_changes()

    requested = [n.strip() for n in names.split(",")]
    for name in requested:
        if name not in changes:
            log.error(f"Unknown changer: {name}")
            log.info(f"Available: {', '.join(changes.keys())}")
            sys.exit(1)

        changer = changes[name]
        if changer.is_changed():
            log.info_from(changer, "Rolling back")
            result = changer.rollback(verbose)
            log.info_from(changer, f"Result: {result}")
        else:
            log.info_from(changer, "Not applied, skipping rollback")


def main():
    parser = argparse.ArgumentParser(
        prog="devbox",
        description="DevBox - Manage system state changes",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    subparsers.add_parser("list", help="List all available changes")

    # apply command
    apply_parser = subparsers.add_parser("apply", help="Apply changes")
    apply_parser.add_argument(
        "names",
        help="Comma-separated list of changes to apply (e.g., claude_code,k9s)",
    )
    apply_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Log full command output (stdout/stderr)",
    )

    # rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback changes")
    rollback_parser.add_argument(
        "names",
        help="Comma-separated list of changes to rollback (e.g., claude_code,k9s)",
    )
    rollback_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Log full command output (stdout/stderr)",
    )

    args = parser.parse_args()
    container = Container()

    if args.command == "list":
        cmd_list(container)
    elif args.command == "apply":
        cmd_apply(container, args.names, args.verbose)
    elif args.command == "rollback":
        cmd_rollback(container, args.names, args.verbose)


if __name__ == "__main__":
    main()
