# Maintainer: Keith Henderson <keith.donaldh@gmail.com>
pkgname=piperss
pkgver=0.1.4
pkgrel=1
pkgdesc="A minimalistic terminal-based RSS reader"
arch=('any')
url="https://github.com/lairizzle/piperss"
license=('MIT')
depends=('python' 'python-rich' 'python-requests' 'python-feedparser' 'python-readability-lxml' 'python-html2text')
makedepends=('python-setuptools')
source=("https://files.pythonhosted.org/packages/source/p/piperss/piperss-$pkgver.tar.gz")
sha256sums=('28c7a9b7b5e306b2edbb098425499398a0975d668f831859f381e4660b339d3d')

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir" --optimize=1
}

