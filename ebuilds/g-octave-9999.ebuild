# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="2"

inherit distutils mercurial

DESCRIPTION="A tool that generates and installs ebuilds for Octave-Forge"
HOMEPAGE="http://bitbucket.org/rafaelmartins/g-octave/"
EHG_REPO_URI="https://bitbucket.org/rafaelmartins/g-octave/"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS=""
IUSE=""

CDEPEND="( >=dev-lang/python-2.6 <dev-lang/python-3 )"
DEPEND="${CDEPEND}
	>=dev-python/docutils-0.6"
RDEPEND="${CDEPEND}
	|| ( >=sys-apps/portage-2.1.7[-python3] <sys-apps/portage-2.1.7 )"

S="${WORKDIR}/${PN}"

src_install() {
	distutils_src_install
	dohtml ${PN}.html
	doman ${PN}.1
}
