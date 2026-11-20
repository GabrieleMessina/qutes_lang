"""Console entry point for the frozen Qutes distribution."""
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    from qutes.cli import main
    raise SystemExit(main())
