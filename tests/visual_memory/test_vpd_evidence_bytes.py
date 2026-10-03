"""Index-backed CRLF compatibility must never canonicalize dirty evidence."""
import subprocess

import pytest

from visual_memory import vpd_task_lock as guard


@pytest.fixture
def indexed_file(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    subprocess.run(['git', '-C', str(tmp_path), 'config', 'core.autocrlf', 'false'], check=True)
    p = tmp_path / 'evidence.json'
    p.write_bytes(b'{"accepted":false}\n')
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'evidence.json'], check=True)
    guard._EVIDENCE_INDEX_CACHE.clear()
    return p


def test_unchanged_crlf_uses_one_index_read_and_no_repeated_git(indexed_file, monkeypatch):
    indexed_file.write_bytes(b'{"accepted":false}\r\n')
    actual = subprocess.check_output
    commands = []

    def observed(args, **kwargs):
        commands.append(args)
        return actual(args, **kwargs)

    monkeypatch.setattr(guard.subprocess, 'check_output', observed)
    assert guard.evidence_bytes(indexed_file) == b'{"accepted":false}\n'
    assert len(commands) == 2
    commands.clear()
    assert guard.evidence_bytes(indexed_file) == b'{"accepted":false}\n'
    assert commands == []


def test_dirty_crlf_is_preserved_including_the_changed_fact(indexed_file):
    changed = b'{"accepted":true}\r\n'
    indexed_file.write_bytes(changed)
    assert guard.evidence_bytes(indexed_file) == changed


def test_untracked_crlf_keeps_actual_bytes(indexed_file):
    other = indexed_file.parent / 'untracked.json'
    raw = b'{"accepted":false}\r\n'
    other.write_bytes(raw)
    assert guard.evidence_bytes(other) == raw


def test_committed_literal_crlf_keeps_exact_blob(indexed_file):
    raw = b'not-a-line-ending-contract\r\n'
    indexed_file.write_bytes(raw)
    subprocess.run(['git', '-C', str(indexed_file.parent), 'add', indexed_file.name], check=True)
    assert guard.evidence_bytes(indexed_file) == raw


def test_new_index_blob_invalidates_cached_entry(indexed_file):
    indexed_file.write_bytes(b'{"accepted":false}\r\n')
    assert guard.evidence_bytes(indexed_file) == b'{"accepted":false}\n'
    new = b'{"accepted":true}\n'
    indexed_file.write_bytes(new)
    subprocess.run(['git', '-C', str(indexed_file.parent), 'add', indexed_file.name], check=True)
    indexed_file.write_bytes(new.replace(b'\n', b'\r\n'))
    assert guard.evidence_bytes(indexed_file) == new
