# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="2"

NEED_PYTHON="2.6"

inherit distutils mercurial

DESCRIPTION="A tool that generates and installs ebuilds for Octave-Forge"
HOMEPAGE="http://bitbucket.org/rafaelmartins/g-octave/"
EHG_REPO_URI="https://bitbucket.org/rafaelmartins/g-octave/"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS=""
IUSE=""

RDEPEND="sys-apps/portage[-python3]"

S="${WORKDIR}/${PN}"
