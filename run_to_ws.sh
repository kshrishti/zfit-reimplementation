#!/bin/bash
dataset=data_obs
ws=HHModel_model_all
version=v1

combineCards.py fitfail=cards_Bin1/HHModel/fitfail.txt SRBin1=cards_Bin1/HHModel/SRBin1.txt SRBin2=cards_Bin2/HHModel/SRBin2.txt SRBin3=cards_Bin3/HHModel/SRBin3.txt > ${ws}.txt

text2workspace.py ${ws}.txt -P HiggsAnalysis.CombinedLimit.hh_model:model_all --mass=125 -o ${ws}.root

echo "limit on HH xs"
combine -M AsymptoticLimits -m 125 -n ${version} ${ws}.root --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,Migrad,1:0.1