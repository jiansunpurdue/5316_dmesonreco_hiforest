#!/bin/sh

echo "import FWCore.ParameterSet.Config as cms" > HiGenJetsCleaned_cff.py
echo "from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *" >> HiGenJetsCleaned_cff.py

# ReReco stuff for jec only
echo "import FWCore.ParameterSet.Config as cms" > HiReRecoJets_cff.py
echo "from RecoHI.HiJetAlgos.HiRecoJets_cff import *" >> HiReRecoJets_cff.py
echo "from RecoHI.HiJetAlgos.HiRecoPFJets_cff import *" >> HiReRecoJets_cff.py

for system in PbPb pp pPb
  do
  for sample in data mc mix jec
    do
    for algo in ak
      do
      for sub in Vs Pu NONE
	do
	for radius in 2 3 4 5 6 7
	  do

	  for object in PF Calo
	    do

	    subt=$sub
	    if [ $sub == "NONE" ]; then
		subt=""
	    fi
	    
	    ismc="False"
	    corrlabel="_hiIterativeTracks"
            domatch="True"
            genjets="HiGenJetsCleaned"
	    genparticles="hiGenParticles"
            tracks="hiGeneralTracks"
            pflow="particleFlowTmp"
            domatch="False"
            match=""
	    eventinfotag="generator"
            echo "" > $algo$subt$radius${object}JetSequence_${system}_${sample}_cff.py

            if [ $system == "pPb" ]; then
		corrlabel="_generalTracks"
		tracks="generalTracks"
		genparticles="genParticles"
            fi

	    if [ $system == "pp" ]; then
		corrlabel="_generalTracks"
		tracks="generalTracks"
		genparticles="genParticles"
	    fi

	    if [ $system == "PbPb" ] && [ $sample == "jec" ]; then
		if [ $sub == "NONE" ]; then
		    corrlabel="_generalTracks" #placeholder
		fi
		genparticles="genParticles"
	    fi

	    if [ $sample == "mc" ] || [ $sample == "jec" ] || [ $sample == "mix" ]; then
		ismc="True"
	    fi

	    if [ $system == "pp" ]; then
		genjets="HiGenJets"
	    fi

	    if [ $sample == "mix" ]; then
                eventinfotag="hiSignal"
            fi

	    if [ $sub == "Vs" ] && [ $object == "Calo" ]; then
		domatch="True"
		match="${algo}Pu${radius}Calo"
	    fi

	    if [ $sub == "Vs" ] && [ $object == "PF" ]; then
                domatch="True"
                match="${algo}Vs${radius}Calo"
            fi

	    if [ $sub == "Pu" ] && [ $object == "Calo" ]; then
                domatch="False" # this will be running first
                match="${algo}Pu${radius}PF"
            fi

            if [ $sub == "Pu" ] && [ $object == "PF" ]; then
                domatch="True"
                match="${algo}Vs${radius}PF"
            fi

	    if [ $sub == "NONE" ]; then
		domatch="True"
                match="${algo}Vs${radius}${object}"
	    fi

	    if [ $object == "Calo" ]; then
                corrlabel="_HI"
            fi

            corrname=`echo ${algo} | sed 's/\(.*\)/\U\1/'`${subt}${radius}${object}${corrlabel}

	    if [ $system == "PbPb" ] && [ $sample == "mc" ] && [ $object == "PF" ] && [ $sub == "Vs" ]; then
		
		cat templateClean_cff.py.txt \
		    | sed "s/ALGO_/$algo/g" \
		    | sed "s/SUB_/$subt/g" \
		    | sed "s/RADIUS_/$radius/g" \
		    | sed "s/OBJECT_/$object/g" \
		    | sed "s/SAMPLE_/$sample/g" \
		    | sed "s/CORRNAME_/$corrname/g" \
		    | sed "s/MATCHED_/$match/g" \
		    | sed "s/ISMC/$ismc/g" \
		    | sed "s/GENJETS/$genjets/g" \
		    | sed "s/GENPARTICLES/$genparticles/g" \
		    | sed "s/TRACKS/$tracks/g" \
		    | sed "s/PARTICLEFLOW/$pflow/g" \
		    | sed "s/DOMATCH/$domatch/g" \
		    >> HiGenJetsCleaned_cff.py
	    fi

	    cat templateSequence_cff.py.txt \
		| sed "s/ALGO_/$algo/g" \
		| sed "s/SUB_/$subt/g" \
		| sed "s/RADIUS_/$radius/g" \
		| sed "s/OBJECT_/$object/g" \
		| sed "s/SAMPLE_/$sample/g" \
		| sed "s/CORRNAME_/$corrname/g" \
		| sed "s/MATCHED_/$match/g" \
		| sed "s/ISMC/$ismc/g" \
		| sed "s/GENJETS/$genjets/g" \
		| sed "s/GENPARTICLES/$genparticles/g" \
		| sed "s/TRACKS/$tracks/g" \
		| sed "s/PARTICLEFLOW/$pflow/g" \
		| sed "s/DOMATCH/$domatch/g" \
		| sed "s/EVENTINFOTAG/$eventinfotag/g" \
		>> $algo$subt$radius${object}JetSequence_${system}_${sample}_cff.py

	    if [ $sample == "jec" ]; then
		echo "${algo}${subt}${radius}${object}Jets.jetPtMin = 1" >> HiReRecoJets_cff.py
		echo "${algo}${subt}${radius}${object}JetAnalyzer.genPtMin = cms.untracked.double(1)" >> $algo$subt$radius${object}JetSequence_${system}_${sample}_cff.py
	    fi

	    
	  done
	done
      done
    done
  done
