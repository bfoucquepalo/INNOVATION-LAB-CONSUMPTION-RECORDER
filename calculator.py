#compute statistic
myProbability = pow(5,11)/pow(6,11)
print('myProbability: ' + str(myProbability))

#constant
myShiftEnergyTransfert_kWh_B = 0.000000000152
myShiftEnergyTransfert_kWh_GB = myShiftEnergyTransfert_kWh_B * pow(1024,3)
print ('myShiftEnergyTransfert_kWh_GB: ' + str(myShiftEnergyTransfert_kWh_GB))
myPALOITEnergyTransfert_kWh_GB = 0.06

myRatioShiftPALOIT = myShiftEnergyTransfert_kWh_GB / myPALOITEnergyTransfert_kWh_GB
print ('myRatioShiftPALOIT: ' + str(myRatioShiftPALOIT))

myTraffic_GB = 1.54

energyShift_kWh = myTraffic_GB * myShiftEnergyTransfert_kWh_GB
energyPALOIT_kWh = myTraffic_GB * myPALOITEnergyTransfert_kWh_GB

print('energyShift_kWh: ' + str(energyShift_kWh))
print('energyPALOIT_kWh: ' + str(energyPALOIT_kWh))



#260-340 TWh for all datacenter: https://www.iea.org/reports/data-centres-and-data-transmission-networks
#trafiic: 150 000GB per s https://wdr2021.worldbank.org/stories/crossing-borders/
myPALOIT_GlobalDataCenterEnegry_Wh = 300*pow(10,12)
myPALOIT_GlobalTrafic_B_s = 150*pow(10,12)*3600*24*365
myPALOIT_EnergyDatacenter_kWh_B = (myPALOIT_GlobalDataCenterEnegry_Wh / myPALOIT_GlobalTrafic_B_s)/1000
myShift_EnergyDatacenter_kWh_B = 0.000000000152
myRatioDataCenter = myShift_EnergyDatacenter_kWh_B / myPALOIT_EnergyDatacenter_kWh_B
print('myRatioDataCenter (shift / Palo): ' + str(myRatioDataCenter))
print('myShift_EnergyDatacenter_kWh_B: ' + str(myShift_EnergyDatacenter_kWh_B))
print('myPALOIT_EnergyDatacenter_kWh_B: ' + str(myPALOIT_EnergyDatacenter_kWh_B))