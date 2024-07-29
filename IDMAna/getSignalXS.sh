#!/bin/bash

rm signalXS.dat


for bp in `seq 1 20`; do
    myres=`grep "Cross-section :" ../../MG5prod/h2h2ll/ECM240_BP${bp}/condor.out | tail -n 1 | awk '{print $3}'`
    numevt=`grep "Nb of events" ../../MG5prod/h2h2ll/ECM240_BP${bp}/condor.out | tail -n 1 | awk '{print $5}'`
    whhll[${bp}]=${myres}/${numevt}
    myres=`grep "Cross-section :" ../../MG5prod/h2h2llvv/ECM240_BP${bp}/condor.out | tail -n 1 | awk '{print $3}'`
    numevt=`grep "Nb of events" ../../MG5prod/h2h2llvv/ECM240_BP${bp}/condor.out | tail -n 1 | awk '{print $5}'`
    whhllvv[${bp}]=${myres}/${numevt}
done

echo "${whhll[*]}"
echo "${whhllvv[*]}"

for datadir in "h2h2ll" "h2h2llvv"; do
    for ecm in 240 365;
    do
	for bp in `seq 1 20`; do
	    myres=`grep "Cross-section :" ../../MG5prod/${datadir}/ECM${ecm}_BP${bp}/condor.out | tail -n 1 | awk '{print $3}'`
	    numevt=`grep "Nb of events" ../../MG5prod/${datadir}/ECM${ecm}_BP${bp}/condor.out | tail -n 1 | awk '{print $5}'`
	    #echo $datadir" ECM " $ecm " BP "$bp" xs = "$myres  >> signalXS.dat
	    echo "\"e${ecm}_bp${bp}_${datadir}\":{\"numberOfEvents\": $numevt, \"sumOfWeights\": $numevt, \"crossSection\":  $myres, \"kfactor\": 1.0, \"matchingEfficiency\": 1.0},"  >> signalXS.dat

	done
    done
done

cat signalXS.dat
