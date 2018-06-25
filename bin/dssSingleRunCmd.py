from PyQt5.uic.Compiler.qtproxies import i18n_string

from PyDSS import dssInstance
#import subprocess
import logging
import click
#import os

@click.command()
# Settings for exporting results
@click.option('--log_results',default=True, type=click.BOOL, help='Set true if results need to be exported')
@click.option('--return_results',default=True, type=click.BOOL, help='Set true to access results after every iteration')
@click.option('--export_mode',default='byClass', type=click.STRING, help='possible options "byClass" and "byElement"')
@click.option('--export_style',default='Single file', type=click.STRING, help='possible options "Single_file" and "Separate_files"')
# Plot Settings
@click.option('--network_layout',default=False, type=click.BOOL, help='Display network layout plot')
@click.option('--time_series', default=False, type=click.BOOL, help='Display time series plot')
@click.option('--xy_plot', default=False, type=click.BOOL, help='Display XY plot plot')
@click.option('--sag_plot', default=False, type=click.BOOL, help='Display voltage / distance plot')
@click.option('--histogram', default=False, type=click.BOOL, help='Display histogram plot')
@click.option('--gis_overlay', default=False, type=click.BOOL, help='Display GIS overlay plot')
# Simulation Settings
@click.option('--start_day', default=286, type=click.INT, help='Start day for the simulation study') # 156-163 and 286-293
@click.option('--end_day', default=287, type=click.INT, help='End day for the simulation study')
@click.option('--step_resolution_min', default=60, type=click.FLOAT, help='Time step resolution in minutes')
@click.option('--max_control_iterations', default=10, type=click.INT, help='Maximum outer loop control iterations')
@click.option('--error_tolerance', default=1, type=click.FLOAT, help='Error tolerance in KVA')
@click.option('--simulation_type', default='Daily', type=click.STRING, help='possible modes "Daily" and "Snapshot"')
@click.option('--active_project', default='Mikilua', type=click.STRING, help='Name of project to run')
@click.option('--active_scenario', default='None-None', type=click.STRING, help='Project scenario to use')
@click.option('--dss_file', default='MasterCircuit_Mikilua_baseline2.dss', type=click.STRING, help='The main OpenDSS file')
# Logger settings
@click.option('--logging_level', default='DEBUG', type=click.STRING, help='possible options "DEBUG" and "INFO"')
@click.option('--log_to_external_file', default=True, type=click.BOOL, help='Boolean variable ')
@click.option('--display_on_screen', default=True, type=click.BOOL, help='Boolean variable')
@click.option('--clear_old_log_files', default=False, type=click.BOOL, help='Boolean variable')

def RunSimulation(**kwargs):
    dssArgs = {
        # Settings for exporting results
        'Log Results'    : kwargs.get('log_results'),
        'Return Results'    : kwargs.get('return_results'),
        'Export Mode'    : kwargs.get('export_mode'),
        'Export Style'   : kwargs.get('export_style').replace('_',' '),

        # Plot Settings
        'Network layout' : kwargs.get('network_layout'),
        'Time series'    : kwargs.get('time_series'),
        'XY plot'        : kwargs.get('xy_plot'),
        'Sag plot'       : kwargs.get('sag_plot'),
        'Histogram'      : kwargs.get('histogram'),
        'GIS overlay'    : kwargs.get('gis_overlay'),

        # Simulation Settings
        'Start Day'              : kwargs.get('start_day'),
        'End Day'                : kwargs.get('end_day'),
        'Step resolution (min)'  : kwargs.get('step_resolution_min'),
        'Max Control Iterations' : kwargs.get('max_control_iterations'),
        'Error tolerance'        : kwargs.get('error_tolerance'),
        'Simulation Type'        : kwargs.get('simulation_type'),
        'Active Project'         : kwargs.get('active_project'),
        'Active Scenario'        : kwargs.get('active_scenario'),
        'DSS File'               : kwargs.get('dss_file'),
        'Open plots in browser'  : True,

        # Logger settings
        'Logging Level'          : logging.DEBUG if kwargs.get('logging_level') == 'DEBUG' else logging.INFO,
        'Log to external file'   : kwargs.get('log_to_external_file'),
        'Display on screen'      : kwargs.get('display_on_screen'),
        'Clear old log files'    : kwargs.get('clear_old_log_files'),
    }

    #BokehServer = subprocess.Popen(["bokeh", "serve"], stdout=subprocess.PIPE)
    DSS = dssInstance.OpenDSS(**dssArgs)
    #DSS.RunMCsimulation(MCscenarios = 3)
    DSS.RunSimulation()
    #BokehServer.terminate()
    DSS.DeleteInstance()

if __name__ == '__main__':
    RunSimulation()
    print('End')
    # process(sys.argv[3:])