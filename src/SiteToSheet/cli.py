#!/usr/bin/env python3
"""
This module provides a command-line interface for the SiteToSheet application.
It allows users to interact with the application by specifying various command-line arguments.
"""
import argparse

def parse_arguments():
    """
    Parses the command line arguments and returns the parsed arguments.

    This function uses the argparse module to define and parse command line arguments.
    It supports the following arguments:

    - --gmaps or -gm: Enable Google Maps.
    - --remove_shelf or -rs: Clear the current shelf.
    - --print_shelf or -ps: Print all current shelf data.
    - --gs_merge or -gs_m: Updates all links in the sheet.
    - --update_config or -uc: Update the configuration file.
    - --update_sheet_id or -us: Update the sheet ID.
    - --set-google-api-key: Set the Google API Key.
    - --set-sheet-id: Set the Google Sheet ID.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps','-gm',action='store_true',
                        help='Enable Google Maps')
    parser.add_argument('--remove_shelf','-rs', action='store_true',
                        help='Clear Current Shelf')
    parser.add_argument('--print_shelf','-ps', action='store_true',
                        help='Print All Current Shelf')
    parser.add_argument('--gs_merge','-gs_m', action='store_true',
                        help='Updates all links in the sheet')
    parser.add_argument('--update_config','-uc', action='store_true',
                        help='Update config file')
    parser.add_argument('--update_sheet_id','-us', type=str,
                        help='Update sheet id')

    # Add arguments for setting configuration values
    parser.add_argument("--set-google-api-key", type=str, help="Set Google API Key")
    parser.add_argument("--set-sheet-id", type=str, help="Set Google Sheet ID")
    parser.add_argument("--log-level",
                        choices=["DEBUG" ,"INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO",
                        help="Set the level of logging")
    parser.add_argument("--log-file",type=str, help="Write logs to specified file")
    return parser.parse_args()