# Maintainer: Keith Henderson <keith.donaldh@gmail.com>
pkgname=piperss
pkgver=0.1.5
pkgrel=1
pkgdesc="A minimalistic terminal-based RSS reader"
arch=('any')
url="https://github.com/lairizzle/piperss"
license=('MIT')
depends=('python')
makedepends=('python-setuptools')
source=("https://files.pythonhosted.org/packages/source/p/piperss/piperss-$pkgver.tar.gz")
sha256sums=('9a8d290ae6c73fabfcc0daeb16d3727e7686829a2bae0f6693c30fe619a4a6f1')

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir" --optimize=1
}

