# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:21:53 2019

@author: GEORGEDICKINSON
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:06:06 2019

@author: GEORGEDICKINSON
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

#get all csv files in folder
filePath_25 = r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\luca\2020-10-5_dNAM_LS_LP25pc_002_locs.csv"
filePath_100 = r"C:\Users\g_dic\OneDrive\Desktop\BSU_DATA\luca\2020-10-5_dNAM_LS_LP100pc_002_locs.csv"
name_25 = os.path.basename(filePath_25)
name_100 = os.path.basename(filePath_100)

#get data
locs_25 = pd.read_csv(filePath_25)
locs_100 = pd.read_csv(filePath_100)

#see head
#print(locs_25.head(n=5))
columnNames = locs_25.columns.values.tolist()
print(columnNames)

#rename columns
locs_25.rename(index=str, columns={'x [nm]': 'x_nm',
                              'y [nm]': 'y_nm',
                              'sigma [nm]': 'sigma_nm',
                              'intensity [photon]': 'intensity_photon',
                              'offset [photon]':'offset_photon',
                              'bkgstd [photon]':'bkgstd_photon',
                              'uncertainty [nm]': 'uncertainty_xy_nm'}, inplace=True)

locs_100.rename(index=str, columns={'x [nm]': 'x_nm',
                              'y [nm]': 'y_nm',
                              'sigma [nm]': 'sigma_nm',
                              'intensity [photon]': 'intensity_photon',
                              'offset [photon]':'offset_photon',
                              'bkgstd [photon]':'bkgstd_photon',
                              'uncertainty [nm]': 'uncertainty_xy_nm'}, inplace=True)


fig, axs = plt.subplots(2, 1)

axs[0].hist(locs_25['intensity_photon'],bins=1000, range=(0,4000))
axs[1].hist(locs_100['intensity_photon'],bins=1000, range=(0,10000))


axs[0].set_title('laser power = 25')
axs[1].set_title('laser power = 100')

axs[1].set_xlabel('intensity_photon')
axs[0].set_xlabel('intensity_photon')
axs[0].set_ylabel('# of observations')
axs[1].set_ylabel('# of observations')

fig.tight_layout()
plt.show()


#filter dataframes by photons
locs_25_filtered = locs_25[(locs_25.intensity_photon > 200) & (locs_25.intensity_photon <500)]
locs_100_filtered = locs_100[(locs_100.intensity_photon > 350) & (locs_100.intensity_photon <1350)]


fig2, axs2 = plt.subplots(2, 1)

axs2[0].hist(locs_25_filtered['intensity_photon'],bins=1000, range=(0,4000))
axs2[1].hist(locs_100_filtered['intensity_photon'],bins=1000, range=(0,10000))

fig2.tight_layout()
plt.show()


#count number of localizations / frame
counts_25 = locs_25_filtered.groupby(['frame']).size().reset_index(name='counts')
counts_100 = locs_100_filtered.groupby(['frame']).size().reset_index(name='counts')

#plot
fig3, axs3 = plt.subplots(2, 1)
axs3[0].scatter(x=counts_25 ['frame'], y=counts_25 ['counts'])
axs3[1].scatter(x=counts_100 ['frame'], y=counts_100 ['counts'])

#axs3[0].set_xlim((0, 1000))
axs3[0].set_ylim((0, 400))

#axs3[1].set_xlim((0, 1000))
axs3[1].set_ylim((0, 400))


axs3[0].set_title('laser power = 25')
axs3[1].set_title('laser power = 100')

axs3[1].set_xlabel('frame')
axs3[0].set_xlabel('frame')
axs3[0].set_ylabel('# of localizations (count)')
axs3[1].set_ylabel('# of localizations (count)')


fig3.tight_layout()
plt.show()

#count number of photons / frame
photons_25 = locs_25_filtered.groupby(['frame']).sum()['intensity_photon'].reset_index(name='photons')
photons_100 = locs_100_filtered.groupby(['frame']).sum()['intensity_photon'].reset_index(name='photons')

#plot
fig4, axs4 = plt.subplots(2, 1)
axs4[0].scatter(x=photons_25 ['frame'], y=photons_25 ['photons'])
axs4[1].scatter(x=photons_100 ['frame'], y=photons_100 ['photons'])

#axs4[0].set_xlim((0, 1000))
axs4[0].set_ylim((0, 300000))

#axs4[1].set_xlim((0, 1000))
axs4[1].set_ylim((0, 300000))

fig4.tight_layout()
plt.show()

#mean sigma / frame
sigma_25 = locs_25_filtered.groupby(['frame']).mean()['sigma_nm'].reset_index(name='mean_sigma')
sigma_100 = locs_100_filtered.groupby(['frame']).mean()['sigma_nm'].reset_index(name='mean_sigma')

#plot
fig5, axs5 = plt.subplots(2, 1)
axs5[0].scatter(x=sigma_25 ['frame'], y=sigma_25 ['mean_sigma'])
axs5[1].scatter(x=sigma_100 ['frame'], y=sigma_100 ['mean_sigma'])

#axs5[0].set_xlim((0, 1000))
axs5[0].set_ylim((0, 150))

#axs5[1].set_xlim((0, 1000))
axs5[1].set_ylim((0, 150))

fig5.tight_layout()
plt.show()

#stdev sigma / frame
sigma_25_sd = locs_25_filtered.groupby(['frame']).std()['sigma_nm'].reset_index(name='stdev_sigma')
sigma_100_sd = locs_100_filtered.groupby(['frame']).std()['sigma_nm'].reset_index(name='stdev_sigma')

