#!/bin/bash
#
# Run this script in kossel_config repo to create symlinks in your home
# directory to the config files.


ln_to_home() {
    # create symlink with absolute paths from current directory to home
    # directory and ask if overwrite
    source=$1
    target=$2

    echo "Creating symlink $PWD/$source -> $HOME/$target..."
    mkdir -p $(dirname $HOME/$target)
    ln -n -i -s $PWD/$source $HOME/$target
}


# Printrun
ln_to_home printrun/.pronsolerc .pronsolerc


# Slic3r
# Note: don't use this double loop if you make config_templates not existing
# for all three folders.
CONFIG_TEMPLATES=("rubinstein")
FOLDERS=("filament" "print" "printer")
for config in ${CONFIG_TEMPLATES[@]}; do
    for folder in ${FOLDERS[@]}; do
        ln_to_home slic3r/$folder/${config}.ini .Slic3r/$folder/${config}.ini
    done
done


# Cura
ln_to_home cura/15.02.1 .cura/15.02.1
ln_to_home cura/15.04.3 .cura/15.04.3
ln_to_home cura/15.04.4 .cura/15.04.4
ln_to_home cura/15.04.6 .cura/15.04.6
ln_to_home cura/2.4/config/cura .config
ln_to_home cura/2.4/local_share/cura .local/share
#ln_to_home cura/15.06.03 .cura/15.06.03

