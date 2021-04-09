#
# infantfs ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import subprocess as sp
from glob import glob
from os import path
import os
import sys
import shutil
import logging

Gstr_title = r"""
 _____       __            _    ______             _____             __
|_   _|     / _|          | |   |  ___|           /  ___|           / _|
  | | _ __ | |_ __ _ _ __ | |_  | |_ _ __ ___  ___\ `--. _   _ _ __| |_ ___ _ __
  | || '_ \|  _/ _` | '_ \| __| |  _| '__/ _ \/ _ \`--. \ | | | '__|  _/ _ \ '__|
 _| || | | | || (_| | | | | |_  | | | | |  __/  __/\__/ / |_| | |  | ||  __/ |
 \___/_| |_|_| \__,_|_| |_|\__| \_| |_|  \___|\___\____/ \__,_|_|  |_| \___|_|
"""

Gstr_synopsis = r"""

ChRIS wrapper for infant_recon_all from Infant FreeSurfer.
Version: against 7.1.1 dev, 2021-01-12

    NAME

       infantfs 

    SYNOPSIS

        python --subject MRN --age M /incoming /outgoing

    ARGS

        [-s MRN] [--subject MRN]
        This identifies the subject that is to be processed. The input
        file, unless indicated otherwise, should be located in
        /incoming/$s/mprage.nii.gz before processing is started.

        [-i FILE] [--inputPathFilter FILE]
        Alternatively, specify a file pattern relative to the input
        directory which identifies the subject that is to be processed.

        [-a M] [--age M]
        Age in months of the FreeSurfer subject that is to be processed.

"""


class Infantfs(ChrisApp):
    """
    Infant MRI reconstruction
    """
    PACKAGE                 = __package__
    TITLE                   = 'Infant FreeSurfer'
    CATEGORY                = 'MRI'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        # this is a future spec
        # https://github.com/FNNDSC/chrisapp/issues/6
        self.add_argument(
            '-p', '--inputPathFilter',
            dest='inputPathFilter',
            help='Specify a file pattern relative to the input directory '
                 'which identifies the subject that is to be processed. '
                 'Alternative to --subject, easier to use.',
            default='*.nii.gz',
            type=str,
            optional=True
        )
        self.add_argument(
            '-s', '--subject',
            dest='subject',
            help='This identifies the subject that is to be processed. The input'
                 'file, unless indicated otherwise, should be located in '
                 '/incoming/$s/mprage.nii.gz before processing is started.',
            default='',
            type=str,
            optional=True
        )
        self.add_argument(
            '-a', '--age',
            dest='age',
            help='Age in months of the FreeSurfer subject that is to be processed.',
            type=str,
            optional=False
        )
        # TODO more args

    def run(self, options):
        if options.subject:
            print(Gstr_title, flush=True)
            logging.debug('--subject was given manually: %s', options.subject)
            shutil.copytree(options.inputdir, options.outputdir)
        else:
            input_pattern = path.join(options.inputdir, options.inputPathFilter)
            input_files = glob(input_pattern)

            if not input_files:
                logging.error('No input files found matching %s', input_pattern)
                sys.exit(1)
            if len(input_files) > 1:
                logging.error('More than one input file found: %s', str(input_files))
                sys.exit(1)

            input_file = input_files[0]
            options.subject = 'subject'
            folder = path.join(options.outputdir, options.subject)
            os.mkdir(folder)
            shutil.copy(input_file, path.join(folder, 'mprage.nii.gz'))

            print(Gstr_title, flush=True)
            logging.debug('Found input file: %s', input_file)

        os.environ['SUBJECTS_DIR'] = options.outputdir

        cmd = [
            'infant_recon_all',
            '--outdir', options.outputdir,
            '--subject', options.subject,
            '--age', options.age
        ]

        if 'NVIDIA_VISIBLE_DEVICES' in os.environ:
            cmd += ['--usegpu']

        logging.info(' '.join(cmd))

        try:
            sp.run(cmd, check=True)
        except sp.CalledProcessError as e:
            sys.exit(e.returncode)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
