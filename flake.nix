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
                  # https://devenv.sh/reference/options/
                  packages = with pkgs; [ 
                    git
                    python3Full
                    poetry
                    gnumake
                  ];
                    
                  enterShell = ''
                       make init
                       clear
                       echo "Discox Development Environment"
                       python --version
                       mariadb --version
                       echo "Python packages in environment: "
                       poetry show
                  '';
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
                            max_allowed_packet = "2560M";
                            log_warnings = "1";
                        };
                    };
                  };
                }
              ];
            };
          });
    };
}
