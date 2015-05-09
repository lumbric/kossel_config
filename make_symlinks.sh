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
    ln -i -s $PWD/$source $HOME/$target
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
ln_to_home cura_15.02.1 .cura/15.02.1
