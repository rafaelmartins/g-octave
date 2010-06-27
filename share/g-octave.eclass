# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

#
# Original Author: Rafael G. Martins <rafael@rafaelmartins.eng.br>
# Purpose: Build Octave-Forge packages automatically using the new-style package
# manager
#

HOMEPAGE="http://octave.sourceforge.net/"
SLOT="0"
LICENSE="GPL-2"
DESCRIPTION="Based on the ${ECLASS} eclass"

# check for octave needed version
if [[ -n "${NEED_OCTAVE}" ]]; then
	OCT_ATOM=">=sci-mathematics/octave-${NEED_OCTAVE}"
else
	OCT_ATOM="sci-mathematics/octave"
fi

# defining some paths
OCT_ROOT="/usr/share/octave"
OCT_PKGDIR="${OCT_ROOT}/packages"
OCT_BIN="$(type -p octave)"

# fixing dependencies
DEPEND="${DEPEND} ${OCT_ATOM}"
RDEPEND="${RDEPEND} ${OCT_ATOM}"

# our packages begin with "octave-forge-". we need to remove this
# to get the raw ${P}
OCT_P=${P#octave-forge-}

S="${WORKDIR}/${OCT_P}"

EXPORT_FUNCTIONS src_install pkg_postinst pkg_prerm pkg_postrm

dist_admin() {
	echo ${OCT_PKGDIR}/${OCT_P}/packinfo/dist_admin
}

g-octave_src_install() {
	emake DESTDIR="${D}" DISTPKG='Gentoo' install
	if [ -d doc/ ]; then
		insinto /usr/share/doc/${PF}
		doins -r doc/* || die 'failed to install the docs'
	fi
}

g-octave_pkg_postinst() {
	einfo "Registering ${CATEGORY}/${PF} on the Octave package database."
	$(dist_admin) install &> /dev/null || die 'failed to register the package.'
}

g-octave_pkg_prerm() {
	einfo 'Running on_uninstall routines to prepare the package to remove.'
	$(dist_admin) &> /dev/null || die 'failed to prepare to uninstall.'
}

g-octave_pkg_postrm() {
	einfo 'Rebuilding the Octave package database.'
	[ -d ${OCT_PKGDIR} ] || mkdir -p ${OCT_PKGDIR}
	${OCT_BIN} -H --silent --eval 'pkg rebuild' &> /dev/null
}
