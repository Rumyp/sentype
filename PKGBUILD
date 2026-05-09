pkgname=sentype
pkgver=0.2.1
pkgrel=1
pkgdesc="SenType — simple terminal typing game"
arch=('any')
url="https://github.com/rumyp/sentype"
license=('MIT')
depends=('python')
source=("https://github.com/rumyp/sentype/archive/refs/tags/${pkgver}.tar.gz")
sha256sums=('448de9bd94b1709c72c5c0a26e7cd0f9ba936e29bfbd8f098989a310504c5473')

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
