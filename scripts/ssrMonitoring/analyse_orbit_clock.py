#!/usr/bin/env python3

"""
Script to compare orbits and clocks in SP3 and CLK files against corresponding reference products,
such as IGS rapid products, for specified time period to
- Calculate orbit/clock differences
- Compute statistics including percentiles, mean, standard deviation, and RMS for each satellite
    and the whole constellation
- Plot out orbit/clock differences and RMS errors
It can run in post-processing (finite) mode or real-time (infinite) mode.
"""

import itertools
import logging
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Union

import click
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib.figure import Figure

import gnssanalysis as ga


sys_meta = {
    "G": {"name": "GPS", "max_sats": 32},
    "R": {"name": "GLO", "max_sats": 27},
    "E": {"name": "GAL", "max_sats": 36},
    "C": {"name": "BDS", "max_sats": 62},
}


def str_to_list(input: str) -> list[str]:
    """
    Split a comma separated string to a list of sub strings

    :param str input: String to split
    :return list[str]: A list of sub strings from the input string
    """
    if input:
        output = input.replace(" ", "").split(",")
    else:
        output = []

    return output


def filter_svs_list(svs: list[str], dataframe: pd.DataFrame) -> list[str]:
    """
    Filter out the unavailable satellites from the given satellite list

    :param list[str] svs: Satellite list to filter
    :param pd.DataFrame dataframe: The Pandas DataFrame containing orbit/clock differences or statistics
    :return list[str]: A new satellite list containing only available satellites
    """
    svs_new = sorted(list(dataframe.index.get_level_values("Satellite").intersection(svs)))
    if not svs_new:
        logging.error("No data found for given satellites")
    return svs_new


def download_ref_products(
    ref_dir: Path,
    ref_prefix: str,
    product_type: str,
    start_epoch: datetime,
    end_epoch: datetime,
    sampling_rate: dict = {},
    if_file_present: str = "dont_replace",
) -> list[Path]:
    """
    Download reference products for orbits and clocks comparison

    :param Path ref_dir: Directory to download reference products to
    :param str ref_prefix: Prefix of reference products, e.g. IGS0OPSRAP
    :param str product_type: Product type to download, SP3 or CLK
    :param datetime start_epoch: Start of epoch time
    :param datetime end_epoch: End of epoch time
    :param dict sampling_rate: Dictionary of sampling rates for SP3 and CLK products in seconds,
            will be determined and saved based on the prefix if not specified
    :return list[Path]: Return list of paths of downloaded files
    """
    logging.info("Downloading reference products ...")

    analysis_center = ref_prefix[0:3]
    version = ref_prefix[3]
    project_type = ref_prefix[4:7]
    solution_type = ref_prefix[7:10]

    days = 2 if solution_type == "ULT" else 1

    if product_type not in sampling_rate.keys() or not sampling_rate[product_type]:
        sampling_rate[product_type] = ga.gn_download.generate_sampling_rate(
            file_ext=product_type, analysis_center=analysis_center, solution_type=solution_type
        )

    download_filepaths = []
    try:
        download_filepaths = ga.gn_download.download_product_from_cddis(
            download_dir=ref_dir,
            start_epoch=start_epoch,
            end_epoch=(end_epoch + timedelta(days - 1)),
            file_ext=product_type,
            long_filename=True,
            analysis_center=analysis_center,
            version=version,
            project_type=project_type,
            solution_type=solution_type,
            timespan=timedelta(days),
            sampling_rate=sampling_rate[product_type],
            if_file_present=if_file_present,
        )
        logging.info("Reference products downloaded\n")
    except Exception as error:
        logging.error(f"Fail to download products: {error}\n")

    return download_filepaths


def search_input_file_case_insensitively(input_path: Path) -> Union[Path, None]:
    """
    Search an input file case-insensitively

    :param Path input_path: Path of the input file to search
    :return Union[Path, None]: None if the input file does not exist otherwise the real path which matches the input file case-insensitively
    """
    matched_input_path = None

    for file in input_path.parent.iterdir():
        if file.is_file() and file.name.lower() == input_path.name.lower():
            matched_input_path = file
            break

    return matched_input_path


