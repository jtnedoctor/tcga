#!/bin/env py
# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Gregory Poore.
#
# Distributed under the terms of the Modified BSD License.
#
# ----------------------------------------------------------------------------
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from pandas.io.json import json_normalize
import json

# Use the public endpoint

sparql_endpoint = "https://opensparql.sbgenomics.com/bigdata/namespace/tcga_metadata_kb/sparql"

# Initialize the SPARQL wrapper with the endpoint
sparql = SPARQLWrapper(sparql_endpoint)

query = """
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix tcga: <https://www.sbgenomics.com/ontologies/2014/11/tcga#>

select distinct ?file_name ?gdc_file_uuid ?file_submitter_id ?case_name ?aliquot_name ?ref_genome_label ?sample_type_label ?experimental_strategy_label ?data_type_label ?data_format_label ?gender_label ?race_label ?ethnicity_label ?ageAtDiagnosis ?disease_type_label ?sample_label ?investigation_label ?histological_diagnosis_label ?primary_site_label ?prior_dx ?clinical_m_label ?clinical_n_label ?clinical_t_label ?pathologic_m_label ?pathologic_n_label ?pathologic_t_label ?pathologic_stage_label ?perf_score_karnofsky_label ?perf_score_eastern_cancer_oncology_group_label ?perf_score_timing_label ?primary_therapy_outcome_success_label ?vital_status_label ?new_tumor_event_label ?new_tumor_event_after_initial_trtmt ?radiation_therapy_code_label ?radiation_therapy_site_label ?radiation_therapy_type_label ?days_to_last_followup ?year_of_diagnosis ?icd10 ?icd03_histology_label ?icd03_histology_site ?data_submitting_center_label ?seq_platform_label ?aliquot_concentration  ?analyte_A260A280Ratio ?analyte_type_label ?analyte_amount ?analyte_well_number ?spectrophotometer_method_label ?file_upload_date ?file_published_date ?file_last_modified_date ?portion_weight ?portion_is_ffpe ?portion_number ?portion_slide_label ?freezing_method_label ?tissue_source_site_label ?country_of_sample_procurement
where
{

  ?file a tcga:File .
  ?file rdfs:label ?file_name .
  
  ?file tcga:hasGDCFileUUID ?gdc_file_uuid .
  
  ?file tcga:hasSubmitterId ?file_submitter_id .
  
  ?file tcga:hasCase ?case .
  ?case rdfs:label ?case_name .
  
  ?file tcga:hasAliquot ?aliquot .  
  ?aliquot rdfs:label ?aliquot_name .
  
  ?file tcga:hasReferenceGenome ?ref_genome .   
  ?ref_genome rdfs:label ?ref_genome_label .
  
  ?file tcga:hasSample ?sample .
  ?sample tcga:hasSampleType ?st .
  ?st rdfs:label ?sample_type_label 
  filter(?sample_type_label='Primary Tumor' || ?sample_type_label='Additional - New Primary' || ?sample_type_label='Additional Metastatic' || ?sample_type_label='Metastatic' || ?sample_type_label='Primary Blood Derived Cancer - Peripheral Blood' || ?sample_type_label='Recurrent Tumor' || ?sample_type_label='Blood Derived Normal' || ?sample_type_label='Bone Marrow Normal' || ?sample_type_label='Buccal Cell Normal' || ?sample_type_label='Solid Tissue Normal')
  
  
  ?file tcga:hasExperimentalStrategy ?xs .
  ?xs rdfs:label ?experimental_strategy_label .
  filter(?experimental_strategy_label='RNA-Seq' || ?experimental_strategy_label='WGS') .
  
  ?file tcga:hasDataType ?type .
  ?type rdfs:label ?data_type_label .
  filter(?data_type_label='Raw sequencing data') .
  
  ?file tcga:hasDataFormat ?format .
  ?format rdfs:label ?data_format_label .
  filter(?data_format_label='BAM') .
  
  ?file tcga:hasCase ?case .
  ?case tcga:hasGender ?gender .
  ?gender rdfs:label ?gender_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasEthnicity ?ethnicity .
  ?ethnicity rdfs:label ?ethnicity_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasRace ?race .
  ?race rdfs:label ?race_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasAgeAtDiagnosis ?ageAtDiagnosis .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasDiseaseType ?diseaseType .
  ?diseaseType rdfs:label ?disease_type_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasSample ?sample .
  ?sample rdfs:label ?sample_label .
  
  ?file tcga:hasCase ?case .  
  ?case tcga:hasInvestigation ?investigation .
  ?investigation rdfs:label ?inv_label .
  
  ?file tcga:hasCase ?case . 
  ?case tcga:hasHistologicalDiagnosis ?hd .
  ?hd rdfs:label ?histological_diagnosis_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPrimarySite ?primary_site .
  ?primary_site rdfs:label ?primary_site_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPriorDiagnosis ?prior_dx_base .
  ?prior_dx_base rdfs:label ?prior_dx .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasClinicalM ?clinical_m .
  ?clinical_m rdfs:label ?clinical_m_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasClinicalM ?clinical_n .
  ?clinical_n rdfs:label ?clinical_n_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasClinicalM ?clinical_t .
  ?clinical_t rdfs:label ?clinical_t_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasClinicalStage ?clinical_stage .
  ?clinical_stage rdfs:label ?clinical_stage_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPathologicM ?pathologic_m .
  ?pathologic_m rdfs:label ?pathologic_m_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPathologicN ?pathologic_n .
  ?pathologic_n rdfs:label ?pathologic_n_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPathologicT ?pathologic_t .
  ?pathologic_t rdfs:label ?pathologic_t_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPathologicStage ?pathologic_stage .
  ?pathologic_stage rdfs:label ?pathologic_stage_label .
  
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPerformanceStatusScoreKarnofsky ?perf_score_karnofsky .
  ?perf_score_karnofsky rdfs:label ?perf_score_karnofsky_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPerformanceStatusScoreECOG ?perf_score_eastern_cancer_oncology_group .
  ?perf_score_eastern_cancer_oncology_group rdfs:label ?perf_score_eastern_cancer_oncology_group_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPerformanceStatusScoreTiming ?perf_score_timing .
  ?perf_score_timing rdfs:label ?perf_score_timing_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasPrimaryTherapyOutcomeSuccess ?primary_therapy_outcome_success .
  ?primary_therapy_outcome_success rdfs:label ?primary_therapy_outcome_success_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasVitalStatus ?vital_status .
  ?vital_status rdfs:label ?vital_status_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasNewTumorEvent ?new_tumor_event .
  ?new_tumor_event rdfs:label ?new_tumor_event_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasRadiationTherapy ?radiation_therapy .
  ?radiation_therapy rdfs:label ?radiation_therapy_code_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasRadiationTherapy ?radiation_therapy .
  ?radiation_therapy tcga:hasRadiationTherapySite ?radiation_therapy_site .
  ?radiation_therapy_site rdfs:label ?radiation_therapy_site_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasRadiationTherapy ?radiation_therapy .
  ?radiation_therapy tcga:hasRadiationType ?radiation_therapy_type .
  ?radiation_therapy_type rdfs:label ?radiation_therapy_type_label .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasNewTumorEventAfterInitialTreatment ?new_tumor_event_after_initial_trtmt .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasDaysToLastFollowUp ?days_to_last_followup .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasYearOfDiagnosis ?year_of_diagnosis .
  
  ?file tcga:hasCase ?case .   
  ?case tcga:hasIcd10 ?icd10 .
  
  ?file tcga:hasCase ?case . 
  ?case tcga:hasIcdO3Histology ?icd03_histology_label .
  
  ?file tcga:hasCase ?case . 
  ?case tcga:hasIcdO3Site ?icd03_histology_site .
  
  ?file tcga:hasDataSubmittingCenter ?data_submitting_center .   
  ?data_submitting_center rdfs:label ?data_submitting_center_label .
  
  ?file tcga:hasPlatform ?seq_platform .   
  ?seq_platform rdfs:label ?seq_platform_label .
  
  ?file tcga:hasAliquot ?aliquot .   
  ?aliquot tcga:hasConcentration ?aliquot_concentration .
  
  ?file tcga:hasAnalyte ?analyte .   
  ?analyte tcga:hasA260A280Ratio ?analyte_A260A280Ratio .
  
  ?file tcga:hasAnalyte ?analyte .   
  ?analyte tcga:hasAnalyteType ?analyte_type .
  ?analyte_type rdfs:label ?analyte_type_label .
  
  ?file tcga:hasAnalyte ?analyte .   
  ?analyte tcga:hasAmount ?analyte_amount .
  
  ?file tcga:hasAnalyte ?analyte .   
  ?analyte rdfs:label ?analyte_well_number .
  
  ?file tcga:hasAnalyte ?analyte .   
  ?analyte tcga:hasSpectrophotometerMethod ?spectrophotometer_method .
  ?spectrophotometer_method rdfs:label ?spectrophotometer_method_label .
  
  ?file tcga:uploadDate ?file_upload_date .
  
  ?file tcga:publishedDate ?file_published_date .
  
  ?file tcga:lastModifiedDate ?file_last_modified_date .
  
  ?file tcga:hasAnalyte ?analyte .
  ?analyte tcga:hasPortion ?portion .
  ?portion tcga:hasWeight ?portion_weight .
  
  ?file tcga:hasAnalyte ?analyte .
  ?analyte tcga:hasPortion ?portion .
  ?portion tcga:hasIsFFPE ?portion_is_ffpe .
  
  ?file tcga:hasAnalyte ?analyte .
  ?analyte tcga:hasPortion ?portion .
  ?portion tcga:hasPortionNumber ?portion_number .
  
  ?file tcga:hasAnalyte ?analyte .
  ?analyte tcga:hasPortion ?portion .
  ?portion tcga:hasSlide ?portion_slide .
  ?portion_slide rdfs:label ?portion_slide_label .
  
  ?file tcga:hasCase ?case .
  ?case tcga:hasSample ?sample .
  ?sample tcga:hasFreezingMethod ?freezing_method .
  ?freezing_method rdfs:label ?freezing_method_label .
  
  ?file tcga:hasCase ?case .
  ?case tcga:hasSample ?sample .
  ?sample tcga:hasTissueSourceSite ?tissue_source_site .
  ?tissue_source_site rdfs:label ?tissue_source_site_label .
  
  ?file tcga:hasCase ?case .
  ?case tcga:hasSample ?sample .
  ?sample tcga:hasCountryOfSampleProcurement ?country_of_sample_procurement .

}

"""

sparql.method = 'POST'
sparql.setReturnFormat(JSON)

sparql.setQuery(query)

results = sparql.query().convert()

df = pd.DataFrame(results["results"]["bindings"])
df.to_csv('Testing_SPARQL.csv')

# print results


for result in results["results"]["bindings"]:
    print(result["file_name"]["value"])


# ?case ?sample ?file_name ?path ?xs_label ?subtype_label
# # From results, we grab a list of files. TCGA metadata database returns a list of filepaths. 
# filelist = [result['path']['value'] for result in results['results']['bindings']]

# # The list of file paths is now in the filelist array, as shown below
# print 'Your query returned %s files with paths:' % len(filelist)

# for file in filelist:
#     print file 
