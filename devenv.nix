{ pkgs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "Discox";

  # https://devenv.sh/packages/
  packages = with pkgs; 
  [ 
    git 
    tmux
    # python3Full
  ];


  # https://devenv.sh/scripts/
  services.mysql = {
      enable = true;
      package = pkgs.mariadb;
      initialDatabases = [{ name = "discox"; }];
      ensureUsers =[
        {
            name = "discox";
            password = "YES";
            ensurePermissions = {
                "discox.*" = "ALL PRIVILEGES"; 
            };
        }
      ];
      settings = {
        mysqld = {
            max_allowed_packet = "256M";
            max_connections = "400";
        };
        mysqldump = {
            max_allowed_packet = "256M";
          };
      };
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
