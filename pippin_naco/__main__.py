#import os
import argparse, configparser
from .pippin_naco import run_pipeline
from .pippin_naco import prepare_calib_files
from .pippin_naco import run_example
from .pippin_naco import download_data

from pathlib import Path
import warnings

def main(args=None):

    # Current working directory as SCIENCE path
    path_cwd = Path.cwd()

    # Default master FLATs, BPMs, and DARKs directories
    path_FLAT_dir = '/home/sam/Documents/PIPPIN_reduction/PIPPIN-NACO/pippin_naco/data/master_FLAT/'
    path_BPM_dir  = '/home/sam/Documents/PIPPIN_reduction/PIPPIN-NACO/pippin_naco/data/master_BPM/'
    path_DARK_dir = '/home/sam/Documents/PIPPIN_reduction/PIPPIN-NACO/pippin_naco/data/master_DARK/'

    # All arguments to expect
    parser = argparse.ArgumentParser()

    parser.add_argument('--download_data', action='store_true')

    parser.add_argument('--run_example', action='store_true')

    parser.add_argument('--run_pipeline', action='store_true')
    parser.add_argument('--prepare_calib_files', nargs='?', default=False, const=True)

    parser.add_argument('--path_FLAT_dir', default=path_FLAT_dir,
                        type=str, help='Path to the FLAT directory.')
    parser.add_argument('--path_BPM_dir', default=path_BPM_dir,
                        type=str, help='Path to the master BPM directory.')
    parser.add_argument('--path_DARK_dir', default=path_DARK_dir,
                        type=str, help='Path to the DARK directory.')

    # Read the arguments in the command line
    args = parser.parse_args()


    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        if args.download_data:
            download_data(path_cwd=path_cwd)

        if args.run_example:
            # Run the example reduction
            run_example(path_cwd=path_cwd)


        new_log_file = True
        if args.prepare_calib_files:
            # Create master FLATs, BPMs and DARKs from the provided paths
            path_master_FLAT_dir, path_master_BPM_dir, path_master_DARK_dir \
            = prepare_calib_files(path_SCIENCE_dir=path_cwd,
                                  path_FLAT_dir=Path(args.path_FLAT_dir),
                                  path_master_BPM_dir=Path(args.path_BPM_dir),
                                  path_DARK_dir=Path(args.path_DARK_dir)
                                  )
            new_log_file = False
        else:
            path_master_FLAT_dir, path_master_BPM_dir, path_master_DARK_dir \
            = Path(args.path_FLAT_dir), Path(args.path_BPM_dir), Path(args.path_DARK_dir)


        if args.run_pipeline and not args.run_example:
            # Run the pipeline
            run_pipeline(path_SCIENCE_dir=path_cwd,
                         path_master_FLAT_dir=path_master_FLAT_dir,
                         path_master_BPM_dir=path_master_BPM_dir,
                         path_master_DARK_dir=path_master_DARK_dir,
                         new_log_file=new_log_file
                         )

if __name__ == '__main__':
    main()
