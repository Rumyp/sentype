pkgname=sentype
pkgver=0.2.1
pkgrel=1
pkgdesc="SenType — simple terminal typing game"
arch=('any')
url="https://github.com/rumyp/sentype"
license=('MIT')
depends=('python')
source=("https://github.com/rumyp/sentype/releases/download/${pkgver}/sentype-${pkgver}.tar.gz")
sha256sums=('5cc79c8e823bc1136905eaed5af49efff87b56f5b2a419318e57ced3fe09ac9a')

build() { :; }

package() {
  install -d "$pkgdir/usr/share/sentype"
  if [ -d "$srcdir/sentype-${pkgver}" ]; then
    cp -r "$srcdir/sentype-${pkgver}/"* "$pkgdir/usr/share/sentype/"
  else
    cp -r "$srcdir"/* "$pkgdir/usr/share/sentype/"
  fi
  install -d "$pkgdir/usr/bin"
  cat > "$pkgdir/usr/bin/$pkgname" <<'WRAPPER'
#!/usr/bin/env bash
exec python3 /usr/share/sentype/game.py "$@"
WRAPPER
  chmod +x "$pkgdir/usr/bin/$pkgname"
}
