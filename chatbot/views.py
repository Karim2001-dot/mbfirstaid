from django.shortcuts import render
from django.http import JsonResponse

# Dictionary of first aid responses with both English and Kiswahili keywords and variations
FIRST_AID_GUIDES = {
    "burns": {
        "en": "For minor burns, run cool (not cold) water over the area for 10 minutes. Do not apply ice. If severe, seek medical attention immediately.",
        "sw": "Kwa kuchomeka kidogo (kichomi), mwaga maji baridi (sio ya barafu) kwa dakika 10. Usitumie barafu. Ikiwa ni mbaya, tafuta matibabu haraka."
    },
    "kuchomeka": {
        "en": "For minor burns, run cool (not cold) water over the area for 10 minutes. Do not apply ice. If severe, seek medical attention immediately.",
        "sw": "Kwa kuchomeka kidogo (kichomi), mwaga maji baridi (sio ya barafu) kwa dakika 10. Usitumie barafu. Ikiwa ni mbaya, tafuta matibabu haraka."
    },
    "nosebleed": {
        "en": "For nosebleed , tilt the head slightly forward and pinch the nostrils for 10 minutes. Avoid leaning back. If bleeding persists, see a doctor.",
        "sw": "Kwa bleki ya pua, inamisha kichwa mbele kidogo na finya pua kwa dakika 10. Epuka kuinamisha kichwa nyuma. Ikiwa damu haikomi, tafuta matibabu."
    },
    "bleki ya pua": {
        "en": "For nosebleed , tilt the head slightly forward and pinch the nostrils for 10 minutes. Avoid leaning back. If bleeding persists, see a doctor.",
        "sw": "Kwa bleki ya pua, inamisha kichwa mbele kidogo na finya pua kwa dakika 10. Epuka kuinamisha kichwa nyuma. Ikiwa damu haikomi, tafuta matibabu."
    },
    "fainting": {
        "en": "For fainting , lay the person down and elevate their legs. Check for breathing and make sure they get fresh air. If they don't regain consciousness, call emergency services.",
        "sw": "Kwa kupoteza fahamu, mweke mtu chini na inua miguu yake. Hakikisha anapumua na anapata hewa safi. Ikiwa hafufuki haraka, piga simu kwa huduma za dharura."
    },
    "kupoteza fahamu": {
        "en": "For fainting , lay the person down and elevate their legs. Check for breathing and make sure they get fresh air. If they don't regain consciousness, call emergency services.",
        "sw": "Kwa kupoteza fahamu, mweke mtu chini na inua miguu yake. Hakikisha anapumua na anapata hewa safi. Ikiwa hafufuki haraka, piga simu kwa huduma za dharura."
    },
    "fracture": {
        "en": "If you suspect a fracture, immobilize the area and avoid moving the person. Apply ice to reduce swelling and seek medical attention immediately.",
        "sw": "Ikiwa unadhani kuna mvunjiko, weka sehemu hiyo katika hali ya kutoshirika na epuka kumhamasisha mtu. Tumia barafu kupunguza uvimbe na tafuta matibabu haraka."
    },
    "mvunjiko": {
        "en": "If you suspect a fracture, immobilize the area and avoid moving the person. Apply ice to reduce swelling and seek medical attention immediately.",
        "sw": "Ikiwa unadhani kuna mvunjiko, weka sehemu hiyo katika hali ya kutoshirika na epuka kumhamasisha mtu. Tumia barafu kupunguza uvimbe na tafuta matibabu haraka."
    },
    "head injury": {
        "en": "If the person has a head injury , apply a cold compress and monitor for symptoms such as dizziness or nausea. If symptoms persist, seek medical attention immediately.",
        "sw": "Ikiwa mtu ameumia kichwa, weka kitambaa baridi na angalia dalili kama vile kizunguzungu au kichefuchefu. Ikiwa dalili haziepukiki, tafuta matibabu haraka."
    },
    "jeraha la kichwa": {
        "en": "If the person has a head injury , apply a cold compress and monitor for symptoms such as dizziness or nausea. If symptoms persist, seek medical attention immediately.",
        "sw": "Ikiwa mtu ameumia kichwa, weka kitambaa baridi na angalia dalili kama vile kizunguzungu au kichefuchefu. Ikiwa dalili haziepukiki, tafuta matibabu haraka."
    },
    "allergic_reaction": {
        "en": "For allergic reaction , remove the allergen and use an antihistamine if available. For severe reactions (swelling, difficulty breathing), seek medical help immediately.",
        "sw": "Kwa madhara ya mzio, toa kipengele kinachosababisha mzio na tumia dawa ya antihistamine ikiwa inapatikana. Kwa majibu makali (kuvimba, ugumu wa kupumua), tafuta msaada wa matibabu haraka."
    },
    "madhara_ya_mzio": {
        "en": "For allergic reaction (madhara ya mzio), remove the allergen and use an antihistamine if available. For severe reactions (swelling, difficulty breathing), seek medical help immediately.",
        "sw": "Kwa madhara ya mzio, toa kipengele kinachosababisha mzio na tumia dawa ya antihistamine ikiwa inapatikana. Kwa majibu makali (kuvimba, ugumu wa kupumua), tafuta msaada wa matibabu haraka."
    },
    "asthma_attack": {
        "en": "If someone is having an asthma attack (shambulio la pumu), help them use their inhaler. Encourage them to stay calm and seek immediate medical assistance if symptoms persist.",
        "sw": "Ikiwa mtu anapata shambulio la pumu, msaidia kutumia inhaler yake. Mhimiza kubaki mtulivu na tafuta msaada wa matibabu haraka ikiwa dalili haziepukiki."
    },
    "shambulio_la_pumu": {
        "en": "If someone is having an asthma attack (shambulio la pumu), help them use their inhaler. Encourage them to stay calm and seek immediate medical assistance if symptoms persist.",
        "sw": "Ikiwa mtu anapata shambulio la pumu, msaidia kutumia inhaler yake. Mhimiza kubaki mtulivu na tafuta msaada wa matibabu haraka ikiwa dalili haziepukiki."
    },
    "seizure": {
        "en": "If someone has a seizure (kifafa), make sure they are in a safe place, clear any nearby objects, and place a cushion or cloth under their head. Afterward, call for medical help.",
        "sw": "Ikiwa mtu ana kifafa, hakikisha yuko mahali salama, ondolea vitu vilivyo karibu, na weka shingo au kitambaa chini ya kichwa chake. Baada ya kifafa, piga simu kwa msaada wa matibabu."
    },
    "kifafa": {
        "en": "If someone has a seizure (kifafa), make sure they are in a safe place, clear any nearby objects, and place a cushion or cloth under their head. Afterward, call for medical help.",
        "sw": "Ikiwa mtu ana kifafa, hakikisha yuko mahali salama, ondolea vitu vilivyo karibu, na weka shingo au kitambaa chini ya kichwa chake. Baada ya kifafa, piga simu kwa msaada wa matibabu."
    },
    "choking": {
        "en": "If someone is choking (kumeza), encourage them to cough. If they are unable to, perform the Heimlich maneuver or seek immediate help from a nearby person or medical professional.",
        "sw": "Ikiwa mtu anameza, mhimize kukohoa. Ikiwa hawawezi, fanya mazoezi ya Heimlich au tafuta msaada wa haraka kutoka kwa mtu wa karibu au mtaalamu wa afya."
    },
    "kumeza": {
        "en": "If someone is choking (kumeza), encourage them to cough. If they are unable to, perform the Heimlich maneuver or seek immediate help from a nearby person or medical professional.",
        "sw": "Ikiwa mtu anameza, mhimize kukohoa. Ikiwa hawawezi, fanya mazoezi ya Heimlich au tafuta msaada wa haraka kutoka kwa mtu wa karibu au mtaalamu wa afya."
    },
    "bleeding": {
        "en": "For heavy bleeding (damu nyingi), apply pressure directly to the wound. If the bleeding does not stop, seek medical help immediately.",
        "sw": "Kwa damu nyingi, weka shinikizo moja kwa moja kwenye jeraha. Ikiwa damu haikomi, tafuta msaada wa matibabu haraka."
    },
    "damu_nyingi": {
        "en": "For heavy bleeding (damu nyingi), apply pressure directly to the wound. If the bleeding does not stop, seek medical help immediately.",
        "sw": "Kwa damu nyingi, weka shinikizo moja kwa moja kwenye jeraha. Ikiwa damu haikomi, tafuta msaada wa matibabu haraka."
    },
    "poisoning": {
        "en": "If poisoning (sumu) is suspected, try to identify the substance. Call a poison control center or emergency services immediately for advice and assistance.",
        "sw": "Ikiwa kuna sumu, jaribu kutambua kiini cha sumu. Piga simu kwa kituo cha kudhibiti sumu au huduma za dharura haraka kwa ushauri na msaada."
    },
    "sumu": {
        "en": "If poisoning (sumu) is suspected, try to identify the substance. Call a poison control center or emergency services immediately for advice and assistance.",
        "sw": "Ikiwa kuna sumu, jaribu kutambua kiini cha sumu. Piga simu kwa kituo cha kudhibiti sumu au huduma za dharura haraka kwa ushauri na msaada."
    },
    "bee sting": {
        "en": "For bee sting, remove the stinger if visible. Wash the area with soap and water. Apply a cold compress and use pain relievers if needed. Watch for allergic reactions.",
        "sw": "Kwa kuumwa na nyuki, ondoa mchomo ikiwa unaonekana. Osha eneo na sabuni na maji. Weka kitambaa baridi na tumia dawa za maumivu ikiwa inahitajika. Angalia dalili za mzio."
    },
    "kuumwa na nyuki": {
        "en": "For bee sting, remove the stinger if visible. Wash the area with soap and water. Apply a cold compress and use pain relievers if needed. Watch for allergic reactions.",
        "sw": "Kwa kuumwa na nyuki, ondoa mchomo ikiwa unaonekana. Osha eneo na sabuni na maji. Weka kitambaa baridi na tumia dawa za maumivu ikiwa inahitajika. Angalia dalili za mzio."
    },
    "sprain": {
        "en": "For a sprain, use RICE (Rest, Ice, Compression, Elevation). Rest the injured area, apply ice for 20 minutes at a time, compress with a bandage, and elevate the limb. Seek medical help if severe.",
        "sw": "Kwa kuumwa na misuli, tumia RICE (Pumzika, Barafu, Benda, Inua). Pumzisha eneo lililojeruhiwa, weka barafu kwa dakika 20 kwa wakati mmoja, funika na bendeji, na inua kiungo. Tafuta msaada wa matibabu ikiwa ni mbaya."
    },
    "misuli": {
        "en": "For a sprain, use RICE (Rest, Ice, Compression, Elevation). Rest the injured area, apply ice for 20 minutes at a time, compress with a bandage, and elevate the limb. Seek medical help if severe.",
        "sw": "Kwa kuumwa na misuli, tumia RICE (Pumzika, Barafu, Benda, Inua). Pumzisha eneo lililojeruhiwa, weka barafu kwa dakika 20 kwa wakati mmoja, funika na bendeji, na inua kiungo. Tafuta msaada wa matibabu ikiwa ni mbaya."
    },
    "heatstroke": {
        "en": "For heatstroke, move the person to a cool place, remove excess clothing, and cool them with water or ice packs. Seek immediate medical attention.",
        "sw": "Kwa kupigwa na joto, mhamishe mtu kwenda sehemu yenye baridi, ondoa nguo za ziada, na mpoze na maji au pakiti za barafu. Tafuta msaada wa matibabu haraka."
    },
    "kupigwa na joto": {
        "en": "For heatstroke, move the person to a cool place, remove excess clothing, and cool them with water or ice packs. Seek immediate medical attention.",
        "sw": "Kwa kupigwa na joto, mhamishe mtu kwenda sehemu yenye baridi, ondoa nguo za ziada, na mpoze na maji au pakiti za barafu. Tafuta msaada wa matibabu haraka."
    },
    "cut": {
        "en": "For a cut, wash the wound with soap and water, apply pressure to stop bleeding, and cover with a clean bandage. Seek medical help if the cut is deep or bleeding doesn't stop.",
        "sw": "Kwa jeraha la kukatwa, osha jeraha na sabuni na maji, weka shinikizo ili kuzuia damu, na funika na bendeji safi. Tafuta msaada wa matibabu ikiwa jeraha ni kubwa au damu haikomi."
    },
    "jeraha_la_kukata": {
        "en": "For a cut, wash the wound with soap and water, apply pressure to stop bleeding, and cover with a clean bandage. Seek medical help if the cut is deep or bleeding doesn't stop.",
        "sw": "Kwa jeraha la kukatwa, osha jeraha na sabuni na maji, weka shinikizo ili kuzuia damu, na funika na bendeji safi. Tafuta msaada wa matibabu ikiwa jeraha ni kubwa au damu haikomi."
    },
    "traffic accident": {
        "en": "In a traffic accident, ensure safety first. Call emergency services immediately. Do not move injured persons unless in immediate danger. Provide comfort and support until help arrives.",
        "sw": "Katika ajali ya barabarani, hakikisha usalama kwanza. Piga simu kwa huduma za dharura mara moja. Usimhamishe mtu aliyejeruhiwa isipokuwa yuko katika hatari ya moja kwa moja. Toa faraja na msaada hadi msaada ufike."
    },
    "ajali_ya_barabarani": {
        "en": "In a traffic accident, ensure safety first. Call emergency services immediately. Do not move injured persons unless in immediate danger. Provide comfort and support until help arrives.",
        "sw": "Katika ajali ya barabarani, hakikisha usalama kwanza. Piga simu kwa huduma za dharura mara moja. Usimhamishe mtu aliyejeruhiwa isipokuwa yuko katika hatari ya moja kwa moja. Toa faraja na msaada hadi msaada ufike."
    },
    "drowning": {
        "en": "For drowning, remove the person from the water if safe. Check for breathing and pulse. If absent, start CPR. Call emergency services immediately.",
        "sw": "Kwa kuzama, mtoe mtu kutoka kwenye maji ikiwa ni salama. Angalia kupumua na mapigo. Ikiwa hayapo, anza CPR. Piga simu kwa huduma za dharura mara moja."
    },
    "kuzama": {
        "en": "For drowning, remove the person from the water if safe. Check for breathing and pulse. If absent, start CPR. Call emergency services immediately.",
        "sw": "Kwa kuzama, mtoe mtu kutoka kwenye maji ikiwa ni salama. Angalia kupumua na mapigo. Ikiwa hayapo, anza CPR. Piga simu kwa huduma za dharura mara moja."
    },
    "electrical shock": {
        "en": "For electrical shock, turn off the power source if safe. Do not touch the person if they are still in contact with electricity. Check for breathing and pulse. Begin CPR if needed. Call emergency services.",
        "sw": "Kwa mshtuko wa umeme, zima chanzo cha umeme ikiwa ni salama. Usimshike mtu ikiwa bado anaunganishwa na umeme. Angalia kupumua na mapigo. Anza CPR ikiwa inahitajika. Piga simu kwa huduma za dharura."
    },
    "mshtuko wa umeme": {
        "en": "For electrical shock, turn off the power source if safe. Do not touch the person if they are still in contact with electricity. Check for breathing and pulse. Begin CPR if needed. Call emergency services.",
        "sw": "Kwa mshtuko wa umeme, zima chanzo cha umeme ikiwa ni salama. Usimshike mtu ikiwa bado anaunganishwa na umeme. Angalia kupumua na mapigo. Anza CPR ikiwa inahitajika. Piga simu kwa huduma za dharura."
    },
    "fire": {
        "en": "For fire injuries, extinguish flames if possible. Cool burns with water. Check for smoke inhalation. Call emergency services immediately.",
        "sw": "Kwa majeraha ya moto, zima moto ikiwa inawezekana. Poa majeraha na maji. Angalia kuvuta moshi. Piga simu kwa huduma za dharura mara moja."
    },
    "majeraha ya moto": {
        "en": "For fire injuries, extinguish flames if possible. Cool burns with water. Check for smoke inhalation. Call emergency services immediately.",
        "sw": "Kwa majeraha ya moto, zima moto ikiwa inawezekana. Poa majeraha na maji. Angalia kuvuta moshi. Piga simu kwa huduma za dharura mara moja."
    },
    "animal bite": {
        "en": "For animal bites, wash the wound with soap and water. Control bleeding with direct pressure. Seek medical attention immediately, especially for rabies risk.",
        "sw": "Kwa kuumwa na mnyama, osha jeraha na sabuni na maji. Zuia damu kwa shinikizo la moja kwa moja. Tafuta matibabu mara moja, haswa kwa hatari ya kichaa cha mbwa."
    },
    "kuumwa na mnyama": {
        "en": "For animal bites, wash the wound with soap and water. Control bleeding with direct pressure. Seek medical attention immediately, especially for rabies risk.",
        "sw": "Kwa kuumwa na mnyama, osha jeraha na sabuni na maji. Zuia damu kwa shinikizo la moja kwa moja. Tafuta matibabu mara moja, haswa kwa hatari ya kichaa cha mbwa."
    },
    "chemical exposure": {
        "en": "For chemical exposure, remove contaminated clothing. Flush affected area with water. Identify the chemical if possible. Call poison control or emergency services.",
        "sw": "Kwa kukaribia kemikali, ondoa nguo zilizochafuliwa. Safisha eneo lililoathiriwa na maji. Tambua kemikali ikiwa inawezekana. Piga simu kwa kudhibiti sumu au huduma za dharura."
    },
    "kukabiliwa na kemikali": {
        "en": "For chemical exposure, remove contaminated clothing. Flush affected area with water. Identify the chemical if possible. Call poison control or emergency services.",
        "sw": "Kwa kukaribia kemikali, ondoa nguo zilizochafuliwa. Safisha eneo lililoathiriwa na maji. Tambua kemikali ikiwa inawezekana. Piga simu kwa kudhibiti sumu au huduma za dharura."
    },
    "eye injury": {
        "en": "For eye injury, do not rub the eye. Rinse with clean water if possible. Seek immediate medical attention, especially for chemical or penetrating injuries.",
        "sw": "Kwa jeraha la jicho, usisugue jicho. Suuza na maji safi ikiwa inawezekana. Tafuta matibabu mara moja, haswa kwa majeraha ya kemikali au kupenya."
    },
    "jeraha la jicho": {
        "en": "For eye injury, do not rub the eye. Rinse with clean water if possible. Seek immediate medical attention, especially for chemical or penetrating injuries.",
        "sw": "Kwa jeraha la jicho, usisugue jicho. Suuza na maji safi ikiwa inawezekana. Tafuta matibabu mara moja, haswa kwa majeraha ya kemikali au kupenya."
    },
    "chemical_burn": {
    "en": "For chemical burns, immediately rinse the affected area with plenty of water. Remove contaminated clothing and continue rinsing for at least 20 minutes. Seek medical attention immediately.",
    "sw": "Kwa michubuko ya kemikali, osha eneo lililoathiriwa kwa maji mengi mara moja. Ondoa mavazi yaliyoathiriwa na kemikali na endelea kuosha kwa angalau dakika 20. Tafuta matibabu haraka."
},
"majeraha ya kemikali": {
    "en": "For chemical burns, immediately rinse the affected area with plenty of water. Remove contaminated clothing and continue rinsing for at least 20 minutes. Seek medical attention immediately.",
    "sw": "Kwa michubuko ya kemikali, osha eneo lililoathiriwa kwa maji mengi mara moja. Ondoa mavazi yaliyoathiriwa na kemikali na endelea kuosha kwa angalau dakika 20. Tafuta matibabu haraka."
},
"playground injury": {
    "en": "For playground injuries, clean the wound with soap and water, apply pressure to stop any bleeding, and cover with a clean bandage. If the injury is severe or there is a broken bone, seek immediate medical attention.",
    "sw": "Kwa majeraha ya uwanjani, osha jeraha na sabuni na maji, weka shinikizo kuzuia damu, na funika na bendeji safi. Ikiwa jeraha ni kubwa au kuna mvunjiko, tafuta matibabu haraka."
},
"majeraha_ya_uwanjani": {
    "en": "For playground injuries, clean the wound with soap and water, apply pressure to stop any bleeding, and cover with a clean bandage. If the injury is severe or there is a broken bone, seek immediate medical attention.",
    "sw": "Kwa majeraha ya uwanjani, osha jeraha na sabuni na maji, weka shinikizo kuzuia damu, na funika na bendeji safi. Ikiwa jeraha ni kubwa au kuna mvunjiko, tafuta matibabu haraka."
},
"laboratory_exposure": {
    "en": "In case of laboratory exposure to harmful substances, immediately remove the affected person from the area, rinse their skin with water for at least 15 minutes, and seek medical help. If eyes are affected, rinse with water for at least 20 minutes.",
    "sw": "Ikiwa mtu ameathiriwa na kemikali au vitu vyenye madhara katika maabara, mtoe mtu huyo haraka kutoka kwenye eneo hilo, osha ngozi yake kwa maji kwa angalau dakika 15, na tafuta msaada wa matibabu. Ikiwa macho yametibiwa, osha kwa maji kwa angalau dakika 20."
},
"athari ya kemikali": {
    "en": "In case of laboratory exposure to harmful substances, immediately remove the affected person from the area, rinse their skin with water for at least 15 minutes, and seek medical help. If eyes are affected, rinse with water for at least 20 minutes.",
    "sw": "Ikiwa mtu ameathiriwa na kemikali au vitu vyenye madhara katika maabara, mtoe mtu huyo haraka kutoka kwenye eneo hilo, osha ngozi yake kwa maji kwa angalau dakika 15, na tafuta msaada wa matibabu. Ikiwa macho yametibiwa, osha kwa maji kwa angalau dakika 20."
},
"lab fire": {
    "en": "In case of fire in the laboratory, use a fire extinguisher if available. Evacuate the area immediately and call emergency services. Do not attempt to fight large fires.",
    "sw": "Ikiwa kuna moto kwenye maabara, tumia kizuia moto ikiwa kinapatikana. Ondoa watu kwenye eneo hilo haraka na piga simu kwa huduma za dharura. Usijaribu kupigana na moto mkubwa."
},
"moto_maabara": {
    "en": "In case of fire in the laboratory, use a fire extinguisher if available. Evacuate the area immediately and call emergency services. Do not attempt to fight large fires.",
    "sw": "Ikiwa kuna moto kwenye maabara, tumia kizuia moto ikiwa kinapatikana. Ondoa watu kwenye eneo hilo haraka na piga simu kwa huduma za dharura. Usijaribu kupigana na moto mkubwa."
}

}

