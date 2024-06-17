from graphviz import Digraph

# Создаем объект графа
dot = Digraph(comment='QKD Protocol E91')

# Определяем узлы
dot.node('A', 'Start')
dot.node('B', 'Generate entangled pairs')
dot.node('C', 'Check interception (10% chance)')
dot.node('D', 'Check noise (0.1% chance)')
dot.node('E', 'Randomly choose basis for Alice and Bob')
dot.node('F', 'Measure photons')
dot.node('G', 'If bases match')
dot.node('H', 'Record results')
dot.node('I', 'Check Bell inequality')
dot.node('J', 'Record results in DataFrame')
dot.node('K', 'Generate secret key')
dot.node('L', 'If secret key >= 256 bits')
dot.node('M', 'Convert to HEX')
dot.node('N', 'Save results to Excel')
dot.node('O', 'End')

# Определяем ребра
dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JK', 'KL', 'LM', 'MN', 'NO'])
dot.edge('F', 'G', constraint='false')
dot.edge('F', 'I', constraint='false')

# Сохранение и отображение графа
dot.render('qkd_protocol_e91', view=True)
