;;;;;DOMINIO;;;;;
;inserindo o fator temporal

(define (domain learning)
    (:requirements :typing :durative-actions :fluents)
    (:types ESTUDANTE)
    (:predicates 
		(c_1_Bloom_lembrar_1_pronto ?e)
		(c_1_Bloom_lembrar_2_pronto ?e)
		(c_1_Bloom_lembrar_3_pronto ?e)
		(c_1_Bloom_lembrar_4_pronto ?e)
		(c_1_Bloom_lembrar_5_pronto ?e)
		(c_1_Bloom_lembrar_6_pronto ?e)
	)

    (:durative-action c_1_Bloom_lembrar_1
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition(at start (and
			(not 
			    (c_1_Bloom_lembrar_1_pronto ?e)
			)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_1_pronto ?e))
            )
    )

	(:durative-action c_1_Bloom_lembrar_2
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition (at start (and
			(not 
			    (c_1_Bloom_lembrar_2_pronto ?e)
			)
			(c_1_Bloom_lembrar_1_pronto ?e)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_2_pronto ?e))
            )
    )
	
	(:durative-action c_1_Bloom_lembrar_3
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition (at start (and
			(not 
			    (c_1_Bloom_lembrar_3_pronto ?e)
			)
			(c_1_Bloom_lembrar_2_pronto ?e)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_3_pronto ?e))
            )
    )

	(:durative-action c_1_Bloom_lembrar_4
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition (at start (and
			(not 
			    (c_1_Bloom_lembrar_4_pronto ?e)
			)
			(c_1_Bloom_lembrar_3_pronto ?e)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_4_pronto ?e))
            )
    )

	(:durative-action c_1_Bloom_lembrar_5
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition (at start (and
			(not 
			    (c_1_Bloom_lembrar_5_pronto ?e)
			)
			(c_1_Bloom_lembrar_4_pronto ?e)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_5_pronto ?e))
            )
    )

	(:durative-action c_1_Bloom_lembrar_6
        :parameters (?e - ESTUDANTE)
		:duration (= ?duration 40)
        :condition (at start (and
			(not 
			    (c_1_Bloom_lembrar_6_pronto ?e)
			)
			(c_1_Bloom_lembrar_5_pronto ?e)
		))
        :effect
            (and 
                (at end (c_1_Bloom_lembrar_6_pronto ?e))
            )
    )
)