# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI="2"

inherit distutils

MY_PV=${PV/_rc/b}
MY_P=${PN}-${MY_PV}

DESCRIPTION="A tool that generates and installs ebuilds for Octave-Forge"
HOMEPAGE="http://bitbucket.org/rafaelmartins/g-octave/"
SRC_URI="http://bitbucket.org/rafaelmartins/${PN}/downloads/${MY_P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="colors"

DEPEND="<dev-lang/python-3"
RDEPEND="${DEPEND}
	sys-apps/portage
	dev-python/simplejson
	colors? ( dev-python/pycolors )"

S="${WORKDIR}/${MY_P}"

src_prepare() {
	if ! use colors; then
		sed -i -e 's/from colors .*/raise/' scripts/g-octave \
			|| die 'sed failed.'
	fi
}