def generate_input_paths(
    job_dir: Path,
    ref_dir: Path,
    sub_job_name: str,
    ref_prefix: str,
    yrdoys: list[str],
    sampling_rate: dict,
    product_type: str,
    orb_ref_frame: str = "ECF",
) -> list[list[Path]]:
    """
    Generate a list of input path pairs of test file (file to analyse) and reference product

    :param Path job_dir: Directory where data is processed
    :param Path ref_dir: Directory where reference products are placed
    :param str sub_job_name: Sub job to process, which should be the name of the parent folder (and the prefix) of test files to analyse
    :param str ref_prefix: Prefix of reference products, e.g. IGS0OPSRAP
    :param list[str] yrdoys: A list of day-of-year strings to analyse data for in the format of 'YYYYDDD'
    :param dict sampling_rate: Dictionary of sampling rates for SP3 and CLK products in seconds
    :param str product_type: Type of files/products to analyse, i.e. 'SP3' or 'CLK'
    :return list[list[str]]: A list of input path pairs (list) of test file and reference product
    """
    input_paths = []

    file_ext = product_type
    if product_type == "SP3" and orb_ref_frame == "ECI":
        file_ext = file_ext + "i"
    content_type = "ORB" if product_type == "SP3" else "CLK" if product_type == "CLK" else None
    if not content_type:
        return input_paths
    solution_type = ref_prefix[7:10]
    timespan = "02D" if solution_type == "ULT" else "01D"

    for yrdoy in yrdoys:
        job_file_path = job_dir / sub_job_name / f"{sub_job_name}_{yrdoy}0000_{content_type}.{file_ext}"
        ref_file_path = (
            ref_dir / f"{ref_prefix}_{yrdoy}0000_{timespan}_{sampling_rate[product_type]}_{content_type}.{file_ext}"
        )

        if not ref_file_path.exists() and product_type == "SP3" and solution_type == "ULT":
            date = datetime.strptime(yrdoy, "%Y%j")
            earlist = date - timedelta(hours=42)  # earliest possible ultra rapid file containing overlapping data

            while date > earlist:
                logging.warning(
                    f"'{ref_file_path.name}' not found, attempting an earlier ultra-rapid product for its predicted part"
                )

                date -= timedelta(hours=6)
                download_ref_products(ref_dir, ref_prefix, product_type, date, date + timedelta(days=1), sampling_rate)

                yrdoy_hr = date.strftime("%Y%j%H")
                ref_file_path = (
                    ref_dir
                    / f"{ref_prefix}_{yrdoy_hr}00_{timespan}_{sampling_rate[product_type]}_{content_type}.{file_ext}"
                )

                if ref_file_path.exists():
                    break

        job_file_path = search_input_file_case_insensitively(job_file_path)
        ref_file_path = search_input_file_case_insensitively(ref_file_path)

        if job_file_path and ref_file_path:
            input_paths.append([ref_file_path, job_file_path])

    return input_paths


def compare_sp3_files(
    input_paths: list[list[Path]],
    output_path: Path,
    svs: Union[dict, list[str]],
    orb_ref_frame: str,
    orb_hlm_mode: str,
    epochwise_hlm: bool,
    clk_norm_types: list[str],
) -> pd.DataFrame:
    """
    Compare SP3 file pairs and to calculate orbit and clock differences. The orbit differences will be represented
    in both X/Y/Z ECEF frame and R/A/C orbit frame, and the clock differences will NOT be normalised.

    :param list[list[Path]] input_paths: A list of input path pairs of test file and reference product
    :param Path output_path: Path of the output file to write results to in CSV format
    :param Union[dict, list[str]] svs: List(s) of satellites to process
    :param str orb_ref_frame: Reference frame of input orbits. Should either be 'ECF' or 'ECI'
    :param str orb_hlm_mode: Helmert transformation to apply to orbits. Can be None, 'ECF', or 'ECI'
    :param bool epochwise_hlm: Epochwise Helmert transformation
    :param list[str] clk_norm_types: Normalizations to apply to clocks. Available options include
            'epoch', 'daily', 'sv', any satellite PRN, or any combination of them
    :return pd.DataFrame: The Pandas DataFrame containing orbit and clock differences
    """
    svs = list(itertools.chain.from_iterable(svs.values()))

    sp3_diff_df = pd.DataFrame()

    for input in input_paths:
        ref_sp3_file = input[0]
        job_sp3_file = input[1]

        logging.info(f"-- '{job_sp3_file}' vs '{ref_sp3_file}'")

        diff_df = pd.DataFrame()
        try:
            diff_df = ga.gn_diffaux.sp3_difference(
                ref_sp3_file, job_sp3_file, svs, orb_ref_frame, orb_hlm_mode, epochwise_hlm, clk_norm_types
            )
        except Exception as error:
            logging.error(f"Error with sp3_difference(): {error}")
            continue

        sp3_diff_df = pd.concat([sp3_diff_df, diff_df])

    sp3_diff_df.to_csv(output_path)

    return sp3_diff_df


def compare_clk_files(
    input_paths: list[list[Path]], output_path: Path, svs: Union[dict, list[str]], clk_norm_types: list[str]
) -> pd.DataFrame:
    """
    Compare CLK file pairs and to calculate clock differences with common mode removed (if specified)
    based on the chosen normalisations.

    :param list[list[Path]] input_paths: A list of input path pairs of test file and reference product
    :param Path output_path: Path of the output file to write results to in CSV format
    :param Union[dict, list[str]] svs: List(s) of satellites to process
    :param list[str] clk_norm_types: Normalizations to apply to clocks. Available options include
            'epoch', 'daily', 'sv', any satellite PRN, or any combination of them
    :return pd.DataFrame: The Pandas DataFrame containing clock differences
    """
    svs = list(itertools.chain.from_iterable(svs.values()))

    clk_diff_df = pd.DataFrame()

    for input in input_paths:
        ref_clk_file = input[0]
        job_clk_file = input[1]

        logging.info(f"-- '{job_clk_file}' vs '{ref_clk_file}'")

        diff_df = pd.DataFrame()
        try:
            diff_df = ga.gn_diffaux.clk_difference(ref_clk_file, job_clk_file, svs, clk_norm_types)
        except Exception as error:
            logging.error(f"Error with clk_difference(): {error}")
            continue

        clk_diff_df = pd.concat([clk_diff_df, diff_df])

    clk_diff_df.to_csv(output_path)

    return clk_diff_df


