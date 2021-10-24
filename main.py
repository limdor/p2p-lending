import argparse
import p2p

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--past", action="store_true",
                        help="Show past investments")
    args = parser.parse_args()
    show_past_investments = args.past
    p2p.main(show_past_investments)
