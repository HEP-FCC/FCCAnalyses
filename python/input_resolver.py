'''Shared input resolution for local paths, CERN EOS mounts and XRootD URLs.

Discovery sorts immediate .root files within each directory and rejects
duplicates. Explicit inputs retain their order. A path ending in .root is a
file; every other path is a directory.
'''

import os
import subprocess
from urllib.parse import urlsplit


class InputResolutionError(ValueError):
    '''An input path cannot be resolved.'''


def ensure_unique_inputs(paths: list[str]) -> None:
    '''Reject duplicate input paths within one sample.'''
    seen = set()
    for path in paths:
        if path in seen:
            raise InputResolutionError(f'Duplicate input path: {path}')
        seen.add(path)


def normalize_input_path(path: str, *,
                         use_xrootd: bool = True) -> str:
    '''Normalize a path and optionally convert EOS paths to XRootD URLs.'''
    if not path:
        raise InputResolutionError('The input path is empty.')
    if path.lower().startswith('root:') or '://' in path:
        try:
            url = urlsplit(path)
            if url.scheme != 'root':
                raise ValueError('the scheme must be root://')
            if not url.hostname:
                raise ValueError('a hostname is required')
            if not url.path.startswith('/'):
                raise ValueError('an absolute remote path is required')
        except ValueError as error:
            raise InputResolutionError(f'Malformed XRootD URL: {error}.') from error
        # Accept /path and //path; use //path in the returned URL.
        remote_path = '//' + url.path.lstrip('/')
        return f'root://{url.netloc}{remote_path}'

    path = os.path.abspath(os.path.expanduser(path))
    if (path == '/eos' or path.startswith('/eos/')) and use_xrootd:
        return eos_to_xrootd(path)
    return path


def join_input_path(directory: str, child: str, *,
                    use_xrootd: bool = True) -> str:
    '''Join a child path to a local directory or XRootD URL.'''
    path = normalize_input_path(
        directory, use_xrootd=use_xrootd
    )
    if path.startswith('root://'):
        return path.rstrip('/') + '/' + child
    return os.path.join(path, child)


def eos_to_xrootd(path: str) -> str:
    '''Convert a CERN EOS path to its XRootD URL, regardless of local mounts.'''
    if path == '/eos/experiment' or path.startswith('/eos/experiment/'):
        host = 'eospublic.cern.ch'
    elif path == '/eos/user' or path.startswith('/eos/user/'):
        host = 'eosuser.cern.ch'
    elif path == '/eos/project' or path.startswith('/eos/project/'):
        host = 'eosproject.cern.ch'
    elif path.startswith('/eos/home-'):
        initial, _, remainder = path[len('/eos/home-'):].partition('/')
        path = f'/eos/user/{initial}/{remainder}'
        host = 'eosuser.cern.ch'
    else:
        raise InputResolutionError(
            f'Cannot infer an EOS redirector for {path!r}. '
            'Provide root://<host>//<remote-path> explicitly.'
        )
    return f'root://{host}/{path}'


def _list_remote_files(path: str) -> list[str]:
    url = urlsplit(path)
    directory = '/' + url.path.lstrip('/')
    try:
        result = subprocess.run(
            ['xrdfs', url.netloc, 'ls', '-l', directory],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or 'xrdfs failed').strip()
        raise InputResolutionError(
            f'Cannot list {directory!r} on {url.hostname}: {detail}. '
            'Check the path, network access and storage credentials.'
        ) from error

    files = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        # Separate listing metadata from the absolute path, preserving spaces.
        metadata, _separator, filename = line.partition('/')
        filename = '/' + filename

        if not metadata.lstrip().startswith('-'):
            continue
        if not filename.endswith('.root'):
            continue
        files.append(f'root://{url.netloc}/{filename}')
    return files


def resolve_directory(directory: str, *,
                      use_xrootd: bool = True) -> list[str]:
    '''Find immediate ROOT files in a local, mounted EOS or remote directory.'''
    path = normalize_input_path(
        directory, use_xrootd=use_xrootd
    )
    if path.startswith('root://'):
        files = _list_remote_files(path)
    else:
        try:
            files = []
            for name in os.listdir(path):
                filename = os.path.join(path, name)
                if name.endswith('.root') and os.path.isfile(filename):
                    files.append(filename)
        except OSError as error:
            raise InputResolutionError(
                f'Cannot read directory {path!r}: {error}.'
            ) from error
    if not files:
        raise InputResolutionError(
            'Input directory contains no immediate .root files. '
            'Check the path; subdirectories are not searched.'
        )
    ensure_unique_inputs(files)
    return sorted(files)


def resolve_inputs(paths: list[str], *,
                   use_xrootd: bool = True) -> list[str]:
    '''Expand directories; leave individual file access checks to the reader.'''
    files = []
    for value in paths:
        path = normalize_input_path(
            value, use_xrootd=use_xrootd
        )
        if not path.endswith('.root'):
            files.extend(resolve_directory(
                path, use_xrootd=use_xrootd
            ))
        else:
            files.append(path)
    ensure_unique_inputs(files)
    return files


def read_input_file_list(filename: str, *,
                         use_xrootd: bool = True) -> list[str]:
    '''Read explicit files, ignoring blanks and full-line comments.
    Relative entries use the working directory, matching the existing runner.
    '''
    try:
        with open(filename, encoding='utf-8') as source:
            paths = []
            for line in source:
                path = line.strip()
                if not path or path.startswith('#'):
                    continue
                paths.append(normalize_input_path(
                    path, use_xrootd=use_xrootd
                ))
    except (OSError, UnicodeError) as error:
        raise InputResolutionError(
            f'Cannot read input list {filename!r}: {error}.'
        ) from error
    if not paths:
        raise InputResolutionError(f'Input file list {filename!r} is empty.')
    ensure_unique_inputs(paths)
    return paths
