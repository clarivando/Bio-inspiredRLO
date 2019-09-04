import unittest
import nlp

#Todos os testes do módulo nlp retornaram OK (sucesso)
#O método self.assertEqual retorna OK se seus dois parâmetros são iguais, caso contrário retorna FAIL
class Simplify_tag_test(unittest.TestCase):

	#Aqui vem variáveis que podem ser usadas pelos testes abaixo
	
	def test_1(self):
	
		tag = 'N<+adj'
		self.assertEqual(nlp.simplify_tag(tag),'adj')

		
if __name__ == '__main__':
	unittest.main()