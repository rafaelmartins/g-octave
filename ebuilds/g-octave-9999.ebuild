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
IUSE="colors"

DEPEND="<dev-lang/python-3"
RDEPEND="${DEPEND}
	sys-apps/portage
	dev-python/simplejson
	colors? ( dev-python/pycolors )"

S="${WORKDIR}/${PN}"

DOCS="README.rst"

src_prepare() {
	if ! use colors; then
		sed -i -e 's/from colors .*/raise/' scripts/g-octave \
			|| die 'sed failed.'
	fi
}
