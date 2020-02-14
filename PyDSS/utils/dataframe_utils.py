
import gzip
import logging
import os
import shutil

import pandas as pd

from PyDSS.exceptions import InvalidParameter


logger = logging.getLogger(__name__)


def read_dataframe(filename, index_col=None, columns=None, parse_dates=False,
                   remove_unnamed=True, strip_column_units=False, **kwargs):
    """Convert filename to a dataframe. Supports .csv, .json, .feather.
    Handles compressed files.

    Parameters
    ----------
    filename : str
    index_col : str | int | None
        Index column name or index
    columns : list or None
        Use these columns if the file is CSV and does not define them.
    parse_dates : bool
    remove_unnamed : bool
        Remove any column that starts with "Unnamed".
    strip_column_units : bool
        Remove units from column names.
    kwargs : kwargs
        Passed to underlying library for dataframe conversion.
        Consider setting parse_dates=True if the index is a timestamp.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    FileNotFoundError
        Raised if the file does not exist.

    """
    if not os.path.exists(filename):
        raise FileNotFoundError("filename={} does not exist".format(filename))

    ext = os.path.splitext(filename)
    if ext[1] == ".gz":
        ext = os.path.splitext(ext[0])[1]
        open_func = gzip.open
    else:
        ext = ext[1]
        open_func = open

    if ext == ".csv":
        df = pd.read_csv(filename, index_col=index_col, usecols=columns,
                         parse_dates=parse_dates, **kwargs)
    elif ext == ".json":
        df = pd.read_json(filename, **kwargs)
    elif ext == ".feather":
        with open_func(filename, "rb") as f_in:
            df = feather.read_dataframe(f_in, **kwargs)
            if index_col is not None:
                df.set_index(index_col, inplace=True)
                if parse_dates:
                    df.set_index(pd.to_datetime(df.index), inplace=True)
    else:
        raise InvalidParameter(f"unsupported file extension {ext}")

    if remove_unnamed:
        cols_to_remove = [x for x in df.columns if x.startswith("Unnamed")]
        df.drop(columns=cols_to_remove, inplace=True)

    if strip_column_units:
        columns = []
        for column in df.columns:
            index = column.find(" [")
            if index != -1:
                column = column[:index]
            columns.append(column)
        df.columns = columns

    return df

def write_dataframe(df, file_path, compress=False, keep_original=False,
                    **kwargs):
    """Write the dataframe to a file with in a format matching the extension.

    Note that the feather format does not support row indices. Index columns
    will be lost for that format. If the dataframe has an index then it should
    be converted to a column before calling this function.

    Parameters
    ----------
    df : pd.DataFrame
    file_path : str
    compress : bool
    keep_original : bool
    kwargs : pass keyword arguments to underlying library

    Raises
    ------
    InvalidParameter if the file extension is not supported.
    InvalidParameter if the DataFrame index is set.

    """
    if not isinstance(df.index, pd.RangeIndex) and not \
            isinstance(df.index, pd.core.indexes.base.Index):
        raise InvalidParameter("DataFrame index must not be set")

    directory = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]

    if ext == ".csv":
        df.to_csv(file_path, **kwargs)
    elif ext == ".feather":
        df.to_feather(file_path, **kwargs)
    elif ext == ".json":
        df.to_json(file_path, **kwargs)
    else:
        raise InvalidParameter(f"unsupported file extension {ext}")

    logger.debug("Created %s", file_path)

    if compress:
        zipped_path = file_path + ".gz"
        with open(file_path, "rb") as f_in:
            with gzip.open(zipped_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        if not keep_original:
            os.remove(file_path)

        file_path = zipped_path
        logger.debug("Compressed %s", zipped_path)

    return file_path
