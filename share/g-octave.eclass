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


REPO_URI="https://octave.svn.sourceforge.net/svnroot/octave/trunk/octave-forge"
if [[ ${PV} = 9999* ]]; then
	inherit subversion autotools
	ESVN_REPO_URI="${REPO_URI}/${G_OCTAVE_CAT}/${PN}"
else
	inherit autotools
	SRC_URI="mirror://sourceforge/octave/${P}.tar.gz"
fi

SRC_URI="${SRC_URI}
	${REPO_URI}/packages/package_Makefile.in -> g-octave_Makefile
	${REPO_URI}/packages/package_configure.in -> g-octave_configure"

HOMEPAGE="http://www.g-octave.org/"
SLOT="0"
LICENSE="GPL-2"
DESCRIPTION="Based on the ${ECLASS} eclass"

# defining some paths
OCT_ROOT="/usr/share/octave"
OCT_PKGDIR="${OCT_ROOT}/packages"
OCT_BIN="$(type -p octave)"

EXPORT_FUNCTIONS src_prepare src_install pkg_postinst pkg_prerm pkg_postrm

g-octave_src_prepare() {
	if [ ! -d "${WORKDIR}/${P}" ]; then
		S="${WORKDIR}/${PN}"
		cd "${S}"
	fi
	[[ ${PV} = 9999* ]] && subversion_src_prepare
	for filename in Makefile configure; do
		cp "${DISTDIR}/g-octave_${filename}" "${S}/${filename}"
	done
	chmod 0755 "${S}/configure"
	if [ -e "${S}"/src/autogen.sh ]; then
		cd "${S}"/src && ./autogen.sh || die 'failed to run autogen.sh'
	fi
	sed -i 's/-s//g' ${S}/src/Makefile || die 'sed failed.'
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
	[ -d ${OCT_PKGDIR} ] || mkdir -p ${OCT_PKGDIR}
	${OCT_BIN} -H -q --no-site-file --eval "pkg('rebuild');" \
		|| die 'failed to register the package.'
}

g-octave_pkg_prerm() {
	einfo 'Running on_uninstall routines to prepare the package to remove.'
	local pkgdir=$(
		${OCT_BIN} -H -q --no-site-file --eval "
			pkg('rebuild');
			l = pkg('list');
			disp(l{cellfun(@(x)strcmp(x.name,'${PN}'),l)}.dir);
		"
	)
	rm -f "${pkgdir}"/packinfo/on_uninstall.m
	if [ -e "${pkgdir}"/packinfo/on_uninstall.m.orig ]; then
		mv "$pkgdir"/packinfo/on_uninstall.m{.orig,}
		cd "$pkgdir"/packinfo
		${OCT_BIN} -H -q --no-site-file --eval "
			l = pkg('list');
			on_uninstall(l{cellfun(@(x)strcmp(x.name,'${PN}'), l)});
		" &> /dev/null || die 'failed to remove the package'
	fi
}

g-octave_pkg_postrm() {
	einfo 'Rebuilding the Octave package database.'
	[ -d ${OCT_PKGDIR} ] || mkdir -p ${OCT_PKGDIR}
	${OCT_BIN} -H --silent --eval 'pkg rebuild' \
		&> /dev/null || die 'failed to rebuild the package database'
}
