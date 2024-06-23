{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.python311Packages; [ websockets watchdog pyperclip pyparsing ];
  }
