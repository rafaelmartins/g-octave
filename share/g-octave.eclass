# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

#
# Original Author: Rafael G. Martins <rafael@rafaelmartins.eng.br>
# Purpose: g-octave helper eclass.
#

# @ECLASS-VARIABLE: G_OCTAVE_CAT
# @DESCRIPTION:
# the octave-forge category of the package.
G_OCTAVE_CAT="${G_OCTAVE_CAT:-main}"


if [[ ${PV} = 9999* ]]; then
	inherit subversion autotools
	ESVN_REPO_URI="https://octave.svn.sourceforge.net/svnroot/octave/trunk/"
	ESVN_PROJECT="octave-forge/${G_OCTAVE_CAT}/${PN}"
	SRC_URI="${ESVN_REPO_URI}/octave-forge/packages/package_Makefile.in
		${ESVN_REPO_URI}/octave-forge/packages/package_configure.in"
else
	SRC_URI="http://g-octave.rafaelmartins.eng.br/distfiles/octave-forge/${P}.tar.gz"
fi


HOMEPAGE="http://g-octave.rafaelmartins.eng.br/"
SLOT="0"
LICENSE="GPL-2"
DESCRIPTION="Based on the ${ECLASS} eclass"

# defining some paths
OCT_ROOT="/usr/share/octave"
OCT_PKGDIR="${OCT_ROOT}/packages"
OCT_BIN="$(type -p octave)"

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
