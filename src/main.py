from pysrc.data_handlers.data_client import DataClient
from pysrc.prediction.lasso_model_predictor import LassoModelPredictor
from pysrc.logging.logging_config import setup_logging

import argparse


def main() -> None:
    setup_logging()


if __name__ == "__main__":
    main()
