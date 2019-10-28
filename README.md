# Package php-sodium for Software Collections

This repository contains sources for RPMs that are used
to build Software Collections for CentOS by SCLo SIG.

This branch is for libsodium-devel, dependency of php-sodium
This package only build the static library, only for EL-7

    build -bs *spec --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php72-sclo-candidate --owner=sclo  libsodium

    cbs build      sclo7-sclo-php72-sclo-el7       <above>.src.rpm

    cbs add-pkg    sclo7-sclo-php73-sclo-candidate --owner=sclo  libsodium
    cbs build      sclo7-sclo-php73-sclo-el7       <above>.src.rpm
	=> libsodium-1.0.18-0.el7
