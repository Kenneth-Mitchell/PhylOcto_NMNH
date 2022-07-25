from enum import Enum
class GeneOrder(Enum):
    A =     ('cox1', 'rrns', 'nad1', 'cob', 'nad6', 'nad3', 'nad4l', 'muts', 'rrnl', 'nad2', 'nad5', 'nad4', 'trnm', 'cox3', 'atp6', 'atp8', 'cox2')
    B =     ('cox1', 'rrns', 'nad1', 'cob', 'cox3', 'trnm', 'nad4', 'nad5', 'nad2', 'rrnl', 'muts', 'nad4l', 'nad3', 'nad6', 'atp6', 'atp8', 'cox2')
    C =     ('cox1', 'rrns', 'nad1', 'cob', 'cox2', 'atp8', 'atp6', 'cox3', 'trnm', 'nad4', 'nad5', 'nad2', 'rrnl', 'muts', 'nad4l', 'nad3', 'nad6')
    D =     ('cox1', 'rrns', 'nad1', 'cob', 'muts', 'rnnl', 'nad2', 'nad5', 'nad4', 'trnm', 'cox3', 'atp6', 'atp8', 'cox2', 'nad4l', 'nad3', 'nad6')
    E =     ('cox1', 'rrns', 'nad1', 'cob', 'muts', 'rrnl', 'nad2', 'nad5', 'nad4', 'nad4l', 'nad3', 'nad6', 'trnm', 'cox3', 'atp6', 'atp8', 'cox2')
    
    

expected_genes = (('cox1',), ('rrns','rns'), ('nad1','nd1'), ('cob','cytb'), ('nad6','nd6'), ('nad3','nd3'), ('nad4l','nd4l'), ('muts',), ('rrnl','rnl'), ('nad2','nd2'), ('nad5','nd5'), ('nad4','nd4'), ('trnm','trna-met'), ('cox3',), ('atp6',), ('atp8',), ('cox2',))
start_gene = 'cox1'