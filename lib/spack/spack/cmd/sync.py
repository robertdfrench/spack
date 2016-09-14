##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse

import llnl.util.tty as tty
import spack.util.spack_yaml as syaml

import spack
import spack.cmd

from IPython import embed

description = "Implement a list of explicit specs"


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="Explicitly set number of make jobs.  Default is #cpus.")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="Don't remove the install prefix if installation fails.")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="Don't remove the build stage if installation succeeds.")
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="Display verbose build output while installing.")
    subparser.add_argument(
        '--fake', action='store_true', dest='fake',
        help="Fake install. Just remove prefix and create a fake file.")
    subparser.add_argument(
        '--dirty', action='store_true', dest='dirty',
        help="Install a package *without* cleaning the environment.")
    subparser.add_argument(
        '--dry-run', action='store_true', dest='dry_run',
        help="Explain changes, but don't apply them")
    subparser.add_argument(
        'specfile', nargs=argparse.REMAINDER,
        help="yaml file with specs of packages to install")
    subparser.add_argument(
        '--run-tests', action='store_true', dest='run_tests',
        help="Run tests during installation of a package.")

def requested_specs(specfile):
    with open(specfile) as f:
        spec_prescription = syaml.load(f)
        for spec_string in spec_prescription['specs']:
            yield spack.cmd.parse_specs([spec_string], concretize=True)[0]

def existing_specs():
    with spack.installed_db.read_transaction():
        q_args = {'installed': any, 'known': any, "explicit": True}
        return spack.installed_db.query(**q_args)

def spec_dict(specs):
    d = {}
    for spec in specs:
        k = spec.__str__()
        d[k] = spec
    return d

def dict_difference(a, b):
    c = a.copy()
    for k in b:
        if k in c:
            del c[k]
    return c

def dict_intersect(a, b):
    c = dict_difference(a, b)
    return dict_difference(a, c)

def sync(parser, args):
    if not args.specfile:
        tty.die("Point to a file containing your desired specs")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.do_checksum = False        # TODO: remove this global.

    specfile = args.specfile[0]

    existing = spec_dict(existing_specs())
    requested = spec_dict(set(requested_specs(specfile)))

    specs_by_action = {
        'remove': dict_difference(existing, requested),
        'install': dict_difference(requested, existing),
        'keep': dict_intersect(requested, existing)
    }

    if args.dry_run:
        dry_run(**specs_by_action)
    else:
        do_sync(args, **specs_by_action)

def dry_run(**kwargs):
    for action in kwargs:
        for spec_string in kwargs[action]:
            print("%s %s" % (action, spec_string))

def do_sync(args, remove={}, keep={}, install={}):
    spack.cmd.uninstall.do_uninstall(remove.values(), True)
    for spec in (keep.keys() + install.keys()):
        print("Attempting to install %s" % spec)
        for c_spec in spack.cmd.parse_specs([spec], concretize=True):
            package = spack.repo.get(c_spec)
            with spack.installed_db.write_transaction():
                package.do_install(
                    keep_prefix=args.keep_prefix,
                    keep_stage=args.keep_stage,
                    ignore_deps=False,
                    make_jobs=args.jobs,
                    run_tests=args.run_tests,
                    verbose=args.verbose,
                    fake=args.fake,
                    dirty=args.dirty,
                    explicit=True)
