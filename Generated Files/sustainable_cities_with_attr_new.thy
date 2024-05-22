theory sustainable_cities_with_attr_new imports Main
begin 

typedecl i
type_synonym entity = "i \<Rightarrow> bool"
type_synonym relation = "i \<Rightarrow> i \<Rightarrow> bool"

definition disjoint :: "entity \<Rightarrow> entity \<Rightarrow> bool" where 
    "disjoint C1 C2 \<equiv> \<not>(\<exists>x::i. C1 x \<and> C2 x)"
definition conv_rel :: "relation \<Rightarrow> relation" where 
   "conv_rel Rel \<equiv> (\<lambda>x y. Rel y x)"
definition is_empty_rel :: "relation \<Rightarrow> bool" where 
   "is_empty_rel Rel \<equiv> \<forall>x y. \<not>Rel x y"

consts
  (*Entities*)
  waste_management_traffic_city_resilience :: entity
  strategy :: entity
  technology_advancement :: entity
  city_digitization :: entity
  4th_Industrial_Revolution :: entity
  Smart_Cities_Global_Smart_Dubai :: entity
  single_shared__system :: entity
  100_per_cent_potable_water_supply :: entity
  Dubai_Smart_City_Accelerator :: entity
  sanitation_facilities :: entity
  sewerage :: entity
  that :: entity
  shared_ICT_services :: entity
  smart_sustainable__cities :: entity
  smart_autonomous_mobility_strategies :: entity
  Dubai_Paperless_Strategy :: entity
  same__period :: entity
  world :: entity
  today_more_than_90__percent :: entity
  Long_term_strategies :: entity
  over_million_3_people :: entity
  economy :: entity
  various_SDG_11__indicators :: entity
  first_city_government :: entity
  Startup_Dubai_startup :: entity
  schools :: entity
  2020 :: entity
  Happiness_Meter :: entity
  AI_roadmap :: entity
  Dubai_city_experiences :: entity
  Smart_Dubai :: entity
  city_experiences :: entity
  just_over_a__decade :: entity
  open__data :: entity
  over_US$_350_million :: entity
  IoT :: entity
  Smart_Dubai_initiative :: entity
  blockchain_case :: entity
  IoT__strategy :: entity
  annually__2021 :: entity
  accelerator :: entity
  2021_further_Dubai_city_resources :: entity
  total :: entity
  inclusive__ecosystem :: entity
  city_level :: entity
  opening_businesses :: entity
  mobility :: entity
  such__tourism :: entity
  more_than_4,000__touchpoints :: entity
  Startupbootcamp_network :: entity
  Several_use_cases :: entity
  Dubai_2021_Smart_strategy :: entity
  Dubai :: entity
  first__city :: entity
  Opening_government_data :: entity
  more_than_million_22_votes :: entity

  (*Relations*)
  Formed :: relation
  Leading :: relation
  Estimated :: relation
  Launched :: relation
  Impact :: relation
  Achieved_in_just :: relation
  Announced :: relation
  Encompasses_various :: relation
  Include :: relation
  Achieved :: relation
  Is_one :: relation
  Entails :: relation
  Technology :: relation
  Connected :: relation
  Implemented_as :: relation
  Implemented :: relation
  Has :: relation
  Aims :: relation
  Working_with :: relation
  Saved :: relation
  Launched_in :: relation
  Is :: relation
  Collected_from :: relation
  Includes :: relation
  Support :: relation
  Striving :: relation
  Studies :: relation
  Adopted_emerging :: relation
  Grown :: relation
  Result_in :: relation
  Provides :: relation

axiomatization where 
one_to_many_1: "one_to_n_rel Dubai such__tourism Is"

axiomatization where 
one_to_many_2: "one_to_n_rel economy same__period Grown"

axiomatization where 
one_to_many_3: "one_to_n_rel Dubai various_SDG_11__indicators Achieved"

axiomatization where 
one_to_many_4: "one_to_n_rel 100_per_cent_potable_water_supply sanitation_facilities Includes"

axiomatization where 
one_to_many_5: "one_to_n_rel Dubai world Has"

axiomatization where 
one_to_many_6: "one_to_n_rel Long_term_strategies smart_autonomous_mobility_strategies Include"

axiomatization where 
one_to_many_7: "one_to_n_rel Smart_Dubai city_experiences Aims"

axiomatization where 
one_to_many_8: "one_to_n_rel Smart_Dubai_initiative IoT Encompasses_various"

axiomatization where 
one_to_many_9: "one_to_n_rel Dubai_2021_Smart_strategy inclusive__ecosystem Includes"

axiomatization where 
one_to_many_10: "one_to_n_rel Smart_Dubai technology_advancement Formed"

axiomatization where 
one_to_many_11: "one_to_n_rel Dubai_city_experiences schools Impact"

axiomatization where 
one_to_many_12: "one_to_n_rel Smart_Dubai city_experiences Adopted_emerging"

axiomatization where 
one_to_many_13: "one_to_n_rel Smart_Dubai opening_businesses Announced"

axiomatization where 
one_to_many_14: "one_to_n_rel Smart_Dubai AI_roadmap Working_with"

axiomatization where 
one_to_many_15: "one_to_n_rel Smart_Dubai 2021_further_Dubai_city_resources Aims"

axiomatization where 
one_to_many_16: "one_to_n_rel sewerage waste_management_traffic_city_resilience Connected"

axiomatization where 
one_to_many_17: "one_to_n_rel Several_use_cases IoT__strategy Implemented_as"

axiomatization where 
one_to_many_18: "one_to_n_rel Smart_Dubai more_than_4,000__touchpoints Implemented"

axiomatization where 
one_to_many_19: "one_to_n_rel more_than_million_22_votes city_level Collected_from"

axiomatization where 
one_to_many_20: "one_to_n_rel Happiness_Meter city_experiences Provides"

axiomatization where 
one_to_many_21: "one_to_n_rel open__data economy Has"

axiomatization where 
one_to_many_23: "one_to_n_rel today_more_than_90__percent single_shared__system Implemented"

axiomatization where 
one_to_many_25: "one_to_n_rel Smart_Dubai shared_ICT_services Saved"

axiomatization where 
one_to_many_26: "one_to_n_rel Smart_Cities_Global_Smart_Dubai smart_sustainable__cities Aims"

axiomatization where 
one_to_many_27: "one_to_n_rel Startup_Dubai_startup 4th_Industrial_Revolution Support"

axiomatization where 
one_to_many_28: "one_to_n_rel Smart_Dubai Dubai_Smart_City_Accelerator Launched"

axiomatization where 
one_to_many_29: "one_to_n_rel accelerator Startupbootcamp_network Launched_in"

axiomatization where 
one_to_many_30: "one_to_n_rel Smart_Dubai city_level Striving"

axiomatization where 
one_to_many_31: "one_to_n_rel Dubai_Paperless_Strategy city_digitization Technology"

axiomatization where 
one_to_many_32: "one_to_n_rel strategy mobility Entails"

axiomatization where 
one_to_many_35: "one_to_n_rel first__city blockchain_case Studies"


(*Consistency Check*) 
lemma True nitpick[satisfy, user_axioms, show_all, format=3] oops (* Model found *)

end
