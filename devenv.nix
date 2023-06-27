{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "Discox";

  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  # https://devenv.sh/scripts/
  scripts.hello.exec = "$GREET Development Environment";

  services.mysql = {
      enable = true;
      package = pkgs.mariadb;
  };

  enterShell = ''
    clear
    echo "Discox Development Environment"
    python --version
    mariadb --version
    echo "Python packages in environment: "
    poetry show
  '';

  # https://devenv.sh/languages/
  # languages.nix.enable = true;

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
