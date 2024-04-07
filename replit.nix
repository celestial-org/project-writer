{pkgs}: {
  deps = [
    pkgs.cacert
    pkgs.rustc
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.pkg-config
    pkgs.libffi
    pkgs.libuv
  ];
}
