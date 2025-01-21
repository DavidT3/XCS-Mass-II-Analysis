from glob import glob
import requests
from warnings import warn
import os
from datetime import datetime

release_ver = "v1.0.0"
tx_url = "https://raw.githubusercontent.com/DavidT3/XCS-Mass-Paper-I-Analysis/refs/tags/{v}/"\
    "outputs/results/sdssrm-xcs_r500_r2500_txlx.csv".format(v=release_ver)
mass_url = "https://raw.githubusercontent.com/DavidT3/XCS-Mass-Paper-I-Analysis/refs/tags/{v}/"\
    "outputs/results/sdssrm-xcs_masses.csv".format(v=release_ver)
out_txlx_samp = "sdssrm-xcs_txlx_{v}.csv".format(v=release_ver)
out_mass_samp = "sdssrm-xcs_mass_{v}.csv".format(v=release_ver)

# Clean up any existing results from an older release version (this may never be relevant as I may never have to update 
#  those results, but I like to plan ahead)
# First look for any sample files with diff versions in this directory

diff_ver_txlx = [f for f in glob(out_txlx_samp.replace(release_ver, '*')) if f != out_txlx_samp]
if len(diff_ver_txlx) != 0:
    warn("A different version(s) of the SDSSRM-XCS Tx & Lx results file than was requested ({v}) have been found, and "\
         "have been moved to the 'discarded' directory.".format(v=release_ver), stacklevel=2)
    if not os.path.exists('discarded'):
        os.makedirs('discarded')
    for f in diff_ver_txlx:
        os.rename(f, 'discarded/' + f.replace('.csv', "_"+str(datetime.now())+'.csv'))
    

diff_ver_mass = [f for f in glob(out_mass_samp.replace(release_ver, '*')) if f != out_mass_samp]
if len(diff_ver_mass) != 0:
    warn("A different version(s) of the SDSSRM-XCS mass results file than was requested ({v}) have been found, and "\
         "have been moved to the 'discarded' directory.".format(v=release_ver), stacklevel=2)
    if not os.path.exists('discarded'):
        os.makedirs('discarded')
    for f in diff_ver_mass:
        os.rename(f, 'discarded/' + f.replace('.csv', "_"+str(datetime.now())+'.csv'))

# Get the files if they don't already exist
if not os.path.exists(out_txlx_samp):
    with open(out_txlx_samp, 'wb') as f, requests.get(tx_url, stream=True) as r:
        for line in r.iter_lines():
            f.write(line+'\n'.encode())

if not os.path.exists(out_mass_samp):
    with open(out_mass_samp, 'wb') as f, requests.get(mass_url, stream=True) as r:
        for line in r.iter_lines():
            f.write(line+'\n'.encode())