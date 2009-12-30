# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="2"

inherit distutils

DESCRIPTION="A tool that generates and installs ebuilds for Octave-Forge"
HOMEPAGE="http://bitbucket.org/rafaelmartins/g-octave/"
SRC_URI="http://bitbucket.org/rafaelmartins/${PN}/downloads/${P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND="( >=dev-lang/python-2.6 <dev-lang/python-3 )"
RDEPEND="${DEPEND}
	|| ( >=sys-apps/portage-2.1.7[-python3] <sys-apps/portage-2.1.7 )"

src_install() {
	distutils_src_install
	dohtml ${PN}.html
	doman ${PN}.1
}