def compute_stats(diff_df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    """
    Compute statistics of orbit and/or clock differences, namely 'count', 'mean', 'std', 'rms',
    'min', '5%', '10%', '50%', '75%', '90%', '95%' percentiles, and 'max'.

    :param pd.DataFrame diff_df: The Pandas DataFrame containing orbit and/or clock differences
    :param Path output_path: Path of the output file to write results to in CSV format
    :return pd.DataFrame: The Pandas DataFrame containing statistics of orbit and/or clock differences
    """
    stats_df = ga.gn_diffaux.difference_statistics(diff_df)
    stats_df.to_csv(output_path)

    return stats_df


def set_up_matplotlib(font: str, colormap: str) -> None:
    """
    Set up font and colormap for matplotlib

    :param str font: font name
    :param str colormap: colormap name
    :return None
    """
    available_fonts = matplotlib.font_manager.get_font_names()
    if font in available_fonts:
        matplotlib.rcParams["font.family"] = font
    else:
        logging.warning(f"Font ['{font}'] not found, falling back to {matplotlib.rcParams['font.family']}")
        logging.warning(f"Available fonts: {available_fonts}")

    available_cmaps = plt.colormaps()
    if colormap in available_cmaps:
        matplotlib.rcParams["image.cmap"] = colormap
    else:
        logging.warning(f"Colormap '{colormap}' not found, falling back to '{matplotlib.rcParams['image.cmap']}'")
        logging.warning(f"Available colormaps: {plt.colormaps()}")


def configure_diff_plot(
    axes: Any,
    start_epoch: datetime,
    end_epoch: datetime,
    nominal_ymin: float,
    nominal_ymax: float,
    fix_ylim: bool,
    xlabel: str,
    ylabel: str,
    title: str,
) -> None:
    """
    Configure the orbit/clock difference plot

    :param Any axes: The axes object to configure
    :param datetime start_epoch: Start of epoch time (lower limit of x-axis)
    :param datetime end_epoch: End of epoch time (upper limit of x-axis)
    :param float nominal_ymin: Nominal lower limit of y-axis
    :param float nominal_ymax: Nominal upper limit of y-axis
    :param bool fix_ylim: Fix Y-axis limit to nominal values.
            If False, the Y-axis limits will be automatically set when any data points exceed the nominal range.
    :param str xlabel: Label of x-axis
    :param str ylabel: Label of y-axis
    :param str title: Title of the axes
    :return None
    """
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = ["%Y", "%m", "%j", "%H:%M", "%H:%M", "%S.%f"]
    formatter.zero_formats = ["", "%Y", "%Y", "%Y-%j", "%H:%M", "%H:%M"]
    formatter.offset_formats = ["", "", "", "", "%Y-%j", "%Y-%j"]

    axes.grid(True)
    ymin, ymax = axes.get_ylim()
    if (ymin >= nominal_ymin and ymax <= nominal_ymax) or fix_ylim:
        ymin = nominal_ymin
        ymax = nominal_ymax
    axes.set_ylim(ymin, ymax)
    axes.set_ylabel(ylabel)
    axes.set_xlim(start_epoch, end_epoch)
    axes.xaxis.set_major_locator(locator)
    axes.xaxis.set_major_formatter(formatter)
    axes.set_xlabel(xlabel)
    axes.set_title(title)


def configure_rms_plot(
    axes: Any,
    xdata: npt.ArrayLike,
    nominal_ymin: float,
    nominal_ymax: float,
    fix_ylim: bool,
    xticklabels: list[str],
    xlabel: str,
    ylabel: str,
    annotation: str,
    title: str,
) -> None:
    """
    Configure the orbit/clock RMS plot

    :param Any axes: The axes object to configure
    :param npt.ArrayLike xdata: Data array for the x-axis
    :param float nominal_ymin: Nominal lower limit of y-axis
    :param float nominal_ymax: Nominal upper limit of y-axis
    :param bool fix_ylim: Fix Y-axis limit to nominal values.
            If False, the Y-axis limits will be automatically set when any data points exceed the nominal range.
    :param list[str] xticklabels: Tick labels of x-axis
    :param str xlabel: Label of x-axis
    :param str ylabel: Label of y-axis
    :param str annotation: Annotation to add on the axes
    :param str title: Title of the axes
    :return None
    """
    axes.grid(True)
    ymin, ymax = axes.get_ylim()
    ymin = nominal_ymin if fix_ylim else min(nominal_ymin, ymin)
    ymax = nominal_ymax if fix_ylim else max(nominal_ymax, ymax)
    axes.set_ylim([ymin, ymax])
    axes.set_ylabel(ylabel)
    axes.set_xlim([xdata[0] - 1, xdata[-1] + 1])
    axes.set_xticks(xdata)
    axes.set_xticklabels(xticklabels, ha="center", rotation=90)
    axes.set_xlabel(xlabel)
    axes.set_title(title)
    axes.legend(loc="upper right")
    axes.text(xdata[0] - 0.5, 0.95 * ymax, annotation, ha="left", va="top")


def plot_orb_diff(
    diff_df: pd.DataFrame,
    svs: list[str],
    title: str,
    start_epoch: datetime,
    end_epoch: datetime,
    nominal_ylim: float,
    fix_ylim: bool,
) -> Union[Figure, None]:
    """
    Plot orbit differences from a Pandas DataFrame.

    :param pd.DataFrame diff_df: The Pandas DataFrame containing orbit differences
    :param list[str] svs: Satellite list to plot differences for
    :param str title: Figure title
    :param datetime start_epoch: Start of epoch time
    :param datetime end_epoch: End of epoch time
    :param float nominal_ylim: Nominal Y-axis plotting limit (used as ±limit) in metres.
    :param bool fix_ylim: Fix Y-axis limit to nominal value.
            If False, the Y-axis limit will be automatically set when any data points exceed the nominal range.
    :return Figure: The Figure object for the plot
    """
    # Filter data with given satellite list and unstack the dataframe to push the satellite PRNs
    # from the index to columns as it's easier to plot
    svs = filter_svs_list(svs, diff_df)
    if not svs:
        return None

    unstacked_diff_df = diff_df[diff_df.index.get_level_values("Satellite").isin(svs)].unstack()

    # Plot epoch-by-epoch orbit comparison results
    fig, ax = plt.subplots(nrows=3, dpi=300.0, figsize=(12, 6))

    for i, dim in enumerate(["Radial", "Along-track", "Cross-track"]):
        ax[i].plot(unstacked_diff_df[dim].index.values, unstacked_diff_df[dim].values)

    configure_diff_plot(
        axes=ax[0],
        start_epoch=start_epoch,
        end_epoch=end_epoch,
        nominal_ymin=-abs(nominal_ylim),
        nominal_ymax=+abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xlabel="",
        ylabel="Radial [m]",
        title=title,
    )
    configure_diff_plot(
        axes=ax[1],
        start_epoch=start_epoch,
        end_epoch=end_epoch,
        nominal_ymin=-abs(nominal_ylim),
        nominal_ymax=+abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xlabel="",
        ylabel="Along-track [m]",
        title="",
    )
    configure_diff_plot(
        axes=ax[2],
        start_epoch=start_epoch,
        end_epoch=end_epoch,
        nominal_ymin=-abs(nominal_ylim),
        nominal_ymax=+abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xlabel="Time",
        ylabel="Cross-track [m]",
        title="",
    )

    plt.legend(svs, ncol=8, loc="upper center", bbox_to_anchor=(0.5, -0.3))
    plt.close()

    return fig


def plot_clk_diff(
    diff_df: pd.DataFrame,
    svs: list[str],
    title: str,
    start_epoch: datetime,
    end_epoch: datetime,
    nominal_ylim: float,
    fix_ylim: bool,
) -> Union[Figure, None]:
    """
    Plot clock differences from a Pandas DataFrame.

    :param pd.DataFrame diff_df: The Pandas DataFrame containing clock differences
    :param list[str] svs: Satellite list to plot differences for
    :param str title: Figure title
    :param datetime start_epoch: Start of epoch time
    :param datetime end_epoch: End of epoch time
    :param float nominal_ylim: Nominal Y-axis plotting limit (used as ±limit) in nanoseconds.
    :param bool fix_ylim: Fix Y-axis limit to nominal value.
            If False, the Y-axis limit will be automatically set when any data points exceed the nominal range.
    :return Figure: The Figure object for the plot
    """
    # Filter data with given satellite list and unstack the dataframe to push the satellite PRNs
    # from the index to columns as it's easier to plot
    svs = filter_svs_list(svs, diff_df)
    if not svs:
        return None

    unstacked_diff_df = diff_df[diff_df.index.get_level_values("Satellite").isin(svs)].unstack()

    # Plot epoch-by-epoch clock comparison results
    fig, ax = plt.subplots(dpi=300.0, figsize=(12, 3))

    ax.plot(unstacked_diff_df["Clock"].index.values, unstacked_diff_df["Clock"].values)

    configure_diff_plot(
        axes=ax,
        start_epoch=start_epoch,
        end_epoch=end_epoch,
        nominal_ymin=-abs(nominal_ylim),
        nominal_ymax=+abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xlabel="Time",
        ylabel="Clock [ns]",
        title=title,
    )

    plt.legend(svs, ncol=8, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    plt.close()

    return fig


def plot_orb_rms(
    stats_df: pd.DataFrame, svs: list[str], title: str, nominal_ylim: float, fix_ylim: bool
) -> Union[Figure, None]:
    """
    Plot orbit RMS errors from a Pandas DataFrame.

    :param pd.DataFrame stats_df: The Pandas DataFrame containing orbit statistics
    :param list[str] svs: Satellite list to plot orbit RMS errors for
    :param str title: Figure title
    :param float nominal_ylim: Nominal Y-axis plotting limit (used as 0 to +limit) in metres.
    :param bool fix_ylim: Fix Y-axis limit to nominal value.
            If False, the Y-axis limit will be automatically set when any data points exceed the nominal range.
    :return Figure: The Figure object for the plot
    """
    svs = filter_svs_list(svs, stats_df)
    if not svs:
        return None

    # Extract data for Radial, Along-track, and Cross-track RMS
    rms = {}
    for sat in svs:
        rms[sat] = {dim: stats_df.loc[(sat, "rms"), dim] for dim in ["Radial", "Along-track", "Cross-track"]}
    rms_all = {
        dim: round(stats_df.loc[("All", "rms"), dim], 3) for dim in ["Radial", "Along-track", "Cross-track"]
    }  # TODO Eugene: RMS/statistics by constellation

    # Plot Radial, Along-track, and Cross-track RMS of each satellite
    fig, ax = plt.subplots(dpi=300.0, figsize=(12, 3))

    bar_width = 0.2
    x = np.arange(len(svs))

    for i, dim in enumerate(["Radial", "Along-track", "Cross-track"]):
        pos = x + (i - 1) * bar_width
        ax.bar(pos, [rms[sat][dim] for sat in svs], bar_width, label=dim)

    configure_rms_plot(
        axes=ax,
        xdata=x,
        nominal_ymin=0,
        nominal_ymax=abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xticklabels=svs,
        xlabel="Satellite",
        ylabel="RMS [m]",
        annotation=f'All satellites: R={rms_all["Radial"]}, A={rms_all["Along-track"]}, C={rms_all["Cross-track"]} m',
        title=title,
    )

    plt.close()

    return fig


def plot_clk_rms(
    stats_df: pd.DataFrame, svs: list[str], title: str, nominal_ylim: float, fix_ylim: bool
) -> Union[Figure, None]:
    """
    Plot clock RMS errors from a Pandas DataFrame.

    :param pd.DataFrame stats_df: The Pandas DataFrame containing clock statistics
    :param list[str] svs: Satellite list to plot clock RMS errors for
    :param str title: Figure title
    :param float nominal_ylim: Nominal Y-axis plotting limit (used as 0 to +limit) in nanoseconds.
    :param bool fix_ylim: Fix Y-axis limit to nominal value.
            If False, the Y-axis limit will be automatically set when any data points exceed the nominal range.
    :return Figure: The Figure object for the plot
    """
    svs = filter_svs_list(svs, stats_df)
    if not svs:
        return None

    # Extract data for Clock
    rms = {}
    for sat in svs:
        rms[sat] = {"Clock": stats_df.loc[(sat, "rms"), "Clock"]}
    rms_all = {"Clock": round(stats_df.loc[("All", "rms"), "Clock"], 3)}  # TODO Eugene: RMS/statistics by constellation

    # Plot Clock RMS of each satellite
    fig, ax = plt.subplots(dpi=300.0, figsize=(12, 3))

    bar_width = 0.2
    x = np.arange(len(svs))

    ax.bar(x, [rms[sat]["Clock"] for sat in svs], bar_width, label="Clock")

    configure_rms_plot(
        axes=ax,
        xdata=x,
        nominal_ymin=0,
        nominal_ymax=abs(nominal_ylim),
        fix_ylim=fix_ylim,
        xticklabels=svs,
        xlabel="Satellite",
        ylabel="RMS [ns]",
        annotation=f'All satellites: {rms_all["Clock"]} ns',
        title=title,
    )

    plt.close()

    return fig


def plot_orbits(
    diff_df: pd.DataFrame,
    stats_df: pd.DataFrame,
    sys_name: str,
    sys_svs: list[str],
    start_epoch: datetime,
    end_epoch: datetime,
    nominal_ylim: float,
    fix_ylim: bool,
    diff_plot_title: str,
    rms_plot_title: str,
    diff_plot_path: Path,
    rms_plot_path: Path,
) -> None:
    """
    Plot orbit differences and RMS errors.

    :param pd.DataFrame diff_df: The Pandas DataFrame containing orbit differences
    :param pd.DataFrame stats_df: The Pandas DataFrame containing orbit statistics
    :param str sys_name: Name of the satellite system to plot orbits
    :param list[str] sys_svs: Satellite list of the satellite system to plot orbits
    :param datetime start_epoch: Start of epoch time
    :param datetime end_epoch: End of epoch time
    :param float nominal_ylim: Nominal Y-axis plotting limit in metres.
            Used as ±limit for orbit differences, and 0 to +limit for RMS errors.
    :param bool fix_ylim: Fix Y-axis limits of orbit plots to nominal value.
            If False, the Y-axis limits will be automatically set when any data points exceed the nominal ranges.
    :param str diff_plot_title: Figure title of orbit differences
    :param str rms_plot_title: Figure title of orbit RMS errors
    :param Path diff_plot_path: Path to save the orbit difference plot
    :param Path rms_plot_path: Path to save the orbit RMS plot
    :return None
    """
    # Plot epoch-by-epoch orbit differences
    logging.info(f"-- Orbit differences - {sys_name}")

    fig = plot_orb_diff(diff_df, sys_svs, diff_plot_title, start_epoch, end_epoch, nominal_ylim, fix_ylim)
    if fig:
        fig.savefig(diff_plot_path, bbox_inches="tight")

    # Plot orbit RMS errors during the whole session
    logging.info(f"-- Orbit RMS - {sys_name}")

    fig = plot_orb_rms(stats_df, sys_svs, rms_plot_title, nominal_ylim, fix_ylim)
    if fig:
        fig.savefig(rms_plot_path, bbox_inches="tight")


def plot_clocks(
    diff_df: pd.DataFrame,
    stats_df: pd.DataFrame,
    sys_name: str,
    sys_svs: list[str],
    start_epoch: datetime,
    end_epoch: datetime,
    nominal_ylim: float,
    fix_ylim: bool,
    diff_plot_title: str,
    rms_plot_title: str,
    diff_plot_path: Path,
    rms_plot_path: Path,
) -> None:
    """
    Plot clock differences and RMS errors.

    :param pd.DataFrame diff_df: The Pandas DataFrame containing clock differences
    :param pd.DataFrame stats_df: The Pandas DataFrame containing clock statistics
    :param str sys_name: Name of the satellite system to plot clocks
    :param list[str] sys_svs: Satellite list of the satellite system to plot clocks
    :param datetime start_epoch: Start of epoch time
    :param datetime end_epoch: End of epoch time
    :param float nominal_ylim: Nominal Y-axis plotting limit in nanoseconds.
            Used as ±limit for clock differences, and 0 to +limit for RMS errors.
    :param bool fix_ylim: Fix Y-axis limits of clock plots to nominal value.
            If False, the Y-axis limits will be automatically set when any data points exceed the nominal ranges.
    :param str diff_plot_title: Figure title of clock differences
    :param str rms_plot_title: Figure title of clock RMS errors
    :param Path diff_plot_path: Path to save the clock difference plot
    :param Path rms_plot_path: Path to save the clock RMS plot
    :return None
    """
    # Plot epoch-by-epoch clock differences
    logging.info(f"-- Clock differences - {sys_name}")

    fig = plot_clk_diff(diff_df, sys_svs, diff_plot_title, start_epoch, end_epoch, nominal_ylim, fix_ylim)
    if fig:
        fig.savefig(diff_plot_path, bbox_inches="tight")

    # Plot clock RMS errors during the whole session
    logging.info(f"-- Clock RMS - {sys_name}")

    fig = plot_clk_rms(stats_df, sys_svs, rms_plot_title, nominal_ylim, fix_ylim)
    if fig:
        fig.savefig(rms_plot_path, bbox_inches="tight")


def analyse_orbit_clock(
    job_dir: Path,
    ref_dir: Path,
    sub_job_list: list[str],
    ref_prefix: str,
    file_types: list[str],
    start_date: datetime,
    session_len: int,
    sat_sys: str,
    excluded_svs: list[str],
    orb_ref_frame: str,
    orb_hlm_mode: str,
    epochwise_hlm: bool,
    clk_norm_types: list[str],
    rel_output_dir: Path,
    nominal_orb_ylim: float,
    nominal_clk_ylim: float,
    fix_ylim: bool,
) -> None:
    """
    Compare orbits and clocks against reference products and plot differences and RMS errors.

    :param Path job_dir: Directory where data is processed
    :param Path ref_dir: Directory where reference products are placed
    :param list[str] sub_job_list: Sub jobs (which should be the names of sub folders in the job directory) to analyse.
            All sub jobs will be processed when empty
    :param str ref_prefix: Prefix of reference products, e.g. 'IGS0OPSRAP'
    :param list[str] file_types: File types to analyse, 'SP3' and/or 'CLK'
    :param datetime start_date: Start of date period (datetime) to analyse data
    :param int session_len: Length of each analysis session
    :param str sat_sys: Satellite systems of orbits and clocks to analyse
    :param list[str] excluded_svs: Satellites to exclude
    :param str orb_hlm_mode: Helmert transformation to apply to orbits. Can be None, 'ECF', or 'ECI'
    :param bool epochwise_hlm: Epochwise Helmert transformation
    :param list[str] clk_norm_types: Normalizations to apply to clocks. Available options include
            'epoch', 'daily', 'sv', any satellite PRN, or any combination of them
    :param Path rel_output_dir: Relative path of output directory under each sub job directory
    :param float nominal_orb_ylim: Nominal Y-axis plotting limit in metres.
            Used as ±limit for orbit differences, and 0 to +limit for RMS errors.
    :param float nominal_clk_ylim: Nominal Y-axis plotting limit in nanoseconds.
            Used as ±limit for clock differences, and 0 to +limit for RMS errors.
    :param bool fix_ylim: Fix Y-axis limits of orbit and clock plots to nominal values.
            If False, the Y-axis limits will be automatically set when any data points exceed the nominal ranges.
    :return None
    """
    # Set matplotlib font and colormap
    set_up_matplotlib("DejaVu Sans", "jet")

    # Get session dates
    dates = [start_date + timedelta(days=i) for i in range(session_len)]
    yrdoys = [date.strftime("%Y%j") for date in dates]
    start_yrdoy = yrdoys[0]

    # Create a full satellite list for each constellation
    svs = {}
    for sys in sat_sys:
        svs[sys] = [
            f"{sys}%02d" % i for i in range(1, sys_meta[sys]["max_sats"] + 1) if f"{sys}%02d" % i not in excluded_svs
        ]

    hlm = orb_hlm_mode if orb_hlm_mode else "none"
    norm = "_".join(clk_norm_types) if clk_norm_types else "none"

    # Download reference sp3 and clock files
    start_epoch = dates[0]
    end_epoch = dates[-1] + timedelta(days=1)

    sampling_rate = {}
    for file_type in file_types:
        download_ref_products(ref_dir, ref_prefix, file_type, start_epoch, end_epoch, sampling_rate)

    # TODO: call Ginan to convert ECEF SP3 files to ECI SP3 files

    if not sub_job_list:
        sub_job_list = [
            f.name for f in job_dir.iterdir() if f.is_dir()
        ]  # get all sub folders when sub_job_list is empty

    for sub_job_name in sub_job_list:
        # Set up output directory
        output_dir = job_dir / sub_job_name / rel_output_dir
        ga.gn_utils.ensure_folders([output_dir])

        if "SP3" in file_types:
            # Compare sp3 using gnssanalysis
            logging.info("Comparing SP3 files ...")

            input_paths = generate_input_paths(
                job_dir, ref_dir, sub_job_name, ref_prefix, yrdoys, sampling_rate, "SP3", orb_ref_frame
            )

            sp3_diff = compare_sp3_files(
                input_paths,
                output_dir / f"diff_{start_yrdoy}_{session_len}D_SP3_{hlm}_{norm}.csv",
                svs,
                orb_ref_frame,
                orb_hlm_mode,
                epochwise_hlm,
                clk_norm_types,
            )

            if not sp3_diff.empty:
                # Compute statistics
                logging.info("Computing statistics of SP3 differences ...")

                sp3_stats = compute_stats(
                    sp3_diff, output_dir / f"stats_{start_yrdoy}_{session_len}D_SP3_{hlm}_{norm}.csv"
                )

                # Plot sp3 comparison results
                logging.info("Plotting SP3 comparison results ...")

                for sys in sat_sys:
                    sys_name = sys_meta[sys]["name"]
                    sys_svs = svs[sys]

                    title = f"Satellite Orbit Comparison (gnssanalysis): {sub_job_name} vs {ref_prefix}"
                    diff_plot_path = output_dir / f"diff_{start_yrdoy}_{session_len}D_ORB_{sys}_{hlm}.png"
                    rms_plot_path = output_dir / f"rms_{start_yrdoy}_{session_len}D_ORB_{sys}_{hlm}.png"
                    plot_orbits(
                        sp3_diff,
                        sp3_stats,
                        sys_name,
                        sys_svs,
                        start_epoch,
                        end_epoch,
                        nominal_orb_ylim,
                        fix_ylim,
                        title,
                        title,
                        diff_plot_path,
                        rms_plot_path,
                    )

                    title = f"Satellite Clock Comparison (gnssanalysis): {sub_job_name} vs {ref_prefix}"
                    diff_plot_path = output_dir / f"diff_{start_yrdoy}_{session_len}D_CLK_{sys}_{norm}.png"
                    rms_plot_path = output_dir / f"rms_{start_yrdoy}_{session_len}D_CLK_{sys}_{norm}.png"
                    plot_clocks(
                        sp3_diff,
                        sp3_stats,
                        sys_name,
                        sys_svs,
                        start_epoch,
                        end_epoch,
                        nominal_clk_ylim,
                        fix_ylim,
                        title,
                        title,
                        diff_plot_path,
                        rms_plot_path,
                    )

        if "CLK" in file_types:
            # Compare clocks using gnssanalysis
            logging.info("Comparing CLK files ...")

            input_paths = generate_input_paths(job_dir, ref_dir, sub_job_name, ref_prefix, yrdoys, sampling_rate, "CLK")

            clk_diff = compare_clk_files(
                input_paths, output_dir / f"diff_{start_yrdoy}_{session_len}D_CLK_{norm}.csv", svs, clk_norm_types
            )

            if not clk_diff.empty:
                # Compute statistics
                logging.info("Computing statistics of CLK differences ...")

                clk_stats = compute_stats(clk_diff, output_dir / f"stats_{start_yrdoy}_{session_len}D_CLK_{norm}.csv")

                # Plot clock comparison results
                logging.info("Plotting CLK comparison results ...")

                for sys in sat_sys:
                    sys_name = sys_meta[sys]["name"]
                    sys_svs = svs[sys]

                    title = f"Satellite Clock Comparison (gnssanalysis): {sub_job_name} vs {ref_prefix}"
                    diff_plot_path = output_dir / f"diff_{start_yrdoy}_{session_len}D_CLK_{sys}_{norm}.png"
                    rms_plot_path = output_dir / f"rms_{start_yrdoy}_{session_len}D_CLK_{sys}_{norm}.png"
                    plot_clocks(
                        clk_diff,
                        clk_stats,
                        sys_name,
                        sys_svs,
                        start_epoch,
                        end_epoch,
                        nominal_clk_ylim,
                        fix_ylim,
                        title,
                        title,
                        diff_plot_path,
                        rms_plot_path,
                    )

        logging.info("Orbit and clock comparison done\n")


@click.command()
@click.option("--job-dir", required=True, help="Directory where data is processed", type=Path)
@click.option("--ref-dir", required=True, help="Directory where reference products are placed", type=Path)
@click.option(
    "--sub-jobs",
    help="Sub jobs (which should be the names of sub folders in the job directory) to analyse. All sub jobs will be processed if not specified. Default: None",
    default=None,
    type=str,
)
@click.option(
    "--ref-prefix",
    required=True,
    help="Prefix of reference products. Default: 'IGS0OPSRAP'",
    default="IGS0OPSRAP",
    type=str,
)
@click.option(
    "--file-types",
    required=True,
    help="File types to analyse, 'SP3' and/or 'CLK'. Default: 'SP3, CLK'",
    default="SP3, CLK",
    type=str,
)
@click.option(
    "--start-yrdoy",
    help="Start of date period (day-of-year) to analyse data for in the format of 'YYYYDDD'. Current day will be used if not set. Default: None",
    default=None,
    type=int,
)
@click.option(
    "--end-yrdoy",
    help="End of date period (day-of-year, inclusive) to analyse data for in the format of 'YYYYDDD'. Do not set for real-time mode. Default: None",
    default=None,
    type=int,
)
@click.option(
    "--session-len",
    required=True,
    help="Length of a session for each rotation period in days. If 0 or not set, no rotation (i.e. only one session) will be applied between start- and end-yrdoy. Default: 0",
    default=0,
    type=int,
)
@click.option(
    "--align-to-gps-week",
    help="Align rotation period to GPS week for weekly solutions. Only effective when session length is 7 days (weekly). Default: False",
    default=False,
    is_flag=True,
)
@click.option(
    "--sat-sys",
    required=True,
    help="Satellite system to analyse, 'G', 'R', 'E', 'C', or any combination without space, e.g. 'GREC'. Default: 'G'",
    default="G",
    type=str,
)
@click.option("--exclude", help="PRNs of satellites to exclude, e.g. 'G01, G03'. Default: None", default=None, type=str)
@click.option(
    "--orb-ref-frame",
    help="Reference frame of input orbits, either 'ECF' or 'ECI'. Default: 'ECF'",
    default="ECF",
    type=str,
)
@click.option(
    "--orb-hlm-mode",
    help="Helmert transformation to apply to orbits, 'ECF', 'ECI', or 'none'. Default: None",
    default=None,
    type=str,
)
@click.option(
    "--epochwise-hlm",
    help="Apply Helmert transformation to orbits epochwisely. Default: False",
    default=False,
    is_flag=True,
)
@click.option(
    "--clk-norm-types",
    help="Normalisations to apply to clocks, e.g. 'none', 'sv', 'G01', 'epoch, daily'. Default: None",
    default=None,
    type=str,
)
@click.option(
    "--rel-output-dir",
    required=True,
    help="Relative path of output directory under each sub job directory. Default: 'gnssanalysis'",
    default="gnssanalysis",
    type=Path,
)
@click.option(
    "--nominal-orb-ylim",
    help="Nominal Y-axis plotting limit in metres. Used as ±limit for orbit differences, and 0 to +limit for RMS errors. The Y-axis limits will be automatically set when any data points exceed the nominal ranges if '--fix-ylim' is not specified. Default: 0.5",
    default=0.5,
    type=float,
)
@click.option(
    "--nominal-clk-ylim",
    help="Nominal Y-axis plotting limit in nanoseconds. Used as ±limit for clock differences, and 0 to +limit for RMS errors. The Y-axis limits will be automatically set when any data points exceed the nominal ranges if '--fix-ylim' is not specified. Default: 1.5",
    default=1.5,
    type=float,
)
@click.option(
    "--fix-ylim",
    help="Fix Y-axis limits of orbit and clock plots to nominal values. If not specified, the Y-axis limits will be automatically set when any data points exceed the nominal ranges. Default: False",
    default=False,
    is_flag=True,
)
@click.option("--verbose", is_flag=True)
def analyse_orbit_clock_main(
    job_dir,
    ref_dir,
    sub_jobs,
    ref_prefix,
    file_types,
    start_yrdoy,
    end_yrdoy,
    session_len,
    align_to_gps_week,
    sat_sys,
    exclude,
    orb_ref_frame,
    orb_hlm_mode,
    epochwise_hlm,
    clk_norm_types,
    rel_output_dir,
    nominal_orb_ylim,
    nominal_clk_ylim,
    fix_ylim,
    verbose,
):
    ga.gn_utils.configure_logging(verbose)

    sub_jobs = str_to_list(sub_jobs)
    file_types = str_to_list(file_types.upper())
    excluded_svs = str_to_list(exclude)
    if orb_hlm_mode == "none":
        orb_hlm_mode = None
    clk_norm_types = str_to_list(clk_norm_types.replace("none", "")) if clk_norm_types is not None else []

    # Post-processing mode
    if end_yrdoy is not None:
        logging.info("Orbit and clock analysis in post-processing mode as '--end-yrdoy' is set")

        if start_yrdoy is None:
            logging.error("'--start-yrdoy' must be specified for post-processing mode ('--end-yrdoy' is set)")
            return
        elif start_yrdoy > end_yrdoy:
            logging.error("Start date must be no later than end date")
            return

        start_date = datetime.strptime(str(start_yrdoy), "%Y%j")
        end_date = datetime.strptime(str(end_yrdoy), "%Y%j")

        if session_len <= 0:
            session_len = (end_date - start_date).days + 1

        if align_to_gps_week and session_len == 7:
            start_date -= timedelta(
                start_date.isoweekday() % 7
            )  # round down start date to nearest Sunday (start of a GPS week)

        while start_date <= end_date:
            analyse_orbit_clock(
                job_dir,
                ref_dir,
                sub_jobs,
                ref_prefix,
                file_types,
                start_date,
                session_len,
                sat_sys,
                excluded_svs,
                orb_ref_frame,
                orb_hlm_mode,
                epochwise_hlm,
                clk_norm_types,
                rel_output_dir,
                nominal_orb_ylim,
                nominal_clk_ylim,
                fix_ylim,
            )

            start_date += timedelta(days=session_len)

    # Real-time mode
    else:
        logging.info("Orbit and clock analysis in real-time mode as '--end-yrdoy' is not set")

        if session_len <= 0:
            logging.error("'--session-len' must be specified for real-time mode ('--end-yrdoy' is not set)")
            return

        if start_yrdoy is None:
            start_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
        else:
            start_date = datetime.strptime(str(start_yrdoy), "%Y%j")

        if align_to_gps_week and session_len == 7:
            start_date -= timedelta(
                start_date.isoweekday() % 7
            )  # round down start date to nearest Sunday (start of a GPS week)

        latency = 2 * 86400  # allow 2 days of latency for reference products to be available

        while True:
            next_start_date = start_date + timedelta(days=session_len)
            end_date = next_start_date - timedelta(seconds=1)
            now = time.time()
            seconds = next_start_date.timestamp() - now + latency
            logging.debug(f"Start time of current session: {start_date}; end time of current session: {end_date}")
            logging.debug(f"{seconds} seconds to wait (for reference products to be available) to start analysis")

            if seconds > 0:
                time.sleep(seconds)

            analyse_orbit_clock(
                job_dir,
                ref_dir,
                sub_jobs,
                ref_prefix,
                file_types,
                start_date,
                session_len,
                sat_sys,
                excluded_svs,
                orb_ref_frame,
                orb_hlm_mode,
                epochwise_hlm,
                clk_norm_types,
                rel_output_dir,
                nominal_orb_ylim,
                nominal_clk_ylim,
                fix_ylim,
            )

            start_date = next_start_date


if __name__ == "__main__":
    analyse_orbit_clock_main()
