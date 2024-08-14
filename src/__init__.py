import logging
from datetime import date
from pathlib import Path
import importlib.util
from . import item
from .verify import Params

src_path = Path(__file__).parent 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a',
                    filename=src_path / 'log' / f'{date.today()}.log'
                    )

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", src_path / "sdk/ecpay_payment_sdk.py"
    )

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)