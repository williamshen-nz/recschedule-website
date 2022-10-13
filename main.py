import sys

from recschedule_website.integ import process_recschedule

if __name__ == "__main__":
    assert (
            len(sys.argv) == 3
    ), "Usage: python main.py <filename of recschedule> <output HTML filename>"
    process_recschedule(in_fname=sys.argv[1], out_fname=sys.argv[2], include_shared_open_rec=True)