done

echo "" >> HiGenJetsCleaned_cff.py
echo "hiGenJetsCleaned = cms.Sequence(" >> HiGenJetsCleaned_cff.py

for algo in ak
  do
  for radius in 2 3 4 5 6 7
    do
    echo "$algo${radius}HiGenJetsCleaned" >> HiGenJetsCleaned_cff.py
    if [ $radius -ne 7 ]; then
	echo "+" >> HiGenJetsCleaned_cff.py
    else
	echo ")" >> HiGenJetsCleaned_cff.py
    fi
    
  done
done

# ReReco stuff, for jec only
echo "" >> HiReRecoJets_cff.py
echo "hiReRecoPFJets = cms.Sequence(" >> HiReRecoJets_cff.py
#echo "PFTowers +" >> HiReRecoJets_cff.py
#echo "voronoiBackgroundPF +" >> HiReRecoJets_cff.py

for sub in NONE Pu Vs
do
    subt=$sub
    if [ $sub == "NONE" ]; then 
	subt=""
    fi
    for radius in 2 3 4 5 6 7 
    do
	echo "${algo}${subt}${radius}PFJets" >> HiReRecoJets_cff.py
	if [ $radius -eq 7 ] && [ $sub == "Vs" ]; then
	    echo ")" >> HiReRecoJets_cff.py
	else
	    echo "+" >> HiReRecoJets_cff.py
	fi
    done
done

echo "" >> HiReRecoJets_cff.py
echo "hiReRecoCaloJets = cms.Sequence(" >> HiReRecoJets_cff.py
#echo "caloTowersRec*caloTowers*iterativeConePu5CaloJets +" >> HiReRecoJets_cff.py
#echo "voronoiBackgroundCalo +" >> HiReRecoJets_cff.py

for sub in NONE Pu Vs
do
    subt=$sub
    if [ $sub == "NONE" ]; then 
	subt=""
    fi
    for radius in 2 3 4 5 6 7 
    do
	echo "${algo}${subt}${radius}CaloJets" >> HiReRecoJets_cff.py
	if [ $radius -eq 7 ] && [ $sub == "Vs" ]; then
	    echo ")" >> HiReRecoJets_cff.py
	else
	    echo "+" >> HiReRecoJets_cff.py
	fi
    done
done
