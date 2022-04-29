import logging
import sys




from clitodoapp.app.args import get_arguments_parser
from clitodoapp.app.config import try_to_load_config
from clitodoapp.app.logger import setup_logging
from clitodoapp.logic import run

LOG = logging.getLogger(__name__)



def main() -> int:
    parser = get_arguments_parser()
    args = parser.parse_args()
    config_path = args.config_path
    config_section_name = args.config_section_name
    
    config = try_to_load_config(config_path, config_section_name)

    setup_logging(config['logging'])

    try:
        LOG.info("clitodoapp started")
        run(parser)
    except Exception:
        LOG.exception("clitodoapp failed")
        exit_code = -1
    else:
        LOG.info("clitodoapp ended")
        exit_code = 0
    finally:
        return exit_code


if __name__ == "__main__":
    sys.exit(main())