# Mapping of keyword variations to standard keywords
KEYWORD_VARIATIONS = {
    "faint": "fainting",
    "kuzimia": "kupoteza_fahamu",
    "burned": "burns",
    "kichomi": "kuchomeka",
    "nosebleeds": "nosebleed",
    "kuvunjika": "mvunjiko",
    "allergy": "allergic_reaction",
    "pumu":"asthma_attack",
    "degedege":"kifafa",
    "kukosa_hewa":"choking",
    "damu_kutoka": "bleeding",
    "sumu_kuingia": "poisoning",
    "wadudu":"bee_sting",
    "misuli_kuumia":"sprain",
    "joto_kali":"heatstroke",
    "jeraha_la_kukata":"cut",
    "ajali_gari":"traffic_accident",
    "kuzamishwa":"drowning",
    "kupigwa_umeme":"electrical_shock",
    "moto":"fire_injury",
    "kuumwa_mnyama":"animal_bite",
    "kemikali":"chemical_exposure",
    "kuumizwa_jicho":"eye_injury",
    "burning": "burns",
    "scald": "burns",
    "scalded": "burns",
    "fire burn": "burns",
    "heat burn": "burns",
    "bleeding nose": "nosebleed",
    "bloody nose": "nosebleed",
    "nasal bleed": "nosebleed",
    "passed out": "fainting",
    "blacked out": "fainting",
    "swoon": "fainting",
    "unconsciousness": "fainting",
    "broken bone": "fracture",
    "break": "fracture",
    "fractures": "fracture",
    "fractured": "fracture",
    "breaks": "fracture",
    "bone fracture": "fracture",
    "head trauma": "head_injury",
    "head wound": "head_injury",
    "head hurt": "head_injury",
    "brain injury": "head_injury",
    "skull fracture": "head_injury",
    "allergic": "allergic_reaction",
    "reaction": "allergic_reaction",
    "allergies": "allergic_reaction",
    "hypersensitivity": "allergic_reaction",
    "asthma": "asthma_attack",
    "wheezing": "asthma_attack",
    "breathing difficulty": "asthma_attack",
    "shortness of breath": "asthma_attack",
    "seizures": "seizure",
    "fit": "seizure",
    "fits": "seizure",
    "convulsion": "seizure",
    "convulsions": "seizure",
    "epileptic fit": "seizure",
    "choke": "choking",
    "choked": "choking",
    "choking hazard": "choking",
    "swallowed wrong": "choking",
    "bleed": "bleeding",
    "bleeds": "bleeding",
    "blood loss": "bleeding",
    "hemorrhage": "bleeding",
    "cut bleeding": "bleeding",
    "poison": "poisoning",
    "poisoned": "poisoning",
    "toxic": "poisoning",
    "toxic exposure": "poisoning",
    "ingestion": "poisoning",
    "wasp sting": "bee_sting",
    "insect sting": "bee_sting",
    "sting": "bee_sting",
    "stung": "bee_sting",
    "sprained": "sprain",
    "twisted ankle": "sprain",
    "twisted": "sprain",
    "strain": "sprain",
    "joint injury": "sprain",
    "heat stroke": "heatstroke",
    "sunstroke": "heatstroke",
    "heat exhaustion": "heatstroke",
    "hyperthermia": "heatstroke",
    "cuts": "cut",
    "laceration": "cut",
    "wound": "cut",
    "slice": "cut",
    "gash": "cut",
    "car crash": "traffic_accident",
    "auto accident": "traffic_accident",
    "vehicle accident": "traffic_accident",
    "road accident": "traffic_accident",
    "accident": "traffic_accident",
    "drowned": "drowning",
    "submerged": "drowning",
    "underwater": "drowning",
    "suffocation": "drowning",
    "electric shock": "electrical_shock",
    "electrocution": "electrical_shock",
    "shocked": "electrical_shock",
    "electricity injury": "electrical_shock",
    "fire": "fire_injury",
    "fire accident": "fire_injury",
    "flame injury": "fire_injury",
    "burnt": "fire_injury",
    "animal attack": "animal_bite",
    "dog bite": "animal_bite",
    "cat bite": "animal_bite",
    "bites": "animal_bite",
    "chemical spill": "chemical_exposure",
    "chemical burn": "chemical_exposure",
    "chemicals": "chemical_exposure",
    "injured eye": "eye_injury",
    "eye wound": "eye_injury",
    "eye trauma": "eye_injury",
    "kuungua":"kuchomeka",
    "moto":"kuchomeka",
    "kuunguzwa":"kuchomeka",
    "kutoka damu puani":"bleki_ya_pua",
    "damu puani":"bleki_ya_pua",
    "pua_kuvuja_damu":"bleki_ya_pua",
    "zimia":"kupoteza_fahamu",
    "kuzirai":"kupoteza_fahamu",
    "kuvunjika_mfupa":"mvunjiko",
    "mfupa_kuvunjika":"mvunjiko",
    "kuumia_kichwa":"jeraha_la_kichwa",
    "jeraha_kichwani":"jeraha_la_kichwa",
    "kichwa_kuumia":"jeraha_la_kichwa",
    "mzio":"madhara_ya_mzio",
    "mzio_mkali":"madhara_ya_mzio",
    "athari_ya_mzio":"madhara_ya_mzio",
    "pumu":"shambulio_la_pumu",
    "kubanwa_na_pumu":"shambulio_la_pumu",
    "mshtuko":"kifafa",
    "mshituko_wa_kifafa":"kifafa",
    "kukwama":"choking",
    "kukosa_pumzi":"choking",
    "kutokwa_na_damu_nyingi":"damu_nyingi",
    "damu_kutoka":"damu_nyingi",
    "sumu":"sumu",
    "kuumwa_na_wadudu":"kuumwa_na_nyuki",
    "misuli_kuumia":"kuumwa_na_misuli",
    "jeraha_la_misuli":"kuumwa_na_misuli",
    "joto_jingi":"kupigwa_na_joto",
    "kuumizwa_na_kitu_chenye_ncha_kali":"jeraha_la_kukata",
    "ajali_gari":"ajali_ya_barabarani",
    "ajali_ya_barabara":"ajali_ya_barabarani",
    "kuzamishwa":"kuzama",
    "kuzama_majini":"kuzama",
    "umeme":"mshtuko_wa_umeme",
    "umeme_kuingia":"mshtuko_wa_umeme",
    "kupigwa_umeme":"mshtuko_wa_umeme",
    "kuungua_na_moto":"majeraha_ya_moto",
    "kuumwa mnyama":"kuumwa_na_mnyama",
    "kuathiriwa_na_kemikali":"kukabiliwa_na_kemikali",
    "jicho":"jeraha_la_jicho"
}

def get_first_aid_response(request):
    keyword = request.GET.get("keyword", "").strip().lower()
    language = request.GET.get("language", "en")  # Default to English

    # Check for variations and map to standard keywords
    if keyword in KEYWORD_VARIATIONS:
        keyword = KEYWORD_VARIATIONS[keyword]

    if keyword in FIRST_AID_GUIDES:
        response_text = FIRST_AID_GUIDES[keyword].get(language, FIRST_AID_GUIDES[keyword]["en"])
    else:
        response_text = "Sorry, I don't have information on that. Please visit a health professional for assistance." if language == 'en' else "Samahani, sina taarifa kuhusu hilo. Tafadhali tembelea mtaalamu wa afya kwa msaada."

    return JsonResponse({"response": response_text})

def first_aid_home(request):
    return render(request, "chatbot/firstaid.html")

def home(request):
    return render(request, 'chatbot/home.html')