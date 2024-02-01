{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    pip
    pkgs.python311Packages.websockets
    pkgs.python311Packages.watchdog
    pkgs.python311Packages.pyperclip
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
