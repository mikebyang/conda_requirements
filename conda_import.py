import subprocess
def condaImport(requirementFile):
    notInstalledPkgs = []

    with open(requirementFile) as reqFile:
        lines = reqFile.readlines()
        for line in lines:
            if line.find('\n') != -1:
                pkg = line[:len(line)-1]
            else:
                pkg = line

            index = pkg.find('=')
            if index == -1:
                print("Error trying to remove version number")
                notInstalledPkgs.append((pkg,"could not remove version number for this package\n"))
                continue
            pkgMod = pkg[:index]

            # check if the package has already been installed
            try:
                __import__(pkgMod)
                print("%s is already installed...\n" % pkgMod)
                continue
            except:
                print("package, %s, is not installed..." % pkgMod)

            # attempt installation of package using the version number specified
            print("trying to install %s..." % pkg)
            cmdRes = subprocess.run(["conda", "install", pkg], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            try:
                cmdRes.stdin.write(b"y")
                cmdRes.stdin.close()
            except AttributeError as ae:
                if type(cmdRes) is not subprocess.CompletedProcess:
                    print("Unexpected %s"%type(ae).__name__)
                    print(e)
                    notInstalledPkgs.append(pkg+"\t!!%s!!\n"%type(ae).__name__)
                    continue
            except Exception as e:
                print("Unexpected error occured: %s"%type(e).__name__)
                print(e)
                notInstalledPkgs.append(pkg+"\t%s\n"%type(e).__name__)
                continue

            # import using version specified failed so attempt non-version specific download
            if cmdRes.returncode:
                print("failed to install with version number...")
                print("trying to install package, %s, without version number..." % pkgMod)

                res = subprocess.run(["conda", "install", pkgMod], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                try:
                    res.stdin.write(b"y")
                    res.stdin.close()
                except AttributeError as ae:
                    if type(res) is not subprocess.CompletedProcess:
                        print("Unexpected %s"%type(e).__name__)
                        print(e)
                        continue
                except Exception as e:
                    print("Unexpected error occured: %s"%type(e).__name__)
                    print(e)
                    continue
                
                if res.returncode:
                    notInstalledPkgs.append((pkgMod,"package was not found\n"))
                    print("could not find package, %s\n" % pkgMod)
                    continue
                else:
                    print("package install was successful\n")
            else:
                print("install with version number successful\n")

    # write to file the packages that were not found
    with open("./uninstalled_pkgs.txt", "w") as f:
        f.write(f'{"Package Name":<25}Failure Reason\n')
        f.write(f'{"------------":<25}--------------\n')
        for pkgNreason in notInstalledPkgs:
            f.write(f'{"%s"%pkgNreason[0]:<25}{"%s"%pkgNreason[1]}')

# condaImport("requirements.txt")