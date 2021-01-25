class States(enumerate):
    SaoPaulo = 'SP'
    RioDeJaneiro = 'RJ'
    MinasGerais = 'MG'
    EspiritoSanto = 'ES'
    Parana = 'PR'
    SantaCatarina = 'SC'
    RioGrandeDoSul = 'RS'
    DistritoFederal = 'DF'
    Goias = 'GO'
    MatoGrosso = 'MT'
    MatoGrossoDoSul = 'MS'
    Bahia = 'BA'
    Sergipe = 'SE'
    Pernanbuco = 'PE'
    Ceara = 'CE'
    Alagoas = 'AL'
    Maranhao = 'MA'
    Paraiba = 'PB'
    RioGrandeDoNorte = 'RN'
    Acre = 'AC'
    Amapa = 'AP'
    Amazonas = 'AM'
    Para = 'PA'
    Rondonia = 'RO'
    Roraima = 'RR'
    Tocantins = 'TO'
    Piaui = 'PI'


DDDs_by_state = {
    States.SaoPaulo: ['11', '12', '13', '14', '15', '16', '17', '18', '19'],
    States.RioDeJaneiro: ['21', '22', '24'],
    States.MinasGerais: ['31', '32', '33', '34', '35', '37', '38'],
    States.EspiritoSanto: ['27', '28'],
    States.Parana: ['41', '42', '43', '44', '45', '46'],
    States.SantaCatarina: ['47', '48', '49'],
    States.RioGrandeDoSul: ['51', '53', '54', '55'],
    States.DistritoFederal: ['61'],
    States.Goias: ['62', '64'],
    States.MatoGrosso: ['65', '66'],
    States.MatoGrossoDoSul: ['67'],
    States.Alagoas: ['82'],
    States.Bahia: ['71', '73', '74', '75', '77'],
    States.Ceara: ['85', '88'],
    States.Maranhao: ['98', '99'],
    States.Paraiba: ['83'],
    States.Pernanbuco: ['81', '87'],
    States.Piaui: ['86', '89'],
    States.RioGrandeDoNorte: ['84'],
    States.Sergipe: ['79'],
    States.Acre: ['68'],
    States.Amapa: ['96'],
    States.Amazonas: ['92', '97'],
    States.Para: ['91', '93', '94'],
    States.Rondonia: ['69'],
    States.Roraima: ['95'],
    States.Tocantins: ['63']
}

DDDs = [ddd for state in [DDDs_by_state[state] for state in DDDs_by_state] for ddd in state]
