# Maintainer: Keith Henderson <keith.donaldh@gmail.com>
pkgname=piperss
pkgver=0.1.6
pkgrel=1
pkgdesc="A minimalistic terminal-based RSS reader"
arch=('any')
url="https://github.com/lairizzle/piperss"
license=('MIT')
depends=('python' 'python-rich' 'python-requests' 'python-feedparser' 'python-readability-lxml' 'python-html2text')
makedepends=('python-setuptools')
source=("https://files.pythonhosted.org/packages/source/p/piperss/piperss-$pkgver.tar.gz")
sha256sums=('15f3c81980870ed4be414c39d56c624fa5dec69cdbf14d6011c6c90048cd75ed')

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir" --optimize=1
}

