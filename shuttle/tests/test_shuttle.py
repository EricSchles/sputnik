import os

import pytest

from .. import Shuttle
from ..archive import PackageNotCompatibleException


def test_build_install_remove(command, sample_package_path, tmp_path):
    archive = command.build(sample_package_path)
    assert os.path.isfile(archive.path)

    packages = command.list()
    assert len(packages) == 0

    package = command.install(archive.path)
    assert os.path.isdir(package.path)

    packages = command.list()
    assert len(packages) == 1
    assert packages[0].ident == package.ident

    command.remove(package.name)
    assert not os.path.isdir(package.path)

    packages = command.list()
    assert len(packages) == 0


def test_install_incompatible(sample_package_path, sample_package_path2, tmp_path):
    s = Shuttle('test', '1.0.0')
    command = s.make_command(
        data_path=tmp_path,
        repository_url=os.environ.get('REPOSITORY_URL'))

    archive1 = command.build(sample_package_path)
    package1 = command.install(archive1.path)

    archive2 = command.build(sample_package_path2)
    with pytest.raises(PackageNotCompatibleException):
        package2 = command.install(archive2.path)

    packages = command.list()
    assert len(packages) == 1
    assert packages[0].ident == package1.ident


def test_install_upgrade(sample_package_path, sample_package_path2, tmp_path):
    s = Shuttle('test', '1.0.0')
    command = s.make_command(
        data_path=tmp_path,
        repository_url=os.environ.get('REPOSITORY_URL'))

    archive = command.build(sample_package_path)
    package = command.install(archive.path)

    s = Shuttle('test', '2.0.0')
    command = s.make_command(
        data_path=tmp_path,
        repository_url=os.environ.get('REPOSITORY_URL'))

    packages = command.list()
    assert len(packages) == 0
