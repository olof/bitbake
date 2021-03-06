SUMMARY = "Python bindings for the Cairo canvas library"
HOMEPAGE = "http://cairographics.org/pycairo"
BUGTRACKER = "http://bugs.freedesktop.org"
SECTION = "python-devel"
LICENSE = "LGPLv2.1 & MPLv1.1"
LIC_FILES_CHKSUM = "file://COPYING;md5=f2e071ab72978431b294a0d696327421 \
                    file://COPYING-LGPL-2.1;md5=fad9b3332be894bab9bc501572864b29 \
                    file://COPYING-MPL-1.1;md5=bfe1f75d606912a4111c90743d6c7325"

# cairo >= 1.14
DEPENDS = "cairo"

SRC_URI = "https://github.com/pygobject/pycairo/releases/download/v${PV}/pycairo-${PV}.tar.gz"

SRC_URI[md5sum] = "7390cd413271fe5569f6eef73d72bf7a"
SRC_URI[sha256sum] = "8642e36cef66acbfc02760d2b40c716f5f183d073fb063ba28fd29a14044719d"

S = "${WORKDIR}/pycairo-${PV}"

inherit setuptools3 pkgconfig

CFLAGS += "-fPIC"

BBCLASSEXTEND = "native"

do_install_append() {
    install -d ${D}${includedir}/pycairo/
    install -m 0644 ${D}${datadir}/include/pycairo/py3cairo.h ${D}${includedir}/pycairo/
}
FILES_${PN} += "${datadir}/include/pycairo/py3cairo.h"
