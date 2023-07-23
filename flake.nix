{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                    packages = with pkgs; [ 
                        git
                        python3Full
                        poetry
                        gnumake
                        tmux
                    ];
                    services.mysql = {
                      enable = true;
                      package = pkgs.mariadb;
                      initialDatabases = [{ name = "discox"; }]; #DB for discox
                      ensureUsers =[
                        {
                            name = "discox"; #User for discox
                            password = "YES"; #Password for discox user
                            ensurePermissions = {
                                "discox.*" = "ALL PRIVILEGES"; 
                            };
                        }
                      ];
                      settings = {
                            mysqld = {
                                max_allowed_packet = "256M";
                                log_warnings = "1";
                        };
                    };
                  };
                  enterShell = ''
                    tmux new -d -s mariadb
                    tmux send-keys -t "mariadb" "devenv up" Enter
                    make init
                    clear
                    echo "Discox Development Environment"
                    echo "Python packages in environment: "
                    poetry show
                    make run
                  '';
                }
              ];
            };
        });
    };
}