#plot
fig6, axs6 = plt.subplots(2, 1)
axs6[0].scatter(x=sigma_25_sd ['frame'], y=sigma_25_sd ['stdev_sigma'])
axs6[1].scatter(x=sigma_100_sd ['frame'], y=sigma_100_sd ['stdev_sigma'])

#axs6[0].set_xlim((0, 1000))
axs6[0].set_ylim((0, 30))

#axs6[1].set_xlim((0, 1000))
axs6[1].set_ylim((0, 30))

fig6.tight_layout()
plt.show()


#plot photons vs sigma
fig7, axs7 = plt.subplots(2, 1)
axs7[0].scatter(x=locs_25_filtered ['intensity_photon'], y=locs_25_filtered ['sigma_nm'])
axs7[1].scatter(x=locs_100_filtered ['intensity_photon'], y=locs_100_filtered ['sigma_nm'])

axs7[0].set_xlim((0, 1500))
axs7[0].set_ylim((0, 350))

axs7[1].set_xlim((0, 1500))
axs7[1].set_ylim((0, 350))


axs7[1].set_xlabel('intensity_photon')
axs7[0].set_ylabel('sigma_nm')

fig7.tight_layout()
plt.show()


#mean uncertainty_xy_nm / frame
uncertainty_25 = locs_25.groupby(['frame']).mean()['uncertainty_xy_nm'].reset_index(name='mean_uncertainty')
uncertainty_100 = locs_100.groupby(['frame']).mean()['uncertainty_xy_nm'].reset_index(name='mean_uncertainty')

#plot
fig8, axs8 = plt.subplots(2, 1)
axs8[0].scatter(x=uncertainty_25 ['frame'], y=uncertainty_25 ['mean_uncertainty'])
axs8[1].scatter(x=uncertainty_100 ['frame'], y=uncertainty_100 ['mean_uncertainty'])

#axs8[0].set_xlim((0, 1000))
axs8[0].set_ylim((0, 25))

#axs8[1].set_xlim((0, 1000))
axs8[1].set_ylim((0, 25))

axs8[0].set_title('laser power = 25')
axs8[1].set_title('laser power = 100')

axs8[1].set_xlabel('frame')
axs8[0].set_xlabel('frame')
axs8[0].set_ylabel('mean_uncertainty')
axs8[1].set_ylabel('mean_uncertainty')

fig8.tight_layout()
plt.show()

#stdev uncertainty / frame
uncertainty_25_sd = locs_25_filtered.groupby(['frame']).std()['uncertainty_xy_nm'].reset_index(name='stdev_uncertainty')
uncertainty_100_sd = locs_100_filtered.groupby(['frame']).std()['uncertainty_xy_nm'].reset_index(name='stdev_uncertainty')

#plot
fig9, axs9 = plt.subplots(2, 1)
axs9[0].scatter(x=uncertainty_25_sd ['frame'], y=uncertainty_25_sd ['stdev_uncertainty'])
axs9[1].scatter(x=uncertainty_100_sd ['frame'], y=uncertainty_100_sd ['stdev_uncertainty'])

#axs9[0].set_xlim((0, 1000))
axs9[0].set_ylim((0, 7))

#axs9[1].set_xlim((0, 1000))
axs9[1].set_ylim((0, 7))

fig9.tight_layout()
plt.show()


#plot photons vs uncertainty
fig10, axs10 = plt.subplots(2, 1)
axs10[0].scatter(x=locs_25_filtered ['intensity_photon'], y=locs_25_filtered ['uncertainty_xy_nm'])
axs10[1].scatter(x=locs_100_filtered ['intensity_photon'], y=locs_100_filtered ['uncertainty_xy_nm'])

axs10[0].set_xlim((0, 1500))
axs10[0].set_ylim((0, 75))

axs10[1].set_xlim((0, 1500))
axs10[1].set_ylim((0, 75))

axs10[0].set_title('laser power = 25')
axs10[1].set_title('laser power = 100')

axs10[1].set_xlabel('intensity_photon')
axs10[0].set_ylabel('uncertainty_xy_nm')

axs10[0].set_xlabel('intensity_photon')
axs10[1].set_ylabel('uncertainty_xy_nm')

fig10.tight_layout()
plt.show()

#plot histograms sigma
fig11, axs11 = plt.subplots(2, 1)

axs11[0].hist(locs_25_filtered['sigma_nm'],bins=1000, range=(0,500))
axs11[1].hist(locs_100_filtered['sigma_nm'],bins=1000, range=(0,500))

fig11.tight_layout()
plt.show()

#plot histograms uncertainty
fig12, axs12 = plt.subplots(2, 1)

axs12[0].hist(locs_25_filtered['uncertainty_xy_nm'],bins=1000, range=(0,50))
axs12[1].hist(locs_100_filtered['uncertainty_xy_nm'],bins=1000, range=(0,50))

fig12.tight_layout()
plt.show()

#plot histograms uncertainty
fig13, axs13 = plt.subplots(2, 1)

axs13[0].hist(locs_25['uncertainty_xy_nm'],bins=1000, range=(0,50))
axs13[1].hist(locs_100['uncertainty_xy_nm'],bins=1000, range=(0,50))

fig13.tight_layout()
plt.show()



# #export counts and photons
# dirname = os.path.dirname(filePath_25)
# name1 = name_25.split('.')[0] + '_counts.csv'
# name2 = name_25.split('.')[0] + '_photons.csv'

# savename1 = os.path.join(dirname, name1)
# savename2 = os.path.join(dirname, name2)

# counts.to_csv(savename1)
# photons.to_csv(savename2)


