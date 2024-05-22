theory sustainable_cities_with_attr imports Main
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
  that :: entity
  development :: entity
  waste__energy :: entity
  maximum__efficiency :: entity
  rich__biodiversity :: entity
  sustainable__cities :: entity
  adequately__residents :: entity
  private__vehicles :: entity
  urban__areas :: entity
  Public_transportation_systems :: entity
  recreational__spaces :: entity
  efficient_sustainable_water_cities :: entity
  Water_conservation_measures :: entity
  Sustainable_urban__development :: entity
  Sustainable__cities :: entity
  Community_engagement :: entity
  Urban__planning :: entity
  Renewable_energy_sources :: entity

  (*Relations*)
  Are_fundamentally :: relation
  Are_imperative :: relation
  Invest_in_robust_green :: relation
  Are_crucially :: relation
  Includes :: relation
  Aim :: relation
  Prioritize_environmental :: relation
  Focuses_on :: relation
  Designed :: relation
  Involves_innovative :: relation

axiomatization where 
one_to_many_0: "one_to_n_rel Sustainable__cities development Prioritize_environmental"

axiomatization where 
one_to_many_1: "one_to_n_rel Urban__planning rich__biodiversity Focuses_on"

axiomatization where 
one_to_many_2: "one_to_n_rel Renewable_energy_sources sustainable__cities Are_crucially"

axiomatization where 
one_to_many_3: "one_to_n_rel Public_transportation_systems private__vehicles Designed"

axiomatization where 
one_to_many_5: "one_to_n_rel Sustainable__cities recreational__spaces Invest_in_robust_green"

axiomatization where 
one_to_many_6: "one_to_n_rel Community_engagement urban__areas Are_fundamentally"

axiomatization where 
one_to_many_7: "one_to_n_rel Sustainable_urban__development maximum__efficiency Includes"

axiomatization where 
one_to_many_8: "one_to_n_rel Water_conservation_measures efficient_sustainable_water_cities Are_imperative"

axiomatization where 
one_to_many_9: "one_to_n_rel Sustainable__cities adequately__residents Aim"


(*Consistency Check*) 
lemma True nitpick[satisfy, user_axioms, show_all, format=3] oops (* Model found *)

end
