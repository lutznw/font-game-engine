from fontemon_blender_addon.fontTools.misc.py23 import *
from fontemon_blender_addon.fontTools.ttLib import TTFont
from fontemon_blender_addon.fontTools.feaLib.builder import addOpenTypeFeatures, Builder
from fontemon_blender_addon.fontTools.feaLib.error import FeatureLibError
from fontemon_blender_addon.fontTools import configLogger
from fontemon_blender_addon.fontTools.misc.cliTools import makeOutputFileName
import sys
import argparse
import logging


log = logging.getLogger("fontemon_blender_addon.fontTools.feaLib")


def main(args=None):
    """Add features from a feature file (.fea) into a OTF font"""
    parser = argparse.ArgumentParser(
        description="Use fontemon_blender_addon.fontTools to compile OpenType feature files (*.fea)."
    )
    parser.add_argument(
        "input_fea", metavar="FEATURES", help="Path to the feature file"
    )
    parser.add_argument(
        "input_font", metavar="INPUT_FONT", help="Path to the input font"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_font",
        metavar="OUTPUT_FONT",
        help="Path to the output font.",
    )
    parser.add_argument(
        "-t",
        "--tables",
        metavar="TABLE_TAG",
        choices=Builder.supportedTables,
        nargs="+",
        help="Specify the table(s) to be built.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Add source-level debugging information to font.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase the logger verbosity. Multiple -v " "options are allowed.",
        action="count",
        default=0,
    )
    parser.add_argument(
        "--traceback", help="show traceback for exceptions.", action="store_true"
    )
    options = parser.parse_args(args)

    levels = ["WARNING", "INFO", "DEBUG"]
    configLogger(level=levels[min(len(levels) - 1, options.verbose)])

    output_font = options.output_font or makeOutputFileName(options.input_font)
    log.info("Compiling features to '%s'" % (output_font))

    font = TTFont(options.input_font)
    try:
        addOpenTypeFeatures(
            font, options.input_fea, tables=options.tables, debug=options.debug
        )
    except FeatureLibError as e:
        if options.traceback:
            raise
        log.error(e)
    font.save(output_font)


if __name__ == "__main__":
    sys.exit(main())