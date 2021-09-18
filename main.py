import argparse
import p2p
import logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--past", action="store_true",
                        help="Show past investments")
    args = parser.parse_args()
    show_past_investments = args.past
    p2p.report(show_past_investments)
