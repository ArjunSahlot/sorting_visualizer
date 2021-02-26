#!/bin/bash

download_link=https://github.com/ArjunSahlot/sorting_visualizer/archive/master.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir master.zip \
&& rm -rf master.zip \
&& mv $temporary_dir/sorting_visualizer-master $1/sorting_visualizer \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/sorting_visualizer[0m"
