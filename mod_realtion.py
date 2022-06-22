from py2neo import Graph, Node, NodeMatcher, Relationship, RelationshipMatcher

graph = Graph('bolt://nas.boeing773er.site:7687')

node_matcher = NodeMatcher(graph)
kcal_nodes = node_matcher.match('kcal')

nutrition_nodes = node_matcher.match('Nutrition')

relationship_matcher = RelationshipMatcher(graph)

for kcal_node in kcal_nodes:
    for nutrition_node in nutrition_nodes:
        relation = relationship_matcher.match([kcal_node, nutrition_node]).first()
        amount = int(float(type(relation).__name__))
        print(type(amount), amount)
        temp_dict = {'value': amount}
        edge = Relationship(kcal_node, "requires", nutrition_node, **temp_dict)
        graph.create(edge)
        graph.push(edge)
        graph.separate(relation)
