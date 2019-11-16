import argparse as ap
from argparse import ArgumentDefaultsHelpFormatter as adhf

DATADIR = '../data/'

def base_parser(desc, output):
    """
    Create parser with common options.
    Desc - Description of script.
    """

    output_help = 'Path to store file'
    output_def = DATADIR + output

    ordered_help = 'Initial spin direction. 1 = up, -1 = down, 0 = random.'
    ordered_def = 0

    # Initialize parser
    parser = ap.ArgumentParser(description=desc,formatter_class=adhf)
    parser.add_argument('--output', '--o', default=output_def, help=output_help)
    parser.add_argument('--ordered', default=ordered_def, help=ordered_help)
    return parser


def equi_parser():
    """
    Create parser for equilibrium check.
    """
    description = 'Run ising model to check for equilibrium.'
    output = 'equilibrium.csv'
    parser = base_parser(description, output)

    exp_help = 'Highest power of 10 Monte Carlo cycles to run experiment for.'
    exp_def = 6



    points_help = 'Number of different sample sizes to run for. '
    points_help += 'Logarithmically spaced between 10 and 10^exp'
    points_def = 30

    L_help = 'Grid size'
    L_def = 20

    parser.add_argument('--L', default=L_def, help=L_help)
    parser.add_argument('--exp', '--e', default=exp_def, help=exp_help)
    parser.add_argument('--points', '--p', default=points_def,help=points_help)
    return parser

def phase_parser():
    """
    Create parser for running phase transisions.
    """
    desc = 'Run ising model to check for phase transitions, varying grid size and temperature.'
    output = 'phase.csv'
    parser = base_parser(desc, output)

    Tstart_help = 'Lowest temperature.'
    Tstart_def = 2.2

    Tstop_help = 'Highest temperature.'
    Tstop_def = 2.35

    dT_help = 'Temperature step size.'
    dT_def = 0.05

    delay_help = 'Number of MC cycles to run before collecting data.'
    delay_def = 50000

    cycles_help = 'Total number of MC cycles.'
    cycles_def = 500000

    estimate_help = 'Estimate run time before running.'
    estimate_def = False

    parser.add_argument('--Tstart', default=Tstart_def, help=Tstart_help)
    parser.add_argument('--Tstop', default=Tstop_def,help=Tstop_help)
    parser.add_argument('--dT', default=dT_def, help=dT_help)
    parser.add_argument('--delay', default=delay_def, help=delay_help)
    parser.add_argument('--cycles', default=cycles_def, help=cycles_help)
    parser.add_argument('--estimate', default=estimate_def,help=estimate_help)
    return parser

def post_parser():
    """
    Create parser for post processing.
    """
    desc = 'Plot results.'
    equi_help = 'Filepath of equilibrium results.'
    equi_def = DATADIR + 'equi_long2.csv'

    error_help = 'Filepath of relative error results.'
    error_def = DATADIR + 'equi_L2_large_7.csv'

    phase_help = 'Filepath of phase transition results.'
    phase_def = DATADIR + 'longrun2.csv'

    distfile_help = 'Filepath of distribution.'
    distdata_help = 'Filepath of distribution results.'
    distfile_def = DATADIR + 'dist_dist.csv'
    distdata_def = DATADIR + 'dist_20.csv'

    parser = ap.ArgumentParser(description=desc,formatter_class=adhf)
    parser.add_argument('--equi',help=equi_help, default=equi_def)
    parser.add_argument('--phase', help=phase_help, default=phase_def)
    parser.add_argument('--distfile', help=distfile_help, default=distfile_def)
    parser.add_argument('--distdata', help=distdata_help, default=distdata_def)
    parser.add_argument('--error',help=error_help, default=error_def)


    return parser

if __name__ == '__main__':

    # Example of loading arguments
    args = phase_parser().parse_args()
