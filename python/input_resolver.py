'''Shared input resolution for local paths, CERN EOS mounts and XRootD URLs.

Discovery keeps only immediate .root files, sorted and deduplicated. For mixed
inputs, a path ending in .root is a file; every other path is a directory.
'''

import os
import subprocess
from urllib.parse import urlsplit


class InputResolutionError(ValueError):
    '''An input path cannot be resolved.'''


def normalize_input_path(path: str) -> str:
    '''Normalize a string path; configuration types are checked by the caller.'''
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
    if path == '/eos' or path.startswith('/eos/'):
        return _eos_url(path)
    return path


def _eos_url(path: str) -> str:
    '''Translate the EOS input namespaces used by the repository examples.'''
    if path.startswith('/eos/experiment/fcc/'):
        host = 'eospublic.cern.ch'
    elif path.startswith('/eos/user/'):
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


def resolve_directory(directory: str) -> list[str]:
    '''Find immediate ROOT files in a local, mounted EOS or remote directory.'''
    path = normalize_input_path(directory)
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
    return sorted(set(files))


def resolve_inputs(paths: list[str]) -> list[str]:
    '''Expand directories; leave individual file access checks to the reader.'''
    files = []
    for value in paths:
        path = normalize_input_path(value)
        if not path.endswith('.root'):
            files.extend(resolve_directory(path))
        else:
            files.append(path)
    return sorted(set(files))


def read_input_file_list(filename: str) -> list[str]:
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
                paths.append(normalize_input_path(path))
    except (OSError, UnicodeError) as error:
        raise InputResolutionError(
            f'Cannot read input list {filename!r}: {error}.'
        ) from error
    if not paths:
        raise InputResolutionError(f'Input file list {filename!r} is empty.')
    return sorted(set(paths))
