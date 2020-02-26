# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# This ebuild was generated by g-octave

EAPI="3"

G_OCTAVE_CAT="extra"

inherit g-octave eutils

DESCRIPTION="This is the Extra 1 description"
HOMEPAGE="http://extra1.org"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND=">sci-mathematics/pkg4-1.0.0
	>=sci-mathematics/pkg1-4.3.2
	<sci-mathematics/pkg2-1.2.3
	sci-mathematics/pkg3"
RDEPEND="${DEPEND}
	>=sci-mathematics/octave-3.2.0"

src_prepare() {
	epatch "${FILESDIR}/001_extra1-0.0.1.patch"
	epatch "${FILESDIR}/002_extra1-0.0.1.patch"
	g-octave_src_prepare
}
